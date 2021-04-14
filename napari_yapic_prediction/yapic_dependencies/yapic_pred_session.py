from yapic.session import Session
from napari_yapic_prediction.yapic_dependencies.yapic_connector import NapariInConnector
from yapic_io.prediction_batch import PredictionBatch
from yapic_io.dataset import Dataset
import logging
import sys


logger = logging.getLogger(__name__)


class NapariSession(Session):
    def load_prediction_data(self, viewer, save_path):
        '''
        Connect to a prediction dataset.
        Parameters
        ----------
        image_path : string
            Path to folder with tiff images to predict.
        save_path : string
            Path to folder for saving prediction images.
        '''

        self.dataset = Dataset(NapariInConnector(viewer, '/tmp/this_should_not_exist', savepath=save_path))
        
        # self.dataset = Dataset(io_connector(image_path,
        #                                     '/tmp/this_should_not_exist',
        #                                     savepath=save_path))
        msg = '\n\nImport dataset for prediction:\n{}\n'.format(
            self.dataset.pixel_connector.__repr__())
        sys.stdout.write(msg)
        
    def predict(self, multichannel=False, progress_bar=None):
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
            # progress_bar.value = (item_nr + 1) / len(data_predict)
            result = self.model.predict(item.pixels())
            item.put_probmap_data(result)

        sys.stdout.write('Writing probability maps finished.\n')
