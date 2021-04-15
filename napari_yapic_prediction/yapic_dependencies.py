from yapic_io.prediction_batch import PredictionBatch
from yapic_io.tiff_connector import TiffConnector
from bigtiff import Tiff, PlaceHolder
from yapic_io.dataset import Dataset
from yapic.session import Session
from functools import lru_cache
from pathlib import Path

import yapic_io.utils as ut
import collections
import numpy as np
import logging
import napari
import sys
import os


FilePair = collections.namedtuple('FilePair', ['img', 'lbl'])
logger = logging.getLogger(os.path.basename(__file__))


class NapariSession(Session):
    """YAPiC Session class modification to support the custom connector NapariInConnector"""

    def load_prediction_data(self, viewer, save_path):
        '''
        Connect to a prediction dataset.
        
        Parameters
        ----------
        image_path : napari.viewer.Viewer
            Napari viewer instance.
        save_path : string
            Path to folder for saving prediction images.
        '''

        self.dataset = Dataset(NapariInConnector(
            viewer, '/tmp/this_should_not_exist', savepath=save_path))
        msg = '\n\nImport dataset for prediction:\n{}\n'.format(
            self.dataset.pixel_connector.__repr__())
        sys.stdout.write(msg)

    def predict(self, multichannel=False, progress_bar=None):
        """Modification to make prediction from the Napari viewer and store results in save_path."""
        data_predict = PredictionBatch(self.dataset,
                                       2,
                                       self.output_tile_size_zxy,
                                       self.padding_zxy)
        data_predict.set_normalize_mode('local')
        data_predict.set_pixel_dimension_order('bzxyc')

        if multichannel:
            data_predict.multichannel_output_on()
        else:
            data_predict.multichannel_output_off()
        print('multichannel output: {}'.format(data_predict.multichannel))

        for item_nr, item in enumerate(data_predict):
            result = self.model.predict(item.pixels())
            item.put_probmap_data(result)
            if progress_bar:
                progress_bar.setValue(100 * (item_nr + 1) / len(data_predict))


class NapariInConnector(TiffConnector):
    """YAPiC connector class modification to support napari.viewer as image provider."""
    def __init__(self, viewer, label_filepath, savepath=None):
        self.data = viewer.layers
        self.img_path = None
        img_filenames = [layer.name for layer in viewer.layers if type(layer) == napari.layers.Image]
        
        self.label_path, lbl_filenames = self._handle_lbl_filenames(
            label_filepath)

        assert img_filenames is not None, 'no filenames for pixel images found'
        assert len(img_filenames) != 0, 'no filenames for pixel images found'

        if lbl_filenames is None or len(lbl_filenames) == 0:
            pairs = [(img, None) for img in img_filenames]
        else:
            pairs = ut.find_best_matching_pairs(img_filenames, lbl_filenames)

        self._assemble_filenames(pairs)

        logger.info('Pixel and label files are assigned as follows:')
        logger.info('\n'.join('{p.img} <-> {p.lbl}'.format(p=pair)
                              for pair in self.filenames))

        self.savepath = Path(savepath) if savepath is not None else None

        original_labels = self.original_label_values_for_all_images()
        self.labelvalue_mapping = self.calc_label_values_mapping(
            original_labels)

        self.check_label_matrix_dimensions()

    @lru_cache(maxsize=10)
    def _open_image_file(self, image_nr):
        """No memmap required when using the napari viewer."""
        im_name = self.filenames[image_nr].img
        data = self.data[im_name].data
        # adding the four dimensions (z, y, x, c)
        if len(data.shape) == 2:  # BW image with a single channel
            data = np.expand_dims(data, axis=0)  # z dim
            data = np.expand_dims(data, axis=-1)  # channel dim
        elif len(data.shape) == 3:  # RGB image (z, y, x, c)
            data = np.expand_dims(data, axis=0)  # z dim
        # arranging dimensions desired (c, z, x, y)
        data = np.moveaxis(data, (0, 1, 3), (1, 3, 0))
        return data

    def image_dimensions(self, image_nr):
        img = self._open_image_file(image_nr)
        return img.shape
    
    def original_label_values_for_all_images(self):
        """Empty return since no label path is required."""
        return []
    
    def _assemble_filenames(self, pairs):
        self.filenames = [FilePair(img, Path(lbl) if lbl else None)
                          for img, lbl in pairs]
        
    def check_label_matrix_dimensions(self):
        """True return since label path is not required"""
        return True
    
    @lru_cache(maxsize=10)
    def _open_label_file(self, image_nr):
        """No label path required"""
        return None
        
    def get_tile(self, image_nr, pos, size):
        """Modification from TiffConnector to get a tile from numpy array."""
        C, Z, X, Y = pos
        CC, ZZ, XX, YY = np.array(pos) + size # offset
        slices = self._open_image_file(image_nr)
        tile = slices[C:CC, Z: ZZ, X: XX, Y: YY]
        return tile.astype('float')
    
    @lru_cache(maxsize=10)
    def _open_probability_map_file(self,
                                   image_nr,
                                   label_value,
                                   multichannel=False):
        """Minor change in the file and path definition."""
        # memmap is slow, so we must cache it to be fast!
        fname = self.filenames[image_nr].img
        T = 1  # time frame in output probmap
        if multichannel:
            fname = Path('{}.tif'.format(fname))
            n_classes = multichannel
            C = n_classes
        else:
            fname = Path('{}_class_{}.tif'.format(fname, label_value))
            C = 1  # channel in output probmap
        path = self.savepath / fname
        if not path.exists():
            _, Z, X, Y = self.image_dimensions(image_nr)
            images = [PlaceHolder((Y, X, C), 'float32')] * Z
            Tiff.write(images, io=str(path), imagej_shape=(T, C, Z))
        return Tiff.memmap_tcz(path)
