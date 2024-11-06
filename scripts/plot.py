import networkx as nx
import matplotlib.pyplot as plt

from utils import *
from optimizer import convert_sql_to_algebra

def construct_tree(expression, is_root=True):
    global position_counter
    if is_root and expression.startswith("π"):
        termination = expression.find("(")
        root_value = expression[:termination].strip()
        remaining_expression = balance_parentheses(expression[termination:].strip())
        
        root = Node(root_value)
        root.left = construct_tree(remaining_expression, is_root=False)
        root.pos = position_counter
        position_counter += 1
        
        return root

    left, main, right = split_expression(expression)

    if main is None:
        root = Node(expression)
        root.pos = position_counter
        position_counter += 1
        return root

    root = Node(main)

    if left:
        root.left = construct_tree(left, is_root=False)
    if right:
        root.right = construct_tree(right, is_root=False)

    root.pos = position_counter
    position_counter += 1

    return root

def add_edges(graph, node, parent=None):
    if node is not None:
        label_node = quebra_linha(f"{node.value} ({node.pos})")
        if "π" in node.value:
            color = '#90ee90'
        elif "σ" in node.value:
            color = '#f08080'
        else:
            color = '#add8e6'

        graph.add_node(label_node, color=color)
        if parent:
            label_parent = quebra_linha(f"{parent.value} ({parent.pos})")
            graph.add_edge(label_parent, label_node)
        add_edges(graph, node.left, node)
        add_edges(graph, node.right, node)

def hierarchy_pos(G, root=None, width=10., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=10., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
        
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  
    if len(children) != 0:
        dx = width / len(children) 
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    return pos

# def plot_tree(root):
#     graph = nx.DiGraph()
#     add_edges(graph, root)

#     pos = hierarchy_pos(graph, root=root.value)
    
#     plt.figure(figsize=(12, 8))
#     nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=False)
#     plt.show()

def plot_tree(root):
    graph = nx.DiGraph()
    add_edges(graph, root)

    pos = hierarchy_pos(graph, root=quebra_linha(f"{root.value} ({root.pos})"))

    node_colors = [data['color'] for _, data in graph.nodes(data=True)]

    fig, ax = plt.subplots(figsize=(20, 12))
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=8, font_weight='bold', arrows=False, ax=ax)
    ax.axis('off')  # Desligar o eixo
    return fig  # Retornar a figura

def quebra_linha(texto, max_linhas=25):
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 > max_linhas:
            linhas.append(linha_atual.strip())
            linha_atual = palavra
        else:
            linha_atual += " " + palavra
    
    if linha_atual:
        linhas.append(linha_atual.strip())
    
    return "\n".join(linhas)

position_counter = 1
# Exibir as queries no array
#for i, query in enumerate(queries, start=1):
#    print(f"\nQuery {i}:")
#    sql_formatada = replace_sql_keywords(query)
#    print(sql_formatada + "\n")
#    algebra_result = convert_sql_to_algebra(sql_formatada)
#    print("Resultado:", "\n")
#    print(algebra_result)
#    tree = construct_tree(algebra_result)
#    plot_tree(tree)