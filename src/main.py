#!/usr/bin/env python3
"""
Main - Script Principal
Algoritmos Avançados 2025/2026 - Trabalho 3
Hugo Gonçalo Lopes Castro - 113889

Este script principal permite executar todas as componentes do trabalho:
- Experimentos completos
- Visualizações
- Testes individuais
"""

import os
import sys
import argparse
from datetime import datetime

# Adicionar pasta src ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from experiments import ExperimentRunner
from visualization import Visualizer


def print_header():
    """Imprime cabeçalho do programa."""
    print("\n" + "═" * 70)
    print("║" + " " * 68 + "║")
    print("║" + "    ADVANCED ALGORITHMS 2025/2026 - PROJECT 3".center(68) + "║")
    print("║" + "    Frequent Items Analysis".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("║" + "    Hugo Gonçalo Lopes Castro - 113889".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("═" * 70)


def print_dataset_info(data_path: str):
    """Imprime informações sobre o dataset."""
    print("\n DATASET:")
    print(f"   File: amazon_prime_titles.csv")
    print(f"   Attribute analyzed: release_year")
    print(f"   Path: {data_path}")


def run_all(data_path: str):
    """
    Executa todos os experimentos e gera visualizações.
    
    Args:
        data_path: Caminho para o dataset
    """
    print("\n MODE: Full Execution")
    print("   - Exact Counters")
    print("   - Csuros' Counter")
    print("   - Lossy-Count")
    print("   - Visualizations")
    
    # Executar experimentos
    runner = ExperimentRunner(data_path, column='release_year')
    results = runner.run_all_experiments()
    
    # Gerar visualizações
    results_dir = os.path.join(os.path.dirname(data_path), 'results')
    viz = Visualizer(results_dir)
    viz.generate_all_plots()
    
    return results


def run_exact_only(data_path: str):
    """Executa apenas contadores exatos."""
    print("\n MODE: Exact Counters Only")
    
    runner = ExperimentRunner(data_path, column='release_year')
    runner.run_exact_counter()
    
    # Mostrar resultados detalhados
    print("\n DETAILED RESULTS:")
    print("\n TOP 20 MOST FREQUENT YEARS:")
    for i, (year, count) in enumerate(runner.exact_counter.get_most_frequent(20), 1):
        print(f"   {i:2}. {int(year)}: {count} titles")
    
    print("\n TOP 10 LEAST FREQUENT YEARS:")
    for i, (year, count) in enumerate(runner.exact_counter.get_least_frequent(10), 1):
        print(f"   {i:2}. {int(year)}: {count} titles")


def run_csuros_only(data_path: str, base: float = 2.0, runs: int = 10):
    """
    Executa apenas Csuros' Counter.
    
    Args:
        data_path: Caminho para o dataset
        base: Base do contador
        runs: Número de execuções
    """
    print(f"\n MODE: Csuros' Counter Only (base={base}, runs={runs})")
    
    runner = ExperimentRunner(data_path, column='release_year')
    runner.run_exact_counter()  # Precisamos do baseline
    runner.run_csuros_experiments(bases=[base], num_runs=runs)


def run_lossy_only(data_path: str, epsilon: float = 0.01):
    """
    Executa apenas Lossy-Count.
    
    Args:
        data_path: Caminho para o dataset
        epsilon: Valor de epsilon
    """
    print(f"\n MODE: Lossy-Count Only (epsilon={epsilon})")
    
    runner = ExperimentRunner(data_path, column='release_year')
    runner.run_exact_counter()  # Precisamos do baseline
    runner.run_lossy_count_experiments(epsilon_values=[epsilon])


def run_visualizations_only(results_dir: str):
    """
    Gera apenas visualizações.
    
    Args:
        results_dir: Diretório com os resultados
    """
    print("\n MODE: Visualizations Only")
    
    if not os.path.exists(results_dir):
        print(f" Results directory not found: {results_dir}")
        print("   Run experiments first!")
        return
    
    viz = Visualizer(results_dir)
    viz.generate_all_plots()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Frequent Items Analysis - AA 2025/2026',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python main.py --all                    # Run everything
  python main.py --exact                  # Exact counters only
  python main.py --csuros --base 2.0      # Csuros with specific base
  python main.py --lossy --epsilon 0.01   # Lossy-Count with specific epsilon
  python main.py --viz                    # Visualizations only
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='Run all experiments and visualizations')
    parser.add_argument('--exact', action='store_true',
                       help='Run exact counters only')
    parser.add_argument('--csuros', action='store_true',
                       help='Run Csuros\' Counter only')
    parser.add_argument('--lossy', action='store_true',
                       help='Run Lossy-Count only')
    parser.add_argument('--viz', action='store_true',
                       help='Generate visualizations only')
    
    parser.add_argument('--base', type=float, default=2.0,
                       help='Base for Csuros\' Counter (default: 2.0)')
    parser.add_argument('--runs', type=int, default=10,
                       help='Number of runs for Csuros (default: 10)')
    parser.add_argument('--epsilon', type=float, default=0.01,
                       help='Epsilon for Lossy-Count (default: 0.01)')
    
    args = parser.parse_args()
    
    # Imprimir cabeçalho
    print_header()
    
    # Caminhos
    data_path = os.path.join(script_dir, "..", "amazon_prime_titles.csv")
    results_dir = os.path.join(script_dir, "..", "results")
    
    print_dataset_info(data_path)
    print(f"\n Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar se o dataset existe
    if not os.path.exists(data_path) and not args.viz:
        print(f"\n Dataset not found: {data_path}")
        sys.exit(1)
    
    # Executar modo selecionado
    if args.viz:
        run_visualizations_only(results_dir)
    elif args.exact:
        run_exact_only(data_path)
    elif args.csuros:
        run_csuros_only(data_path, args.base, args.runs)
    elif args.lossy:
        run_lossy_only(data_path, args.epsilon)
    elif args.all:
        run_all(data_path)
    else:
        # Default: executar tudo
        print("\n No mode specified. Running everything...")
        run_all(data_path)
    
    print(f"\n End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "═" * 70)
    print(" Completed!")
    print("═" * 70 + "\n")


if __name__ == "__main__":
    main()
