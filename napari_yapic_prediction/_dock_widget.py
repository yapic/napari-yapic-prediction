from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton,
                             QLabel, QFileDialog, QProgressBar,
                             QGroupBox, QCheckBox)
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

        self.save_flag = QCheckBox('Save probability maps', self)

        btn_predict = QPushButton('Predict', self)
        btn_predict.clicked.connect(self.predict)

        GroupBox = QGroupBox()
        progress_layout = QGridLayout()

        self.progress_map_label = QLabel('Mapping:')
        self.progress_map = QProgressBar()
        self.progress_upload_label = QLabel('Uploading:')
        self.progress_upload = QProgressBar()

        progress_layout.addWidget(self.progress_map_label, 0, 0)
        progress_layout.addWidget(self.progress_map, 0, 1)
        progress_layout.addWidget(self.progress_upload_label, 1, 0)
        progress_layout.addWidget(self.progress_upload, 1, 1)

        GroupBox.setLayout(progress_layout)

        layout.addWidget(btn_upload)
        layout.addWidget(self.model_name)
        layout.addWidget(self.save_flag)
        layout.addWidget(btn_predict)
        layout.addWidget(GroupBox)

        self.setLayout(layout)

    def load_model(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Model File',
                                                   'Model files (*.h5)')
        self.model_path = Path(file_name)
        self.model_name.setText('Selected Model: {}'.format(
            self.model_path.name))

    def predict(self):
        self.progress_map.setValue(0)
        self.progress_upload.setValue(0)
        yapic_prediction(self.model_path, self.viewer, self.progress_map,
                         self.progress_upload, self.save_flag.isChecked())


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return MyWidget, {'area': 'left'}
