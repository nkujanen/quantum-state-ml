from qutip import (
    basis,
    ket2dm,
    tensor,
    qzero
)

# Single photon basis
H = basis(2, 0)
V = basis(2, 1)

# Linear polarisation
D = (H + V).unit()
A = (H - V).unit()

# Circular polarisation
R = (H - 1j*V).unit()
L = (H + 1j*V).unit()

# Two-photon basis
HH = tensor(H, H)
HV = tensor(H, V)
VH = tensor(V, H)
VV = tensor(V, V)

# Bell states
Bell_Phi_Plus = (HH + VV).unit()
Bell_Phi_Minus = (HH - VV).unit()
Bell_Psi_Plus = (HV + VH).unit()
Bell_Psi_Minus = (HV - VH).unit()

# Maximally mixed 2-photon state
MM = (
    0.25 * ket2dm(HH)
    + 0.25 * ket2dm(HV)
    + 0.25 * ket2dm(VH)
    + 0.25 * ket2dm(VV)
)

SINGLE_PHOTON_PRESETS = {
    "None": qzero([2]),
    "H": ket2dm(H),
    "V": ket2dm(V),
    "D": ket2dm(D),
    "A": ket2dm(A),
    "R": ket2dm(R),
    "L": ket2dm(L),
    "50/50": (0.5 * ket2dm(H) + 0.5 * ket2dm(V)),
    "80/20": (0.8 * ket2dm(H) + 0.2 * ket2dm(V))
}

TWO_PHOTON_PRESETS = {
    "None": qzero([2,2]),
    "HH": ket2dm(HH),
    "HV": ket2dm(HV),
    "VH": ket2dm(VH),
    "VV": ket2dm(VV),
    "Bell Phi+": ket2dm(Bell_Phi_Plus),
    "Bell Phi-": ket2dm(Bell_Phi_Minus),
    "Bell Psi+": ket2dm(Bell_Psi_Plus),
    "Bell Psi-": ket2dm(Bell_Psi_Minus),
    "Maximally mixed": MM,
    "Werner Phi- 80%": (
        0.8 * ket2dm(Bell_Phi_Minus)
        +
        0.2 * MM
    )
}