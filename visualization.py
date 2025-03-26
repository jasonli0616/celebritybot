"""Visualization"""
import random

from graph import Graph
import networkx as nx
import plotly

from vertex import VertexKind


def visualize_graph_plotly(g: Graph, n: int):
    """Generate a visualization for g using n arbitrary vertices.
    If g has less than n vertices, plot all vertices."""

    vis = nx.DiGraph()
    vertices = [v for v in g.vertices.values() if v.kind == VertexKind.NGRAM]
    max_vertices = n
    added_vertices = []
    NUM_NEIGHBOURS = 3

    # Make network
    for _ in range(max_vertices // NUM_NEIGHBOURS):
        v = random.choice(vertices)
        vertices.remove(v)

        vis.add_node(v.word)
        added_vertices.append(v)

    for v in added_vertices:
        neighbours_vertices = list(v.neighbours.keys())
        if len(neighbours_vertices) >= NUM_NEIGHBOURS:
            for _ in range(NUM_NEIGHBOURS):
                u = random.choice(neighbours_vertices)
                neighbours_vertices.remove(u)
                if u not in added_vertices:
                    added_vertices.append(u)
                vis.add_edge(v.word, u.word, weight=v.neighbours[u])
    pos = nx.spring_layout(vis, weight="weight", seed=42, iterations=50)

    # Extract coordinates
    edge_x = []
    edge_y = []
    annotations = []
    for u, v in vis.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

        # Add arrow annotation
        annotations.append(
            dict(
                ax=x0, ay=y0,
                x=x1, y=y1,
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.5,
                arrowwidth=1.5,
                arrowcolor="gray"
            )
        )

    # Create figure
    figure = plotly.graph_objs.Figure()

    # Add edges to figure
    figure.add_trace(plotly.graph_objs.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='gray', shape='linear'),
        hoverinfo='none',
    ))

    # Add nodes to figure
    node_x = [pos[node][0] for node in vis.nodes()]
    node_y = [pos[node][1] for node in vis.nodes()]
    figure.add_trace(plotly.graph_objs.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(vis.nodes()),
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=10,
            color='blue',
            opacity=0.8
        )
    ))

    # Specify layout with arrows
    figure.update_layout(
        showlegend=False,
        title=f"Word Map for {g.file_name}",
        title_x=0.5,
        title_y=0.95,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        annotations=annotations
    )

    # Display
    figure.show()
