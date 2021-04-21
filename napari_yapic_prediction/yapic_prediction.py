from .yapic_dependencies import NapariSession
from skimage import io
import numpy as np
import h5py
import os


def get_lbl_map(model_path):
    """Returns a dictionary retriving the label mapping done by Yapic.
    
    Keys: Napari label values.
    Values: YAPiC label mapping.
    """
    f = h5py.File(model_path, 'r')
    map_dataset = f['lbl_map']
    return {nap: yap for yap, nap in map_dataset}
    
    
def tif_2_layer(tif_path, lbl_map):
    """Reads temporal tiff file and returns a numpy array. Tiff file is deleted before within the function."""
    img_data = io.imread(tif_path)
    if img_data.shape == 3:
        img_data = np.expand_dims(img_data, axis=0)
    depth, width, height, _ = img_data.shape
    label_output = np.zeros((depth, width, height))
    for z in range(depth):
        for x in range(width):
            for y in range(height):
                pixel_probs = img_data[z, x, y]
                max_index = np.argmax(pixel_probs)
                label_output[z, x, y] = lbl_map[max_index + 1]
    os.remove(tif_path)
    return label_output.astype(int)

def yapic_prediction(model_path, viewer, progress_label, progress_bar):
    """This function adds the label layers corresponding to the prediction of all the images uploaded in the Napari viewer.
    
    Parameters
        ----------
        model_path : str
            YAPiC model with .h5 extension.
        viewer : napari.viewer.Viewer
            Napari viewer instance.
        progress_label : PyQt5.QtWidgets.QLabel
            PyQt label instance - Progress bar label.
        progress_bar : PyQt5.QtWidgets.QProgressBar
            PyQt progress bar instance.
    """
    assert os.path.isfile(model_path) and os.path.splitext(model_path)[-1] == '.h5', '<network> must be a h5 model file'
    
    # temporal folder creation
    work_dir = os.path.dirname(model_path)
    tmp_dir = os.path.join(work_dir, 'tmp')
    os.mkdir(tmp_dir)
    
    # Geting label mapping values (dictionary)
    lbl_map = get_lbl_map(model_path)
    
    # predicting
    s = NapariSession()
    s.load_prediction_data(viewer, tmp_dir)
    s.load_model(model_path)
    s.set_normalization('local')
    s.predict(True, progress_bar)
    
    # Widget update
    progress_label.setText('Uploading:')
    progress_bar.setValue(0)
    
    # Adding to Napari
    files2upload = os.listdir(tmp_dir)
    N = len(files2upload)
    
    for i, label_file in enumerate(files2upload):
        file_path = os.path.join(tmp_dir, label_file)
        label_name = label_file.split('.')[0]
        label_data = tif_2_layer(file_path, lbl_map)
        viewer.add_labels(label_data, name='{}_prediction'.format(label_name))
        progress_bar.setValue((i + 1) * 100 / N)
        
    # Deleting temporal folder
    os.rmdir(tmp_dir)
    
