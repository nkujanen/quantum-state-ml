import numpy as np

from qutip import basis, ket2dm, tensor, Qobj, qeye

from config import MAX_STEPS, OAM_DIMENSION

from physics.operators import SHIFT_UP, SHIFT_DOWN
from physics.states import L, R

class Walker:
    def __init__(self, initial_polarization, initial_oam=0):

        if abs(initial_oam) > MAX_STEPS:
            raise ValueError(f"Initial OAM must be less than {MAX_STEPS}")

        oam_state = ket2dm(
            basis(OAM_DIMENSION, initial_oam + MAX_STEPS)
        )

        self.state = tensor(oam_state, initial_polarization)

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

        qplate_hv = transform.dag() * qplate_lr * transform

        self.state = qplate_hv * self.state * qplate_hv.dag()

    def get_probabilities(self):
        probabilities = []

        for l in range(-MAX_STEPS, MAX_STEPS + 1):
            projector = tensor(
                basis(OAM_DIMENSION, l + MAX_STEPS)
                *
                basis(OAM_DIMENSION, l + MAX_STEPS).dag(),
                qeye(2)
            )
        
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

        polarization_operator = rotation.dag() * phase * rotation

        operator = tensor(qeye(OAM_DIMENSION), polarization_operator)

        self.state = operator * self.state * operator.dag()