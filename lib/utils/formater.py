# lib/analysis.py

from collections import defaultdict
import math

def _calcular_graus_entrada(grafo):
    """Calcula o grau de entrada para cada vértice em um grafo direcionado."""
    graus_entrada = defaultdict(int)
    for vertice in grafo.vertices:
        # Garante que todos os vértices estejam no dicionário, mesmo com grau de entrada zero
        graus_entrada[vertice] 
    
    for vizinhos in grafo.lista_adj.values():
        for vizinho in vizinhos:
            graus_entrada[vizinho] += 1
    return graus_entrada

def formatar_matriz_adj(grafo):
    """Formata a matriz de adjacência com alinhamento dinâmico."""
    output = ["==== MATRIZ DE ADJACÊNCIA ===="]
    ids = [str(v.id) for v in grafo.vertices]
    
    if not ids:
        output.append("Vazia.")
        return "\n".join(output)

    # Calcula o espaçamento necessário com base no ID de vértice mais longo
    max_width = max(len(id) for id in ids) if ids else 1

    # Formata o cabeçalho
    header = f"{' ' * max_width} |"
    for id in ids:
        header += f" {id:>{max_width}}"
    output.append(header)
    
    # Adiciona a linha separadora
    output.append(f"{'-' * (max_width + 2)}{'-' * (len(ids) * (max_width + 1))}")

    # Formata cada linha da matriz
    for i, linha in enumerate(grafo.matriz_adj):
        row_str = f"{ids[i]:>{max_width}} |"
        for val in linha:
            row_str += f" {val:>{max_width}}"
        output.append(row_str)
        
    return "\n".join(output)

def formatar_lista_adj(grafo):
    """Formata a lista de adjacência com vértices e vizinhos ordenados."""
    output = ["\n==== LISTA DE ADJACÊNCIA ===="]
    
    # Ordena os vértices para uma exibição consistente
    sorted_vertices = sorted(grafo.lista_adj.keys(), key=lambda v: str(v.id))

    if not sorted_vertices:
        output.append("Vazia.")
        return "\n".join(output)
        
    for vertice in sorted_vertices:
        # Ordena os vizinhos para uma exibição consistente
        vizinhos_ids = sorted([str(v.id) for v in grafo.lista_adj[vertice]])
        output.append(f"{vertice.id}: {vizinhos_ids}")
        
    return "\n".join(output)

def formatar_graus(grafo):
    """Formata os graus dos vértices em múltiplas colunas."""
    output = ["\n==== GRAU DE CADA VÉRTICE NO GRAFO ===="]
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))

    if not sorted_vertices:
        output.append("Vazio.")
        return "\n".join(output)

    degree_strings = []
    if grafo.direcionado:
        graus_entrada = _calcular_graus_entrada(grafo)
        for v in sorted_vertices:
            grau_saida = len(grafo.lista_adj[v])
            grau_entrada = graus_entrada[v]
            degree_strings.append(f"d+({v.id}) = {grau_saida}, d-({v.id}) = {grau_entrada}")
    else:
        for v in sorted_vertices:
            grau = len(grafo.lista_adj[v])
            degree_strings.append(f"d({v.id}) = {grau}")

    # Formatação em colunas
    num_cols = 3
    max_len = max(len(s) for s in degree_strings) if degree_strings else 0
    
    # Preenche as strings para que todas tenham o mesmo comprimento para alinhamento
    padded_strings = [s.ljust(max_len) for s in degree_strings]
    
    num_rows = math.ceil(len(padded_strings) / num_cols)
    
    for i in range(num_rows):
        row_parts = []
        for j in range(num_cols):
            index = i + j * num_rows
            if index < len(padded_strings):
                row_parts.append(padded_strings[index])
        output.append("   ".join(row_parts))
        
    return "\n".join(output)

def gerar_relatorio_completo(grafo):
    """Gera um relatório completo e formatado para um único grafo."""
    report = []
    report.append(f"Arquivo: {grafo.nome_arquivo}")
    report.append(formatar_matriz_adj(grafo))
    report.append(formatar_lista_adj(grafo))
    report.append(formatar_graus(grafo))
    return "\n".join(report)