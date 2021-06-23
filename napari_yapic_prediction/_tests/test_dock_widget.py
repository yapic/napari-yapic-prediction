from napari_yapic_prediction.yapic_prediction import tif_2_layer, get_lbl_map
from skimage import io
import numpy as np
import os

im_path = './napari_yapic_prediction/_tests/data/leaves_2.tif'
lbl_map_path = './napari_yapic_prediction/_tests/data/test_file.h5'

def test_get_lbl_map():
    mapping = get_lbl_map(lbl_map_path)
    assert mapping == {1:100, 2:200, 3:300}
    
def test_tif_2_layer():
    img_data = io.imread(im_path)
    tmp_path = './napari_yapic_prediction/_tests/data/leaves_2_tmp.tif'
    io.imsave(tmp_path, img_data)
    output = tif_2_layer(tmp_path, {1: 1, 2: 2}, False)
    assert isinstance(output, np.ndarray)
    assert output.shape == (1, 790, 790)
    assert not os.path.exists(tmp_path)
