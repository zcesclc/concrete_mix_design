# tests/test_constraints.py
import pytest
from utils.constraints import ConcreteConstraints

def test_valid_mix_design():
    valid_mix = [350, 100, 50, 175, 5, 1000, 800]
    assert ConcreteConstraints.check_constraints(valid_mix) == True

def test_invalid_water_binder_ratio():
    invalid_mix = [350, 100, 50, 300, 5, 1000, 800]  # High water content
    assert ConcreteConstraints.check_constraints(invalid_mix) == False