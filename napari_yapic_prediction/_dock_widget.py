"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_yapic_prediction.yapic_dependencies.yapic_prediction import yapic_prediction
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QHBoxLayout, QGroupBox
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
        
        self.model_name = QLabel('')
        self.model_name.setAlignment(QtCore.Qt.AlignCenter)
        
        btn2 = QPushButton('Predict', self)
        btn2.clicked.connect(self.predict)
        
        self.horizontalGroupBox = QGroupBox()
        progress_layout = QHBoxLayout()
        self.progres_label = QLabel('Mapping:')
        self.progress = QProgressBar()
        progress_layout.addWidget(self.progres_label)
        progress_layout.addWidget(self.progress)
        
        self.horizontalGroupBox.setLayout(progress_layout)
        
        
        layout.addWidget(btn1)
        layout.addWidget(self.model_name)
        layout.addWidget(btn2)
        layout.addWidget(self.horizontalGroupBox)

        # activate layout
        self.setLayout(layout)
        
    def load_model(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Model File', 'Model files (*.h5)')
        self.model_path = Path(file_name)
        # self.model_name.setText('Selected model: {}'.format(self.model_path.name))
        self.model_name.setText('Selected Model: {}'.format(self.model_path.name))
        
    def predict(self):
        self.progress_label.setText('Mapping:')
        yapic_prediction(self.model_path, self.viewer, self.progres_label, self.progress)

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return MyWidget, {'area':'left'}

