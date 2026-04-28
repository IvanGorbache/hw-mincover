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
    var = {node: cvxpy.Variable(boolean=True) for node in graph.nodes}
    objective = cvxpy.sum(var[node] for node in graph.nodes)
    constraints = [var[u] + var[v] >= 1 for u, v in graph.edges]
    prob = cvxpy.Problem(cvxpy.Minimize(objective), constraints)
    prob.solve(solver=cvxpy.SCIPY)
    return {node for node, nodevar in var.items() if nodevar.value > 0}


if __name__ == '__main__':
    import doctest

    print(doctest.testmod())

    # Use this code for testing via console input-output:
    # edges=eval(input())
    # graph = nx.Graph(edges)
    # print(len(mincover(graph)))
