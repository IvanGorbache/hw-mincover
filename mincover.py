# import subprocess, sys
# subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy"], stdout=subprocess.DEVNULL)
# subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx>=3.4"], stdout=subprocess.DEVNULL)

import networkx as nx, cvxpy, numpy as np

np.float_ = np.float64


def mincover(graph: nx.Graph) -> set:
    """
    Return a minimum-cardinality vertex cover in the given graph.
    
    >>> len(mincover(nx.Graph([(1,2),(2,3)])))
    1
    >>> len(mincover(nx.Graph([(1,2),(2,3),(3,1)])))
    2
    >>> len(mincover(nx.Graph([(1,2),(2,3),(3,4),(4,1)])))
    2
    >>> len(mincover(nx.Graph([])))
    0
    """
    if graph.number_of_nodes() == 0:
        return set()

    nodes = list(graph.nodes())
    node_index = {node: i for i, node in enumerate(nodes)}

    x = cvxpy.Variable(len(nodes), boolean=True)

    constraints = []
    for u, v in graph.edges():
        constraints.append(x[node_index[u]] + x[node_index[v]] >= 1)

    prob = cvxpy.Problem(cvxpy.Minimize(cvxpy.sum(x)), constraints)
    prob.solve(solver=cvxpy.SCIPY)

    return {nodes[i] for i in range(len(nodes)) if x.value[i] > 0.5}


if __name__ == '__main__':
    import doctest

    print(doctest.testmod())

    # Use this code for testing via console input-output:
    # edges=eval(input())
    # graph = nx.Graph(edges)
    # print(len(mincover(graph)))
