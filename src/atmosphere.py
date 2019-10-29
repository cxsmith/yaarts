import itertools
import math

class GasParcel(object):
    """
    In pre-release this represents an atmospheric layer.
    
    molar_composition is a dictionary from GasSpecies to molar fraction
    pressure in Pa
    temperature in kelvins
    altitudes in meters
    """

    def __init__(self, species_mixture, pressure, temperature,
            low_altitude_boundary, high_altitude_boundary):
        self.species_mixture = species_mixture
        self.pressure = pressure
        self.temperature = temperature
        self.low_altitude_boundary = low_altitude_boundary
        self.high_altitude_boundary = high_altitude_boundary

class GasMixture(object):
    def __init__(self, molar_composition):
        """
        Molar composition is a dictionary from GasSpecies to its molar fraction.
        """
        self.molar_composition = molar_composition

        # see: https://en.wikipedia.org/wiki/Van_der_Waals_equation#Gas_mixture
        self.a = GasMixture.gas_mixture_van_der_waals(
                [(species.a, Xf) for species, Xf in molar_composition.items()])
        self.b = GasMixture.gas_mixture_van_der_waals(
                [(species.b, Xf) for species, Xf in molar_composition.items()])
        self.mm = sum(species.mm * Xf
                for species, Xf in molar_composition.items())

    @staticmethod
    def gas_mixture_van_der_waals(molar_composition):
        """
        Accepts a list of tuples:
            (parameter_to_be_combined, molar_fraction)
        """
        return sum(Xf1 * Xf2 * math.sqrt(species1_param * species2_param)
            for (species1_param, Xf1), (species2_param, Xf2)
            in itertools.product(molar_composition, molar_composition))

class GasSpecies(object):
    def __init__(self, a, b, mm, spectrum):
        self.a = a
        self.b = b
        self.mm = mm
        self.spectrum = spectrum
