#
# ATTRIBUTION file inclusion based off of:
# https://gist.github.com/joshbode/569627ced3076931b02f#file-loader-py
# 
import os
import json
import yaml
import re
from atmosphere import GasParcel, GasMixture, GasSpecies
from typing import Any, IO

class Loader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor that accepts
    yaml, json, and hitran files."""

    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""
        try:
            self._root = os.path.dirname(stream.name)
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)


def read_hitran(stream: IO) -> Any:
    """Construct an object from a HITRAN stream"""
    def hitran_line(line):
        line = re.match(r'^...(.{12})(.{10}).{10}(.....)(.....).{10}(....)(.{8}).*$', line)
        nu, sw, gamma_air, gamma_self, n_air, delta_air = line.groups()
        del line
        line_vars = dict(locals())
        line_vars = {k: float(v) for k, v in line_vars.items()}
        return line_vars

    return [hitran_line(line) for line in stream]


def construct_include(loader: Loader, node: yaml.Node) -> Any:
    """Include a yaml file referenced at node."""

    filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
    extension = os.path.splitext(filename)[1].lstrip('.')

    with open(filename, 'r') as f:
        if extension in ('yaml', 'yml'):
            return yaml.load(f, Loader)
        elif extension in ('json', ):
            return json.load(f)
        elif extension in ('hitran', 'par'):
            return read_hitran(f)
        else:
            return ''.join(f.readlines())

def construct_layer(loader: Loader, node: yaml.Node) -> GasParcel:
    kw = loader.construct_mapping(node)
    return GasParcel(**kw)

def construct_mixture(loader: Loader, node: yaml.Node) -> GasMixture:
    species_weights = loader.construct_sequence(node)
    it = iter(species_weights)
    return GasMixture({x: next(it) for x in it})

def construct_species(loader: Loader, node: yaml.Node) -> GasSpecies:
    kw = loader.construct_mapping(node)
    return GasSpecies(**kw)

yaml.add_constructor('!include', construct_include, Loader)
yaml.add_constructor('!layer', construct_layer, Loader)
yaml.add_constructor('!mixture', construct_mixture, Loader)
yaml.add_constructor('!species', construct_species, Loader)

def parse_atmosphere_file(atmosphere_file_name):
    with open(atmosphere_file_name, 'r') as f:
        return yaml.load(f, Loader)
