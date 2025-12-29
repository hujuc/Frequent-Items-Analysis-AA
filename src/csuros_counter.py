"""
Csuros' Counter - Contador Aproximado
Algoritmos Avançados 2025/2026 - Trabalho 3
Hugo Gonçalo Lopes Castro - 113889

Este módulo implementa o algoritmo Csuros' Counter para
contagem aproximada de itens com uso reduzido de memória.

Referência:
Csűrös, M. (2010). "Approximate counting with a floating-point counter"
Computing, 85(1-2), 71-89.
"""

import random
import math
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import time
import pandas as pd


class CsurosCounter:
    """
    Implementação do contador aproximado de Csűrös.
    
    O algoritmo usa contadores de ponto flutuante com incrementos probabilísticos
    para reduzir o uso de memória mantendo estimativas com erro controlado.
    
    Parâmetros:
        base (float): Base do contador (tipicamente 2). Controla precisão vs memória.
                     Valores maiores = menos memória, mais erro.
    """
    
    def __init__(self, base: float = 2.0):
        """
        Inicializa o contador Csűrös.
        
        Args:
            base: Base do contador logarítmico (default: 2.0)
        """
        self.base = base
        self.counters: Dict[any, float] = defaultdict(float)
        self.total_items: int = 0
        self.processing_time: float = 0.0
    
    def _increment(self, current_value: float) -> float:
        """
        Incrementa um contador usando o algoritmo de Csűrös.
        
        O incremento é probabilístico:
        - Se valor < 1: incrementa sempre para 1
        - Caso contrário: incrementa com probabilidade 1/base^floor(log_base(valor))
        
        Args:
            current_value: Valor atual do contador
            
        Returns:
            Novo valor do contador
        """
        if current_value < 1:
            return 1.0
        
        # Calcular o expoente atual
        exponent = math.floor(math.log(current_value, self.base))
        
        # Probabilidade de incremento
        probability = 1.0 / (self.base ** exponent)
        
        # Incremento probabilístico
        if random.random() < probability:
            # Incrementar por base^exponent
            increment = self.base ** exponent
            return current_value + increment
        
        return current_value
    
    def _estimate(self, counter_value: float) -> float:
        """
        Estima a contagem real a partir do valor do contador.
        
        Args:
            counter_value: Valor armazenado no contador
            
        Returns:
            Estimativa da contagem real
        """
        if counter_value <= 0:
            return 0.0
        
        # A estimativa é baseada na fórmula de Csűrös
        # Para base b, o valor esperado é aproximadamente:
        # E[n] ≈ (b / (b-1)) * (counter_value - 1) + 1
        
        return ((self.base / (self.base - 1)) * (counter_value - 1)) + 1
    
    def increment(self, item) -> None:
        """
        Incrementa o contador para um item específico.
        
        Args:
            item: Item a incrementar
        """
        self.counters[item] = self._increment(self.counters[item])
        self.total_items += 1
    
    def process_stream(self, stream) -> None:
        """
        Processa um stream de itens.
        
        Args:
            stream: Iterável de itens a processar
        """
        start_time = time.time()
        
        for item in stream:
            if pd.notna(item):  # Ignorar valores NaN
                self.increment(item)
        
        self.processing_time = time.time() - start_time
    
    def get_estimate(self, item) -> float:
        """
        Retorna a estimativa de contagem para um item.
        
        Args:
            item: Item a consultar
            
        Returns:
            Estimativa da contagem
        """
        return self._estimate(self.counters[item])
    
    def get_raw_counter(self, item) -> float:
        """
        Retorna o valor bruto do contador (não estimado).
        
        Args:
            item: Item a consultar
            
        Returns:
            Valor bruto do contador
        """
        return self.counters[item]
    
    def get_all_estimates(self) -> Dict:
        """
        Retorna estimativas para todos os itens.
        
        Returns:
            Dicionário {item: estimativa}
        """
        return {item: self._estimate(value) for item, value in self.counters.items()}
    
    def get_most_frequent(self, n: int = 10) -> List[Tuple]:
        """
        Retorna os n itens com maiores estimativas.
        
        Args:
            n: Número de itens a retornar
            
        Returns:
            Lista de tuplos (item, estimativa) ordenada
        """
        estimates = self.get_all_estimates()
        sorted_items = sorted(estimates.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:n]
    
    def get_least_frequent(self, n: int = 10) -> List[Tuple]:
        """
        Retorna os n itens com menores estimativas.
        
        Args:
            n: Número de itens a retornar
            
        Returns:
            Lista de tuplos (item, estimativa) ordenada
        """
        estimates = self.get_all_estimates()
        sorted_items = sorted(estimates.items(), key=lambda x: x[1])
        return sorted_items[:n]
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas sobre o contador.
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.counters:
            return {}
        
        estimates = list(self.get_all_estimates().values())
        
        return {
            'total_items': self.total_items,
            'unique_items': len(self.counters),
            'base': self.base,
            'min_estimate': min(estimates),
            'max_estimate': max(estimates),
            'avg_estimate': sum(estimates) / len(estimates),
            'processing_time': self.processing_time
        }
    
    def reset(self) -> None:
        """Reinicia o contador."""
        self.counters = defaultdict(float)
        self.total_items = 0
        self.processing_time = 0.0


def run_csuros_experiment(filepath: str, column: str = 'release_year', 
                          base: float = 2.0, num_runs: int = 10) -> Dict:
    """
    Executa múltiplas corridas do contador Csűrös para análise estatística.
    
    Args:
        filepath: Caminho para o ficheiro CSV
        column: Coluna a analisar
        base: Base do contador
        num_runs: Número de execuções
        
    Returns:
        Dicionário com resultados de todas as corridas
    """
    df = pd.read_csv(filepath)
    data = df[column].dropna()
    
    results = {
        'runs': [],
        'base': base,
        'num_runs': num_runs
    }
    
    for run in range(num_runs):
        counter = CsurosCounter(base=base)
        counter.process_stream(data)
        
        results['runs'].append({
            'run_id': run + 1,
            'estimates': counter.get_all_estimates(),
            'most_frequent': counter.get_most_frequent(20),
            'least_frequent': counter.get_least_frequent(20),
            'processing_time': counter.processing_time
        })
    
    return results


def analyze_csuros_results(results: Dict, exact_counts: Dict) -> Dict:
    """
    Analisa os resultados do Csűrös comparando com contagens exatas.
    
    Args:
        results: Resultados de run_csuros_experiment
        exact_counts: Dicionário com contagens exatas
        
    Returns:
        Análise estatística dos erros
    """
    all_items = set(exact_counts.keys())
    
    # Agregar estimativas por item
    item_estimates = defaultdict(list)
    
    for run in results['runs']:
        for item, estimate in run['estimates'].items():
            item_estimates[item].append(estimate)
    
    # Calcular estatísticas de erro por item
    analysis = {
        'per_item': {},
        'overall': {
            'absolute_errors': [],
            'relative_errors': []
        }
    }
    
    for item in all_items:
        exact = exact_counts[item]
        estimates = item_estimates.get(item, [0] * results['num_runs'])
        
        # Estatísticas das estimativas
        mean_est = sum(estimates) / len(estimates)
        min_est = min(estimates)
        max_est = max(estimates)
        
        # Erros
        abs_errors = [abs(e - exact) for e in estimates]
        rel_errors = [abs(e - exact) / exact if exact > 0 else 0 for e in estimates]
        
        analysis['per_item'][item] = {
            'exact': exact,
            'mean_estimate': mean_est,
            'min_estimate': min_est,
            'max_estimate': max_est,
            'std_estimate': (sum((e - mean_est)**2 for e in estimates) / len(estimates)) ** 0.5,
            'mean_absolute_error': sum(abs_errors) / len(abs_errors),
            'mean_relative_error': sum(rel_errors) / len(rel_errors)
        }
        
        analysis['overall']['absolute_errors'].extend(abs_errors)
        analysis['overall']['relative_errors'].extend(rel_errors)
    
    # Estatísticas globais
    all_abs = analysis['overall']['absolute_errors']
    all_rel = analysis['overall']['relative_errors']
    
    analysis['overall']['mean_absolute_error'] = sum(all_abs) / len(all_abs)
    analysis['overall']['max_absolute_error'] = max(all_abs)
    analysis['overall']['min_absolute_error'] = min(all_abs)
    
    analysis['overall']['mean_relative_error'] = sum(all_rel) / len(all_rel)
    analysis['overall']['max_relative_error'] = max(all_rel)
    analysis['overall']['min_relative_error'] = min(all_rel)
    
    return analysis


if __name__ == "__main__":
    import os
    from exact_counter import run_exact_count
    
    # Caminho para o dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "amazon_prime_titles.csv")
    
    print("=" * 60)
    print("CSUROS' COUNTER - Amazon Prime Dataset")
    print("Attribute: release_year")
    print("=" * 60)
    
    # Primeiro, obter contagens exatas para comparação
    print("\n Getting exact counts for comparison...")
    exact_counter = run_exact_count(data_path, 'release_year')
    exact_counts = exact_counter.get_all_counts()
    
    # Testar com diferentes bases
    for base in [1.5, 2.0, 4.0]:
        print(f"\n{'='*60}")
        print(f" TEST WITH BASE = {base}")
        print(f"{'='*60}")
        
        # Executar experimento com 10 corridas
        results = run_csuros_experiment(data_path, 'release_year', 
                                        base=base, num_runs=10)
        
        # Analisar resultados
        analysis = analyze_csuros_results(results, exact_counts)
        
        print(f"\n ERROR STATISTICS:")
        print(f"   Mean Absolute Error: {analysis['overall']['mean_absolute_error']:.2f}")
        print(f"   Max Absolute Error: {analysis['overall']['max_absolute_error']:.2f}")
        print(f"   Mean Relative Error: {analysis['overall']['mean_relative_error']*100:.2f}%")
        print(f"   Max Relative Error: {analysis['overall']['max_relative_error']*100:.2f}%")
        
        # Mostrar top 5 para a última corrida
        last_run = results['runs'][-1]
        print(f"\n TOP 5 (last run):")
        for i, (year, estimate) in enumerate(last_run['most_frequent'][:5], 1):
            exact = exact_counts.get(year, 0)
            error = abs(estimate - exact)
            print(f"   {i}. {int(year)}: estimate={estimate:.0f}, exact={exact}, error={error:.0f}")
    
    print("\n" + "=" * 60)
