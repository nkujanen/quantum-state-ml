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

        single_operator = transform.dag() * qplate_lr * transform

        if self.system == "single":
            full_operator = single_operator
        else:
            full_operator = tensor(single_operator, single_operator)

        self.state = full_operator * self.state * full_operator.dag()

    def single_photon_probabilities(self):
        if self.system != "single":
            raise ValueError("Single probabilities can only be calculated for a single-photon system")
        probabilities = []

        identity = qeye(2)
        
        for l in range(-MAX_STEPS, MAX_STEPS + 1):
            oam_projector = (
                basis(OAM_DIMENSION, l + MAX_STEPS)
                *
                basis(OAM_DIMENSION, l + MAX_STEPS).dag()
            )

            projector = tensor(oam_projector, identity)
            probability = (self.state * projector).tr().real
            probabilities.append(probability)

        return probabilities

    def two_photon_probabilities(self):
        if self.system != "two":
            raise ValueError("Joint probabilities can only be calculated for a two-photon system")

        joint_probabilities = np.zeros((OAM_DIMENSION, OAM_DIMENSION))

        identity = qeye(2)

        for i, l_a in enumerate(range(-MAX_STEPS, MAX_STEPS + 1)):
            projector_a = (
                basis(OAM_DIMENSION, l_a + MAX_STEPS)
                *
                basis(OAM_DIMENSION, l_a + MAX_STEPS).dag()
            )

            for j, l_b in enumerate(range(-MAX_STEPS, MAX_STEPS + 1)):
                projector_b = (
                    basis(OAM_DIMENSION, l_b + MAX_STEPS)
                    *
                    basis(OAM_DIMENSION, l_b + MAX_STEPS).dag()
                )

                projector = tensor(
                    projector_a,
                    identity,
                    projector_b,
                    identity
                )

                joint_probabilities[i, j] = (self.state * projector).tr().real

        return joint_probabilities

    def sample_photons(self, number_of_photons):
        if self.system == "single":
            probabilities = self.single_photon_probabilities()

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

        else:
            joint_probabilities = self.two_photon_probabilities()

            joint_probabilities = joint_probabilities.flatten()
            joint_probabilities /= joint_probabilities.sum()

            samples = np.random.choice(
                OAM_DIMENSION ** 2,
                size=number_of_photons,
                p=joint_probabilities
            )

            coincidence_counts = np.bincount(
                samples,
                minlength=OAM_DIMENSION ** 2
            ).reshape(OAM_DIMENSION, OAM_DIMENSION)

            a_counts = coincidence_counts.sum(axis=1)
            b_counts = coincidence_counts.sum(axis=0)

            return coincidence_counts, a_counts, b_counts

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
            full_operator = single_operator
        else:
            full_operator = tensor(single_operator, single_operator)

        self.state = full_operator * self.state * full_operator.dag()