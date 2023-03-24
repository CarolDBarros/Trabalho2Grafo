"""
Este módulo contém o código principal da aplicação que carrega um grafo a
 partir de um arquivo Excel.
O arquivo de dados deve estar no formato XLSX e deve conter informações 
sobre os
 nós e as arestas do grafo.
"""

import pandas as pd
import networkx as nx 
import matplotlib.pyplot as plt
import random

def leitura_arquivo():
    print("Digite o numero do arquivo que deseja escollher\n")
    print("1=Engenharia Ambiental\n")
    print("2=Musica\n")
    print("0=sair\n")
    escolha = int(input("Digite o numero do arquivo que deseja utilizar: "))
    if escolha == 1:
        return pd.read_excel('Eambiental.xlsx')
    elif escolha == 2:
        return pd.read_excel('musicaOP.xlsx')
    else:
        print("ERRO")
        return None

# Criação do grafo
G = nx.DiGraph()

def cria_grafo(df):
    G = nx.DiGraph()
    nodes_dict = {}
    for i in range(len(df)):
        node_name = df['Codigo'][i]
        nodes_dict[node_name] = {
            'nome': df['Nome'][i],
            'periodo': df['Periodo'][i],
            'duracao': df['Duracao'][i],
        }
        G.add_node(node_name)
    for i in range(len(df)):
        dependencies = df['Dependencias'][i]
        if pd.isna(dependencies):
            continue
        dependencies = dependencies.split(',')
        for dependency in dependencies:
            dependency = dependency.strip() 
            if dependency:
                weight_array = df.loc[df['Codigo'] == dependency, 'Peso da Aresta']
                if len(weight_array) == 1:
                    weight = weight_array.item()
                else:
                    weight = 1
                    print(f"Erro: múltiplos valores encontrados para o código {dependency}. O peso da aresta foi definido como {weight}.")
                G.add_edge(dependency, df['Codigo'][i], weight=weight)
    return G, nodes_dict

def calcula_posicoes(G, nodes_dict):
    pos = {}
    for node in G.nodes:
        if node == 'T':
            pos[node] = (nodes_dict['T']['periodo'], 1)
        elif node == 'S':
            pos[node] = (nodes_dict['S']['periodo'], 1)
        else:
            pos[node] = (nodes_dict[node]['periodo'], random.random())
    return pos


# Encontrando o caminho máximo (crítico)
def encontrar_caminho_critico(G, nodes_dict):
    # Encontrando o caminho máximo (crítico)
    longest_path = nx.dag_longest_path(G)
    print("Caminho maximo para a conclusão do curso:")
    for node in longest_path:
        print(f"{nodes_dict[node]['nome']} ({node})")
    return longest_path

def exibir_caminho_minimo(longest_path, nodes_dict):
    # Exibição das tarefas que fazem parte do caminho crítico e tempo mínimo de conclusão do projeto
    min_time = 0
    print(f"Caminho Minimo")
    for i in range(len(longest_path)):
        node = longest_path[i]
        task_name = nodes_dict[node]['nome']
        task_duration = nodes_dict[node]['duracao']
        min_time += task_duration
        print(f"- {i+1}: {task_name} - Duracao: {task_duration}")
    print(f"Tempo minimo para a conclusao: {min_time} periodos")






def visualizar_grafo(G, pos):
    nx.draw(G, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

# Programa principal
nome_arquivo = leitura_arquivo()
df = leitura_arquivo()
if df is not None:
    G, nodes_dict = cria_grafo(df)
    pos = calcula_posicoes(G, nodes_dict)
    visualizar_grafo(G, pos)
    longest_path = encontrar_caminho_critico(G, nodes_dict)
    exibir_caminho_minimo(longest_path, nodes_dict)
