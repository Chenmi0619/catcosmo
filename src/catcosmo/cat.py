import math
import random
from datetime import datetime, date
import numpy as np


def name_entropy(name):
    """
    Compute normalized Shannon entropy of a name.

    This measures the "information content" of the name,
    used as a correction factor in the model.

    Parameters
    ----------
    name : str

    Returns
    -------
    float
        Normalized entropy in [0, 1]
    """
    if name is None or not str(name).strip():
        return 0.0

    name = str(name).strip()
    counts = {}

    # Count character frequency
    for ch in name:
        counts[ch] = counts.get(ch, 0) + 1

    n = len(name)
    probs = [c / n for c in counts.values()]

    # Shannon entropy
    entropy = -sum(p * math.log(p, 2) for p in probs if p > 0)

    # Normalize to [0, 1]
    max_entropy = math.log(len(counts), 2) if len(counts) > 1 else 1.0
    return entropy / max_entropy if max_entropy > 0 else 0.0


def encode_ems(ems):
    """
    Encode EMS (coat pattern) string into a numeric value.

    This acts as a "structure density term" in the model.

    Parameters
    ----------
    ems : str

    Returns
    -------
    int
    """
    if ems is None:
        return 0

    s = str(ems).replace(" ", "").strip()
    val = 0

    # Polynomial hash encoding
    for i, ch in enumerate(s):
        val += ord(ch) * (37 ** i)

    return val


def eye_color_sigma(eye):
    """
    Convert eye color into a stochastic uncertainty scale (sigma).

    This controls the strength of Monte Carlo perturbation.

    Parameters
    ----------
    eye : str

    Returns
    -------
    float
        Standard deviation for Gaussian noise
    """
    if eye is None or not str(eye).strip():
        return 0.05  # default small uncertainty

    s = str(eye).lower().strip()
    val = 0

    # Encode string to numeric value
    for i, ch in enumerate(s):
        val += ord(ch) * (17 ** i)

    sigma = (val % 10000) / 10000.0

    # Avoid zero variance
    return max(sigma, 1e-4)


def age_years(birth):
    """
    Convert birth date to age in years.

    Parameters
    ----------
    birth : str (YYYY-MM-DD)

    Returns
    -------
    float
        Age in years
    """
    if birth is None:
        return 1e-6

    dob = datetime.strptime(str(birth).strip(), "%Y-%m-%d").date()

    # Avoid zero age
    return max((date.today() - dob).days / 365.25, 1e-6)


def a_cat(sex):
    """
    Convert sex into a cosmological scale factor.

    Parameters
    ----------
    sex : str

    Returns
    -------
    float
        Scale factor a_cat
    """
    if sex is None:
        return 1.0

    s = str(sex).lower().strip()

    if s in ["male", "m"]:
        return 1.05
    elif s in ["female", "f"]:
        return 0.95

    return 1.0


def seed(
    name,
    birth,
    weight,
    sex,
    ems,
    eye,
    n_samples=1000,
    master_seed=42
):
    """
    Compute the cosmological-inspired random seed mean for a given cat.

    The model combines deterministic physical-like terms with stochastic
    perturbations derived from eye color.

    Model form:
        seed ∝ H² (Ω_m a⁻³ + Ω_c a⁻² + Ω_Λ) × F × (1 + ε)

    Parameters
    ----------
    name : str
    birth : str (YYYY-MM-DD)
    weight : float
    sex : str
    ems : str
    eye : str
    n_samples : int
        Number of Monte Carlo samples
    master_seed : int
        Global seed for reproducibility

    Returns
    -------
    int
        Mean seed value (uint32-compatible)
    """

    # Ensure reproducibility
    random.seed(master_seed)

    # Generate a per-cat random seed
    cat_seed = random.randint(0, 10**9)
    np.random.seed(cat_seed)

    # --- Cosmological components ---

    # Age → expansion rate (Hubble-like term)
    A = age_years(birth)
    H = 1.0 / (A + 0.1)

    # Mass density term
    Omega_m = float(weight) / 70

    # Coat structure term
    Omega_c = encode_ems(ems) / 1e7

    # Dark energy term (closure condition)
    Omega_L = 1.0 - Omega_m - Omega_c

    # Scale factor from sex
    a = a_cat(sex)

    # Name entropy correction
    F = 1.0 + 0.2 * name_entropy(name)

    # Stochastic uncertainty from eye color
    sigma_eye = eye_color_sigma(eye)

    # --- Monte Carlo perturbation ---
    eps_eye = np.random.normal(0.0, sigma_eye, n_samples)

    # Compute cosmological-like values
    values = (
        1e6
        * H**2
        * (Omega_m * a**-3 + Omega_c * a**-2 + Omega_L)
        * F
        * (1.0 + eps_eye)
    )

    # Convert to uint32-compatible seeds
    seeds = (values.astype(np.int64) & 0xFFFFFFFF).astype(np.uint32)

    # Return mean seed
    return int(np.mean(seeds))