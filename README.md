# Frequent Items Analysis - AA 2025/2026

## Projeto 3: Análise de Itens Frequentes e Menos Frequentes

**Aluno:** Hugo Gonçalo Lopes Castro  
**Número:** 113889  
**Dataset:** Amazon Prime Movies and TV Shows  
**Atributo:** `release_year`  

---

## 📋 Descrição

Este projeto implementa e compara três métodos para identificação de itens frequentes:

1. **Contadores Exatos** - Baseline com contagem precisa
2. **Csuros' Counter** - Contador aproximado com memória reduzida
3. **Lossy-Count** - Algoritmo de data stream para itens frequentes

---

## 🚀 Como Executar

### Requisitos

```bash
pip install pandas numpy matplotlib
```

### Execução Completa

```bash
cd src
python main.py --all
```

### Modos de Execução

```bash
# Apenas contadores exatos
python main.py --exact

# Apenas Csuros' Counter (com base específica)
python main.py --csuros --base 2.0 --runs 10

# Apenas Lossy-Count (com epsilon específico)
python main.py --lossy --epsilon 0.01

# Apenas visualizações (requer resultados existentes)
python main.py --viz
```

---

## 📁 Estrutura do Projeto

```
Frequent-Items-Analysis-AA/
│
├── amazon_prime_titles.csv    # Dataset
├── README.md                   # Este ficheiro
├── PROJETO_EXPLICACAO.md      # Explicação detalhada do projeto
│
├── src/
│   ├── __init__.py
│   ├── main.py                # Script principal
│   ├── exact_counter.py       # Contadores exatos
│   ├── csuros_counter.py      # Csuros' Counter
│   ├── lossy_count.py         # Lossy-Count
│   ├── experiments.py         # Gestão de experimentos
│   └── visualization.py       # Geração de gráficos
│
└── results/
    ├── exact_counts.csv       # Contagens exatas
    ├── csuros_results.csv     # Resultados Csuros
    ├── lossy_count_results.csv # Resultados Lossy-Count
    ├── comparison_summary.json # Comparação final
    └── plots/                  # Gráficos gerados
```

---

## 📊 Resultados

Após execução, os resultados são guardados em `results/`:

- **exact_counts.csv** - Anos ordenados por frequência
- **csuros_results.csv** - Estatísticas de erro por base
- **lossy_count_results.csv** - Precisão por epsilon e n
- **comparison_summary.json** - Comparação entre métodos

### Visualizações

Os gráficos são gerados em `results/plots/`:
- `frequency_distribution.png` - Distribuição de frequências
- `csuros_error_analysis.png` - Análise de erros Csuros
- `lossy_count_precision.png` - Precisão Lossy-Count
- `memory_vs_precision.png` - Trade-off memória/precisão
- `method_comparison.png` - Comparação de métodos
- `error_heatmap.png` - Heatmap de F1-Score

---

## 📚 Algoritmos Implementados

### 1. Contadores Exatos
- Complexidade: O(n) tempo, O(k) espaço
- Precisão: 100%
- Baseline para comparação

### 2. Csuros' Counter
- Contador probabilístico com incrementos logarítmicos
- Parâmetro: `base` (tipicamente 2.0)
- Trade-off: maior base = menos memória, mais erro

### 3. Lossy-Count
- Algoritmo de data stream para itens frequentes
- Parâmetros: `epsilon`, `support`
- Garantias: não perde itens com freq >= (support - epsilon) * N

---

## 📈 Métricas Avaliadas

- **Erro Absoluto**: |estimativa - valor_exato|
- **Erro Relativo**: |estimativa - valor_exato| / valor_exato
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1-Score**: 2 * Precision * Recall / (Precision + Recall)

---

## 👤 Autor

Hugo Gonçalo Lopes Castro - 113889  
Algoritmos Avançados, DETI, Universidade de Aveiro  
2025/2026
