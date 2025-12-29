"""
Visualization - Geração de Gráficos
Algoritmos Avançados 2025/2026 - Trabalho 3
Hugo Gonçalo Lopes Castro - 113889

Este módulo gera visualizações para o relatório:
- Distribuição de frequências
- Comparação de métodos
- Análise de erros
- Performance vs Precisão
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

# Configuração de estilo para gráficos de qualidade
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10


class Visualizer:
    """
    Classe para gerar visualizações dos resultados experimentais.
    """
    
    def __init__(self, results_dir: str):
        """
        Inicializa o visualizador.
        
        Args:
            results_dir: Diretório com os resultados
        """
        self.results_dir = results_dir
        self.plots_dir = os.path.join(results_dir, 'plots')
        os.makedirs(self.plots_dir, exist_ok=True)
        
        # Carregar dados
        self.exact_counts = None
        self.csuros_results = None
        self.lossy_count_results = None
        self.comparison = None
        
        self._load_data()
    
    def _load_data(self) -> None:
        """Carrega os dados dos ficheiros CSV/JSON."""
        try:
            # Contagens exatas
            exact_path = os.path.join(self.results_dir, 'exact_counts.csv')
            if os.path.exists(exact_path):
                df = pd.read_csv(exact_path)
                self.exact_counts = dict(zip(df['year'], df['count']))
            
            # Resultados Csuros
            csuros_path = os.path.join(self.results_dir, 'csuros_results.csv')
            if os.path.exists(csuros_path):
                self.csuros_results = pd.read_csv(csuros_path)
            
            # Resultados Lossy-Count
            lc_path = os.path.join(self.results_dir, 'lossy_count_results.csv')
            if os.path.exists(lc_path):
                self.lossy_count_results = pd.read_csv(lc_path)
            
            # Comparação
            comp_path = os.path.join(self.results_dir, 'comparison_summary.json')
            if os.path.exists(comp_path):
                with open(comp_path, 'r') as f:
                    self.comparison = json.load(f)
                    
        except Exception as e:
            print(f"⚠️ Aviso ao carregar dados: {e}")
    
    def plot_frequency_distribution(self) -> str:
        """
        Gera gráfico de barras com a distribuição de frequências.
        
        Returns:
            Caminho para o ficheiro guardado
        """
        if self.exact_counts is None:
            print("❌ Dados exatos não disponíveis")
            return ""
        
        # Ordenar por frequência
        sorted_items = sorted(self.exact_counts.items(), key=lambda x: x[1], reverse=True)
        years = [int(item[0]) for item in sorted_items[:30]]
        counts = [item[1] for item in sorted_items[:30]]
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        bars = ax.bar(range(len(years)), counts, color='steelblue', edgecolor='darkblue', alpha=0.8)
        
        # Destacar top 10
        for i in range(min(10, len(bars))):
            bars[i].set_color('coral')
            bars[i].set_edgecolor('darkred')
        
        ax.set_xlabel('Ano de Lançamento')
        ax.set_ylabel('Número de Títulos')
        ax.set_title('Distribuição de Títulos Amazon Prime por Ano de Lançamento\n(Top 30 anos mais frequentes)')
        ax.set_xticks(range(len(years)))
        ax.set_xticklabels(years, rotation=45, ha='right')
        
        # Legenda
        top10_patch = mpatches.Patch(color='coral', label='Top 10')
        other_patch = mpatches.Patch(color='steelblue', label='Outros')
        ax.legend(handles=[top10_patch, other_patch], loc='upper right')
        
        plt.tight_layout()
        
        filepath = os.path.join(self.plots_dir, 'frequency_distribution.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   📈 Guardado: {filepath}")
        return filepath
    
    def plot_csuros_error_analysis(self) -> str:
        """
        Gera gráfico de análise de erros do Csuros' Counter.
        
        Returns:
            Caminho para o ficheiro guardado
        """
        if self.csuros_results is None:
            print("❌ Dados Csuros não disponíveis")
            return ""
        
        df = self.csuros_results
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Gráfico 1: Erro Absoluto por Base
        ax1 = axes[0]
        x = range(len(df))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], df['mean_abs_error'], width, 
                label='Erro Médio', color='steelblue', alpha=0.8)
        ax1.bar([i + width/2 for i in x], df['max_abs_error'], width,
                label='Erro Máximo', color='coral', alpha=0.8)
        
        ax1.set_xlabel('Base do Contador')
        ax1.set_ylabel('Erro Absoluto')
        ax1.set_title('Erro Absoluto por Base - Csuros\' Counter')
        ax1.set_xticks(x)
        ax1.set_xticklabels([f'{b:.1f}' for b in df['base']])
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Gráfico 2: Erro Relativo por Base
        ax2 = axes[1]
        
        ax2.bar([i - width/2 for i in x], df['mean_rel_error'] * 100, width,
                label='Erro Médio', color='steelblue', alpha=0.8)
        ax2.bar([i + width/2 for i in x], df['max_rel_error'] * 100, width,
                label='Erro Máximo', color='coral', alpha=0.8)
        
        ax2.set_xlabel('Base do Contador')
        ax2.set_ylabel('Erro Relativo (%)')
        ax2.set_title('Erro Relativo por Base - Csuros\' Counter')
        ax2.set_xticks(x)
        ax2.set_xticklabels([f'{b:.1f}' for b in df['base']])
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        filepath = os.path.join(self.plots_dir, 'csuros_error_analysis.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   📈 Guardado: {filepath}")
        return filepath
    
    def plot_lossy_count_precision(self) -> str:
        """
        Gera gráfico de precisão do Lossy-Count por epsilon e n.
        
        Returns:
            Caminho para o ficheiro guardado
        """
        if self.lossy_count_results is None:
            print("❌ Dados Lossy-Count não disponíveis")
            return ""
        
        df = self.lossy_count_results
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Gráfico 1: Precision por Epsilon (para diferentes n)
        ax1 = axes[0]
        
        n_values = df['n'].unique()
        colors = plt.cm.viridis(np.linspace(0, 1, len(n_values)))
        
        for i, n in enumerate(sorted(n_values)):
            subset = df[df['n'] == n].sort_values('epsilon')
            ax1.plot(subset['epsilon'], subset['precision'] * 100, 
                    marker='o', label=f'n={n}', color=colors[i], linewidth=2)
        
        ax1.set_xlabel('Epsilon (ε)')
        ax1.set_ylabel('Precision (%)')
        ax1.set_title('Precision do Lossy-Count por Epsilon')
        ax1.set_xscale('log')
        ax1.legend(title='Top-N', loc='lower right')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([0, 105])
        
        # Gráfico 2: F1-Score por Epsilon
        ax2 = axes[1]
        
        for i, n in enumerate(sorted(n_values)):
            subset = df[df['n'] == n].sort_values('epsilon')
            ax2.plot(subset['epsilon'], subset['f1_score'] * 100,
                    marker='s', label=f'n={n}', color=colors[i], linewidth=2)
        
        ax2.set_xlabel('Epsilon (ε)')
        ax2.set_ylabel('F1-Score (%)')
        ax2.set_title('F1-Score do Lossy-Count por Epsilon')
        ax2.set_xscale('log')
        ax2.legend(title='Top-N', loc='lower right')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 105])
        
        plt.tight_layout()
        
        filepath = os.path.join(self.plots_dir, 'lossy_count_precision.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   📈 Guardado: {filepath}")
        return filepath
    
    def plot_memory_vs_precision(self) -> str:
        """
        Gera gráfico de memória vs precisão para Lossy-Count.
        
        Returns:
            Caminho para o ficheiro guardado
        """
        if self.lossy_count_results is None:
            print("❌ Dados Lossy-Count não disponíveis")
            return ""
        
        df = self.lossy_count_results
        
        # Filtrar para n=10
        df_n10 = df[df['n'] == 10].copy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scatter = ax.scatter(df_n10['memory_used'], df_n10['precision'] * 100,
                            c=df_n10['epsilon'], cmap='viridis_r',
                            s=150, edgecolors='black', linewidth=1)
        
        # Adicionar labels
        for _, row in df_n10.iterrows():
            ax.annotate(f'ε={row["epsilon"]}',
                       (row['memory_used'], row['precision'] * 100),
                       textcoords="offset points", xytext=(5, 5),
                       fontsize=8)
        
        ax.set_xlabel('Memória Utilizada (número de entries)')
        ax.set_ylabel('Precision Top-10 (%)')
        ax.set_title('Trade-off: Memória vs Precisão (Lossy-Count)')
        ax.set_xscale('log')
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Epsilon (ε)')
        
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filepath = os.path.join(self.plots_dir, 'memory_vs_precision.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   📈 Guardado: {filepath}")
        return filepath
    
    def plot_method_comparison(self) -> str:
        """
        Gera gráfico comparando os diferentes métodos.
        
        Returns:
            Caminho para o ficheiro guardado
        """
        if self.comparison is None:
            print("❌ Dados de comparação não disponíveis")
            return ""
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Dados para comparação
        methods = ['Exato', 'Csuros (b=2)', 'Lossy (ε=0.01)']
        
        # Precisão no Top-10
        ax1 = axes[0]
        
        precisions = [100]  # Exato = 100%
        
        if 'csuros_base2' in self.comparison.get('methods', {}):
            precisions.append(self.comparison['methods']['csuros_base2']['precision_top10'] * 100)
        else:
            precisions.append(0)
            
        if 'lossy_count_e001' in self.comparison.get('methods', {}):
            precisions.append(self.comparison['methods']['lossy_count_e001']['precision_top10'] * 100)
        else:
            precisions.append(0)
        
        colors = ['green', 'steelblue', 'coral']
        bars = ax1.bar(methods, precisions, color=colors, edgecolor='black', alpha=0.8)
        
        # Adicionar valores nas barras
        for bar, precision in zip(bars, precisions):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{precision:.0f}%', ha='center', va='bottom', fontsize=11)
        
        ax1.set_ylabel('Precisão (%)')
        ax1.set_title('Precisão na Identificação dos Top-10')
        ax1.set_ylim([0, 110])
        ax1.grid(axis='y', alpha=0.3)
        
        # Top 10 comparação visual
        ax2 = axes[1]
        
        if self.exact_counts:
            sorted_exact = sorted(self.exact_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            years = [int(y) for y, c in sorted_exact]
            counts = [c for y, c in sorted_exact]
            
            ax2.barh(range(len(years)), counts, color='steelblue', alpha=0.8)
            ax2.set_yticks(range(len(years)))
            ax2.set_yticklabels(years)
            ax2.set_xlabel('Número de Títulos')
            ax2.set_title('Top 10 Anos Mais Frequentes (Contagem Exata)')
            ax2.invert_yaxis()
            ax2.grid(axis='x', alpha=0.3)
            
            # Adicionar valores
            for i, count in enumerate(counts):
                ax2.text(count + 5, i, str(count), va='center', fontsize=9)
        
        plt.tight_layout()
        
        filepath = os.path.join(self.plots_dir, 'method_comparison.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   📈 Guardado: {filepath}")
        return filepath
    
    def plot_error_heatmap(self) -> str:
        """
        Gera heatmap de erros do Lossy-Count.
        
        Returns:
            Caminho para o ficheiro guardado
        """
        if self.lossy_count_results is None:
            print("❌ Dados Lossy-Count não disponíveis")
            return ""
        
        df = self.lossy_count_results
        
        # Criar matriz para heatmap
        pivot = df.pivot(index='epsilon', columns='n', values='f1_score')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        im = ax.imshow(pivot.values * 100, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
        
        # Configurar eixos
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_xticklabels(pivot.columns)
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels([f'{e:.3f}' for e in pivot.index])
        
        ax.set_xlabel('N (Top-N)')
        ax.set_ylabel('Epsilon (ε)')
        ax.set_title('F1-Score (%) - Lossy-Count\n(Verde=Melhor, Vermelho=Pior)')
        
        # Adicionar valores nas células
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                value = pivot.values[i, j] * 100
                color = 'white' if value < 50 else 'black'
                ax.text(j, i, f'{value:.0f}', ha='center', va='center', 
                       color=color, fontsize=9)
        
        plt.colorbar(im, ax=ax, label='F1-Score (%)')
        
        plt.tight_layout()
        
        filepath = os.path.join(self.plots_dir, 'error_heatmap.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   📈 Guardado: {filepath}")
        return filepath
    
    def generate_all_plots(self) -> List[str]:
        """
        Gera todos os gráficos.
        
        Returns:
            Lista de caminhos para os ficheiros guardados
        """
        print("\n" + "=" * 70)
        print("📊 GERANDO VISUALIZAÇÕES")
        print("=" * 70)
        
        plots = []
        
        print("\n1. Distribuição de Frequências...")
        plots.append(self.plot_frequency_distribution())
        
        print("\n2. Análise de Erros - Csuros...")
        plots.append(self.plot_csuros_error_analysis())
        
        print("\n3. Precisão Lossy-Count...")
        plots.append(self.plot_lossy_count_precision())
        
        print("\n4. Memória vs Precisão...")
        plots.append(self.plot_memory_vs_precision())
        
        print("\n5. Comparação de Métodos...")
        plots.append(self.plot_method_comparison())
        
        print("\n6. Heatmap de Erros...")
        plots.append(self.plot_error_heatmap())
        
        print("\n" + "=" * 70)
        print(f"✅ {len([p for p in plots if p])} gráficos gerados!")
        print(f"📁 Guardados em: {self.plots_dir}")
        print("=" * 70)
        
        return plots


if __name__ == "__main__":
    # Caminho para resultados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "..", "results")
    
    print("\n" + "=" * 70)
    print("   GERAÇÃO DE VISUALIZAÇÕES")
    print("   Algoritmos Avançados - Trabalho 3")
    print("=" * 70)
    
    # Verificar se existem resultados
    if not os.path.exists(results_dir):
        print("\n❌ Diretório de resultados não encontrado!")
        print("   Execute primeiro: python experiments.py")
        sys.exit(1)
    
    # Gerar visualizações
    viz = Visualizer(results_dir)
    viz.generate_all_plots()
