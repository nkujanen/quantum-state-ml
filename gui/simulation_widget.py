from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton
)

from config import (
    MIN_STEPS,
    MAX_STEPS,
    DEFAULT_STEPS,
    MIN_PHOTONS,
    MAX_PHOTONS,
    DEFAULT_PHOTONS
)


class SimulationWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()


        # Step configuration
        step_box = QGroupBox("Step configuration")
        step_layout = QGridLayout()

        # HWP
        step_layout.addWidget(
            QLabel("HWP angle (deg)"),
            0,
            0
        )
        self.hwp_angle = QDoubleSpinBox()
        self.hwp_angle.setRange(0, 90)
        self.hwp_angle.setSingleStep(1)
        step_layout.addWidget(self.hwp_angle, 0, 1)

        # QWP
        step_layout.addWidget(
            QLabel("QWP angle (deg)"),
            1,
            0
        )
        self.qwp_angle = QDoubleSpinBox()
        self.qwp_angle.setRange(0, 180)
        self.qwp_angle.setSingleStep(1)
        step_layout.addWidget(self.qwp_angle, 1, 1)

        # Q plate
        step_layout.addWidget(
            QLabel("Q-plate"),
            2,
            0
        )
        qplate_label = QLabel("q = 1/2")
        qplate_label.setEnabled(False)
        step_layout.addWidget(qplate_label, 2, 1)

        step_box.setLayout(step_layout)

        # Simulation parameters
        parameter_box = QGroupBox("Simulation parameters")
        parameter_layout = QGridLayout()

        # Steps
        parameter_layout.addWidget(
            QLabel("Number of steps"),
            0,
            0
        )
        self.steps_input = QSpinBox()
        self.steps_input.setRange(MIN_STEPS, MAX_STEPS)
        self.steps_input.setValue(DEFAULT_STEPS)
        parameter_layout.addWidget(self.steps_input, 0, 1)

        # Photons
        parameter_layout.addWidget(
            QLabel("Number of photons"),
            1,
            0
        )
        self.photons_input = QSpinBox()
        self.photons_input.setRange(MIN_PHOTONS, MAX_PHOTONS)
        self.photons_input.setValue(DEFAULT_PHOTONS)
        parameter_layout.addWidget(self.photons_input, 1, 1)

        parameter_box.setLayout(parameter_layout)

        # Buttons
        self.run_button = QPushButton("RUN SIMULATION")
        self.save_button = QPushButton("SAVE TO CSV")
        self.append_button = QPushButton("APPEND CSV")

        # Combine sections
        main_layout.addWidget(step_box)
        main_layout.addWidget(parameter_box)
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.append_button)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def get_steps(self):
        return self.steps_input.value()
    
    def get_hwp_angle(self):
        return self.hwp_angle.value()
    
    def get_qwp_angle(self):
        return self.qwp_angle.value()

    def get_photons(self):
        return self.photons_input.value()