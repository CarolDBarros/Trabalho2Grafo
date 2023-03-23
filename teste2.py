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

   
    
# Leitura do arquivo Excel
df = pd.read_excel('Eambiental.xlsx')

# Criação do grafo
G = nx.DiGraph()

# Adição dos nós
nodes_dict = {}  # Dicionário para armazenar as informações de cada nó
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
                weight = 1  # valor padrão para o peso da aresta
                print(f"Erro: múltiplos valores encontrados para o código {dependency}. O peso da aresta foi definido como {weight}.")
            G.add_edge(dependency, df['Codigo'][i], weight=weight)


# Cálculo da posição dos nós
pos = {}
for node in G.nodes:
    if node == 'T':
        pos[node] = (df.loc[df['Codigo']=='T', 'Periodo'].item(), 1)
    elif node == 'S':
        pos[node] = (df.loc[df['Codigo']=='S', 'Periodo'].item(), 1)
    else:
        pos[node] = (df.loc[df['Codigo']==node, 'Periodo'].item(), random.random())


# Encontrando o caminho máximo (crítico)
longest_path = nx.dag_longest_path(G)
print("Caminho maximo para a conclusão do curso:")
for node in longest_path:
    print(f"{nodes_dict[node]['nome']} ({node})")

print(f" ")

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




# Visualização do grafo
nx.draw(G, pos=pos, with_labels=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()