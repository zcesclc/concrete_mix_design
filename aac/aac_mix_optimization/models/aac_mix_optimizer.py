# models/aac_mix_optimizer.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from deap import base, creator, tools
import random
import os

class AACMixOptimizer:
    def __init__(self):
        self.feature_names = [
            'Si/Al', 'Na/Al', 'Ca/Si', 'Activator_binder',
            'Fine_aggregate_to_binder', 'Coarse_aggregate_to_binder',
            'Curing_temperature (C)', 'Curing_age (d)'
        ]
        self.target_name = 'CS (MPa)'
        self.scaler = None
        self.model = None

    def load_data(self):
        """Load AAC mix data"""
        current_directory = os.getcwd()
        file_name = "aac_data.csv"
        file_path = os.path.join(current_directory, file_name)
        print("before reading the csv")
        df = pd.read_csv(file_path, encoding='utf-8', encoding_errors='replace')
        print("after reading the csv")
        df = df.iloc[:, 1:]  # Drop first column
        return df

    def prepare_data(self, df):
        """Prepare data and filter for 28-day mixes only"""
        # Filter for 28-day samples only
        df_28d = df[df['Curing_age (d)'] == 28]
        print(df.head())
        
        X = df_28d[self.feature_names]
        y = df_28d[self.target_name]
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled, y

    def train_model(self, X, y, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        self.model = GradientBoostingRegressor(
            n_estimators=100, learning_rate=0.1,
            max_depth=3, random_state=42
        )
        self.model.fit(X_train, y_train)
        
        return self.model, (X_train, X_test, y_train, y_test)

    def setup_genetic_algorithm(self):
        """Setup GA with fixed 28-day curing age"""
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        toolbox = base.Toolbox()
        
        # Define bounds - curing age fixed at 28 days
        bounds = [
            (1.5, 3.0),    # Si/Al
            (0.8, 1.2),    # Na/Al  
            (0.8, 1.5),    # Ca/Si
            (0.3, 0.6),    # Activator/binder
            (0.5, 2.0),    # Fine aggregate/binder
            (0.0, 1.0),    # Coarse aggregate/binder
            (170, 190),    # Curing temperature
            (28, 28)       # Fixed 28 day curing
        ]

        def generate_within_bounds():
            return [random.uniform(low, high) for low, high in bounds[:-1]] + [28]

        toolbox.register("attr_float", generate_within_bounds)
        toolbox.register("individual", tools.initIterate, creator.Individual, 
                        toolbox.attr_float)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        return toolbox, bounds