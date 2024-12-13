import json
import sys,re

def args_parser(argv : list) -> None:
    global graphs
    in1, out1 = None, None
    for el in argv:
        if "input1=" in el:
            in1 = el[el.find("=") + 1:]
        if "output1=" in el:
            out1 = el[el.find("=") + 1:]
    if (in1 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " для ввода и вывода.\n"
              "Пример: input1=in.json output1=out.txt\n")
        return False
    if in1 is not None:
        if out1 is None:
            out1 = f"func.txt"
            print(f"Файл для вывода не был введен.\n"
                f"Поэтому был установлен файл по умолчанию ({out1})")
        return in1, out1
        

class Node:
    def __init__(self, node, parents=None, child=None) -> None:
        self.node = node
        self.from_nodes = [] if parents is None else parents
        self.to_nodes = [] if child is None else child

def get_graph_from_json(json_graph):

    with open(json_graph, "r") as f:
        data = json.load(f)

    graph_data = data['graph']

    graph = {}
    nodes = {}

    for vertex in graph_data['vertex']:
        graph[vertex] = []
        nodes[vertex] = Node(vertex)

    for arc in graph_data['arc']:
        from_vertex = arc['from']
        to_vertex = arc['to']
        graph[from_vertex].append(to_vertex)
        nodes[from_vertex].to_nodes.append(to_vertex)
        nodes[to_vertex].from_nodes.append(from_vertex)

    if cycle_check(graph):
        print("В графе обнаружен цикл.")
        raise RuntimeError("Цикл в графе.")
    
    return graph, nodes

def cycle_check(graph):
    path = set()
    def visit(vertex):
        path.add(vertex)
        for neighbour in graph.get(vertex, ()):
            if neighbour in path or visit(neighbour):
                return True
        path.remove(vertex)
        return False
    return any(visit(v) for v in graph)

def get_prefix_func(graph, output):

    def iterates(cur_node, nodes):
        from_nodes = [iterates(nodes[p], nodes)
                    for p in cur_node.from_nodes]
        return f'{cur_node.node}({", ".join(from_nodes)})'

    graph, nodes = graph
    root = None
    result = []
    for vertex in graph.keys():
        if not graph[vertex]:
            root = vertex
            result.append(iterates(nodes[root], nodes))

    with open(output, 'w') as file:
        file.write(", ".join(result))
    print(f"Линейное представление функции сохранено в файл {output}.")

def main():

    try:
        input, output = args_parser(sys.argv)
    except:
        print("Ошибка чтения аргументов!")
        return 0
    
    try:
        graph = get_graph_from_json(input)
    except:
        print("Не получилось считать граф с файла", input)
        return 0

    try:
        get_prefix_func(graph, output)
    except:
        print("Не получилось составить префиксную фунцкию")
        return 0

if __name__ == "__main__":
    main()