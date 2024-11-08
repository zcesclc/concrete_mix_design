# utils/visualization.py
from typing import Dict, List
import matplotlib.pyplot as plt
from deap.tools import Logbook
from config.settings import PLOT_SETTINGS

def plot_convergence(logbook: Logbook) -> None:
    """
    Plot optimization convergence over generations
    
    Args:
        logbook: DEAP logbook containing optimization statistics
    """
    gen = range(len(logbook))
    mins = [d['min'] for d in logbook]
    avgs = [d['avg'] for d in logbook]
    
    plt.figure(figsize=PLOT_SETTINGS['FIGSIZE'])
    plt.plot(gen, mins, 'b-', label='Minimum Fitness')
    plt.plot(gen, avgs, 'r-', label='Average Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness (Distance from Target)')
    plt.title('Optimization Convergence')
    plt.legend()
    plt.grid(True)
    plt.show()

def save_convergence_plot(logbook: Logbook, filename: str) -> None:
    """Save convergence plot to file"""
    plot_convergence(logbook)
    plt.savefig(filename)
    plt.close()