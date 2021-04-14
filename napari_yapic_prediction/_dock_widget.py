"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from qtpy.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QFileDialog
from napari_plugin_engine import napari_hook_implementation

class MyWidget(QWidget):
    def __init__(self, napari_viewer):
        self.viewer = napari_viewer
        super().__init__()

        # initialize layout
        layout = QGridLayout()

        # add a button
        btn = QPushButton('Click me!', self)
        def load_model():
            file_name, _ = QFileDialog.getOpenFileName(self, 'Select Model File', 'Model files (*.h5)')
            model_name.setText('Selected model: {}'.format(file_name.name))
            return 'hola.h5'
        btn.clicked.connect(load_model)
        
        model_name = QLabel()
        
        layout.addWidget(btn)
        layout.addWidget(model_name)

        # activate layout
        self.setLayout(layout)

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return MyWidget

# _________________________________________

# from napari_plugin_engine import napari_hook_implementation
# from magicgui.widgets import FileEdit, Label, Container, ProgressBar, PushButton
# from napari_yapic_prediction.yapic_dependencies.yapic_prediction import yapic_prediction
# from magicgui import magicgui, magic_factory
# from pathlib import Path
# from napari import Viewer
# import napari

# def mywidget(napari_viewer: napari.viewer.Viewer):
#     # make some widgets
#     file_picker = FileEdit(label='Model file path:', value='')
#     label = Label(label='Uploaded model:', value=file_picker.value)
#     button = PushButton(label='Predict')
#     progress = ProgressBar(label='Prediction mapping:', visible=False, value = 0, min = 0, max=1)

#     #set up callbacks
#     def set_label(event):
#         label.value = file_picker.value.name

#     def prediction(event):
#         progress.visible = True
#         yapic_prediction(file_picker.value, napari_viewer, progress)
            

#     file_picker.changed.connect(set_label)
#     button.changed.connect(prediction)

#     # create a container to hold the widgets:
#     container = Container(widgets=[file_picker, label, button, progress])
#     return container, {'area':'left'}

# @napari_hook_implementation
# def napari_experimental_provide_dock_widget():
#     return mywidget

# _________________________________________________________________


