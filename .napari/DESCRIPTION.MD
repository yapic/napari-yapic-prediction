# Description

This plugin creates a section within the napari window to upload and run trained models generated with [YAPiC](https://yapic.github.io/yapic/). The model prediction results will be display in the napari window as label layers that you can edit.

# Who is this for?

In order to make segmentation predictions, the model must be trained in advance, outside of the napari window. Any user with a trained YAPiC model can use this plugin to see their results.

# Quick start

Before starting using this plugin, please install either the GPU or CPU version of tensorflow in case you do not have it installed.

Once the `napari-yapic-prediction` plugin is installed, click on "Plugins" and click on "napari-yapic-prediction: My Widget". After this, a new menu should appear in the bottom left corner of the napari window.

Click in the "Upload a YAPiC Model" button to browse and upload your model file. The uploaded model name will be displayed in the napari window.

Optionally, you can click the "Save probability maps" option in case you want to store the original probability maps in a folder located in the same place as the model.

Finally, clicking on "Predict" will make a prediction over all the present image layers in the napari window. The results will be new label layers which took the label value with the highest probability from the probability maps.

You do not have to worry about having additional layers, this plugin will only take into account the image layers.

Tip: You can use the `napari-hdf5-labels-io` to store your results or to store the labels you will use in YAPiC to perform the model training.