# Checklist - Trabalho de Grafos

## A. Para Grafos

### Requisitos Essenciais
- [x] (1) Criação do Grafo a partir da Lista de Adjacências
- [x] (2) Criação do Grafo a partir da Matriz de Adjacências
- [x] (3) Criação do Grafo a partir da Matriz de Incidência
- [x] (4) Conversão de matriz de adjacência para lista de Adjacências e vice-versa
- [X] **(5) Função que calcula o grau de cada vértice**
- [x] (6) Função que determina se dois vértices são adjacentes
- [x] (7) Função que determina o número total de vértices
- [x] (8) Função que determina o número total de arestas
- [x] (9) Inclusão de um novo vértice
- [x] (10) Exclusão de um vértice existente
- [x] (11) Função que determina se um grafo é conexo ou não
- [x] (13) Busca em Largura (BFS), a partir de um vértice específico
- [x] (14) Busca em Profundidade (DFS), com determinação de arestas de retorno
- [X] **(15) Determinação de articulações e blocos (biconectividade), com `lowpt`**

### Requisitos Opcionais
- [x] (12) Determinar se um grafo é bipartido (OPC)

## B. Para Digrafos

### Requisitos Essenciais
- [x] (16) Representação do Digrafo a partir da Matriz de Adjacências
- [x] (17) Representação do Digrafo a partir da Matriz de Incidência
- [x] (19) Busca em Largura (BFS)
- [x] (20) Busca em Profundidade (DFS), com tempos de entrada/saída e classificação completa das arestas

### Requisitos Opcionais
- [X] **(18) Determinação do Grafo subjacente (OPC)**

---

### Resumo do que falta implementar:
1.  **Função de Grau:** Criar um método que retorne o grau de um vértice.
2.  **Grafo Subjacente:** Criar uma função que transforme um dígrafo em seu grafo subjacente não direcionado.
3.  **Articulações e Blocos:** Implementar o algoritmo de biconectividade usando DFS e a função `lowpt`.