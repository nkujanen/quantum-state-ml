from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from gui.state_widget import StateWidget
from gui.simulation_widget import SimulationWidget
from gui.results_widget import ResultsWidget

from physics.walker import Walker


class QuantumStateGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quantum Walk Simulator")

        self.init_ui()

    def init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()

        # Top horizontal section
        top_layout = QHBoxLayout()

        # Create panels
        self.state_widget = StateWidget()
        self.simulation_widget = SimulationWidget()
        self.results_widget = ResultsWidget()

        # Add left and right panels
        top_layout.addWidget(self.state_widget, 1)
        top_layout.addWidget(self.simulation_widget, 1)

        # Add top section
        main_layout.addLayout(top_layout, 1)

        # Add results below
        main_layout.addWidget(self.results_widget, 2)
        self.setLayout(main_layout)

        # Connect "run simulation" button
        self.simulation_widget.run_button.clicked.connect(
            self.run_simulation
        )

    def run_simulation(self):
        # Retrieve parameters from input fields
        polarization_state = self.state_widget.get_state()
        steps = self.simulation_widget.get_steps()
        hwp_angle = self.simulation_widget.get_hwp_angle()
        qwp_angle = self.simulation_widget.get_qwp_angle()
        n_photons = self.simulation_widget.get_photons()

        # Initialise walker
        walker = Walker(polarization_state)

        for _ in range(steps):
            walker.hwp(hwp_angle)
            walker.qwp(qwp_angle)
            walker.qplate()

        measurements = walker.sample_photons(n_photons)

        if walker.system == "single":
            self.results_widget.update_histogram(measurements)
        else:
            coincidence_counts, a_counts, b_counts = measurements
            self.results_widget.update_heatmap(coincidence_counts)