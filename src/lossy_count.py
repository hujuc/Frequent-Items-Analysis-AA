"""
Lossy-Count Algorithm - Algoritmo de Data Stream
Algoritmos Avançados 2025/2026 - Trabalho 3
Hugo Gonçalo Lopes Castro - 113889

Este módulo implementa o algoritmo Lossy-Count para identificação
de itens frequentes em data streams com memória limitada.

Referência:
Manku, G. S., & Motwani, R. (2002). "Approximate frequency counts over data streams"
Proceedings of the 28th VLDB Conference.
"""

import math
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import time
import pandas as pd


class LossyCount:
    """
    Implementação do algoritmo Lossy-Count para data streams.
    
    O algoritmo divide o stream em "buckets" e mantém contadores para
    itens frequentes. Garante que nenhum item com frequência >= (support - epsilon)*N
    será perdido, onde N é o tamanho do stream.
    
    Parâmetros:
        epsilon (float): Parâmetro de erro (0 < epsilon < 1)
                        Valores menores = mais precisão, mais memória
        support (float): Suporte mínimo para reportar item (0 < support < 1)
                        Itens com freq >= support*N são reportados
    """
    
    def __init__(self, epsilon: float = 0.01, support: float = 0.1):
        """
        Inicializa o algoritmo Lossy-Count.
        
        Args:
            epsilon: Parâmetro de erro (default: 0.01 = 1%)
            support: Suporte mínimo (default: 0.1 = 10%)
        """
        if epsilon <= 0 or epsilon >= 1:
            raise ValueError("epsilon deve estar entre 0 e 1 (exclusivo)")
        if support <= 0 or support >= 1:
            raise ValueError("support deve estar entre 0 e 1 (exclusivo)")
        if epsilon >= support:
            raise ValueError("epsilon deve ser menor que support")
        
        self.epsilon = epsilon
        self.support = support
        
        # Tamanho do bucket: w = ceil(1/epsilon)
        self.bucket_width = math.ceil(1.0 / epsilon)
        
        # Estrutura: {item: (count, bucket_id_when_inserted)}
        self.entries: Dict[any, Tuple[int, int]] = {}
        
        # Contadores
        self.current_bucket = 1  # Bucket atual (b_current)
        self.items_in_current_bucket = 0
        self.total_items = 0
        self.processing_time = 0.0
        
        # Estatísticas
        self.max_entries = 0  # Máximo de entries em memória
        self.prune_count = 0  # Número de vezes que limpámos entries
    
    def _process_item(self, item) -> None:
        """
        Processa um único item do stream.
        
        Args:
            item: Item a processar
        """
        self.total_items += 1
        self.items_in_current_bucket += 1
        
        # Atualizar ou inserir entry
        if item in self.entries:
            count, delta = self.entries[item]
            self.entries[item] = (count + 1, delta)
        else:
            # Novo item: count=1, delta=b_current-1
            self.entries[item] = (1, self.current_bucket - 1)
        
        # Atualizar estatística de memória
        self.max_entries = max(self.max_entries, len(self.entries))
        
        # Verificar se completámos um bucket
        if self.items_in_current_bucket >= self.bucket_width:
            self._prune_entries()
            self.current_bucket += 1
            self.items_in_current_bucket = 0
    
    def _prune_entries(self) -> None:
        """
        Remove entries com contagem baixa (fase de limpeza).
        
        Remove entries onde count + delta <= b_current
        """
        items_to_remove = []
        
        for item, (count, delta) in self.entries.items():
            if count + delta <= self.current_bucket:
                items_to_remove.append(item)
        
        for item in items_to_remove:
            del self.entries[item]
        
        if items_to_remove:
            self.prune_count += 1
    
    def process_stream(self, stream) -> None:
        """
        Processa um stream completo de itens.
        
        Args:
            stream: Iterável de itens a processar
        """
        start_time = time.time()
        
        for item in stream:
            if pd.notna(item):  # Ignorar valores NaN
                self._process_item(item)
        
        self.processing_time = time.time() - start_time
    
    def get_frequent_items(self, min_support: float = None) -> List[Tuple]:
        """
        Retorna itens com frequência estimada >= min_support * N.
        
        Args:
            min_support: Suporte mínimo (default: self.support)
            
        Returns:
            Lista de tuplos (item, count_estimado, freq_estimada) ordenada por frequência
        """
        if min_support is None:
            min_support = self.support
        
        threshold = (min_support - self.epsilon) * self.total_items
        
        frequent = []
        for item, (count, delta) in self.entries.items():
            estimated_count = count  # Estimativa inferior
            estimated_freq = count / self.total_items if self.total_items > 0 else 0
            
            if count >= threshold:
                frequent.append((item, count, estimated_freq))
        
        # Ordenar por contagem decrescente
        frequent.sort(key=lambda x: x[1], reverse=True)
        return frequent
    
    def get_top_n(self, n: int = 10) -> List[Tuple]:
        """
        Retorna os n itens mais frequentes encontrados.
        
        Args:
            n: Número de itens a retornar
            
        Returns:
            Lista de tuplos (item, count) ordenada por frequência
        """
        sorted_items = sorted(
            self.entries.items(),
            key=lambda x: x[1][0],  # Ordenar por count
            reverse=True
        )
        
        return [(item, count) for item, (count, delta) in sorted_items[:n]]
    
    def get_count(self, item) -> int:
        """
        Retorna a contagem estimada para um item.
        
        Args:
            item: Item a consultar
            
        Returns:
            Contagem estimada (0 se não presente)
        """
        if item in self.entries:
            return self.entries[item][0]
        return 0
    
    def get_all_counts(self) -> Dict:
        """
        Retorna todas as contagens armazenadas.
        
        Returns:
            Dicionário {item: count}
        """
        return {item: count for item, (count, delta) in self.entries.items()}
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas sobre a execução do algoritmo.
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            'total_items': self.total_items,
            'unique_items_stored': len(self.entries),
            'epsilon': self.epsilon,
            'support': self.support,
            'bucket_width': self.bucket_width,
            'current_bucket': self.current_bucket,
            'max_entries': self.max_entries,
            'prune_count': self.prune_count,
            'processing_time': self.processing_time,
            'memory_efficiency': len(self.entries) / self.bucket_width if self.bucket_width > 0 else 0
        }
    
    def reset(self) -> None:
        """Reinicia o algoritmo."""
        self.entries = {}
        self.current_bucket = 1
        self.items_in_current_bucket = 0
        self.total_items = 0
        self.processing_time = 0.0
        self.max_entries = 0
        self.prune_count = 0


def run_lossy_count_experiment(filepath: str, column: str = 'release_year',
                                epsilon_values: List[float] = None,
                                n_values: List[int] = None) -> Dict:
    """
    Executa experimentos com diferentes parâmetros do Lossy-Count.
    
    Args:
        filepath: Caminho para o ficheiro CSV
        column: Coluna a analisar
        epsilon_values: Lista de valores de epsilon a testar
        n_values: Lista de valores de n (top-n) a retornar
        
    Returns:
        Dicionário com resultados
    """
    if epsilon_values is None:
        epsilon_values = [0.1, 0.05, 0.01, 0.005, 0.001]
    if n_values is None:
        n_values = [5, 10, 15, 20, 25, 30]
    
    df = pd.read_csv(filepath)
    data = df[column].dropna().tolist()  # Converter para lista para reutilizar
    
    results = {
        'epsilon_values': epsilon_values,
        'n_values': n_values,
        'experiments': []
    }
    
    for epsilon in epsilon_values:
        # Support deve ser maior que epsilon
        support = max(epsilon * 2, 0.001)  # Garantir support > epsilon
        
        lc = LossyCount(epsilon=epsilon, support=support)
        lc.process_stream(data)
        
        experiment = {
            'epsilon': epsilon,
            'support': support,
            'statistics': lc.get_statistics(),
            'top_n_results': {}
        }
        
        for n in n_values:
            top_n = lc.get_top_n(n)
            experiment['top_n_results'][n] = top_n
        
        results['experiments'].append(experiment)
    
    return results


def analyze_lossy_count_results(results: Dict, exact_counts: Dict) -> Dict:
    """
    Analisa resultados do Lossy-Count comparando com contagens exatas.
    
    Args:
        results: Resultados de run_lossy_count_experiment
        exact_counts: Dicionário com contagens exatas
        
    Returns:
        Análise de precisão e recall
    """
    # Ordenar itens exatos por frequência
    sorted_exact = sorted(exact_counts.items(), key=lambda x: x[1], reverse=True)
    
    analysis = {
        'per_epsilon': [],
        'per_n': defaultdict(list)
    }
    
    for exp in results['experiments']:
        epsilon = exp['epsilon']
        epsilon_analysis = {
            'epsilon': epsilon,
            'memory_used': exp['statistics']['max_entries'],
            'per_n': {}
        }
        
        for n, top_n in exp['top_n_results'].items():
            # Top-n exato
            exact_top_n = set(item for item, count in sorted_exact[:n])
            
            # Top-n do Lossy-Count
            lc_top_n = set(item for item, count in top_n)
            
            # Métricas
            true_positives = len(exact_top_n & lc_top_n)
            false_positives = len(lc_top_n - exact_top_n)
            false_negatives = len(exact_top_n - lc_top_n)
            
            precision = true_positives / len(lc_top_n) if lc_top_n else 0
            recall = true_positives / len(exact_top_n) if exact_top_n else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            # Calcular erros nas contagens
            abs_errors = []
            rel_errors = []
            for item, lc_count in top_n:
                exact = exact_counts.get(item, 0)
                abs_error = abs(lc_count - exact)
                rel_error = abs_error / exact if exact > 0 else 0
                abs_errors.append(abs_error)
                rel_errors.append(rel_error)
            
            n_analysis = {
                'n': n,
                'true_positives': true_positives,
                'false_positives': false_positives,
                'false_negatives': false_negatives,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'mean_abs_error': sum(abs_errors) / len(abs_errors) if abs_errors else 0,
                'mean_rel_error': sum(rel_errors) / len(rel_errors) if rel_errors else 0
            }
            
            epsilon_analysis['per_n'][n] = n_analysis
            analysis['per_n'][n].append({
                'epsilon': epsilon,
                **n_analysis
            })
        
        analysis['per_epsilon'].append(epsilon_analysis)
    
    return analysis


if __name__ == "__main__":
    import os
    from exact_counter import run_exact_count
    
    # Caminho para o dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "amazon_prime_titles.csv")
    
    print("=" * 60)
    print("LOSSY-COUNT - Amazon Prime Dataset")
    print("Atributo: release_year")
    print("=" * 60)
    
    # Primeiro, obter contagens exatas para comparação
    print("\n📊 A obter contagens exatas para comparação...")
    exact_counter = run_exact_count(data_path, 'release_year')
    exact_counts = exact_counter.get_all_counts()
    sorted_exact = sorted(exact_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n📋 TOP 10 EXATO:")
    for i, (year, count) in enumerate(sorted_exact[:10], 1):
        print(f"   {i:2}. {int(year)}: {count}")
    
    # Testar Lossy-Count com diferentes epsilon
    print("\n" + "=" * 60)
    print("🔄 EXPERIMENTOS COM LOSSY-COUNT")
    print("=" * 60)
    
    epsilon_values = [0.1, 0.05, 0.01, 0.005]
    
    for epsilon in epsilon_values:
        support = epsilon * 2
        
        print(f"\n{'─'*50}")
        print(f"ε = {epsilon}, support = {support}")
        print(f"{'─'*50}")
        
        df = pd.read_csv(data_path)
        data = df['release_year'].dropna()
        
        lc = LossyCount(epsilon=epsilon, support=support)
        lc.process_stream(data)
        
        stats = lc.get_statistics()
        print(f"📈 Estatísticas:")
        print(f"   Total processado: {stats['total_items']}")
        print(f"   Itens armazenados: {stats['unique_items_stored']}")
        print(f"   Tamanho bucket: {stats['bucket_width']}")
        print(f"   Máx. entries: {stats['max_entries']}")
        print(f"   Podas realizadas: {stats['prune_count']}")
        print(f"   Tempo: {stats['processing_time']*1000:.2f} ms")
        
        # Comparar top-10
        top_10_lc = lc.get_top_n(10)
        exact_top_10 = set(item for item, count in sorted_exact[:10])
        lc_top_10 = set(item for item, count in top_10_lc)
        
        hits = len(exact_top_10 & lc_top_10)
        
        print(f"\n🎯 TOP 10 Lossy-Count (Precision: {hits}/10 = {hits*10}%):")
        for i, (year, count) in enumerate(top_10_lc, 1):
            exact = exact_counts.get(year, 0)
            marker = "✓" if year in exact_top_10 else "✗"
            print(f"   {i:2}. {int(year)}: {count} (exato: {exact}) {marker}")
    
    print("\n" + "=" * 60)
