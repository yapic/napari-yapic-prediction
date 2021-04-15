from napari_yapic_prediction.yapic_dependencies.yapic_pred_session import NapariSession
from skimage import io
import numpy as np
import os

def tif_2_layer(tif_path):
    img_data = io.imread(tif_path)
    width, height, _ = img_data.shape
    label_output = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            pixel_probs = img_data[x, y]
            label_output[x, y] = np.argmax(pixel_probs)
    return label_output.astype(int)

def yapic_prediction(model_path, viewer, progress_label, progress_bar):
    assert os.path.isfile(model_path) and os.path.splitext(model_path)[-1] == '.h5', '<network> must be a h5 model file'
    
    # temporal folder creation
    work_dir = os.path.dirname(model_path)
    tmp_dir = os.path.join(work_dir, 'tmp')
    os.mkdir(tmp_dir)
    
    # predicting
    s = NapariSession()
    s.load_prediction_data(viewer, tmp_dir)
    s.load_model(model_path)
    s.set_normalization('local')
    s.predict(True, progress_bar)
    
    progress_label.setText('Uploading:')
    progress_bar.setValue(0)
    
    # Adding to Napari
    files2upload = os.listdir(tmp_dir)
    N = len(files2upload)
    
    for i, label_file in enumerate(files2upload):
        file_path = os.path.join(tmp_dir, label_file)
        label_name = label_file.split('.')[0]
        label_data = tif_2_layer(file_path)
        viewer.add_labels(label_data, name='{}_prediction'.format(label_name))
        os.remove(file_path)
        progress_bar.setValue((i + 1) * 100 / N)
        
    # Deleting temporal folder
    os.rmdir(tmp_dir)
    
