from graphviz import Digraph

dot = Digraph(format="svg")
dot.node(
    "node1",
    label="""
        <<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR><TD>Top</TD></TR>
            <TR><TD>Bottom</TD></TR>
        </TABLE>>
    """,
    shape="none"
)

# 保存して確認
output_path = dot.render("test_html_label", cleanup=False)
print(f"SVGファイルが生成されました: {output_path}")
