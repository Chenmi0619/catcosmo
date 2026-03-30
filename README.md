# 🐱 CatCosmo

A cosmological-inspired random seed generator based on cat properties.

> "Cats are the true interpreters of the universe."

---

## ✨ Features

- Deterministic + stochastic hybrid seed generation
- Physically-inspired parameters:
  - Mass density (weight)
  - Coat pattern encoding (EMS)
  - Dark energy closure
  - Name entropy correction
  - Eye-color-driven perturbation by Monte **Catlo**

---

## 🚀 Installation

Install from PyPI:

pip install catcosmo

For local development:

git clone https://github.com/yourusername/catcosmo.git
cd catcosmo
pip install -e .

---

## 📦 Requirements

- Python >= 3.8
- NumPy

---

## 🧪 Quick Start

from catcosmo import cosmological_seed_mean

seed = cosmological_seed_mean(
    name="Mimi",
    birth="2022-05-14",
    weight=4.2,
    sex="female",
    ems="n 22",
    eye="green"
)

print(seed)

---

## 🔬 Model Overview

seed ∝ H² (Ω_m a⁻³ + Ω_c a⁻² + Ω_Λ) × F × (1 + ε)

---

## 📜 License

MIT License
