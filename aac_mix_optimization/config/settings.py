# config/settings.py
# AAC mix bounds
AAC_CONSTRAINTS = {
    'SI_AL_RATIO': (1.5, 7.5),
    'NA_AL_RATIO': (0.2, 5.0),
    'CA_SI_RATIO': (0.0, 1.6),
    'AGG_BINDER_RATIO': (1.0, 4.0)
}

GA_SETTINGS = {
    'POPULATION_SIZE': 100,
    'GENERATIONS': 50,
    'MUTATION_MU': 0,
    'MUTATION_SIGMA': 0.5,
    'MUTATION_PROB': 0.2,
    'CROSSOVER_PROB': 0.7,
    'TOURNAMENT_SIZE': 3
}

PLOT_SETTINGS = {
    'FIGSIZE': (10, 6)
}