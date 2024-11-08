# models/concrete_optimizer.py
from typing import Tuple, List
import numpy as np
from deap import tools, algorithms
from config.settings import GA_SETTINGS
from utils.constraints import ConcreteConstraints
from models.concrete_mix_optimizer import ConcreteMixOptimizer

class ConcreteOptimizer:
    def __init__(self, model, scaler, target_strength: float):
        self.model = model
        self.scaler = scaler
        self.target_strength = target_strength
        optimizer = ConcreteMixOptimizer()
        self.toolbox, self.bounds = optimizer.setup_genetic_algorithm()
        
        # Register genetic operators
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, 
                            mu=GA_SETTINGS['MUTATION_MU'], 
                            sigma=GA_SETTINGS['MUTATION_SIGMA'], 
                            indpb=GA_SETTINGS['MUTATION_PROB'])
        self.toolbox.register("select", tools.selTournament, 
                            tournsize=GA_SETTINGS['TOURNAMENT_SIZE'])
    
    def evaluate(self, individual: List[float]) -> Tuple[float]:
        """Fitness function"""
        if not ConcreteConstraints.check_constraints(individual):
            return float('inf'),
        
        features = list(individual) + [28]  # Age fixed at 28 days
        features_scaled = self.scaler.transform([features])
        predicted_strength = self.model.predict(features_scaled)[0]
        
        return abs(predicted_strength - self.target_strength),
    
    def optimize(self, pop_size: int = 300, ngen: int = 50) -> Tuple[List[float], tools.Logbook]:
        """Run optimization"""
        pop = self.toolbox.population(n=pop_size)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min)
        stats.register("avg", np.mean)
        
        final_pop, logbook = algorithms.eaSimple(
            pop, self.toolbox,
            cxpb=GA_SETTINGS['CROSSOVER_PROB'],
            mutpb=GA_SETTINGS['MUTATION_PROB'],
            ngen=ngen,
            stats=stats,
            verbose=True
        )
        
        return tools.selBest(final_pop, k=1)[0], logbook