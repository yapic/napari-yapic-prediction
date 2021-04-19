from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QHBoxLayout, QGroupBox
from napari_plugin_engine import napari_hook_implementation
from .yapic_prediction import yapic_prediction
from pathlib import Path
from PyQt5 import QtCore

class MyWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        
        self.viewer = napari_viewer
        self.model_path = None

        layout = QGridLayout()

        btn_upload = QPushButton('Upload a YAPiC Model', self)
        btn_upload.clicked.connect(self.load_model)
        
        self.model_name = QLabel('')
        self.model_name.setAlignment(QtCore.Qt.AlignCenter)
        
        btn_predict = QPushButton('Predict', self)
        btn_predict.clicked.connect(self.predict)
        
        horizontalGroupBox = QGroupBox()
        progress_layout = QHBoxLayout()
        self.progress_label = QLabel('Mapping:')
        self.progress = QProgressBar()
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress)
        horizontalGroupBox.setLayout(progress_layout)
        
        layout.addWidget(btn_upload)
        layout.addWidget(self.model_name)
        layout.addWidget(btn_predict)
        layout.addWidget(horizontalGroupBox)

        self.setLayout(layout)
        
    def load_model(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Model File', 'Model files (*.h5)')
        self.model_path = Path(file_name)
        self.model_name.setText('Selected Model: {}'.format(self.model_path.name))
        
    def predict(self):
        self.progress_label.setText('Mapping:')
        yapic_prediction(self.model_path, self.viewer, self.progress_label, self.progress)

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return MyWidget, {'area':'left'}

