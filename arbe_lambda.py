import math
from typing import Iterable, Sequence

R_STAR = math.sqrt(2) - 1

def compute_lambda_star(wavelengths: Sequence[float], reflectances: Sequence[float]) -> float:
    """Compute the lambda* value for a spectrum.

    Parameters
    ----------
    wavelengths : Sequence[float]
        Wavelength values corresponding to reflectances.
    reflectances : Sequence[float]
        Reflectance values between 0 and 1.

    Returns
    -------
    float
        The interpolated wavelength at which the spectrum first crosses R_STAR
        on a rising edge.
    """
    if len(wavelengths) != len(reflectances):
        raise ValueError("wavelength and reflectance arrays must have same length")

    for i in range(len(wavelengths) - 1):
        r0, r1 = reflectances[i], reflectances[i + 1]
        if r0 < R_STAR <= r1:
            w0, w1 = wavelengths[i], wavelengths[i + 1]
            # Linear interpolation
            fraction = (R_STAR - r0) / (r1 - r0)
            return w0 + fraction * (w1 - w0)

    raise ValueError("spectrum does not cross the R* threshold")
