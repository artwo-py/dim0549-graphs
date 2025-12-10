"""
Módulo:    Formatador
Descriçao: Contém funções para gerar representações textuais das estruturas
           de dados e resultados de análise de um objeto Grafo.
"""
import math
from math import inf as infinito
from lib.algorithms.bellman_ford import formatar_caminho_bellman_ford
from lib.algorithms.chu_liu_edmonds import chu_liu_edmonds
from lib.core.graph import Grafo
from lib.algorithms.is_bipartite import is_bipartite
from lib.algorithms.is_connected import is_connected
from lib.algorithms.lowpt import lowpt 
from lib.core.graph_converter import matriz_adj_para_lista_adj, lista_adj_para_matriz_adj, get_grafo_subjacente
from lib.algorithms.floyd_warshall import floyd_warshall, reconstruir_caminho
from lib.algorithms.kruskal import kruskal
from lib.algorithms.prim import prim
from lib.algorithms.hierholzer_ciclos import hierholzer_ciclos
from lib.algorithms.hierholzer_caminhos import hierholzer_caminhos

def formatar_lista_adj(grafo: Grafo):
    """
    Info: (Função de relatórios) Formata a lista de adjacências do grafo
          em uma representação textual legível.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A representação textual da lista de adjacências.
    """
    titulo = "\n==== REPRESENTAÇÃO POR LISTA DE ADJACÊNCIA ===="
    output = [titulo]
    if not grafo.vertices:
        output.append("Vazia.")
        return "\n".join(output)
    
    sorted_vertices = sorted(grafo.lista_adj.keys(), key=lambda v: str(v.id))
    for vertice in sorted_vertices:
        vizinhos_ids = sorted([str(v.id) for v in grafo.lista_adj.get(vertice, [])])
        output.append(f"{vertice.id}: {vizinhos_ids}")
    return "\n".join(output)

def formatar_matriz_adj(grafo: Grafo):
    """
    Info: (Função de relatórios) Formata a matriz de adjacências do grafo
          em uma representação textual legível.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A representação textual da matriz de adjacências.
    """
    titulo = "\n==== REPRESENTAÇÃO POR MATRIZ DE ADJACÊNCIA ===="
    if grafo.direcionado:
        titulo = "\n==== REPRESENTAÇÃO POR MATRIZ DE ADJACÊNCIA ===="

    output = [titulo]
    ids = [str(v.id) for v in grafo.vertices]
    if not ids:
        output.append("Vazia.")
        return "\n".join(output)
        
    max_width = max(len(id) for id in ids)
    header = f"{' ' * max_width} |" + "".join(f" {id:>{max_width}}" for id in ids)
    output.append(header)
    output.append(f"{'-' * (max_width + 1)}+{'-' * (len(ids) * (max_width + 1))}")
    for i, linha in enumerate(grafo.matriz_adj):
        row_str = f"{ids[i]:>{max_width}} |" + "".join(f" {val:>{max_width}}" for val in linha)
        output.append(row_str)
    return "\n".join(output)

def formatar_matriz_incidencia(grafo: Grafo):
    """
    Info: (Função de relatórios) Formata a matriz de incidência do grafo
          em uma representação textual legível.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A representação textual da matriz de incidência.
    """
    titulo = "\n==== (3) REPRESENTAÇÃO POR MATRIZ DE INCIDÊNCIA ===="
    if grafo.direcionado:
        titulo = "\n==== (17) REPRESENTAÇÃO POR MATRIZ DE INCIDÊNCIA ===="
    
    output = [titulo]
    if not grafo.vertices or not grafo.arestas:
        output.append("Vazia.")
        return "\n".join(output)

    v_ids = [str(v.id) for v in grafo.vertices]
    e_ids = [f"e{i+1}" for i in range(grafo.num_arestas())]
    
    max_width = 0
    if v_ids: max_width = max(max_width, max(len(id) for id in v_ids))
    if e_ids: max_width = max(max_width, max(len(id) for id in e_ids))

    header = f"{' ' * max_width} |" + "".join(f" {id:>{max_width}}" for id in e_ids)
    output.append(header)
    output.append(f"{'-' * (max_width + 1)}+{'-' * (len(e_ids) * (max_width + 1))}")

    for i, linha in enumerate(grafo.matriz_incidencia):
        row_str = f"{v_ids[i]:>{max_width}} |" + "".join(f" {val:>{max_width}}" for val in linha)
        output.append(row_str)
        
    return "\n".join(output)

def formatar_conversoes(grafo: Grafo):
    """
    Info: (Função de relatórios) Demonstra a conversão entre as representações
          de lista e matriz de adjacências. As representações originais
          do grafo são restauradas após o teste.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado textual da conversão.
    """
    output = ["\n==== (4) CONVERSÃO ENTRE REPRESENTAÇÕES ===="]
    lista_adj_original = {k: list(v) for k, v in grafo.lista_adj.items()}
    matriz_adj_original = [row[:] for row in grafo.matriz_adj]
    output.append("\n--- Matriz -> Lista ---")
    matriz_adj_para_lista_adj(grafo)
    output.append(formatar_lista_adj(grafo).split('\n', 2)[-1])
    grafo.lista_adj = lista_adj_original
    output.append("\n--- Lista -> Matriz ---")
    lista_adj_para_matriz_adj(grafo)
    output.append(formatar_matriz_adj(grafo).split('\n', 2)[-1])
    grafo.lista_adj = lista_adj_original
    grafo.matriz_adj = matriz_adj_original
    return "\n".join(output)

def formatar_graus(grafo: Grafo):
    """
    Info: (Função de relatórios) Lista o grau de cada vértice.
          Para grafos não direcionados, mostra o grau total.
          Para dígrafos, mostra os graus de entrada (d-) e saída (d+).
    E: grafo (Grafo) - A instância do grafo.
    S: str - A lista de graus formatada.
    """
    output = []
    if not grafo.direcionado:
        output.append("\n==== GRAU DE CADA VÉRTICE ====")
    else:
        output.append("\n==== GRAU DE CADA VÉRTICE (ENTRADA/SAÍDA) ====") 
    
    if not grafo.vertices:
        output.append("Vazio.")
        return "\n".join(output)
        
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    degree_strings = []

    for v in sorted_vertices:
        grau = grafo.get_grau(v.id)
        if grau is None:
            continue
        
        if not grafo.direcionado:
            degree_strings.append(f"d({v.id}) = {grau}")
        else:
            degree_strings.append(f"d-({v.id}) = {grau[0]}, d+({v.id}) = {grau[1]}")
    
    num_cols = 3
    max_len = max(len(s) for s in degree_strings) if degree_strings else 0
    padded_strings = [s.ljust(max_len) for s in degree_strings]
    num_rows = math.ceil(len(padded_strings) / num_cols)
    
    for i in range(num_rows):
        row_parts = [padded_strings[i + j * num_rows] for j in range(num_cols) if i + j * num_rows < len(padded_strings)]
        output.append("   ".join(row_parts))
    
    return "\n".join(output)

def formatar_adjacencias_por_vertice(grafo: Grafo):
    """
    Info: (Função de relatórios) Lista os vizinhos adjacentes para cada vértice.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A lista de adjacências formatada.
    """
    output = ["\n==== (6) ADJACÊNCIAS DE CADA VÉRTICE ===="]
    if not grafo.vertices:
        output.append("Vazio.")
        return "\n".join(output)
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    for v in sorted_vertices:
        adjacentes_ids = sorted([str(adj.id) for adj in grafo.lista_adj.get(v, [])])
        output.append(f"Adjacentes de {v.id}: {adjacentes_ids}")
    return "\n".join(output)

def formatar_info_gerais(grafo: Grafo):
    """
    Info: (Função de relatórios) Informa o número total de vértices e arestas.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resumo das informações gerais.
    """
    output = [
        f"\n==== (7) NÚMERO TOTAL DE VÉRTICES ====\n{grafo.num_vertices()}",
        f"\n==== (8) NÚMERO TOTAL DE ARESTAS ====\n{grafo.num_arestas()}"
    ]
    return "\n".join(output)

def formatar_eh_conexo(grafo: Grafo):
    """
    Info: (Função de relatórios) Verifica e reporta se o grafo é conexo.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado da conectividade.
    """
    output = ["\n==== (11) CONECTIVIDADE ===="]
    resultado = "Sim" if is_connected(grafo) else "Não"
    output.append(f"O grafo é conexo? {resultado}")
    return "\n".join(output)

def formatar_bipartido(grafo: Grafo):
    """
    Info: (Função de relatórios) Verifica e reporta se o grafo é bipartido.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado da bipartição.
    """
    output = ["\n==== (12) BIPARTIÇÃO (OPC) ===="]
    resultado = "Sim" if is_bipartite(grafo) else "Não"
    output.append(f"O grafo é bipartido? {resultado}")
    return "\n".join(output)

def formatar_biconectividade(grafo: Grafo):
    """
    Info: (Função de relatórios) Encontra e reporta os pontos de articulação
          e as pontes do grafo usando o algoritmo lowpt.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado da análise de biconectividade.
    """
    output = ["\n==== (15) BICONECTIVIDADE (ARTICULAÇÕES E PONTES) ===="]
    if grafo.num_vertices() == 0:
        output.append("Grafo vazio.")
        return "\n".join(output)
    articulacoes, pontes = lowpt(grafo)
    if not articulacoes:
        output.append("Pontos de Articulação: Nenhum.")
    else:
        output.append(f"Pontos de Articulação: {sorted(list(articulacoes), key=str)}")
    if not pontes:
        output.append("Pontes: Nenhuma.")
    else:
        output.append(f"Pontes: {sorted(list(pontes))}")
    return "\n".join(output)
    
def formatar_grafo_subjacente(grafo: Grafo):
    """
    Info: (Função de relatórios) Gera a representação textual do grafo
          subjacente (não-direcionado) de um dígrafo.
    E: grafo (Grafo) - A instância do dígrafo.
    S: str - A representação textual do grafo subjacente.
    """
    output = ["\n==== (18) GRAFO SUBJACENTE (OPC) ===="]
    subjacente = get_grafo_subjacente(grafo)

    texto_lista = formatar_lista_adj(subjacente).split('\n', 2)[-1]
    output.append(texto_lista)
    return "\n".join(output)


def formatar_caminho_floyd_warshall(grafo: Grafo, id_inicio: str, id_fim: str):
    """
    Info: (Função de relatórios) Executa o Floyd-Warshall, reconstrói o caminho
          mais curto entre dois vértices e formata o resultado textual.
          
    E: grafo (Grafo) - A instância do grafo.
    E: id_inicio (str) - ID do vértice inicial.
    E: id_fim (str) - ID do vértice final.
    
    S: tupla (str, list[Vertice] or None) 
         - str: O relatório textual formatado (para impressão).
         - list or None: Os dados do caminho (para o renderer), ou None se não houver.
    """
    titulo = f"\n\n==== CAMINHO MAIS CURTO (FLOYD-WARSHALL {id_inicio} -> {id_fim}) ===="
    
    if not grafo.ponderado:
        report = "  Algoritmo não aplicável (grafo não ponderado)."
        return (titulo + "\n" + report, None)
    
    try:
        dist, pred, vertices = floyd_warshall(grafo)
        
        idx_map = {v.id: i for i, v in enumerate(vertices)}
        idx_inicio = idx_map.get(id_inicio)
        idx_fim = idx_map.get(id_fim)

        if idx_inicio is None or idx_fim is None:
            report = f"  Erro: Vértice {id_inicio} ou {id_fim} não encontrado."
            return (titulo + "\n" + report, None)

        custo = dist[idx_inicio][idx_fim]
        caminho = reconstruir_caminho(pred, vertices, idx_inicio, idx_fim)

        if caminho:
            custo_str = f"{custo:.0f}" if custo != infinito else "INF"
            caminho_str = " -> ".join([v.id for v in caminho])
            report = f"  Custo: {custo_str}\n  Caminho: {caminho_str}"
            return (titulo + "\n" + report, caminho)
        else:
            report = "  Não há caminho entre os vértices."
            return (titulo + "\n" + report, None)
            
    except Exception as e:
        report = f"  Ocorreu um erro inesperado: {e}"
        return (titulo + "\n" + report, None)
def formatar_agm_resultado(agm_grafo: Grafo, nome_algoritmo: str):
    """
    Info: (Função de relatórios) Formata o resultado de um algoritmo de AGM.
    E: agm_grafo (Grafo) - O grafo resultante (a AGM).
    E: nome_algoritmo (str) - O nome (ex: "Kruskal")
    S: str - O relatório textual formatado.
    """
    titulo = f"\n\n==== RESULTADO {nome_algoritmo.upper()} ===="
    output = [titulo]
    if not agm_grafo or not agm_grafo.arestas:
        output.append("  AGM vazia.")
        return "\n".join(output)
    
    custo_total = 0
    arestas_str = []
    
    arestas_ordenadas = sorted(agm_grafo.arestas, key=lambda a: (str(a.v1.id), str(a.v2.id)))
    
    for aresta in arestas_ordenadas:
        if aresta.peso is not None:
            custo_total += aresta.peso
        arestas_str.append(f"  ({aresta.v1.id}, {aresta.v2.id}, {aresta.peso})")
    
    output.append(f"  Custo Total: {custo_total}")
    output.append("  Arestas da AGM:")
    output.extend(arestas_str)
    return "\n".join(output)

def formatar_hierholzer_resultado(grafo: Grafo):
    """
    Info: (Função de relatórios) Executa e formata o resultado do Hierholzer.
    E: grafo (Grafo) - O grafo de entrada.
    S: str - O relatório textual formatado.
    """
    try:
        if 'CICLO_HIERHOLZER' in grafo.nome_arquivo:
            titulo = "\n\n==== RESULTADO HIERHOLZER (CICLO) ===="
            resultado = hierholzer_ciclos(grafo)
            path_str = " -> ".join(map(str, resultado))
            return f"{titulo}\n  Ciclo Euleriano: {path_str}"
            
        elif 'CAMINHO_HIERHOLZER' in grafo.nome_arquivo:
            titulo = "\n\n==== RESULTADO HIERHOLZER (CAMINHO) ===="
            resultado = hierholzer_caminhos(grafo)
            path_str = " -> ".join(map(str, resultado))
            return f"{titulo}\n  Caminho Euleriano: {path_str}"
            
    except Exception as e:
        return f"\n==== RESULTADO HIERHOLZER ====\n  Erro ao processar: {e}"
        
    return "" 
def formatar_arborescencia(arbo_grafo: Grafo, nome_algoritmo: str):
    """
    Info: (Função de relatórios) Formata o resultado de uma Arborescência Geradora Mínima.
    E: arbo_grafo (Grafo) - O grafo resultante do algoritmo (direcionado).
    E: nome_algoritmo (str) - Nome ("Chu-Liu/Edmonds")
    S: str - Texto formatado.
    """
    titulo = f"\n\n==== RESULTADO {nome_algoritmo.upper()} ===="
    output = [titulo]
    if not arbo_grafo or not arbo_grafo.arestas:
        output.append("  Arborescência vazia.")
        return "\n".join(output)
    custo_total = 0
    arestas_str = []
    arestas_ordenadas = sorted(
        arbo_grafo.arestas,
        key=lambda a: (str(a.v1.id), str(a.v2.id))
    )

    for aresta in arestas_ordenadas:
        if aresta.peso is not None:
            custo_total += aresta.peso
        arestas_str.append(f"  {aresta.v1.id} -> {aresta.v2.id} (peso {aresta.peso})")

    output.append(f"  Custo Total: {custo_total}")
    output.append("  Arestas da Arborescência:")
    output.extend(arestas_str)
    return "\n".join(output)

def formatar_vmp(vmp_ciclo: dict, nome_algoritmo: str, it=None):
    """
    Info: (Função de relatórios) Formata o resultado do algoritmo de inserção do
        vizinho mais próximo para o PCV.
    E: vmp_ciclo (list) - O ciclo resultante do algoritmo.
    E: nome_algoritmo (str) - Nome ("Vizinho Mais Próximo + Busca Local")
    S: str - Texto formatado.
    """
    titulo = f"\n\n==== RESULTADO {nome_algoritmo.upper()} ===="
    output = [titulo]
    if not vmp_ciclo or len(vmp_ciclo) == 0:
        output.append("  Grafo vazio.")
        return "\n".join(output)
    
    custo_total = list(vmp_ciclo.values())[0]

    output.append(f"  Custo Total: {custo_total}")
    output.append("  Rota encontrada:")

    rota = list(vmp_ciclo.keys())[0]
    rota_formatada = " -> ".join(map(str, rota))
    output.append(f"  {rota_formatada}\n")
    return "\n".join(output)

def formatar_vmp_melhorado(vmp_ciclo: dict, nome_algoritmo: str):
    """
    Info: (Função de relatórios) Formata o resultado do algoritmo de inserção do
        vizinho mais próximo para o PCV.
    E: vmp_ciclo (list) - O ciclo resultante do algoritmo.
    E: nome_algoritmo (str) - Nome ("Vizinho Mais Próximo + Busca Local")
    S: str - Texto formatado.
    """
    output = []
    if not vmp_ciclo or len(vmp_ciclo) == 0:
        output.append("  Grafo vazio.")
        return "\n".join(output)
    
    custo_total = list(vmp_ciclo.values())[0]

    output.append(f"\n  Custo Total após busca local: {custo_total}")
    output.append("  Rota encontrada após busca local:")

    rota = list(vmp_ciclo.keys())[0]
    rota_formatada = " -> ".join(map(str, rota))
    output.append(f"  {rota_formatada}")
    return "\n".join(output)

def gerar_relatorio_memetico(dados_estatisticos):
    """
    Info: (Função de relatórios) Gera o relatório estatístico
          contendo melhor custo, média e tempo médio das 20 execuções.
    E: dados_estatisticos (list[dict]) - Lista contendo métricas de cada instância processada.
    S: None
    """
    with open("resultados_memetico.txt", "w", encoding='utf-8') as f:
        for i, dados in enumerate(dados_estatisticos):
            f.write(f"\n==== RESULTADO MEMÉTICO - INSTÂNCIA {i+1} ====\n")
            f.write(f"  Melhor Custo (em 20 execuções): {dados['melhor_custo']}\n")
            f.write(f"  Custo Médio: {dados['media_custo']:.2f}\n")
            f.write("  Melhor Rota encontrada:\n")
            rota_formatada = " -> ".join(map(str, dados['melhor_rota']))
            f.write(f"  {rota_formatada}\n")
            f.write("*********************************************************************\n")


def gerar_relatorio_genetico(dados_estatisticos: list):
    """
    Info: (Função de relatórios) Gera o relatório estatístico (resultados_genetico.txt)
          contendo melhor custo, média e tempo médio das 20 execuções do Genético + Shift.
    E: dados_estatisticos (list[dict]) - Lista contendo métricas de cada instância processada.
    S: None (escreve em "resultados_genetico.txt")
    """
    with open("resultados_genetico.txt", "w", encoding='utf-8') as f:
        for i, dados in enumerate(dados_estatisticos):
            f.write(f"\n==== RESULTADO GENÉTICO + SHIFT - INSTÂNCIA {i+1} ====\n")
            f.write(f"  Melhor Custo (em 20 execuções): {dados['melhor_custo']}\n")
            f.write(f"  Custo Médio: {dados['media_custo']:.2f}\n")
            f.write(f"  Tempo Médio de Execução: {dados['media_tempo']:.4f} segundos\n")
            f.write("  Melhor Rota encontrada:\n")
            
            rota_formatada = " -> ".join(map(str, dados['melhor_rota']))
            f.write(f"  {rota_formatada}\n")
            f.write("*********************************************************************\n")

def gerar_relatorio_unidade_3(ciclos: list, ciclos_melhorados):
    """
    Info: (Função de relatórios) Agrega todos os resultados da unidade 3
          em um relatório textual completo (resultados.txt).
          Esta função executa os algoritmos específicos para cada grafo
          e formata seus resultados.
    E: ciclos (list[Grafo]) - A lista de todos os ciclos carregados.
    E: ciclos_melhorados (list[Grafo]) - A lista de todos os ciclos melhorados (via busca local) carregados.
    S: None (escreve diretamente em "resultados.txt")
    """
    with open("resultados.txt", "w", encoding='utf-8') as f:        
        for i in range(len(ciclos)):
            # f.write(f"Arquivo: {grafo.nome_arquivo}\n")
            
            f.write(formatar_vmp(ciclos[i], f"Vizinho Mais Próximo + Busca Local - Instância {i+1}"))
            f.write(formatar_vmp_melhorado(ciclos_melhorados[i], f"Vizinho Mais Próximo + Busca Local Melhorado - Instância {i+1}"))
            f.write("*********************************************************************\n")
            f.write("\n")


def gerar_relatorio_completo(grafo: Grafo):
    """
        Info: (Função de relatórios) Agrega todos os resultados de análise em
        um relatório textual completo, formatando-o de forma diferente
        dependendo se o objeto é um Grafo (não-direcionado) ou Dígrafo.
        E: grafo (Grafo) - A instância do grafo a ser analisada.
            S: str - O relatório completo.
        """
    header = [
        "*********************************************************************",
        f"Arquivo: {grafo.nome_arquivo}",
    ]
    if not grafo.direcionado:
        report_body = [
            "Análise para: GRAFO NÃO-DIRECIONADO",
            formatar_lista_adj(grafo),                 # (1)
            formatar_matriz_adj(grafo),                # (2)
            formatar_matriz_incidencia(grafo),         # (3)
            formatar_conversoes(grafo),                # (4)
            formatar_graus(grafo),                     # (5)
            formatar_adjacencias_por_vertice(grafo),   # (6)
            formatar_info_gerais(grafo),               # (7) e (8)
            "\n==== (9) e (10) INCLUSÃO E EXCLUSÃO DE VÉRTICES ====\nINFO: Funções implementadas na classe Grafo para manipulação dos dados.",
            formatar_eh_conexo(grafo),                 # (11)
            formatar_bipartido(grafo),                 # (12)
            "\n==== (13) e (14) BUSCAS BFS E DFS ====\nINFO: As buscas são executadas e seus resultados renderizados visualmente.",
            formatar_biconectividade(grafo),           # (15)
        ]
    else:
        report_body = [
            "Análise para: DÍGRAFO",
            formatar_matriz_adj(grafo),                # (16)
            formatar_matriz_incidencia(grafo),         # (17)
            formatar_grafo_subjacente(grafo),          # (18)
            "\n==== (19) e (20) BUSCAS BFS E DFS ====\nINFO: As buscas são executadas e seus resultados (com classificação completa de arestas para DFS) são renderizados visualmente.",
        ]
    return "\n".join(header + report_body)

def gerar_relatorio_unidade_2(grafos: list):
    """
    Info: (Função de relatórios) Agrega todos os resultados da unidade 2
          em um relatório textual completo (resultados.txt).
          Esta função executa os algoritmos específicos para cada grafo
          e formata seus resultados.
    E: grafos (list[Grafo]) - A lista de todos os grafos carregados.
    S: None (escreve diretamente em "resultados.txt")
    """
    with open("resultados.txt", "w", encoding='utf-8') as f:
        grafos_ordenados = sorted(grafos, key=lambda g: g.nome_arquivo)
        
        for grafo in grafos_ordenados:
            f.write("*********************************************************************\n")
            f.write(f"Arquivo: {grafo.nome_arquivo}\n")
            
            f.write(formatar_matriz_adj(grafo))
            f.write("\n")
            f.write(formatar_lista_adj(grafo))
            f.write("\n")
            f.write(formatar_graus(grafo))
                        
            if 'GRAFO_AGM' in grafo.nome_arquivo:
                try:
                    agm_k = kruskal(grafo) 
                    f.write(formatar_agm_resultado(agm_k, "Kruskal")) # (1)
                except Exception as e:
                    f.write(f"\n==== RESULTADO KRUSKAL ====\n  Erro: {e}")
                try:
                    agm_p = prim(grafo) 
                    f.write(formatar_agm_resultado(agm_p, "Prim")) # (2)
                except Exception as e:
                    f.write(f"\n==== RESULTADO PRIM ====\n  Erro: {e}")
                report_bf, _ = formatar_caminho_bellman_ford(grafo, "1", "15")
                f.write(report_bf)# (6)
                report_fw, _ = formatar_caminho_floyd_warshall(grafo, "1", "15")
                f.write(report_fw) # (7)
            elif 'CHU_LIU_EDMONDS' in grafo.nome_arquivo:
                agm_chu, erro = chu_liu_edmonds(grafo, raiz="1")
                if agm_chu:
                    f.write(formatar_arborescencia(agm_chu, "Chu-Liu/Edmonds"))
                else:
                    f.write(f"\n==== RESULTADO CHU-LIU/EDMONDS ====\n  Erro: {erro}")
            elif 'HIERHOLZER' in grafo.nome_arquivo:
                f.write(formatar_hierholzer_resultado(grafo)) # (8) - (9)          
            f.write("\n\n")
