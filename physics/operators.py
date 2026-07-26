from qutip import basis

from config import MAX_STEPS, OAM_DIMENSION

def build_shift_up():
    operator = 0

    for l in range(-MAX_STEPS, MAX_STEPS):
        operator += (
            basis(OAM_DIMENSION, l + 1 + MAX_STEPS)
            *
            basis(OAM_DIMENSION, l + MAX_STEPS).dag()
        )

    return operator

def build_shift_down():
    operator = 0

    for l in range(-MAX_STEPS + 1, MAX_STEPS + 1):
        operator += (
            basis(OAM_DIMENSION, l - 1 + MAX_STEPS)
            *
            basis(OAM_DIMENSION, l + MAX_STEPS).dag()
        )

    return operator

SHIFT_UP = build_shift_up()

SHIFT_DOWN = build_shift_down()