import os
from .core.graph import Grafo

def criar_grafo_de_matriz_incidencia(caminho_arquivo):
    """
    (3) Criação do Grafo a partir da Matriz de Incidência

    Args:
        caminho_arquivo (str): o caminho para o arquivo .txt
    Returns:
        Grafo: o objeto Grafo construído
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

    rotulos_vertices = linhas[0].strip().split()
    
    if not rotulos_vertices:
        print("Erro: Não foi possível identificar os rótulos dos vértices na primeira linha.")
        return Grafo()

    nome_arquivo = caminho_arquivo.split('/')[-1].split('.')[0]

    grafo = Grafo(direcionado=False, nome_arquivo=nome_arquivo)

    for rotulo in rotulos_vertices:
        grafo.adicionar_vertice(rotulo)
    
    # Processar as linhas da matriz de incidência
    for linha in linhas[1:]:
        partes = linha.strip().split()
        if not partes:
            continue # Ignora linhas vazias

        # o primeiro elemento é o rótulo da aresta, os demais são os valores da matriz
        # ID_aresta = partes[0]
        incidencia = [int(val) for val in partes[1:]]

        if len(incidencia) != len(grafo.get_vertices()):
            print(f"Alerta: Linha da aresta incompleta ou mal formatada: {linha.strip()}")
            continue

        vertices_incidentes = []
        for i, valor in enumerate(incidencia):
            if valor == 1:
                vertices_incidentes.append(grafo.get_vertices()[i].id)

        # para um grafo não-direcionado simples, aresta deve ter exatamente dois '1's
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


def criar_digrafo_de_matriz_incidencia(caminho_arquivo):
    """
    (17) Representação do Digrafo a partir da Matriz de Incidência.
    
    Info: Lê a Matriz de Incidência de um arquivo e constrói um objeto Grafo
          (Direcionado). Assume que:
          - A primeira linha contém os rótulos dos vértices.
          - As linhas seguintes contêm o rótulo do arco e os valores de incidência.
          - REGRA ATUALIZADA: -1 (saída do vértice), 1 (entrada no vértice).
    
    Args:
        caminho_arquivo (str): o caminho para o arquivo .txt.

    Returns:
        Grafo: o objeto Grafo direcionado construído.
    """
    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    if not linhas:
        print("Erro: O arquivo está vazio.")
        return Grafo(direcionado=True)

    rotulos_vertices = linhas[0].strip().split()
    
    if not rotulos_vertices:
        print("Erro: Não foi possível identificar os rótulos dos vértices na primeira linha.")
        return Grafo(direcionado=True)
    
    nome_arquivo = caminho_arquivo.split('/')[-1].split('.')[0]

    grafo = Grafo(direcionado=True, nome_arquivo=nome_arquivo)

    for rotulo in rotulos_vertices:
        grafo.adicionar_vertice(rotulo)

    for linha in linhas[1:]:
        partes = linha.strip().split()
        if not partes:
            continue

        id_arco = partes[0]
        try:
            incidencia = [int(val) for val in partes[1:]]
        except ValueError:
            print(f"Alerta: Valores não numéricos na linha do arco {id_arco}. Ignorando...")
            continue

        if len(incidencia) != grafo.num_vertices():
            print(f"Alerta: Arco {id_arco} incompleto ou mal formatado. Ignorando...")
            continue

        vertice_saida_id = None
        vertice_entrada_id = None
        
        for i, valor in enumerate(incidencia):
            vertice_atual_id = grafo.get_vertices()[i].id
      
            if valor == -1:
                if vertice_saida_id is not None:
                    print(f"Alerta: Arco {id_arco} tem mais de um valor '-1'. Tratando como erro/hiper-aresta. Ignorando...")
                    vertice_saida_id = None
                    break
                vertice_saida_id = vertice_atual_id
            

            elif valor == 1:
                if vertice_entrada_id is not None:
                    print(f"Alerta: Arco {id_arco} tem mais de um valor '1'. Tratnado como erro/hiper-aresta. Ignorando...")
                    vertice_entrada_id = None
                    break
                vertice_entrada_id = vertice_atual_id
        
        
        if vertice_saida_id is not None and vertice_entrada_id is not None:
            grafo.adicionar_aresta(vertice_saida_id, vertice_entrada_id)
        
        elif vertice_saida_id is None and vertice_entrada_id is None:
              print(f"Alerta: Arco {id_arco} não possui '1' e '-1'. Ignorando...")
        else:
              print(f"Alerta: Arco {id_arco} não tem par completo (1 e -1). Ignorando...")
            
    return grafo



def escrever_grafo_em_arquivo(grafo, nome_arquivo):
    """
    Escreve a estrutura do grafo em um arquivo de texto no formato:
    - Primeira linha: número de vértices
    - Linhas seguintes: arestas no formato "v1,v2"
    """
    try:
        with open(nome_arquivo, 'w') as f:
            num_vertices = grafo.num_vertices()
            f.write(f"{num_vertices}\n")

            arestas_escritas = set() # uado para evitar duplicatas em grafos
            
            for aresta in grafo.get_arestas():
                v1_id = aresta.v1.id
                v2_id = aresta.v2.id
                
                # escrever apenas uma vez cada par "v1,v2"
                if not grafo.direcionado:
                    # cria uma chave canônica (ordenada) para a aresta
                    chave_aresta = tuple(sorted((v1_id, v2_id)))
                    
                    if chave_aresta in arestas_escritas:
                        continue # já escreveu esta aresta
                    
                    arestas_escritas.add(chave_aresta)
                    
                f.write(f"{v1_id},{v2_id}\n")
                
        print(f"Grafo escrito com sucesso no arquivo '{nome_arquivo}'.")

    except Exception as e:
        print(f"Erro ao escrever o grafo no arquivo: {e}")


def escrever_digrafo_grafo_em_arquivo_a_partir_de_matriz(directory, subdirectory):
    caminho_completo = os.path.join(directory, subdirectory)
    arquivos = []
    try:
        for nome_arquivo in os.listdir(caminho_completo):
            if nome_arquivo.endswith(".txt"):
                arquivos.append(os.path.join(caminho_completo, nome_arquivo))
    except FileNotFoundError:
        print(f"Erro: Diretório '{caminho_completo}' não encontrado.")
    for caminho_arquivo in arquivos:
        nome_arquivo_completo = os.path.basename(caminho_arquivo)
        nome_base = os.path.splitext(nome_arquivo_completo)[0]
        
        grafo = None
        
        # Diferenciar Grafo e Dígrafo
        if nome_base.upper().startswith('DIGRAFO_'):
            print(f"Processando Dígrafo (Matriz Incidência): {nome_arquivo_completo}")
            grafo = criar_digrafo_de_matriz_incidencia(caminho_arquivo)
            nome_saida_base = nome_base.replace('_MATRIZ_INCIDENCIA', '_POR_MATRIZ_INCIDENCIA')
            nome_saida = os.path.join(directory, f"{nome_saida_base}.txt")
            
        elif nome_base.upper().startswith('GRAFO_'):
            print(f"Processando Grafo (Matriz Incidência): {nome_arquivo_completo}")
            grafo = criar_grafo_de_matriz_incidencia(caminho_arquivo)
            nome_saida_base = nome_base.replace('_MATRIZ_INCIDENCIA', '_POR_MATRIZ_INCIDENCIA')
            nome_saida = os.path.join(directory, f"{nome_saida_base}.txt")
        
        else:
            print(f"Alerta: O arquivo {nome_arquivo_completo} não segue o padrão 'GRAFO_' ou 'DIGRAFO_'. Ignorando...")
            continue 

        # Escrever o Grafo/Dígrafo no arquivo de saída
        if grafo and grafo.num_vertices() > 0:
            escrever_grafo_em_arquivo(grafo, nome_saida)
        elif grafo:
            print(f"Alerta: O arquivo {nome_arquivo_completo} resultou em um grafo vazio. Ignorando a escrita.")
        else:
            print(f"Erro: Falha na criação do grafo a partir de {nome_arquivo_completo}.")