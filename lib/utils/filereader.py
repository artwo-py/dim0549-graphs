"""
Módulo:    Leitor de Arquivos
Descriçao: Funcionalidades para leitura e tratamento com arquivos.
"""
import os
import sys
from lib.core.graph import Grafo
from lib.core.graph_display import imprimir_lista_adj, imprimir_matriz_adj

def ler_grafo(caminho_arquivo, direcionado=False, renomear=None, ponderado=False):
    """
    Lê um arquivo de definição de grafo, cria o objeto Grafo e escreve
    suas representações (matriz e lista de adjacência) e graus em um arquivo.
    Se o parâmetro 'renomear' for fornecido, o grafo e seu respectivo arquivo de output 
    serão nomeados com esse valor
    """
    print(f"Lendo arquivo: {caminho_arquivo}")
    nome_arquivo = renomear if renomear else os.path.basename(caminho_arquivo)
    grafo = Grafo(direcionado, nome_arquivo, ponderado=ponderado)
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            primeira_linha = arquivo.readline().strip()

            if len(primeira_linha) > 1 and not primeira_linha.isdigit():
                partes = [p.strip() for p in primeira_linha.replace('(', '').replace(')', '').replace('{', '').replace('}', '').split(',')]
                if len(partes) >= 2 and partes[0] and partes[1]:
                    v1_id, v2_id = partes[0], partes[1]
                    peso = int(partes[2]) if len(partes) > 2 else None
                    grafo.adicionar_vertice(v1_id)
                    grafo.adicionar_vertice(v2_id)
                    grafo.adicionar_aresta(v1_id, v2_id, peso)

            for linha in arquivo:
                partes = [p.strip() for p in linha.replace('(', '').replace(')', '').replace('{', '').replace('}', '').split(',')]
                if len(partes) < 2 or not partes[0] or not partes[1]:
                    continue
                v1_id, v2_id = partes[0], partes[1]

                peso = int(partes[2]) if len(partes) > 2 else None

                grafo.adicionar_vertice(v1_id)
                grafo.adicionar_vertice(v2_id)
                grafo.adicionar_aresta(v1_id, v2_id, peso)

        graus = {}
        for vertice in grafo.vertices:
            id_vertice_str = str(vertice.id)
            if direcionado:
                graus[id_vertice_str] = [0, 0] 
            else:
                graus[id_vertice_str] = 0
        for aresta in grafo.arestas:
            v1_id_str, v2_id_str = str(aresta.v1.id), str(aresta.v2.id)
            if direcionado:
                graus[v2_id_str][0] += 1  
                graus[v1_id_str][1] += 1  
            else:
                graus[v1_id_str] += 1
                graus[v2_id_str] += 1

        with open("resultados.txt", "a", encoding='utf-8') as arquivo_resultados:
            stdout_original = sys.stdout
            sys.stdout = arquivo_resultados
            
            try:
                print(f"Arquivo: {nome_arquivo}\n")
                
                print("==== MATRIZ DE ADJACÊNCIA ====")
                imprimir_matriz_adj(grafo)
                
                print("\n==== LISTA DE ADJACÊNCIA ====")
                imprimir_lista_adj(grafo)
                
                print("\n==== GRAU DE CADA VÉRTICE NO GRAFO ====")
                if not grafo.direcionado:
                    for v, d in graus.items():
                        print(f"d({v}) = {d}")
                else:
                    for v, d in graus.items():
                        print(f"d+({v}) = {d[1]}, d-({v}) = {d[0]}")
                print("\n" + "="*40 + "\n")

            finally:
                sys.stdout = stdout_original

        return grafo
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        return None

def ler_diretorio(diretorio):
    """
    Lê todos os arquivos de grafos e digrafos de um diretório,
    processando cada um e limpando o arquivo de resultados no início.
    """
    with open("resultados.txt", "w", encoding='utf-8') as arquivo:
        arquivo.write("")

    try:
        arquivos = os.listdir(diretorio)
    except FileNotFoundError:
        print(f"ERRO: A pasta '{diretorio}' não foi encontrada.")
        return []

    lista_grafos = []
    for nome_arquivo in arquivos:
        caminho = os.path.join(diretorio, nome_arquivo)
        if os.path.isfile(caminho):
            nome_lower = nome_arquivo.lower()
            if nome_lower.startswith('grafo') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(caminho, direcionado=False)
                if grafo:
                    lista_grafos.append(grafo)
            elif nome_lower.startswith('digrafo') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(caminho, direcionado=True)
                if grafo:
                    lista_grafos.append(grafo)
            elif nome_lower.startswith('agm') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(caminho, direcionado=True, renomear='GRAFO_AGM', ponderado=True)
                if grafo:
                    lista_grafos.append(grafo) 
            elif nome_lower.startswith('hierholzer_digrafo') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(caminho, direcionado=True, renomear='DIGRAFO_HIERHOLZER')
                if grafo:
                    lista_grafos.append(grafo)
            elif nome_lower.startswith('hierholzer_grafo') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(caminho, direcionado=False, renomear='GRAFO_HIERHOLZER')
                if grafo:
                    lista_grafos.append(grafo)
    return lista_grafos
