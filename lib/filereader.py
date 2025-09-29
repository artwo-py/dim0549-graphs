import os
from .matrixbuilder import construir_matriz_adj, lista_para_matriz
from .classes import Vertice, Grafo

def ler_grafo(caminho_arquivo, direcionado=False):
        print(f"Lendo arquivo: {caminho_arquivo}")
        vertices = []
        nome_arquivo = caminho_arquivo.replace('/', '-').replace('.', '-').split("-")[1]
        grafo = Grafo(direcionado, nome_arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                ordem_grafo = int(arquivo.readline())
                matriz_adj = construir_matriz_adj(ordem_grafo)

                for linha in arquivo:
                    partes = [p.strip() for p in linha.split(',')]
                    
                    if len(partes) < 2 or not partes[0] or not partes[1]:
                        continue

                    v1, v2 = partes[0], partes[1]

                    if v1 not in vertices:
                        vertices.append(v1)
                        grafo.adicionar_vertice(v1)
                    if v2 not in vertices:
                        vertices.append(v2)
                        grafo.adicionar_vertice(v2)

                    i = vertices.index(v1)
                    j = vertices.index(v2)

                    matriz_adj[i][j] = 1
                    if not direcionado:
                        matriz_adj[j][i] = 1
            
                for i in range(ordem_grafo):
                    for j in range(ordem_grafo):
                        if direcionado:
                            if matriz_adj[i][j] == 1:
                                grafo.adicionar_aresta(grafo.vertices[i], grafo.vertices[j], direcionado)
                        else:
                            if j>=i:
                                if matriz_adj[i][j] == 1:
                                    grafo.adicionar_aresta(grafo.vertices[i], grafo.vertices[j], direcionado)

            with open("resultados.txt", "a") as arquivo:
                arquivo.write(f"Arquivo: {caminho_arquivo}\n")
                arquivo.write("==== MATRIZ DE ADJACÊNCIA ==== \n")
                arquivo.write("   " + " ".join(vertices)+"\n")
                for rotulo, linha in zip(vertices, matriz_adj):
                        arquivo.write(f"{rotulo:>2} " + " ".join(map(str, linha))+"\n")

                lista_adj = {}

                for i in range(ordem_grafo):
                        for j in range(ordem_grafo):
                            if direcionado:
                                if matriz_adj[i][j] == 1:
                                    lista_adj.setdefault(vertices[i], [])
                                    lista_adj.setdefault(vertices[j], [])

                                    lista_adj[vertices[i]].append(vertices[j])
                                    
                            else:
                                if j >=i:
                                    if matriz_adj[i][j] == 1:
                                        lista_adj.setdefault(vertices[i], [])
                                        lista_adj.setdefault(vertices[j], [])

                                        lista_adj[vertices[i]].append(vertices[j])
                                        lista_adj[vertices[j]].append(vertices[i])

                adjacencias = lista_adj.items()

                arquivo.write("\n==== MATRIZ DE ADJACÊNCIA -> LISTA DE ADJACÊNCIA ====")
                for adjacencias in adjacencias:
                    arquivo.write(f"\n{adjacencias[0]}: {adjacencias[1]}")
                arquivo.write("\n")
                
                matriz_reconstruida, vertices_matriz_rec = lista_para_matriz(lista_adj)
                
                arquivo.write("\n==== LISTA DE ADJACÊNCIA -> MATRIZ DE ADJACÊNCIA ==== \n")
                arquivo.write("   " + " ".join(vertices_matriz_rec)+"\n")
                
                for v, row in zip(vertices_matriz_rec, matriz_reconstruida):
                    arquivo.write(f"{v:>2} " + " ".join(map(str, row))+"\n")
                
                graus = {}

                for vertice in grafo.vertices:
                    if direcionado:
                        graus[str(vertice.id)] = [0, 0]
                    else:
                        graus[str(vertice.id)] = 0
                    
                    for aresta in grafo.arestas:
                        if direcionado:
                            if aresta.v1.id == vertice.id:
                                graus[str(vertice.id)][0] -= 1
                            
                            if aresta.v2.id == vertice.id:
                                graus[str(vertice.id)][1] += 1

                        else:
                            if aresta.v1.id == vertice.id or aresta.v2.id == vertice.id:
                                graus[str(vertice.id)] += 1
                
                arquivo.write("\n==== GRAU DE CADA VÉRTICE NO GRAFO ==== \n")

                if not grafo.direcionado:
                    for v, d in graus.items():
                        arquivo.write(f"d({v}) = {d}\n")
                    arquivo.write("\n")
                
                else:
                    for v, d in graus.items():
                        arquivo.write(f"d-({v}) = {d[0]}, d+({v}) = {d[1]}\n")
                    arquivo.write("\n")

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
                lista_grafos.append(grafo)
            
            elif nome_arquivo.lower().startswith('digrafo') and nome_arquivo.lower().endswith('.txt'):
                grafo = ler_grafo(caminho, True)
                lista_grafos.append(grafo)
    
    return lista_grafos

            
