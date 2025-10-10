from collections import defaultdict
import math
import os

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

def formatar_eh_conexo(grafo):
    """Formata a resposta do grafo ser conexo ou não"""
    resultado = "Sim" if grafo.eh_conexo() else "Não"
    obs = "(fortemente conexo)" if grafo.direcionado else ""
    return f"\nCONEXO?  {resultado} {obs}\n"

def gerar_relatorio_completo(grafo):
    """Gera um relatório completo e formatado para um único grafo."""
    report = []
    report.append(f"Arquivo: {grafo.nome_arquivo}")
    report.append(formatar_eh_conexo(grafo))
    report.append(formatar_matriz_adj(grafo))
    report.append(formatar_lista_adj(grafo))
    report.append(formatar_graus(grafo))
    return "\n".join(report)


def gerar_arquivos_grafos_por_matriz(directory, subdirectory):
    """
    Lê os arquivos de matriz de incidencia no diretório 'data/matrix_incidencia/' e 
    gera os arquivos de lista de incidencia (formatado como DIGRAFO_X_POR_MATRIZ.TXT 
    ou GRAFO_X_POR_MATRIZ.TXT) na pasta 'data/matrix_incidencia'.
    """
    matrix_dir = os.path.join(directory, subdirectory)
    if not os.path.exists(matrix_dir):
        print(f"Erro: o diretório '{matrix_dir}' não foi encontrado.")
        return

    arquivos = sorted([f for f in os.listdir(matrix_dir) if f.lower().endswith('.txt')])

    for arquivo in arquivos:
        caminho = os.path.join(matrix_dir, arquivo)
        base_name = os.path.splitext(arquivo)[0]
        nome_saida = f"{base_name}_POR_MATRIZ_INCIDENCIA.TXT"

        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                linhas = [linha.strip() for linha in f if linha.strip()]

            if not linhas:
                print(f"Aviso: '{arquivo}' está vazio. Pulando.")
                continue

            primeira_linha = linhas[0].replace(',', ' ').split()
            cabecalho_tem_numeros = all(valor.lstrip('-').isdigit() for valor in primeira_linha)

            if cabecalho_tem_numeros:
                quant_vertices = len(primeira_linha)
                dados = linhas[1:]
            else:
                dados = linhas
                # Descobrindo o número de colunas (vértices)
                exemplo = dados[0].replace(',', ' ').split()
                if exemplo[0][0].isalpha():
                    quant_vertices = len(exemplo) - 1
                else:
                    quant_vertices = len(exemplo)

            arestas = []

            for index, linha in enumerate(dados, start=1):
                partes = linha.replace(',', ' ').split()

                # Verifica se o primeiro valor é rótulo (ex: "a_1")
                if partes[0][0].isalpha():
                    valores = partes[1:]
                else:
                    valores = partes

                if len(valores) != quant_vertices:
                    print(f"Aviso: linha {index} de '{arquivo}' com número incorreto de colunas. Pulando...")
                    continue

                try:
                    nums = [int(v) for v in valores]
                except ValueError:
                    print(f"Aviso: linha {index} contém valor não numérico. Pulando...")
                    continue

                origem = None
                destino = None
                for j, v in enumerate(nums, start=1):
                    if v == -1:
                        origem = j
                    elif v == 1:
                        destino = j

                if origem is not None and destino is not None:
                    arestas.append((origem, destino))
                else:
                    print(f"Aviso: linha {index} sem -1 e 1 válidos. Pulando.")

            # Gerando arquivo de saída
            caminho_saida = os.path.join(directory, nome_saida)
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(f"{quant_vertices}\n")
                for origem, destino in arestas:
                    f.write(f"{origem},{destino}\n")

            print(f"Gerado: {caminho_saida}")

        except Exception as e:
            print(f"Erro ao processar '{arquivo}': {e}")