# """
# This module is an example of a barebones QWidget plugin for napari

# It implements the ``napari_experimental_provide_dock_widget`` hook specification.
# see: https://napari.org/docs/dev/plugins/hook_specifications.html

# Replace code below according to your needs.
# """
from napari_plugin_engine import napari_hook_implementation
# from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton


# class MyWidget(QWidget):
#     # your QWidget.__init__ can optionally request the napari viewer instance
#     # in one of two ways:
#     # 1. use a parameter called `napari_viewer`, as done here
#     # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
#     def __init__(self, napari_viewer):
#         super().__init__()
#         self.viewer = napari_viewer

#         btn = QPushButton("Click me!")
#         btn.clicked.connect(self._on_click)

#         self.setLayout(QHBoxLayout())
#         self.layout().addWidget(btn)

#     def _on_click(self):
#         print("napari has", len(self.viewer.layers), "layers")



# @napari_hook_implementation
# def napari_experimental_provide_dock_widget():
#     return MyWidget

from magicgui.widgets import FileEdit, Label, Container, ProgressBar, PushButton
from napari_yapic_prediction.yapic_dependencies.yapic_prediction import yapic_prediction
from magicgui import magicgui
from pathlib import Path
import napari


def mywidget(napari_viewer: napari.viewer.Viewer):
    # make some widgets
    file_picker = FileEdit(label='Model file path:', value='')
    label = Label(label='Uploaded model:', value=file_picker.value)
    button = PushButton(label='Predict')
    progress = ProgressBar(label='Prediction mapping:', visible=False, value = 0, min = 0, max=1)

    #set up callbacks
    def set_label(event):
        label.value = file_picker.value.name

    def prediction(event):
        progress.visible = True
        yapic_prediction(file_picker.value, napari_viewer, progress)
            

    file_picker.changed.connect(set_label)
    button.changed.connect(prediction)

    # create a container to hold the widgets:
    container = Container(widgets=[file_picker, label, button, progress])
    return container, {'area':'left'}

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return mywidget
