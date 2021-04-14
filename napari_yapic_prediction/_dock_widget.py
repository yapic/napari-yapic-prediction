"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_yapic_prediction.yapic_dependencies.yapic_prediction import yapic_prediction
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QGroupBox
from napari_plugin_engine import napari_hook_implementation
from pathlib import Path
from PyQt5 import QtCore

class MyWidget(QWidget):
    def __init__(self, napari_viewer):
        self.viewer = napari_viewer
        super().__init__()
        
        self.model_path = None

        # initialize layout
        layout = QGridLayout()

        # add a button
        btn1 = QPushButton('Upload a YAPiC Model', self)
        btn1.clicked.connect(self.load_model)
        
        self.model_name = QLabel('Please select a model')
        self.model_name.setAlignment(QtCore.Qt.AlignCenter)
        
        btn2 = QPushButton('Predict', self)
        btn2.clicked.connect(self.predict)
        
        self.horizontalGroupBox = QGroupBox("Grid")
        
        layout.addWidget(btn1)
        layout.addWidget(self.model_name)
        layout.addWidget(btn2)

        # activate layout
        self.setLayout(layout)
        
    def load_model(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Model File', 'Model files (*.h5)')
        self.model_path = Path(file_name)
        # self.model_name.setText('Selected model: {}'.format(self.model_path.name))
        self.model_name.setText('Selected Model: {}'.format(self.model_path.name))
        
    def predict(self):
        yapic_prediction(self.model_path, self.viewer, None)

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return MyWidget, {'area':'left'}

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


