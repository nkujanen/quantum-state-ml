from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)

from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap

from config import MAX_STEPS


class ResultsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_histogram(self, counts):
        self.axes.clear()

        oam_values = range(-MAX_STEPS, MAX_STEPS + 1)

        self.axes.bar(oam_values, counts)
        self.axes.set_xlabel(r"OAM mode $\ell$")
        self.axes.set_ylabel("Photon counts")
        self.axes.set_title("Measured OAM distribution")

        self.canvas.draw()

    def update_heatmap(self, counts):
        self.axes.clear()

        cmap = LinearSegmentedColormap.from_list(
            "white_to_blue",
            ["white", "blue"]
        )
        
        self.axes.imshow(
            counts,
            origin="lower",
            extent=[
                -MAX_STEPS - 0.5,
                MAX_STEPS + 0.5,
                -MAX_STEPS - 0.5,
                MAX_STEPS + 0.5
            ],
            aspect="auto",
            cmap=cmap
        )

        self.axes.set_xlabel(r"Photon B OAM mode $\ell_B$")
        self.axes.set_ylabel(r"Photon A OAM mode $\ell_A$")
        self.axes.set_title("Measured OAM coincidences")

        self.canvas.draw()