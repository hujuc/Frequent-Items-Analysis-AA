# Frequent Items Analysis - AA 2025/2026

## Project 3: Frequent and Less Frequent Items Analysis

**Student:** Hugo Gonçalo Lopes Castro  
**Number:** 113889  
**Dataset:** Amazon Prime Movies and TV Shows  
**Attribute:** `release_year`  

---

##  Description

This project implements and compares three methods for identifying frequent items:

1. **Exact Counters** - Baseline with precise counting
2. **Csuros' Counter** - Approximate counter with reduced memory
3. **Lossy-Count** - Data stream algorithm for frequent items

---

##  How to Run

### Requirements

```bash
pip install pandas numpy matplotlib
```

### Full Execution

```bash
cd src
python main.py --all
```

### Execution Modes

```bash
# Exact counters only
python main.py --exact

# Csuros' Counter only (with specific base)
python main.py --csuros --base 2.0 --runs 10

# Lossy-Count only (with specific epsilon)
python main.py --lossy --epsilon 0.01

# Visualizations only (requires existing results)
python main.py --viz
```

---

##  Project Structure

```
Frequent-Items-Analysis-AA/
│
├── amazon_prime_titles.csv    # Dataset
├── README.md                   # This file
├── PROJETO_EXPLICACAO.md      # Detailed project explanation
│
├── src/
│   ├── __init__.py
│   ├── main.py                # Main script
│   ├── exact_counter.py       # Exact counters
│   ├── csuros_counter.py      # Csuros' Counter
│   ├── lossy_count.py         # Lossy-Count
│   ├── experiments.py         # Experiment management
│   └── visualization.py       # Plot generation
│
└── results/
    ├── exact_counts.csv       # Exact counts
    ├── csuros_results.csv     # Csuros results
    ├── lossy_count_results.csv # Lossy-Count results
    ├── comparison_summary.json # Final comparison
    └── plots/                  # Generated plots
```

---

##  Results

After execution, results are saved in `results/`:

- **exact_counts.csv** - Years ordered by frequency
- **csuros_results.csv** - Error statistics by base
- **lossy_count_results.csv** - Precision by epsilon and n
- **comparison_summary.json** - Method comparison

### Visualizations

Plots are generated in `results/plots/`:
- `frequency_distribution.png` - Frequency distribution
- `csuros_error_analysis.png` - Csuros error analysis
- `lossy_count_precision.png` - Lossy-Count precision
- `memory_vs_precision.png` - Memory/precision trade-off
- `method_comparison.png` - Method comparison
- `error_heatmap.png` - F1-Score heatmap

---

##  Implemented Algorithms

### 1. Exact Counters
- Complexity: O(n) time, O(k) space
- Precision: 100%
- Baseline for comparison

### 2. Csuros' Counter
- Probabilistic counter with logarithmic increments
- Parameter: `base` (typically 2.0)
- Trade-off: higher base = less memory, more error

### 3. Lossy-Count
- Data stream algorithm for frequent items
- Parameters: `epsilon`, `support`
- Guarantees: doesn't lose items with freq >= (support - epsilon) * N

---

##  Evaluated Metrics

- **Absolute Error**: |estimate - exact_value|
- **Relative Error**: |estimate - exact_value| / exact_value
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1-Score**: 2 * Precision * Recall / (Precision + Recall)

---

##  Author

Hugo Gonçalo Lopes Castro - 113889  
Advanced Algorithms, DETI, University of Aveiro  
2025/2026
