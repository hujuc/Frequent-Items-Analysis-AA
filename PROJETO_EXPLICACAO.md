# Trabalho 3 - Algoritmos Avançados 2025/2026
## Análise de Itens Mais Frequentes e Menos Frequentes

---

## 📋 Informações do Projeto

**Disciplina:** Algoritmos Avançados  
**Período:** 2025/2026 - 1º Semestre  
**Deadline:** 22 de Dezembro de 2025  
**Relatório:** Máximo 10 páginas

---

## 🎯 Atribuição Específica

**Aluno:** HUGO GONÇALO LOPES CASTRO  
**Número:** 113889  
**Dataset:** [Amazon Prime Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows/data)  
**Ficheiro:** `amazon_prime_titles.csv`  
**Atributo a Analisar:** `release_year` (ano de lançamento)

### Algoritmos Atribuídos:
1. **Csuros' Counter** (Contador Aproximado)
2. **Lossy-Count** (Algoritmo de Data Stream)

---

## 🎯 Objetivos do Projeto

O objetivo é **identificar itens frequentes** em datasets usando diferentes métodos e **avaliar a qualidade das estimativas** em relação às contagens exatas.

### O que deve ser desenvolvido:

1. ✅ **Contadores Exatos** - contagem precisa de todas as ocorrências
2. ✅ **Contadores Aproximados** - estimativas usando Csuros' Counter
3. ✅ **Algoritmo de Data Stream** - identificação de itens frequentes usando Lossy-Count

---

## 📊 Dataset: Amazon Prime Titles

### Descrição
O dataset contém informações sobre filmes e séries disponíveis na Amazon Prime, com os seguintes campos:
- `show_id`: ID único
- `type`: Movie ou TV Show
- `title`: Título
- `director`: Realizador
- `cast`: Elenco
- `country`: País
- `date_added`: Data de adição
- **`release_year`: Ano de lançamento** ⭐ (campo a analisar)
- `rating`: Classificação etária
- `duration`: Duração
- `listed_in`: Géneros
- `description`: Descrição

### Estatísticas Básicas
- **Total de registos:** 9,688 linhas
- **Campo de análise:** `release_year` - anos em que os conteúdos foram lançados

### Objetivo da Análise
Identificar os **anos mais frequentes de lançamento** de conteúdos na Amazon Prime e os **menos frequentes**, comparando diferentes métodos de contagem.

---

## 🔧 Tarefas a Implementar

### A) Contadores Exatos
**Objetivo:** Computar o número exato de ocorrências de cada ano de lançamento.

**Implementação:**
- Percorrer todo o dataset
- Contar quantas vezes cada `release_year` aparece
- Armazenar num dicionário/hashmap: `{ano: contagem}`
- Identificar os anos mais frequentes e menos frequentes

**Output esperado:**
- Tabela com anos e suas contagens exatas
- Lista ordenada dos N anos mais frequentes
- Lista ordenada dos N anos menos frequentes

---

### B) Contadores Aproximados - Csuros' Counter

**Objetivo:** Estimar o número de ocorrências usando o algoritmo de Csuros.

#### O que é o Csuros' Counter?
É um contador aproximado que usa **menos memória** que contadores exatos, mas mantém estimativas com erro controlado.

**Características:**
- Usa contadores probabilísticos
- Reduz uso de memória à custa de alguma imprecisão
- Adequado para datasets grandes

**Implementação:**
1. Implementar o algoritmo Csuros' Counter
2. Processar o dataset completo
3. **Repetir o processo várias vezes** (5-10 repetições)
4. Registar as estimativas obtidas

**Análise requerida:**
- Erro absoluto: `|estimativa - valor_exato|`
- Erro relativo: `|estimativa - valor_exato| / valor_exato`
- Para cada ano: valor mínimo, máximo e médio das estimativas
- Comparar a ordem dos anos mais/menos frequentes

---

### C) Algoritmo de Data Stream - Lossy-Count

**Objetivo:** Identificar os N itens mais frequentes num stream de dados.

#### O que é o Lossy-Count?
É um algoritmo para **data streams** que:
- Processa dados em **uma única passagem**
- Usa **memória limitada**
- Identifica itens frequentes com garantias de erro
- Funciona com um parâmetro de erro **ε (epsilon)**

**Parâmetros do algoritmo:**
- **ε (epsilon)**: parâmetro de erro (ex: 0.01, 0.001, 0.0001)
- **n**: número de itens mais frequentes a retornar (ex: 5, 10, 15, 20)

**Implementação:**
1. Implementar o algoritmo Lossy-Count
2. Processar o dataset como um stream (linha a linha)
3. **Experimentar diferentes valores de n**: 5, 10, 15, 20, 25, 30
4. **Experimentar diferentes valores de ε**: testar valores como 0.1, 0.01, 0.001

**Análise requerida:**
- Quais anos são identificados como mais frequentes?
- Estão na mesma ordem que os contadores exatos?
- Como o parâmetro ε afeta os resultados?
- Como o valor de n afeta a precisão?
- Uso de memória vs. precisão

---

## 📈 D) Comparação de Performance

### Métricas a Analisar:

#### 1. **Precisão (Accuracy)**
- Comparar os itens identificados por cada método
- Verificar se os top-N são os mesmos
- Comparar a ordem relativa

#### 2. **Erro Absoluto**
- Para cada ano: `erro = |contagem_aproximada - contagem_exata|`
- Calcular: mínimo, máximo, média, mediana, desvio padrão

#### 3. **Erro Relativo**
- Para cada ano: `erro_rel = |contagem_aproximada - contagem_exata| / contagem_exata`
- Calcular: mínimo, máximo, média, mediana

#### 4. **Eficiência Computacional**
- Tempo de execução de cada método
- Uso de memória (estimado ou medido)
- Número de passagens pelos dados

#### 5. **Qualidade das Estimativas**
- Os métodos aproximados identificam corretamente os top-N?
- Quantos itens frequentes são "perdidos"?
- Quantos falsos positivos existem?

#### 6. **Trade-offs**
- Memória vs. Precisão
- Tempo vs. Precisão
- Parâmetros vs. Qualidade dos resultados

---

## 📊 Experimentos Sugeridos

### Experimento 1: Contadores Exatos (Baseline)
```
- Executar contagem exata
- Identificar top-5, top-10, top-15, top-20
- Identificar bottom-5, bottom-10, etc.
- Guardar como referência
```

### Experimento 2: Csuros' Counter
```
Para diferentes configurações do algoritmo:
  - Executar 10 repetições
  - Calcular médias e desvios
  - Comparar com valores exatos
  - Registar erros
```

### Experimento 3: Lossy-Count
```
Para n = [5, 10, 15, 20]:
  Para ε = [0.1, 0.01, 0.001]:
    - Executar algoritmo
    - Identificar itens frequentes
    - Comparar com valores exatos
    - Registar precisão e recall
```

### Experimento 4: Comparação Global
```
- Criar tabelas comparativas
- Gerar gráficos de erro
- Analisar trade-offs
- Tirar conclusões
```

---

## 📝 E) Relatório (Máximo 10 páginas)

### Estrutura Sugerida:

#### 1. Introdução (0.5-1 página)
- Contextualização do problema
- Objetivos do trabalho
- Descrição do dataset
- Estrutura do relatório

#### 2. Fundamentação Teórica (2-3 páginas)
- **Contadores Exatos**: complexidade e limitações
- **Csuros' Counter**: 
  - Princípio de funcionamento
  - Complexidade temporal e espacial
  - Garantias teóricas de erro
- **Lossy-Count**:
  - Princípio de funcionamento
  - Parâmetros (ε, suporte)
  - Complexidade e garantias
  - Quando usar data stream algorithms

#### 3. Implementação (1-2 páginas)
- Linguagem e ferramentas utilizadas
- Estruturas de dados escolhidas
- Decisões de implementação importantes
- Pseudocódigo (se relevante)

#### 4. Resultados Experimentais (3-4 páginas)
- **Descrição dos experimentos**
- **Resultados dos Contadores Exatos**:
  - Tabela com anos mais frequentes
  - Distribuição de frequências
  
- **Resultados do Csuros' Counter**:
  - Tabelas de comparação
  - Gráficos de erros (absolutos e relativos)
  - Estatísticas de erro (min, max, média, std)
  
- **Resultados do Lossy-Count**:
  - Tabelas para diferentes valores de n e ε
  - Precisão na identificação dos top-N
  - Gráficos de performance
  
- **Comparação entre métodos**:
  - Tabela comparativa de precisão
  - Gráficos de tempo de execução
  - Análise de memória

#### 5. Discussão e Análise (1-2 páginas)
- Interpretação dos resultados
- Análise dos trade-offs observados
- Impacto dos parâmetros nos resultados
- Situações onde cada método é mais adequado
- Limitações encontradas

#### 6. Conclusões (0.5-1 página)
- Síntese dos principais resultados
- Resposta aos objetivos
- Trabalho futuro

#### 7. Referências
- Artigos científicos sobre os algoritmos
- Documentação do dataset
- Bibliotecas utilizadas

---

## 🛠️ Implementação Técnica

### Linguagens Sugeridas:
- **Python** (recomendado): pandas, numpy, matplotlib
- Java
- C++

### Bibliotecas Úteis (Python):
```python
import pandas as pd           # Manipulação de dados
import numpy as np            # Operações numéricas
import matplotlib.pyplot as plt  # Visualização
import time                   # Medição de tempo
import sys                    # Medição de memória
from collections import Counter, defaultdict
```

### Estrutura do Código:
```
project/
│
├── data/
│   └── amazon_prime_titles.csv
│
├── src/
│   ├── exact_counter.py          # Contadores exatos
│   ├── csuros_counter.py         # Implementação Csuros
│   ├── lossy_count.py            # Implementação Lossy-Count
│   ├── experiments.py            # Scripts de experimentos
│   └── visualization.py          # Geração de gráficos
│
├── results/
│   ├── exact_counts.csv
│   ├── csuros_results.csv
│   ├── lossy_count_results.csv
│   └── plots/
│
├── report/
│   └── relatorio.pdf
│
└── README.md
```

---

## ✅ Checklist do Projeto

### Implementação:
- [ ] Carregar e explorar o dataset
- [ ] Implementar contadores exatos
- [ ] Implementar Csuros' Counter
- [ ] Implementar Lossy-Count
- [ ] Criar scripts de experimentos
- [ ] Implementar medições de performance

### Experimentos:
- [ ] Executar contadores exatos (baseline)
- [ ] Executar Csuros com múltiplas repetições
- [ ] Executar Lossy-Count com diferentes n
- [ ] Executar Lossy-Count com diferentes ε
- [ ] Medir tempos de execução
- [ ] Medir uso de memória

### Análise:
- [ ] Calcular erros absolutos e relativos
- [ ] Comparar top-N de cada método
- [ ] Criar tabelas comparativas
- [ ] Gerar gráficos de visualização
- [ ] Analisar trade-offs

### Relatório:
- [ ] Escrever introdução
- [ ] Escrever fundamentação teórica
- [ ] Documentar implementação
- [ ] Apresentar resultados
- [ ] Discutir resultados
- [ ] Escrever conclusões
- [ ] Adicionar referências
- [ ] Verificar limite de 10 páginas

### Entrega:
- [ ] Código comentado e organizado
- [ ] Relatório em PDF
- [ ] README com instruções
- [ ] Submeter até 22/12/2025

---

## 📚 Referências Úteis

### Artigos Científicos:
1. **Lossy Counting**: Manku, G. S., & Motwani, R. (2002). "Approximate frequency counts over data streams"
2. **Csuros' Counter**: Csuros, M. (2008). "Approximate counting with a floating-point counter"
3. **Survey on Streaming Algorithms**: Muthukrishnan, S. (2005). "Data streams: Algorithms and applications"

### Recursos Online:
- Kaggle Dataset: https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows/data
- Documentação dos algoritmos
- Tutoriais sobre data stream algorithms

---

## 💡 Dicas Importantes

1. **Comece pelos contadores exatos** - são a base de comparação
2. **Documente bem os parâmetros** usados em cada experimento
3. **Faça múltiplas execuções** dos métodos probabilísticos
4. **Use gráficos** para visualizar comparações
5. **Analise os trade-offs** - não existe método perfeito para tudo
6. **Seja crítico** na discussão - explique quando cada método é melhor
7. **Gerencie bem o tempo** - 22 de Dezembro está próximo!
8. **Teste o código incrementalmente** - não deixe tudo para o fim

---

## 🎓 Critérios de Avaliação (Estimados)

- **Implementação correta dos algoritmos** (40%)
- **Qualidade dos experimentos e análise** (30%)
- **Qualidade do relatório** (20%)
- **Apresentação dos resultados** (10%)

---

**Boa sorte com o projeto! 🚀**
