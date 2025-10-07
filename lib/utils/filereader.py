import os
from lib.core.graph import Grafo

def ler_grafo(caminho_arquivo, direcionado=False):
        print(f"Lendo arquivo: {caminho_arquivo}")
        nome_arquivo = os.path.basename(caminho_arquivo)
        grafo = Grafo(direcionado, nome_arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                arquivo.readline() 
                for linha in arquivo:
                    partes = [p.strip() for p in linha.split(',')]
                    if len(partes) < 2 or not partes[0] or not partes[1]:
                        continue
                    v1_id, v2_id = partes[0], partes[1]
                    grafo.adicionar_vertice(v1_id)
                    grafo.adicionar_vertice(v2_id)
                    grafo.adicionar_aresta(v1_id, v2_id)
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
                arquivo_resultados.write(f"Arquivo: {caminho_arquivo}\n")
                
                arquivo_resultados.write("==== MATRIZ DE ADJACÊNCIA ====\n")
                ids_vertices = [v.id for v in grafo.vertices]
                header = "  " + " ".join(map(str, ids_vertices))
                arquivo_resultados.write(header + "\n")
                for i, linha in enumerate(grafo.matriz_adj):
                    arquivo_resultados.write(f"{ids_vertices[i]}| " + " ".join(map(str, linha)) + "\n")
                    
                arquivo_resultados.write("\n==== LISTA DE ADJACÊNCIA ====\n")
                for vertice, vizinhos in grafo.lista_adj.items():
                    vizinhos_ids = [v.id for v in vizinhos]
                    arquivo_resultados.write(f"{vertice.id}: {vizinhos_ids}\n")
                    
                arquivo_resultados.write("\n==== GRAU DE CADA VÉRTICE NO GRAFO ====\n")
                if not grafo.direcionado:
                    for v, d in graus.items():
                        arquivo_resultados.write(f"d({v}) = {d}\n")
                else:
                    for v, d in graus.items():
                        arquivo_resultados.write(f"d+({v}) = {d[1]}, d-({v}) = {d[0]}\n")
                arquivo_resultados.write("\n\n")
            return grafo
        except Exception as e:
            print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")

def ler_diretorio(diretorio):
    with open("resultados.txt", "w") as arquivo:
        arquivo.write("")
    try:
        arquivos = os.listdir(diretorio)
    except FileNotFoundError:
        print(f"ERRO: A pasta '{diretorio}' não foi encontrada.")
        return
    lista_grafos = []
    for nome_arquivo in arquivos:
        caminho = os.path.join(diretorio, nome_arquivo)
        if os.path.isfile(caminho):
            if nome_arquivo.lower().startswith('grafo') and nome_arquivo.lower().endswith('.txt'):
                grafo = ler_grafo(caminho)
                if grafo: lista_grafos.append(grafo)
            elif nome_arquivo.lower().startswith('digrafo') and nome_arquivo.lower().endswith('.txt'):
                grafo = ler_grafo(caminho, True)
                if grafo: lista_grafos.append(grafo)
    return lista_grafos