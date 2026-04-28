from time import perf_counter

import pytest
import networkx as nx
from mincover import mincover
from testcases import parse_testcases
import random

testcases = parse_testcases("testcases.txt")


def run_testcase(input: str):
    graph = nx.Graph(input)
    cover = mincover(graph)
    return len(cover)


@pytest.mark.parametrize("testcase", testcases, ids=[testcase["name"] for testcase in testcases])
def test_cases(testcase):
    actual_output = run_testcase(testcase["input"])
    assert actual_output == testcase["output"], f"Expected {testcase['output']}, got {actual_output}"


def test_complete():
    nodes = 100
    graph = nx.complete_graph(nodes)
    cover_kn = mincover(graph)
    assert valid_cover(graph, cover_kn)
    assert len(cover_kn) == nodes - 1


def test_star():
    nodes = 20
    star = nx.star_graph(nodes - 1)
    cover_star = mincover(star)
    assert len(cover_star) == 1


def test_no_edges():
    nodes = 1000
    graph = nx.gnm_random_graph(nodes, 0)
    assert len(mincover(graph)) == 0


def test_disconnected():
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (3, 4), (5, 6)])
    cover_dis = mincover(graph)
    assert valid_cover(graph, cover_dis)
    assert len(cover_dis) == 3


def test_random():
    random.seed(42)
    nodes, edges = 50, 1000
    large_graph = nx.gnm_random_graph(nodes, edges)

    assert measure_time(mincover, large_graph) < 1.0
    assert valid_cover(large_graph, mincover(large_graph))


def measure_time(func, *args, **kwargs):
    start = perf_counter()
    func(*args, **kwargs)
    end = perf_counter()
    return end - start


def valid_cover(G, cover):
    cover_set = set(cover)
    for u, v in G.edges():
        if u not in cover_set and v not in cover_set:
            return False
    return True
