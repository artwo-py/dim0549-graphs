import os
from lib.core.graph import Grafo

def criar_grafo_de_matriz_incidencia(caminho_arquivo):
    """
    (3) Criação do Grafo a partir da Matriz de Incidência
    """
    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    if not linhas: return Grafo()

    rotulos_vertices = linhas[0].strip().split()
    if not rotulos_vertices: return Grafo()

    nome_arquivo = os.path.basename(caminho_arquivo)
    grafo = Grafo(direcionado=False, nome_arquivo=nome_arquivo)

    for rotulo in rotulos_vertices:
        grafo.adicionar_vertice(rotulo)
    
    for linha in linhas[1:]:
        partes = linha.strip().split()
        if not partes: continue

        id_aresta = partes[0]
        incidencia = [int(val) for val in partes[1:]]

        # CORREÇÃO: Removido o len() extra. Compara o tamanho da lista com o número de vértices.
        if len(incidencia) != grafo.num_vertices():
            print(f"Alerta: Linha da aresta incompleta ou mal formatada: {linha.strip()}")
            continue

        vertices_incidentes = []
        for i, valor in enumerate(incidencia):
            if valor == 1:
                # CORREÇÃO: Acesso direto ao atributo 'vertices'
                vertices_incidentes.append(grafo.vertices[i].id)

        if len(vertices_incidentes) == 2:
            v1_id, v2_id = vertices_incidentes[0], vertices_incidentes[1]
            grafo.adicionar_aresta(v1_id, v2_id)
        elif len(vertices_incidentes) == 1:
            print(f"Alerta: Aresta {id_aresta} possui apenas um vértice incidente. Ignorando.")
        elif len(vertices_incidentes) > 2:
            print(f"Alerta: Aresta {id_aresta} com mais de 2 vértices (Hiper-aresta). Ignorando.")

    return grafo


def criar_digrafo_de_matriz_incidencia(caminho_arquivo):
    """
    (17) Representação do Digrafo a partir da Matriz de Incidência.
    """
    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None

    if not linhas: return Grafo(direcionado=True)

    rotulos_vertices = linhas[0].strip().split()
    if not rotulos_vertices: return Grafo(direcionado=True)
    
    nome_arquivo = os.path.basename(caminho_arquivo)
    grafo = Grafo(direcionado=True, nome_arquivo=nome_arquivo)

    for rotulo in rotulos_vertices:
        grafo.adicionar_vertice(rotulo)

    for linha in linhas[1:]:
        partes = linha.strip().split()
        if not partes: continue

        id_arco = partes[0]
        incidencia = [int(val) for val in partes[1:]]

        # CORREÇÃO: Removido o len() extra.
        if len(incidencia) != grafo.num_vertices():
            print(f"Alerta: Arco {id_arco} incompleto ou mal formatado. Ignorando...")
            continue

        vertice_saida_id = None
        vertice_entrada_id = None
        
        for i, valor in enumerate(incidencia):
            # CORREÇÃO: Acesso direto ao atributo 'vertices'
            vertice_atual_id = grafo.vertices[i].id
      
            if valor == -1:
                if vertice_saida_id is not None:
                    vertice_saida_id = None; break
                vertice_saida_id = vertice_atual_id
            
            elif valor == 1:
                if vertice_entrada_id is not None:
                    vertice_entrada_id = None; break
                vertice_entrada_id = vertice_atual_id
        
        if vertice_saida_id and vertice_entrada_id:
            grafo.adicionar_aresta(vertice_saida_id, vertice_entrada_id)
        elif not vertice_saida_id and not vertice_entrada_id:
            print(f"Alerta: Arco {id_arco} não possui '1' ou '-1'. Ignorando...")
        else:
            print(f"Alerta: Arco {id_arco} não tem par completo (1 e -1). Ignorando...")
            
    return grafo

def escrever_grafo_em_arquivo(grafo, nome_arquivo):
    """
    Escreve a estrutura do grafo em um arquivo de texto.
    """
    try:
        with open(nome_arquivo, 'w') as f:
            f.write(f"{grafo.num_vertices()}\n")
            arestas_escritas = set()
            
            # CORREÇÃO: Acesso direto ao atributo 'arestas'
            for aresta in grafo.arestas:
                v1_id = aresta.v1.id
                v2_id = aresta.v2.id
                
                if not grafo.direcionado:
                    chave_aresta = tuple(sorted((v1_id, v2_id)))
                    if chave_aresta in arestas_escritas: continue
                    arestas_escritas.add(chave_aresta)
                    
                f.write(f"{v1_id},{v2_id}\n")
                
        print(f"Grafo escrito com sucesso no arquivo '{nome_arquivo}'.")
    except Exception as e:
        print(f"Erro ao escrever o grafo no arquivo: {e}")


def escrever_digrafo_grafo_em_arquivo_a_partir_de_matriz(directory, subdirectory):
    caminho_completo = os.path.join(directory, subdirectory)
    try:
        arquivos = [os.path.join(caminho_completo, f) for f in os.listdir(caminho_completo) if f.endswith(".txt")]
    except FileNotFoundError:
        print(f"Erro: Diretório '{caminho_completo}' não encontrado."); return

    for caminho_arquivo in arquivos:
        nome_base = os.path.splitext(os.path.basename(caminho_arquivo))[0]
        
        grafo = None
        if 'DIGRAFO' in nome_base.upper():
            grafo = criar_digrafo_de_matriz_incidencia(caminho_arquivo)
        elif 'GRAFO' in nome_base.upper():
            grafo = criar_grafo_de_matriz_incidencia(caminho_arquivo)
        else:
            continue 

        if grafo and grafo.num_vertices() > 0:
            nome_saida = os.path.join(directory, f"{nome_base.replace('_MATRIZ_INCIDENCIA', '')}_via_matriz.txt")
            escrever_grafo_em_arquivo(grafo, nome_saida)

