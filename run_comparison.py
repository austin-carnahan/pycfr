#!/usr/bin/env python3
"""
Simple comparison script to test CFR algorithm variants on Leduc poker.
Runs 100,000 iterations and generates a convergence plot.
"""

from pokergames import leduc_rules
from pokercfr import CounterfactualRegretMinimizer, ChanceSamplingCFR, PublicChanceSamplingCFR, OutcomeSamplingCFR, RetrospectiveSamplingCFR
from cfr_benchmark import CFRBenchmark

def main():
    # Initialize benchmark with Leduc poker rules
    print("Setting up benchmark for Leduc poker...")
    benchmark = CFRBenchmark(leduc_rules(), game_name="Leduc Poker")
    
    # Define the CFR algorithms to compare (class, display name, kwargs)
    # For algorithms without kwargs, use empty dict
    algorithms = [
        # (CounterfactualRegretMinimizer, 'Vanilla CFR', {}),
        # (ChanceSamplingCFR, 'Chance Sampling CFR', {}),
        # (PublicChanceSamplingCFR, 'Public Chance Sampling CFR', {}),
        (OutcomeSamplingCFR, 'Outcome Sampling CFR', {}),
        (RetrospectiveSamplingCFR, 'RS-CFR (k=1)', {'lookback_depth': 1}),
        (RetrospectiveSamplingCFR, 'RS-CFR (k=2)', {'lookback_depth': 2}),
        (RetrospectiveSamplingCFR, 'RS-CFR (k=3)', {'lookback_depth': 3})
    ]
    
    total_iterations = 1000000
    checkpoint_interval = 10000
    
    print(f"\nRunning {len(algorithms)} algorithms for {total_iterations:,} iterations...")
    print(f"Exploitability checkpoints every {checkpoint_interval:,} iterations\n")
    
    benchmark.compare_algorithms(
        algorithm_configs=algorithms,
        total_iterations=total_iterations,
        checkpoint_interval=checkpoint_interval
    )
    
    # Print summary table
    print("\n" + "="*60)
    benchmark.print_summary()
    
    # Generate convergence plot
    print("\nGenerating convergence plot...")
    benchmark.plot_convergence(
        save_path='results/leduc_comparison.png',
        log_scale=True
    )
    print("Plot saved to: results/leduc_comparison.png")
    
    print("\nBenchmark complete!")

if __name__ == '__main__':
    main()
