# yaarts
Yet Another Atmospheric Radiative Transfer Simulator

YAARTS is a radiative transfer simulator designed to be easy to use and modify. YAARTS is far from being ready for release. Here are the already existing, pre-release, and post-release feature lists:

# Existing features

* Calculates parameters of a mixture of gas species.
* Import gas species definitions from yaml and HITRAN
* Import atmospheric definitions from yaml

# Pre-release feature priorities

* Include broadening in spectrum definitions:
  - See if HAPI does this and use it if so
  - Pressure
  - Doppler
  - Other?
* Build solver

# Post-release feature priorities

* Account for refraction
* Remove temperature as a boundary condition and have it be dynamic in sim
* Add scattering
* Add reflection (eg aerosols)
* Account for polarization
