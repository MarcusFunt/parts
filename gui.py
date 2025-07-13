import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from optimization import Optimizer, default_control_points
from geometry import SplineProfile


class SplineCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(4, 3))
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.profile = None

    def draw_profile(self, control_points):
        self.ax.clear()
        profile = SplineProfile(control_points)
        pts = profile.sample()
        self.ax.plot(pts[:, 0], pts[:, 1])
        self.ax.set_xlabel('Radius')
        self.ax.set_ylabel('Axial')
        self.ax.set_aspect('equal')
        self.draw()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vortex Cannon Optimizer')
        self.optimizer = None
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        self.diameter_edit = QtWidgets.QDoubleSpinBox()
        self.diameter_edit.setValue(0.1)
        self.stroke_edit = QtWidgets.QDoubleSpinBox()
        self.stroke_edit.setValue(0.05)
        self.chamber_edit = QtWidgets.QDoubleSpinBox()
        self.chamber_edit.setValue(0.2)
        self.energy_edit = QtWidgets.QDoubleSpinBox()
        self.energy_edit.setValue(1.0)
        form.addRow('Driver diameter (m)', self.diameter_edit)
        form.addRow('Stroke (m)', self.stroke_edit)
        form.addRow('Chamber length (m)', self.chamber_edit)
        form.addRow('Max energy (J)', self.energy_edit)
        layout.addLayout(form)

        self.surface_check = QtWidgets.QCheckBox('3D print texture')
        layout.addWidget(self.surface_check)

        self.start_btn = QtWidgets.QPushButton('Start Optimization')
        self.start_btn.clicked.connect(self.start_optimization)
        layout.addWidget(self.start_btn)

        self.canvas = SplineCanvas(self)
        layout.addWidget(self.canvas)

        self.metrics_label = QtWidgets.QLabel('Metrics:')
        layout.addWidget(self.metrics_label)

    def start_optimization(self):
        hardware = {
            'diameter': self.diameter_edit.value(),
            'stroke': self.stroke_edit.value(),
            'chamber': self.chamber_edit.value(),
            'energy': self.energy_edit.value(),
        }
        targets = {'velocity': 1.0, 'range': 1.0, 'stability': 0.5}
        bounds = [((0.0, 0.0), (0.5, 0.5)) for _ in range(4)]
        self.optimizer = Optimizer(hardware, targets, bounds, iterations=20,
                                   callback=self.update_results,
                                   surface_roughness=self.surface_check.isChecked())
        self.optimizer.start()

    def update_results(self, points, metrics, score):
        QtCore.QMetaObject.invokeMethod(self, '_update_results', QtCore.Qt.QueuedConnection,
                                        QtCore.Q_ARG(object, points),
                                        QtCore.Q_ARG(object, metrics),
                                        QtCore.Q_ARG(float, score))

    @QtCore.pyqtSlot(object, object, float)
    def _update_results(self, points, metrics, score):
        self.canvas.draw_profile(points)
        text = '\n'.join(f'{k}: {v:.3f}' for k, v in metrics.items())
        self.metrics_label.setText(text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
