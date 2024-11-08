# main.py
import warnings
import logging
from models.aac_mix_optimizer import AACMixOptimizer
from models.aac_optimizer import AACOptimizer
from utils.visualization import plot_convergence

def main():
    """Main execution function for AAC mix optimization"""
    try:
        warnings.filterwarnings('ignore', category=UserWarning)
        logging.getLogger().setLevel(logging.ERROR)
        
        optimizer = AACMixOptimizer()
        
        # Load and prepare data
        df = optimizer.load_data()
        X_scaled, y = optimizer.prepare_data(df)
        
        # Train model
        model, _ = optimizer.train_model(X_scaled, y)
        
        # Get target strength
        target_strength = float(input("Enter target strength (MPa): "))
        
        # Run optimization
        optimizer = AACOptimizer(model, optimizer.scaler, target_strength)
        best_mix, stats = optimizer.optimize()
        
        # Print results
        print(f"\nOptimal Mix Design for {target_strength} MPa:")
        for component, value in zip(optimizer.feature_names, best_mix):
            print(f"{component}: {value:.2f}")
        
        # Plot convergence
        plot_convergence(stats)
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    main()