from typing import Dict, List, Tuple, Union
from pathlib import Path

# Type aliases
Number = Union[int, float]
Range = Tuple[Number, Number]

# Data settings
DATA_PATH: str = r'C:\Users\cherrychan9898\Downloads\Copy of Concrete_Data.csv'

FEATURE_NAMES: List[str] = [
    'Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water',
    'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate',
    'Age'
]

# Concrete mix bounds
CONCRETE_BOUNDS: Dict[str, Range] = {
    'Cement': (100, 550),
    'Blast Furnace Slag': (0, 360),
    'Fly Ash': (0, 200),
    'Water': (120, 250),
    'Superplasticizer': (0, 32),
    'Coarse Aggregate': (800, 1150),
    'Fine Aggregate': (590, 950)
}

# Engineering constraints
CONSTRAINT_LIMITS: Dict[str, Union[Range, Number]] = {
    'W_B_RATIO': (0.3, 0.6),        # Water-binder ratio bounds
    'TOTAL_BINDER': (300, 600),      # Total cementitious content (kg/m³)
    'MIN_CEMENT': 100,               # Minimum cement content (kg/m³)
    'FINE_AGG_RATIO': (0.35, 0.45)   # Fine/total aggregate ratio
}

# Genetic Algorithm settings
GA_SETTINGS: Dict[str, Number] = {
    'POPULATION_SIZE': 100,
    'GENERATIONS': 50,
    'MUTATION_MU': 0,
    'MUTATION_SIGMA': 1,
    'MUTATION_PROB': 0.1,
    'CROSSOVER_PROB': 0.8,
    'TOURNAMENT_SIZE': 3
}

# Model parameters
MODEL_SETTINGS = {
    'TEST_SIZE': 0.2,
    'RANDOM_STATE': 42,
    'N_ESTIMATORS': 100
}

# Add visualization settings
PLOT_SETTINGS = {
    'FIGSIZE': (10, 6),
    'PLOT_DIR': 'outputs/plots/'
}

# Export all settings
__all__ = [
    'DATA_PATH',
    'FEATURE_NAMES', 
    'CONCRETE_BOUNDS',
    'CONSTRAINT_LIMITS',
    'GA_SETTINGS'
]
