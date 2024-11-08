# models/concrete_mix_optimizer.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from deap import base, creator, tools
import random
from config.settings import CONCRETE_BOUNDS
from utils.constraints import ConcreteConstraints

class ConcreteMixOptimizer:
    def __init__(self):
        self.feature_names = [
            'Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water',
            'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate',
            'Age'
        ]
        self.target_name = 'Compressive Strength'
        self.scaler = None
        self.model = None

    def load_data(self):
        """Load and preprocess concrete mix data"""
        try:
            df = pd.read_csv(r'C:\Users\cherrychan9898\Downloads\Copy of Concrete_Data.csv')
            df.columns = self.feature_names + [self.target_name]
            return df
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def prepare_data(self, df):
        X = df[self.feature_names]
        y = df[self.target_name]
        
        self.scaler = StandardScaler()
        X_scaled = pd.DataFrame(
            self.scaler.fit_transform(X),
            columns=self.feature_names
        )
        
        return X_scaled, y

    def train_model(self, X, y, test_size=0.2):
        """Train the random forest model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=42
        )
        
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Optional: Calculate and print model performance
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        print(f"Train R² score: {train_score:.4f}")
        print(f"Test R² score: {test_score:.4f}")
        
        return self.model, (X_train, X_test, y_train, y_test)

    def setup_genetic_algorithm(self):
        """Initialize GA components"""
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        
        toolbox = base.Toolbox()
        
        # Define bounds for each component
        bounds = {
            'Cement': (100, 550),
            'Blast Furnace Slag': (0, 360),
            'Fly Ash': (0, 200),
            'Water': (120, 250),
            'Superplasticizer': (0, 32),
            'Coarse Aggregate': (800, 1150),
            'Fine Aggregate': (590, 950)
        }
        
        # Register genes with proper feature names
        for name, (min_val, max_val) in bounds.items():
            toolbox.register(f"attr_{name}", random.uniform, min_val, max_val)
        
        toolbox.register("individual", tools.initCycle, creator.Individual,
                        [getattr(toolbox, f"attr_{name}") for name in self.feature_names[:-1]], n=1)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        
        return toolbox, bounds

def check_constraints(individual):
    """Verify if mix design meets engineering constraints"""
    cement, slag, fly_ash, water, superplast, coarse, fine = individual
    
    # Water-binder ratio (0.3-0.6)
    total_binder = cement + slag + fly_ash
    if total_binder == 0:
        return False
    w_b_ratio = water / total_binder
    if not (0.3 <= w_b_ratio <= 0.6):
        return False
    
    # Total cementitious content (300-600 kg/m³)
    if not (300 <= total_binder <= 600):
        return False
    
    # Minimum cement content
    if cement < 100:
        return False
    
    # Aggregate proportions
    total_agg = coarse + fine
    if not (0.35 <= fine/total_agg <= 0.45):
        return False
    
    return True