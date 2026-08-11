import numpy as np

from qutip import basis, ket2dm, tensor, Qobj, qeye

from config import MAX_STEPS, OAM_DIMENSION

from physics.operators import SHIFT_UP, SHIFT_DOWN
from physics.states import L, R

class Walker:
    def __init__(self, initial_polarization, initial_oam=0):

        if abs(initial_oam) > MAX_STEPS:
            raise ValueError(f"Initial OAM must be between -{MAX_STEPS} and {MAX_STEPS}")

        shape = initial_polarization.shape

        if shape == (2,2):
            self.system = "single"
        elif shape == (4,4):
            self.system = "two"
        else:
            raise ValueError(f"Unsupported polarization dimension {shape}")

        oam_state = ket2dm(basis(OAM_DIMENSION, initial_oam + MAX_STEPS))

        if self.system == "single":
            self.state = tensor(oam_state, initial_polarization)
        else:
            self.state = tensor(oam_state, oam_state, initial_polarization)
            self.state = self.state.permute([0, 2, 1, 3])

    # Public methods
    def hwp(self, angle):
        self._waveplate(angle, np.pi)

    def qwp(self, angle):
        self._waveplate(angle, np.pi/2)

    def qplate(self):
        qplate_lr = (
            tensor(SHIFT_UP, R * L.dag())
            +
            tensor(SHIFT_DOWN, L * R.dag())
        )
        
        hv_to_lr = Qobj([
            [1, 1],
            [1j, -1j]
        ]) / np.sqrt(2)

        transform = tensor(qeye(OAM_DIMENSION), hv_to_lr)

        single_qplate_hv = transform.dag() * qplate_lr * transform

        if self.system == "single":
            qplate_hv = single_qplate_hv
        else:
            qplate_hv = tensor(single_qplate_hv, single_qplate_hv)

        self.state = qplate_hv * self.state * qplate_hv.dag()

    def get_probabilities(self):
        probabilities = []

        if self.system == "single":
            identity = tensor(qeye(2))
        else:
            # Everything but OAM modes of the first photon are ignored
            identity = tensor(qeye(2), qeye(OAM_DIMENSION), qeye(2))

        for l in range(-MAX_STEPS, MAX_STEPS + 1):
            oam_projector = (
                basis(OAM_DIMENSION, l + MAX_STEPS)
                *
                basis(OAM_DIMENSION, l + MAX_STEPS).dag()
            )

            # Only get the OAM mode probabilities of the first photon
            projector = tensor(oam_projector, identity)
        
            probability = (self.state * projector).tr().real
            probabilities.append(probability)

        return probabilities
    
    def sample_photons(self, number_of_photons):
        probabilities = self.get_probabilities()

        samples = np.random.choice(
            OAM_DIMENSION,
            size=number_of_photons,
            p=probabilities
        )

        counts = np.bincount(
            samples,
            minlength=OAM_DIMENSION
        )

        return counts

    def get_state(self):
        return self.state

    # Private methods
    def _waveplate(self, angle, retardance):
        theta = np.deg2rad(angle)

        rotation = Qobj([
            [np.cos(2 * theta), np.sin(2 * theta)],
            [np.sin(2 * theta), -np.cos(2 * theta)]
        ])

        phase = Qobj([
            [np.exp(1j * retardance / 2), 0],
            [0, np.exp(-1j * retardance / 2)]
        ])

        single_operator = rotation.dag() * phase * rotation

        single_operator = tensor(qeye(OAM_DIMENSION), single_operator)

        if self.system == "single":
            polarization_operator = single_operator
        else:
            polarization_operator = tensor(single_operator, single_operator)

        self.state = polarization_operator * self.state * polarization_operator.dag()