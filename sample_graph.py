from graphviz import Digraph

# グラフの作成
dot = Digraph(format='svg')
dot.attr(nodesep='0.5', rankdir='TB')  # グラフ全体の設定

# ノードの定義
num_nodes = 9
for i in range(num_nodes):
    dot.node(f"A{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"B{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"C{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"D{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"E{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"F{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"G{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"H{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"I{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"J{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"K{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"L{i}")  # ノード A0, A1, ..., A49 を定義
    dot.node(f"M{i}")  # ノード A0, A1, ..., A49 を定義

# エッジの定義（ここでは一部だけ作成し、スタイルはinvis）
for i in range(10):  # A0 -> A1 -> ... -> A5
    dot.edge(f"A{i}", f"B{i}", style='invis')
    dot.edge(f"B{i}", f"C{i}", style='invis')
    dot.edge(f"C{i}", f"D{i}", style='invis')
    dot.edge(f"D{i}", f"E{i}", style='invis')
    dot.edge(f"E{i}", f"F{i}", style='invis')
    dot.edge(f"F{i}", f"G{i}", style='invis')
    dot.edge(f"G{i}", f"H{i}", style='invis')
    dot.edge(f"H{i}", f"I{i}", style='invis')
    dot.edge(f"I{i}", f"J{i}", style='invis')
    dot.edge(f"J{i}", f"K{i}", style='invis')
    dot.edge(f"K{i}", f"L{i}", style='invis')
    dot.edge(f"L{i}", f"M{i}", style='invis')

# DOT形式を保存または表示
dot.render('sample_graph', view=False)  # graph_output.dot を保存し、結果を表示
