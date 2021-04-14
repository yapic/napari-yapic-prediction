from yapic_io.tiff_connector import TiffConnector
from bigtiff import Tiff, PlaceHolder
from functools import lru_cache
from pathlib import Path
import yapic_io.utils as ut
import collections
import numpy as np
import napari
import logging
import os

# change io_connector to include this new connector (check how)
#     other option is to change the sesion load_prediction_data and instead of using io_connector.
#     simply make the connector with this new implementation.

#  should also overwrite session to connect the progress bar

FilePair = collections.namedtuple('FilePair', ['img', 'lbl'])
logger = logging.getLogger(os.path.basename(__file__))

class NapariInConnector(TiffConnector):
    # def __init__(self, images_dict, label_filepath, savepath=None):
    def __init__(self, viewer, label_filepath, savepath=None):

        # self.data = images_dict
        self.data = viewer.layers
        
        # self.img_path, img_filenames = None, list(images_dict.keys())
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

# might check _open_probability_map_file
# might check put_tile

    @lru_cache(maxsize=10)
    def _open_image_file(self, image_nr):
        im_name = self.filenames[image_nr].img
        data = self.data[im_name].data

        # adding the four dimensions (z, y, x, c)
        if len(data.shape) == 2:  # BW image with a single channel
            data = np.expand_dims(data, axis=0)  # z dim
            data = np.expand_dims(data, axis=-1)  # channel dim
        elif len(data.shape) == 3:  # RGB image (z, y, x, c)
            data = np.expand_dims(data, axis=0)  # z dim

        # arranging dimensions desired (c, z, x, y)
        # seting channel as the first dimension
        data = np.moveaxis(data, (0, 1, 3), (1, 3, 0))
        
        # data = np.moveaxis(data, -1, 0)
        # data = np.moveaxis(data, 2, 3)  # seting y as the last dimension

        return data

    def image_dimensions(self, image_nr):

        img = self._open_image_file(image_nr)
        return img.shape
    
    def original_label_values_for_all_images(self):
        return []
    
    def _assemble_filenames(self, pairs):
        self.filenames = [FilePair(img, Path(lbl) if lbl else None)
                          for img, lbl in pairs]
        
    def check_label_matrix_dimensions(self):
        return True
    
    @lru_cache(maxsize=10)
    def _open_label_file(self, image_nr):
        # memmap is slow, so we must cache it to be fast!
        label_filename = self.filenames[image_nr].lbl

        if label_filename is None:
            logger.warning(
                'no label matrix file found for image file %s', str(image_nr))
            return None
        
    def get_tile(self, image_nr, pos, size):
        C, Z, X, Y = pos
        CC, ZZ, XX, YY = np.array(pos) + size

        slices = self._open_image_file(image_nr)
        
        tile = slices[C:CC, Z: ZZ, X: XX, Y: YY]

        return tile.astype('float')
    
    @lru_cache(maxsize=10)
    def _open_probability_map_file(self,
                                   image_nr,
                                   label_value,
                                   multichannel=False):
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

# might check get_tile
