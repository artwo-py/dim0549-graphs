from .classes import Grafo
from .rendering import renderizar_grafo

# Definicao: uma matriz A=[a_ij] de dimensão m x n é denominada 
# Matriz de Incidência de um grafo G=(V,A) quando:
#  - a_ij = 1, se o vértice v_j é extremo da aresta a_i
#  - a_ij = 0, caso contrário

def criar_grafo_de_matriz_incidencia(caminho_arquivo):
    """
    (3) Criação do Grafo a partir da Matriz de Incidência

    Args:
        caminho_arquivo (str): o caminho para o arquivo .txt.

    Returns:
        Grafo: o objeto Grafo construído.
    """

    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    if not linhas:
        print("Erro: O arquivo está vazio.")
        return Grafo()

    # Obter os rótulos dos vértices (primeira linha)
    rotulos_vertices = linhas[0].strip().split()
    
    if not rotulos_vertices:
        print("Erro: Não foi possível identificar os rótulos dos vértices na primeira linha.")
        return Grafo()

    nome_arquivo = caminho_arquivo.replace('/', '-').replace('.', '-').replace('\\', '-').split("-")[1]
    grafo = Grafo(direcionado=False, nome_arquivo=nome_arquivo)

    # Adiciona os vértices ao grafo
    for rotulo in rotulos_vertices:
        grafo.adicionar_vertice(rotulo)
    
    # Processar as linhas da matriz de incidência (arestas)
    for linha in linhas[1:]:
        partes = linha.strip().split()
        if not partes:
            continue # Ignora linhas vazias

        # o primeiro elemento é o rótulo da aresta, os demais são os valores da matriz
        # ID_aresta = partes[0]
        incidencia = [int(val) for val in partes[1:]]

        # verifica se o número de colunas de incidência corresponde ao número de vértices
        if len(incidencia) != len(grafo.get_vertices()):
            print(f"Alerta: Linha da aresta incompleta ou mal formatada: {linha.strip()}")
            continue

        vertices_incidentes = []
        for i, valor in enumerate(incidencia):
            if valor == 1:
                # o índice 'i' corresponde à posição do vértice na lista 'rotulos_vertices' e 'vertices'
                vertices_incidentes.append(grafo.get_vertices()[i].id)

        # para um grafo não-direcionado simples, uma aresta deve ter exatamente dois '1's
        if len(vertices_incidentes) == 2:
            v1_id, v2_id = vertices_incidentes[0], vertices_incidentes[1]
            # usa os IDs de string para adicionar a aresta
            grafo.adicionar_aresta(v1_id, v2_id)
        elif len(vertices_incidentes) > 2:
            print(f"Alerta: Aresta com mais de 2 vértices incidentes (possível Hiper-aresta ou erro): {partes[0]}. Ignorando.")
        elif len(vertices_incidentes) < 2:
            if len(vertices_incidentes) == 1:
                 print(f"Alerta: Aresta {partes[0]} possui apenas um vértice incidente. Ignorando.")
            else:
                print(f"Alerta: Aresta {partes[0]} não possui vértices incidentes. Ignorando.")


    return grafo


def escrever_grafo_em_arquivo(grafo, nome_arquivo):
    """
    Escreve a estrutura do grafo em um arquivo de texto no formato:
    - Primeira linha: número de vértices
    - Linhas seguintes: arestas no formato "v1,v2"
    """
    try:
        with open(nome_arquivo, 'w') as f:
            # escrever o número de vértices
            num_vertices = grafo.num_vertices()
            f.write(f"{num_vertices}\n")

            # escrever as arestas
            arestas_escritas = set() # uado para evitar duplicatas em grafos não-direcionados
            
            for aresta in grafo.get_arestas():
                v1_id = aresta.v1.id
                v2_id = aresta.v2.id
                
                # como o grafo for não-direcionado, precisamos garantir que cada par (v1,v2) 
                # seja escrito apenas uma vez para manter o formato simples "v1,v2".
                if not grafo.direcionado:
                    # cria uma chave canônica (ordenada) para a aresta
                    chave_aresta = tuple(sorted((v1_id, v2_id)))
                    
                    if chave_aresta in arestas_escritas:
                        continue # Já escrevemos esta aresta
                    
                    arestas_escritas.add(chave_aresta)
                    
                # escreve a aresta no formato v1,v2
                f.write(f"{v1_id},{v2_id}\n")
                
        print(f"Grafo escrito com sucesso no arquivo '{nome_arquivo}'.")

    except Exception as e:
        print(f"Erro ao escrever o grafo no arquivo: {e}")



