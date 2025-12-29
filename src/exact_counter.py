"""
Exact Counter - Contagem Exata de Itens
Algoritmos Avançados 2025/2026 - Trabalho 3
Hugo Gonçalo Lopes Castro - 113889

Este módulo implementa contadores exatos para estabelecer 
o baseline de comparação com métodos aproximados.
"""

import pandas as pd
from collections import Counter
from typing import Dict, List, Tuple
import time


class ExactCounter:
    """
    Contador exato que mantém a contagem precisa de cada item.
    Complexidade: O(n) tempo, O(k) espaço onde k é número de itens únicos.
    """
    
    def __init__(self):
        self.counts: Counter = Counter()
        self.total_items: int = 0
        self.processing_time: float = 0.0
    
    def process_stream(self, stream) -> None:
        """
        Processa um stream de itens e conta cada ocorrência.
        
        Args:
            stream: Iterável de itens a processar
        """
        start_time = time.time()
        
        for item in stream:
            if pd.notna(item):  # Ignorar valores NaN
                self.counts[item] += 1
                self.total_items += 1
        
        self.processing_time = time.time() - start_time
    
    def get_count(self, item) -> int:
        """Retorna a contagem exata de um item."""
        return self.counts[item]
    
    def get_all_counts(self) -> Dict:
        """Retorna todas as contagens."""
        return dict(self.counts)
    
    def get_most_frequent(self, n: int = 10) -> List[Tuple]:
        """
        Retorna os n itens mais frequentes.
        
        Args:
            n: Número de itens a retornar
            
        Returns:
            Lista de tuplos (item, contagem) ordenada por frequência
        """
        return self.counts.most_common(n)
    
    def get_least_frequent(self, n: int = 10) -> List[Tuple]:
        """
        Retorna os n itens menos frequentes.
        
        Args:
            n: Número de itens a retornar
            
        Returns:
            Lista de tuplos (item, contagem) ordenada por frequência crescente
        """
        return self.counts.most_common()[:-n-1:-1]
    
    def get_unique_count(self) -> int:
        """Retorna o número de itens únicos."""
        return len(self.counts)
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas sobre as contagens.
        
        Returns:
            Dicionário com estatísticas descritivas
        """
        if not self.counts:
            return {}
        
        values = list(self.counts.values())
        
        return {
            'total_items': self.total_items,
            'unique_items': len(self.counts),
            'min_count': min(values),
            'max_count': max(values),
            'avg_count': sum(values) / len(values),
            'processing_time': self.processing_time
        }
    
    def reset(self) -> None:
        """Reinicia o contador."""
        self.counts = Counter()
        self.total_items = 0
        self.processing_time = 0.0


def load_dataset(filepath: str, column: str) -> pd.Series:
    """
    Carrega um dataset CSV e retorna a coluna especificada.
    
    Args:
        filepath: Caminho para o ficheiro CSV
        column: Nome da coluna a extrair
        
    Returns:
        Série pandas com os valores da coluna
    """
    df = pd.read_csv(filepath)
    return df[column]


def run_exact_count(filepath: str, column: str = 'release_year') -> ExactCounter:
    """
    Executa contagem exata num ficheiro CSV.
    
    Args:
        filepath: Caminho para o ficheiro CSV
        column: Coluna a analisar
        
    Returns:
        ExactCounter com os resultados
    """
    data = load_dataset(filepath, column)
    counter = ExactCounter()
    counter.process_stream(data)
    return counter


if __name__ == "__main__":
    # Teste com o dataset Amazon Prime
    import os
    
    # Caminho relativo ao ficheiro
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "amazon_prime_titles.csv")
    
    print("=" * 60)
    print("CONTADORES EXATOS - Amazon Prime Dataset")
    print("Atributo: release_year")
    print("=" * 60)
    
    # Executar contagem
    counter = run_exact_count(data_path, 'release_year')
    
    # Mostrar estatísticas
    stats = counter.get_statistics()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de itens processados: {stats['total_items']}")
    print(f"   Itens únicos (anos): {stats['unique_items']}")
    print(f"   Contagem mínima: {stats['min_count']}")
    print(f"   Contagem máxima: {stats['max_count']}")
    print(f"   Média de contagens: {stats['avg_count']:.2f}")
    print(f"   Tempo de processamento: {stats['processing_time']*1000:.2f} ms")
    
    # Top 10 mais frequentes
    print(f"\n🔝 TOP 10 ANOS MAIS FREQUENTES:")
    for i, (year, count) in enumerate(counter.get_most_frequent(10), 1):
        print(f"   {i:2}. {int(year)}: {count} ocorrências")
    
    # Top 10 menos frequentes
    print(f"\n🔻 TOP 10 ANOS MENOS FREQUENTES:")
    for i, (year, count) in enumerate(counter.get_least_frequent(10), 1):
        print(f"   {i:2}. {int(year)}: {count} ocorrências")
    
    print("\n" + "=" * 60)
