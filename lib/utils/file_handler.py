"""
Módulo:    Leitor de Arquivos
Descriçao: Funcionalidades para leitura e tratamento com arquivos.
"""
import os
import sys
from lib.core.graph import Grafo
import csv

def ler_grafo(caminho_arquivo, direcionado=False, renomear=None, ponderado=False):
    """
    Lê um arquivo de definição de grafo e cria o objeto Grafo.
    Se o parâmetro 'renomear' for fornecido, o grafo será nomeado com esse valor.
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
        
        return grafo
        
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        return None

def ler_grafo_csv(caminho_csv, renomear=None):
    with open(caminho_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        linhas = list(reader)

    cabecalhos = [h.strip() for h in linhas[0][1:]]  # ignora coluna vazia da esquerda

    grafo = Grafo(direcionado=False, nome_arquivo=renomear or caminho_csv, ponderado=True)

    # adiciona vértices
    for v in cabecalhos:
        grafo.adicionar_vertice(v)

    # percorre a matriz
    for i, linha in enumerate(linhas[1:]):
        v1 = cabecalhos[i]
        valores = linha[1:]  # ignora primeira coluna (nome da linha)

        for j, valor in enumerate(valores):
            if j <= i:
                continue  # evita duplicar aresta (grafo não direcionado)

            if valor.strip() == "" or valor.strip() == "0":
                continue  # sem aresta

            peso = float(valor)
            v2 = cabecalhos[j]

            grafo.adicionar_aresta(v1, v2, peso)

    return grafo


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
            elif nome_lower.startswith('hierholzer_ciclo') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(caminho, direcionado=False, renomear='GRAFO_CICLO_HIERHOLZER')
                if grafo:
                    lista_grafos.append(grafo)
            elif nome_lower.startswith('hierholzer_caminho') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(caminho, direcionado=True, renomear='GRAFO_CAMINHO_HIERHOLZER')
                if grafo:
                    lista_grafos.append(grafo)
            elif nome_lower.startswith('chu_liu_edmonds') and nome_lower.endswith('.txt'):
                grafo = ler_grafo(
                    caminho,
                    direcionado=True,
                    ponderado=True,
                    renomear='DIGRAFO_CHU_LIU_EDMONDS'
                )
                if grafo:
                    lista_grafos.append(grafo)
            elif nome_lower.endswith('.csv'):
                grafo = ler_grafo_csv(
                    caminho,
                    renomear='GRAFO_PCV'
                )
                if grafo:
                    lista_grafos.append(grafo)
    return lista_grafos
