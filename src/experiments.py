"""
Experiments - Script de Experimentos Completos
Algoritmos Avançados 2025/2026 - Trabalho 3
Hugo Gonçalo Lopes Castro - 113889

Este script executa todos os experimentos necessários para o trabalho:
- Contadores exatos (baseline)
- Csuros' Counter com múltiplas execuções
- Lossy-Count com diferentes parâmetros
- Análise comparativa completa
"""

import os
import sys
import json
import csv
import time
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd

# Adicionar pasta src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exact_counter import ExactCounter, run_exact_count
from csuros_counter import CsurosCounter, run_csuros_experiment, analyze_csuros_results
from lossy_count import LossyCount, run_lossy_count_experiment, analyze_lossy_count_results


class ExperimentRunner:
    """
    Classe para executar e gerir todos os experimentos.
    """
    
    def __init__(self, data_path: str, column: str = 'release_year'):
        """
        Inicializa o runner de experimentos.
        
        Args:
            data_path: Caminho para o ficheiro CSV
            column: Coluna a analisar
        """
        self.data_path = data_path
        self.column = column
        self.results_dir = os.path.join(os.path.dirname(data_path), 'results')
        
        # Criar diretório de resultados se não existir
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(os.path.join(self.results_dir, 'plots'), exist_ok=True)
        
        # Resultados
        self.exact_counts = None
        self.exact_counter = None
        self.csuros_results = {}
        self.lossy_count_results = {}
        self.comparison_results = {}
    
    def run_exact_counter(self) -> Dict:
        """
        Executa o contador exato e armazena como baseline.
        
        Returns:
            Estatísticas do contador exato
        """
        print("\n" + "=" * 70)
        print("📊 EXPERIMENT 1: EXACT COUNTERS (BASELINE)")
        print("=" * 70)
        
        self.exact_counter = run_exact_count(self.data_path, self.column)
        self.exact_counts = self.exact_counter.get_all_counts()
        
        stats = self.exact_counter.get_statistics()
        
        print(f"\n✅ Processing completed!")
        print(f"   • Total items: {stats['total_items']}")
        print(f"   • Unique items: {stats['unique_items']}")
        print(f"   • Time: {stats['processing_time']*1000:.2f} ms")
        
        # Guardar resultados
        self._save_exact_results()
        
        return stats
    
    def run_csuros_experiments(self, bases: List[float] = None, 
                                num_runs: int = 10) -> Dict:
        """
        Executa experimentos com Csuros' Counter.
        
        Args:
            bases: Lista de bases a testar
            num_runs: Número de execuções por base
            
        Returns:
            Resultados agregados
        """
        if bases is None:
            bases = [1.3, 1.5, 2.0, 3.0, 4.0]
        
        print("\n" + "=" * 70)
        print("🔢 EXPERIMENT 2: CSUROS' COUNTER")
        print(f"   Bases: {bases}")
        print(f"   Runs per base: {num_runs}")
        print("=" * 70)
        
        if self.exact_counts is None:
            self.run_exact_counter()
        
        for base in bases:
            print(f"\n{'─'*50}")
            print(f"🔄 Testing base = {base}")
            
            results = run_csuros_experiment(
                self.data_path, 
                self.column,
                base=base,
                num_runs=num_runs
            )
            
            analysis = analyze_csuros_results(results, self.exact_counts)
            
            self.csuros_results[base] = {
                'results': results,
                'analysis': analysis
            }
            
            print(f"   • Mean Absolute Error: {analysis['overall']['mean_absolute_error']:.2f}")
            print(f"   • Mean Relative Error: {analysis['overall']['mean_relative_error']*100:.2f}%")
            print(f"   • Max Relative Error: {analysis['overall']['max_relative_error']*100:.2f}%")
        
        self._save_csuros_results()
        
        return self.csuros_results
    
    def run_lossy_count_experiments(self, 
                                     epsilon_values: List[float] = None,
                                     n_values: List[int] = None) -> Dict:
        """
        Executa experimentos com Lossy-Count.
        
        Args:
            epsilon_values: Valores de epsilon a testar
            n_values: Valores de n (top-n) a testar
            
        Returns:
            Resultados agregados
        """
        if epsilon_values is None:
            epsilon_values = [0.1, 0.05, 0.01, 0.005, 0.001]
        if n_values is None:
            n_values = [5, 10, 15, 20, 25, 30]
        
        print("\n" + "=" * 70)
        print("📈 EXPERIMENT 3: LOSSY-COUNT")
        print(f"   Epsilon values: {epsilon_values}")
        print(f"   N values: {n_values}")
        print("=" * 70)
        
        if self.exact_counts is None:
            self.run_exact_counter()
        
        results = run_lossy_count_experiment(
            self.data_path,
            self.column,
            epsilon_values=epsilon_values,
            n_values=n_values
        )
        
        analysis = analyze_lossy_count_results(results, self.exact_counts)
        
        self.lossy_count_results = {
            'results': results,
            'analysis': analysis
        }
        
        # Mostrar resumo
        print("\n📋 PRECISION SUMMARY (Top-10):")
        print(f"{'Epsilon':<10} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("─" * 46)
        
        for exp in analysis['per_epsilon']:
            epsilon = exp['epsilon']
            n_10 = exp['per_n'].get(10, {})
            precision = n_10.get('precision', 0)
            recall = n_10.get('recall', 0)
            f1 = n_10.get('f1_score', 0)
            print(f"{epsilon:<10} {precision*100:>10.1f}% {recall*100:>10.1f}% {f1*100:>10.1f}%")
        
        self._save_lossy_count_results()
        
        return self.lossy_count_results
    
    def run_all_experiments(self) -> Dict:
        """
        Executa todos os experimentos.
        
        Returns:
            Todos os resultados agregados
        """
        start_time = time.time()
        
        print("\n" + "🚀" * 25)
        print("   STARTING ALL EXPERIMENTS")
        print("🚀" * 25)
        
        # 1. Contadores Exatos
        self.run_exact_counter()
        
        # 2. Csuros' Counter
        self.run_csuros_experiments()
        
        # 3. Lossy-Count
        self.run_lossy_count_experiments()
        
        # 4. Comparação Final
        self.generate_comparison()
        
        total_time = time.time() - start_time
        
        print("\n" + "=" * 70)
        print("✅ ALL EXPERIMENTS COMPLETED!")
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        print("=" * 70)
        
        return {
            'exact': self.exact_counter.get_statistics(),
            'csuros': self.csuros_results,
            'lossy_count': self.lossy_count_results,
            'comparison': self.comparison_results,
            'total_time': total_time
        }
    
    def generate_comparison(self) -> Dict:
        """
        Gera comparação entre todos os métodos.
        
        Returns:
            Resultados da comparação
        """
        print("\n" + "=" * 70)
        print("📊 METHOD COMPARISON")
        print("=" * 70)
        
        if not self.exact_counts:
            print("❌ Error: Run experiments first!")
            return {}
        
        sorted_exact = sorted(self.exact_counts.items(), key=lambda x: x[1], reverse=True)
        exact_top_10 = [item for item, count in sorted_exact[:10]]
        exact_top_20 = [item for item, count in sorted_exact[:20]]
        
        comparison = {
            'exact_top_10': [(item, self.exact_counts[item]) for item in exact_top_10],
            'exact_top_20': [(item, self.exact_counts[item]) for item in exact_top_20],
            'methods': {}
        }
        
        # Csuros - usar base 2.0 como referência
        if 2.0 in self.csuros_results:
            csuros_data = self.csuros_results[2.0]
            last_run = csuros_data['results']['runs'][-1]
            csuros_top = [item for item, est in last_run['most_frequent'][:10]]
            
            hits_10 = len(set(exact_top_10) & set(csuros_top))
            
            comparison['methods']['csuros_base2'] = {
                'top_10': last_run['most_frequent'][:10],
                'precision_top10': hits_10 / 10,
                'mean_abs_error': csuros_data['analysis']['overall']['mean_absolute_error'],
                'mean_rel_error': csuros_data['analysis']['overall']['mean_relative_error']
            }
        
        # Lossy-Count - usar epsilon 0.01 como referência
        if self.lossy_count_results:
            for exp in self.lossy_count_results['analysis']['per_epsilon']:
                if exp['epsilon'] == 0.01:
                    comparison['methods']['lossy_count_e001'] = {
                        'memory_used': exp['memory_used'],
                        'precision_top10': exp['per_n'].get(10, {}).get('precision', 0),
                        'recall_top10': exp['per_n'].get(10, {}).get('recall', 0),
                        'f1_top10': exp['per_n'].get(10, {}).get('f1_score', 0)
                    }
        
        self.comparison_results = comparison
        
        # Mostrar comparação
        print("\n🔝 TOP 10 - EXACT COUNT:")
        for i, (year, count) in enumerate(comparison['exact_top_10'], 1):
            print(f"   {i:2}. {int(year)}: {count}")
        
        if 'csuros_base2' in comparison['methods']:
            csuros = comparison['methods']['csuros_base2']
            print(f"\n📊 CSUROS (base=2.0):")
            print(f"   Precision Top-10: {csuros['precision_top10']*100:.0f}%")
            print(f"   Mean Absolute Error: {csuros['mean_abs_error']:.2f}")
            print(f"   Mean Relative Error: {csuros['mean_rel_error']*100:.2f}%")
        
        if 'lossy_count_e001' in comparison['methods']:
            lc = comparison['methods']['lossy_count_e001']
            print(f"\n📈 LOSSY-COUNT (ε=0.01):")
            print(f"   Precision Top-10: {lc['precision_top10']*100:.0f}%")
            print(f"   Recall Top-10: {lc['recall_top10']*100:.0f}%")
            print(f"   F1-Score Top-10: {lc['f1_top10']*100:.0f}%")
            print(f"   Memory used: {lc['memory_used']} entries")
        
        self._save_comparison_results()
        
        return comparison
    
    def _save_exact_results(self) -> None:
        """Guarda resultados dos contadores exatos."""
        filepath = os.path.join(self.results_dir, 'exact_counts.csv')
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['year', 'count'])
            for year, count in sorted(self.exact_counts.items(), 
                                       key=lambda x: x[1], reverse=True):
                writer.writerow([int(year), count])
        
        print(f"   💾 Saved: {filepath}")
    
    def _save_csuros_results(self) -> None:
        """Guarda resultados do Csuros' Counter."""
        filepath = os.path.join(self.results_dir, 'csuros_results.csv')
        
        rows = []
        for base, data in self.csuros_results.items():
            analysis = data['analysis']
            rows.append({
                'base': base,
                'mean_abs_error': analysis['overall']['mean_absolute_error'],
                'max_abs_error': analysis['overall']['max_absolute_error'],
                'min_abs_error': analysis['overall']['min_absolute_error'],
                'mean_rel_error': analysis['overall']['mean_relative_error'],
                'max_rel_error': analysis['overall']['max_relative_error'],
                'min_rel_error': analysis['overall']['min_relative_error']
            })
        
        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False)
        
        print(f"   💾 Saved: {filepath}")
    
    def _save_lossy_count_results(self) -> None:
        """Guarda resultados do Lossy-Count."""
        filepath = os.path.join(self.results_dir, 'lossy_count_results.csv')
        
        rows = []
        for exp in self.lossy_count_results['analysis']['per_epsilon']:
            for n, n_data in exp['per_n'].items():
                rows.append({
                    'epsilon': exp['epsilon'],
                    'n': n,
                    'memory_used': exp['memory_used'],
                    'precision': n_data['precision'],
                    'recall': n_data['recall'],
                    'f1_score': n_data['f1_score'],
                    'mean_abs_error': n_data['mean_abs_error'],
                    'mean_rel_error': n_data['mean_rel_error']
                })
        
        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False)
        
        print(f"   💾 Saved: {filepath}")
    
    def _save_comparison_results(self) -> None:
        """Guarda resultados da comparação."""
        filepath = os.path.join(self.results_dir, 'comparison_summary.json')
        
        # Converter para formato serializável
        comparison_serializable = {
            'exact_top_10': [(int(item), count) for item, count in self.comparison_results['exact_top_10']],
            'exact_top_20': [(int(item), count) for item, count in self.comparison_results['exact_top_20']],
            'methods': {}
        }
        
        for method, data in self.comparison_results.get('methods', {}).items():
            comparison_serializable['methods'][method] = {}
            for key, value in data.items():
                if key == 'top_10':
                    comparison_serializable['methods'][method][key] = [
                        (int(item), float(est)) for item, est in value
                    ]
                elif isinstance(value, float):
                    comparison_serializable['methods'][method][key] = round(value, 6)
                else:
                    comparison_serializable['methods'][method][key] = value
        
        with open(filepath, 'w') as f:
            json.dump(comparison_serializable, f, indent=2)
        
        print(f"   💾 Saved: {filepath}")


if __name__ == "__main__":
    # Caminho para o dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "amazon_prime_titles.csv")
    
    # Criar runner e executar todos os experimentos
    runner = ExperimentRunner(data_path, column='release_year')
    
    print("\n" + "=" * 70)
    print("   ADVANCED ALGORITHMS - PROJECT 3")
    print("   Frequent Items Analysis")
    print("   Hugo Gonçalo Lopes Castro - 113889")
    print("=" * 70)
    print(f"\n📁 Dataset: {data_path}")
    print(f"📊 Attribute: release_year")
    print(f"🕐 Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Executar tudo
    results = runner.run_all_experiments()
    
    print(f"\n🕐 End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📁 Results saved in: results/")
    print("   • exact_counts.csv")
    print("   • csuros_results.csv")
    print("   • lossy_count_results.csv")
    print("   • comparison_summary.json")
