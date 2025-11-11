import matplotlib.pyplot as plt
import numpy as np
from pokercfr import *
from pokergames import *
from pokerstrategy import *

class CFRBenchmark:
    """
    Benchmarks different CFR algorithms and compares their convergence.
    """
    def __init__(self, game_rules, game_name=""):
        self.game_rules = game_rules
        self.game_name = game_name
        self.results = {}  # algorithm_name -> {iterations: [], exploitability: []}
    
    def run_algorithm(self, algorithm_class, algorithm_name, 
                     total_iterations=100000, checkpoint_interval=5000, 
                     algorithm_kwargs=None):
        """
        Run a CFR algorithm and track exploitability over time.
        
        Args:
            algorithm_class: The CFR class (e.g., CounterfactualRegretMinimizer)
            algorithm_name: Display name for the algorithm
            total_iterations: Total number of iterations to run
            checkpoint_interval: How often to compute exploitability
            algorithm_kwargs: Optional dict of kwargs to pass to algorithm constructor
        
        Returns:
            Dictionary with 'iterations' and 'exploitability' lists
        """
        print(f"\n{'='*60}")
        print(f"Running {algorithm_name} on {self.game_name}")
        print(f"{'='*60}")
        
        if algorithm_kwargs is None:
            algorithm_kwargs = {}
        cfr = algorithm_class(self.game_rules, **algorithm_kwargs)
        
        iterations_list = []
        exploitability_list = []
        
        num_checkpoints = total_iterations // checkpoint_interval
        
        for checkpoint in range(num_checkpoints):
            current_iter = (checkpoint + 1) * checkpoint_interval
            
            # Run the CFR algorithm
            cfr.run(checkpoint_interval)
            
            # Compute exploitability
            result = cfr.profile.best_response()
            exploitability = sum(result[1])
            
            # Store results
            iterations_list.append(current_iter)
            exploitability_list.append(exploitability)
            
            print(f"Iterations: {current_iter:8d} | "
                  f"Exploitability: {exploitability:.6f}")
        
        self.results[algorithm_name] = {
            'iterations': iterations_list,
            'exploitability': exploitability_list,
            'final_strategy': cfr.profile
        }
        
        return self.results[algorithm_name]
    
    def compare_algorithms(self, algorithm_configs, total_iterations=100000, 
                          checkpoint_interval=5000):
        """
        Compare multiple CFR algorithms.
        
        Args:
            algorithm_configs: List of (class, name) tuples or (class, name, kwargs) tuples
                Example: [
                    (CounterfactualRegretMinimizer, "Vanilla CFR"),
                    (ChanceSamplingCFR, "Chance Sampling CFR"),
                    (RetrospectiveSamplingCFR, "RS-CFR k=1", {"lookback_depth": 1}),
                ]
            total_iterations: Total iterations for each algorithm
            checkpoint_interval: How often to checkpoint
        """
        for config in algorithm_configs:
            if len(config) == 2:
                algorithm_class, algorithm_name = config
                algorithm_kwargs = {}
            elif len(config) == 3:
                algorithm_class, algorithm_name, algorithm_kwargs = config
            else:
                raise ValueError(f"Invalid config format: {config}")
            
            self.run_algorithm(
                algorithm_class, 
                algorithm_name, 
                total_iterations, 
                checkpoint_interval,
                algorithm_kwargs
            )
    
    def plot_convergence(self, save_path=None, log_scale=True, 
                        figsize=(10, 6), style_config=None):
        """
        Create a convergence plot comparing all algorithms.
        
        Args:
            save_path: If provided, save plot to this path
            log_scale: Use log scale for both axes (like the example image)
            figsize: Figure size tuple
            style_config: Dict mapping algorithm names to style dicts
                Example: {
                    "Vanilla CFR": {"color": "blue", "linestyle": "-", "linewidth": 2},
                }
        """
        plt.figure(figsize=figsize)
        
        # Set style similar to the example image
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Plot each algorithm
        for algorithm_name, data in self.results.items():
            # Get style config for this algorithm
            if style_config and algorithm_name in style_config:
                style = style_config[algorithm_name]
            else:
                style = {"linewidth": 2}
            
            plt.plot(data['iterations'], data['exploitability'], 
                    label=algorithm_name, **style)
        
        plt.xlabel('Iterations', fontsize=12)
        plt.ylabel('Exploitability', fontsize=12)
        plt.title(f'{self.game_name}', fontsize=14)
        plt.legend(fontsize=10, loc='best')
        plt.grid(True, alpha=0.3)
        
        if log_scale:
            plt.xscale('log')
            plt.yscale('log')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nPlot saved to: {save_path}")
        
        plt.show()
    
    def print_summary(self):
        """Print a summary table of final results."""
        print(f"\n{'='*80}")
        print(f"SUMMARY - {self.game_name}")
        print(f"{'='*80}")
        print(f"{'Algorithm':<35} {'Final Iterations':<20} {'Final Exploitability':<20}")
        print(f"{'-'*80}")
        
        for algorithm_name, data in self.results.items():
            final_iter = data['iterations'][-1]
            final_exploit = data['exploitability'][-1]
            print(f"{algorithm_name:<35} {final_iter:<20} {final_exploit:<20.6f}")
        
        print(f"{'='*80}\n")
