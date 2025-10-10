import os
import sys
from lib.core.graph import Grafo
from lib.core.graph_display import imprimir_lista_adj, imprimir_matriz_adj

def ler_grafo(caminho_arquivo, direcionado=False):
    """
    Lê um arquivo de definição de grafo, cria o objeto Grafo e escreve
    suas representações (matriz e lista de adjacência) e graus em um arquivo.
    """
    print(f"Lendo arquivo: {caminho_arquivo}")
    nome_arquivo = os.path.basename(caminho_arquivo)
    grafo = Grafo(direcionado, nome_arquivo)
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            arquivo.readline()  # Pula o cabeçalho
            for linha in arquivo:
                partes = [p.strip() for p in linha.split(',')]
                if len(partes) < 2 or not partes[0] or not partes[1]:
                    continue
                v1_id, v2_id = partes[0], partes[1]
                grafo.adicionar_vertice(v1_id)
                grafo.adicionar_vertice(v2_id)
                grafo.adicionar_aresta(v1_id, v2_id)

        # Calcula os graus de cada vértice
        graus = {}
        for vertice in grafo.vertices:
            id_vertice_str = str(vertice.id)
            if direcionado:
                graus[id_vertice_str] = [0, 0]  # [grau_entrada, grau_saida]
            else:
                graus[id_vertice_str] = 0
        for aresta in grafo.arestas:
            v1_id_str, v2_id_str = str(aresta.v1.id), str(aresta.v2.id)
            if direcionado:
                graus[v2_id_str][0] += 1  # Grau de entrada de v2
                graus[v1_id_str][1] += 1  # Grau de saída de v1
            else:
                graus[v1_id_str] += 1
                graus[v2_id_str] += 1

        # Abre o arquivo de resultados para adicionar as informações do grafo
        with open("resultados.txt", "a", encoding='utf-8') as arquivo_resultados:
            # Armazena a saída padrão original e a redireciona para o arquivo
            stdout_original = sys.stdout
            sys.stdout = arquivo_resultados
            
            try:
                print(f"Arquivo: {nome_arquivo}\n")
                
                # Usa a nova função para imprimir a matriz de adjacência
                print("==== MATRIZ DE ADJACÊNCIA ====")
                imprimir_matriz_adj(grafo)
                
                # Usa a nova função para imprimir a lista de adjacência
                print("\n==== LISTA DE ADJACÊNCIA ====")
                imprimir_lista_adj(grafo)
                
                # Imprime os graus calculados
                print("\n==== GRAU DE CADA VÉRTICE NO GRAFO ====")
                if not grafo.direcionado:
                    for v, d in graus.items():
                        print(f"d({v}) = {d}")
                else:
                    for v, d in graus.items():
                        # d[1] é grau de saída, d[0] é grau de entrada
                        print(f"d+({v}) = {d[1]}, d-({v}) = {d[0]}")
                print("\n" + "="*40 + "\n")

            finally:
                # Restaura a saída padrão original para o console
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
    # Limpa o arquivo de resultados antes de começar a processar os novos arquivos
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
    return lista_grafos
