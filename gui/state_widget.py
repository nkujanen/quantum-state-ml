from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QComboBox,
    QLineEdit,
    QGridLayout,
    QGroupBox,
    QLabel
)

from physics.states import (
    SINGLE_PHOTON_PRESETS,
    TWO_PHOTON_PRESETS
)


class StateWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.system = "Single photon"
        self.current_state = None
        self.parameters = {}

        self.init_ui()


    def init_ui(self):
        # Main box
        main_layout = QVBoxLayout()

        # System selection
        system_box = QGroupBox("System")
        system_layout = QVBoxLayout()


        self.single_radio = QRadioButton("Single photon")
        self.two_radio = QRadioButton("Two photons")


        self.single_radio.setChecked(True)
        self.single_radio.clicked.connect(self.change_system)
        self.two_radio.clicked.connect(self.change_system)


        system_layout.addWidget(self.single_radio)
        system_layout.addWidget(self.two_radio)

        system_box.setLayout(system_layout)

        # Preset selection
        preset_box = QGroupBox("Preset")
        preset_layout = QVBoxLayout()

        self.preset_dropdown = QComboBox()
        self.preset_dropdown.currentTextChanged.connect(self.load_preset)
        preset_layout.addWidget(self.preset_dropdown)

        preset_box.setLayout(preset_layout)

        # Density matrix
        self.matrix_box = QGroupBox("Density matrix")
        self.state_layout = QGridLayout()

        self.matrix_box.setLayout(self.state_layout)

        # Combine sections
        main_layout.addWidget(system_box)
        main_layout.addWidget(preset_box)
        main_layout.addWidget(self.matrix_box)

        self.setLayout(main_layout)

        self.update_fields()

    def change_system(self):
        if self.single_radio.isChecked():
            self.system = "Single photon"
        else:
            self.system = "Two photons"

        self.update_fields()

    def update_fields(self):
        # Remove previous widgets
        while self.state_layout.count():
            item = self.state_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.parameters.clear()

        # Set basis and presets
        if self.system == "Single photon":
            presets = list(SINGLE_PHOTON_PRESETS.keys())
            basis = ["H", "V"]
        else:
            presets = list(TWO_PHOTON_PRESETS.keys())
            basis = ["HH", "HV", "VH", "VV"]

        # Update dropdown
        self.preset_dropdown.clear()

        self.preset_dropdown.addItems(presets)

        # Density matrix labels
        self.state_layout.addWidget(QLabel(""), 0, 0)

        # Columns
        for col, col_label in enumerate(basis):
            self.state_layout.addWidget(
                QLabel(col_label),
                0,
                col + 1
            )

        # Rows and entries
        for row, row_label in enumerate(basis):
            self.state_layout.addWidget(
                QLabel(row_label),
                row + 1,
                0
            )

            for col in range(len(basis)):
                entry = QLineEdit()

                self.parameters[(row, col)] = entry

                self.state_layout.addWidget(
                    entry,
                    row + 1,
                    col + 1
                )

        self.load_preset(self.preset_dropdown.currentText())

    def load_preset(self, preset):
        if not preset:
            return

        if self.system == "Single photon":
            state = SINGLE_PHOTON_PRESETS[preset]
        else:
            state = TWO_PHOTON_PRESETS[preset]

        self.current_state = state

        self.fill_matrix_fields(state)

    def fill_matrix_fields(self, state):
        matrix = state.full()

        for (row, col), entry in self.parameters.items():
            value = matrix[row, col]
            entry.setText(f"{value:.2f}")

    def get_state(self):
        return self.current_state