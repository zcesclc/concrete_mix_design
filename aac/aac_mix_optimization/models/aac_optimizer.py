# models/aac_optimizer.py
from typing import Tuple, List
import numpy as np
from deap import tools, algorithms
from config.settings import GA_SETTINGS
from utils.constraints import AACConstraints
from models.aac_mix_optimizer import AACMixOptimizer

class AACOptimizer:
    def __init__(self, model, scaler, target_strength: float):
        self.model = model
        self.scaler = scaler
        self.target_strength = target_strength
        mix_optimizer = AACMixOptimizer()
        self.toolbox, self.bounds = mix_optimizer.setup_genetic_algorithm()
        self.feature_names = mix_optimizer.feature_names
        
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
        """Evaluate fitness of an individual"""
        # Check constraints
        if not AACConstraints.check_constraints(individual):
            return (-1000.0,)  # Return large negative value for invalid solutions
            
        # Scale individual
        scaled_ind = self.scaler.transform([individual])
        
        # Predict strength
        predicted_strength = self.model.predict(scaled_ind)[0]
        
        # Calculate fitness based on difference from target
        fitness = -abs(predicted_strength - self.target_strength)
        return (fitness,)
    
    def optimize(self, pop_size: int = 100, ngen: int = 50) -> Tuple[List[float], tools.Logbook]:
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
