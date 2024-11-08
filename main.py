# main.py
import warnings
import logging
from models.concrete_mix_optimizer import ConcreteMixOptimizer
from models.concrete_optimizer import ConcreteOptimizer
from utils.visualization import plot_convergence
from config.settings import FEATURE_NAMES

def main():
    """Main execution function for concrete mix optimization"""
    try:
        # Configure logging and warnings
        warnings.filterwarnings('ignore', category=UserWarning)
        logging.getLogger().setLevel(logging.ERROR)  # Only show errors, hide warnings
        
        optimizer = ConcreteMixOptimizer()
        
        # Load and prepare data
        df = optimizer.load_data()
        X_scaled, y = optimizer.prepare_data(df)
        
        # Train model
        model, _ = optimizer.train_model(X_scaled, y)
        
        # Get target strength
        target_strength = float(input("Enter target strength (MPa): "))
        
        # Run optimization
        optimizer = ConcreteOptimizer(model, optimizer.scaler, target_strength)
        best_mix, stats = optimizer.optimize()
        
        # Print results
        print(f"\nOptimal Mix Design for {target_strength} MPa:")
        for component, value in zip(FEATURE_NAMES[:-1], best_mix):
            print(f"{component}: {value:.1f} kg/m³")
        
        # Plot convergence
        plot_convergence(stats)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        raise

if __name__ == '__main__':
    main()