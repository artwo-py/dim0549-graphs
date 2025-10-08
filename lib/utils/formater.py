from collections import defaultdict
import math

def _calcular_graus_entrada(grafo):
    """Calcula o grau de entrada para cada vértice em um grafo direcionado."""
    graus_entrada = defaultdict(int)
    for vertice in grafo.vertices:
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

    max_width = max(len(id) for id in ids) if ids else 1

    header = f"{' ' * max_width} |"
    for id in ids:
        header += f" {id:>{max_width}}"
    output.append(header)
    
    output.append(f"{'-' * (max_width + 2)}{'-' * (len(ids) * (max_width + 1))}")

    for i, linha in enumerate(grafo.matriz_adj):
        row_str = f"{ids[i]:>{max_width}} |"
        for val in linha:
            row_str += f" {val:>{max_width}}"
        output.append(row_str)
        
    return "\n".join(output)

def formatar_lista_adj(grafo):
    """Formata a lista de adjacência com vértices e vizinhos ordenados."""
    output = ["\n==== LISTA DE ADJACÊNCIA ===="]
    
    sorted_vertices = sorted(grafo.lista_adj.keys(), key=lambda v: str(v.id))

    if not sorted_vertices:
        output.append("Vazia.")
        return "\n".join(output)
        
    for vertice in sorted_vertices:
        vizinhos_ids = sorted([str(v.id) for v in grafo.lista_adj[vertice]])
        output.append(f"{vertice.id}: {vizinhos_ids}")
        
    return "\n".join(output)

def formatar_bipartido(grafo):
    """Verifica se o grafo é bipartido e formata a saída."""
    resultado = "Sim" if grafo.e_bipartido() else "Não"
    if grafo.direcionado:
        resultado += " (Verificação feita no grafo não-direcionado subjacente)"
    return f"\nBipartido: {resultado}"

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

    num_cols = 3
    max_len = max(len(s) for s in degree_strings) if degree_strings else 0
    
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

def _calcular_antecessores(grafo):
    """Helper para calcular os antecessores de todos os vértices em um dígrafo."""
    antecessores = {v: [] for v in grafo.vertices}
    for u, vizinhos in grafo.lista_adj.items():
        for v in vizinhos:
            antecessores[v].append(u)
    return antecessores

def formatar_adjacencias_por_vertice(grafo):
    """Formata os adjacentes (ou sucessores/antecessores) de cada vértice."""
    output = ["\n==== ADJACÊNCIAS DE CADA VÉRTICE ===="]
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))

    if not sorted_vertices:
        output.append("Vazio.")
        return "\n".join(output)

    if grafo.direcionado:
        antecessores = _calcular_antecessores(grafo)
        for v in sorted_vertices:
            sucessores_ids = sorted([str(s.id) for s in grafo.lista_adj[v]])
            antecessores_ids = sorted([str(a.id) for a in antecessores[v]])
            output.append(f"{v.id}: Sucessores: {sucessores_ids}, Antecessores: {antecessores_ids}")
    else:
        for v in sorted_vertices:
            adjacentes_ids = sorted([str(adj.id) for adj in grafo.lista_adj[v]])
            output.append(f"Adjacentes de {v.id}: {adjacentes_ids}")
            
    return "\n".join(output)

def formatar_conversoes(grafo):
    """Formata a demonstração de conversão entre matriz e lista."""
    output = ["\n==== DEMONSTRAÇÃO DE CONVERSÃO ===="]

    lista_adj_original = grafo.lista_adj
    matriz_adj_original = grafo.matriz_adj

    output.append("\n--- 1. Matriz de Adjacências -> Lista de Adjacências ---")
    grafo.sincronizar_lista_pela_matriz()
    output.append(formatar_lista_adj(grafo))

    grafo.lista_adj = lista_adj_original

    output.append("\n--- 2. Lista de Adjacências -> Matriz de Adjacências ---\n")
    grafo.sincronizar_matriz_pela_lista()
    output.append(formatar_matriz_adj(grafo))

    grafo.lista_adj = lista_adj_original
    grafo.matriz_adj = matriz_adj_original
    
    return "\n".join(output)

def gerar_relatorio_completo(grafo):
    """Gera um relatório completo e formatado para um único grafo."""
    report = []
    report.append(f"\nArquivo: {grafo.nome_arquivo}\n")
    report.append(formatar_matriz_adj(grafo))
    report.append(formatar_lista_adj(grafo))
    report.append(formatar_conversoes(grafo))
    report.append(formatar_graus(grafo))
    report.append(formatar_adjacencias_por_vertice(grafo))
    report.append(formatar_bipartido(grafo))
    return "\n".join(report)