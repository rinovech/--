import sys,re
import json
import math
import os


def sum(x, y):
    return x + y


def multiply(x, y):
    return x * y


def exponent(x):
    return math.exp(x)


STRING_TO_OPERATION = {
    "+": "sum",
    "*": "multiply",
    "exp": "exponent"
}


class GraphCreation:

    def __init__(self, input, output) -> None:
        self._in = input
        self._out = output
        self.data = None
        self.graph = None
        self.g = Graph()

    def check_params(self) -> bool:
        if self._in is None:
            return False
        if self._out is None:
            self._out = f"output.json"
            print(f"Файл для вывода не был введен.\n"
                  f"Поэтому был установлен файл по умолчанию ({self._out})")
        return True


    def read_from_file(self) -> bool:
        try:
            f = open(self._in, 'r', encoding='utf-8')
            self.data = f.read()
            f.close()
        except:
            print(f"Файла `{self._in}` не существует. "
                  "Проверьте корректность имени файла.")
            return False
        return True


    def data_parser(self) -> None:
        rawdata = self.data
        self.data = []
        cnt = 0
        tmp = []
        for el in re.split(r"\W+", rawdata):
            if el.isalnum():
                cnt += 1
                tmp.append(el)
                if cnt == 3:
                    if not tmp[2].isdigit():
                        self.data = []
                        return
                    cnt = 0
                    self.data.append(tmp)
                    tmp = []


    def check_data(self) -> bool:
        if self.data == []:
            return False
        arcs_cnt = {}
        arcs = {}
        for el in self.data:
            s = f'{el[0]}-{el[1]}'
            if s not in arcs and s not in arcs_cnt:
                arcs_cnt[s] = 0
                arcs[s] = set()
            arcs_cnt[s] += 1
            arcs[s].add(el[2])
        for k in arcs.keys():
            if len(arcs[k]) != arcs_cnt[k]:
                return False
        return True


    def get_graph(self) -> None:
        self.g.graph_construction(self.data)
        arc = []
        for el in self.g.adjc.keys():
            for tpl in self.g.adjc[el]:
                arc.append({ "from" : el
                           , "to" : tpl[0]
                           , "order" : tpl[1]})
        self.graph = {"graph" : {"vertex" : self.g.vertex, "arc" : arc}}


    def write_to_file(self) -> bool:
        try:
            with open(self._out, 'w') as f:
                f.write(json.dumps(self.graph, indent=2))
        except:
            print(f"Не удалось записать в файл `{self._out}`.\n")
            return False
        return True


    def graph_creation(self) -> None:
        if self.check_params():
            if self.read_from_file():
                self.data_parser()
                if not self.check_data():
                    print('Некорректный ввод данных.\n'
                          'Проверьте уникальность порядковых номеров '
                          'у каждой из дуг.')
                    return
                self.get_graph()
                if self.g.vertex == [-1]:
                    return
                if self.write_to_file():
                    print(f"Граф был успешно записан в файл")

class Graph:
    
    def __init__(self) -> None:
        self.vertex = set() # множество для хранения всех вершин графа
        self.adjc = {} # словарь для хранения списка дуг, исходящих из каждой вершины
        self.check = {} # словарь для хранения списка дуг, входящих в каждую вершину


    def graph_construction(self, data : list) -> None:
        for el in data:
            # Добавление вершин в множество vertex
            self.vertex.add(el[0])
            self.vertex.add(el[1])
            # Добавление входящей дуги в словарь check
            if el[1] not in self.check:
                self.check[el[1]] = []
            self.check[el[1]].append((el[0], int(el[2])))
            # Добавление исходящей дуги в словарь adjc
            if el[0] not in self.adjc:
                self.adjc[el[0]] = []
            self.adjc[el[0]].append((el[1], int(el[2])))
        # Сортировка списка вершин
        self.vertex = list(self.vertex)
        self.vertex.sort()
        # Проверка уникальности номеров входящих дуг для каждой вершины
        for _, vs in self.check.items(): # Проход по каждой вершине в словаре check
            n = len(vs) 
            tmp = [''] * n 
            for el, k in vs: 
                t = (k - 1) % n 
                if tmp[t] == el: 
                    tmp[t + 1] = el
                else:
                    tmp[t] = el
            test = set()
            for el in tmp:
                test.add(el)
                if el == '':
                    self.vertex = [-1]
                    print('В графе некорректно заданы номера!\nПроверьте уникальность номеров.')
                    return

def args_parser(argv : list) -> None:
    global graphs
    in1, op1, out1 = None, None, None
    for el in argv:
        if "input1=" in el:
            in1 = el[el.find("=") + 1:]
        elif "oper1=" in el:
            op1 = el[el.find("=") + 1:]
        elif "output1" in el:
            out1 = el[el.find("=") + 1:]
    if (in1 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " для ввода и вывода.\n"
              "Пример: input1=in.txt oper1=operations.json output1=out.txt\n")
        return False
    if op1 is not None:
        graphs.append(GraphCreation(in1, 'tmp.json')) 
        return in1, op1, out1
    else:
        print('Необходимо также ввести название файла, в котором содержатся операции'
              '\nНапример oper1=op.json')

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

def get_prefix_func(graph):

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

    return(", ".join(result))
    

def evaluate_graph(graph_string, ops):
    graph_string = graph_string.replace("()", "")
    for cur_op in ops:
        operation = None
        if ops[cur_op] in STRING_TO_OPERATION.keys():
            operation = STRING_TO_OPERATION[ops[cur_op]]
        else:
            operation = str(ops[cur_op])
        graph_string = graph_string.replace(cur_op, operation)
    return eval(graph_string)


def main():
    try:
        graph_input, operations_path, output = args_parser(sys.argv)
    except:
        print("Ошибка чтения аргументов!")
        return 0

    try:
        for g in graphs:
            g.graph_creation()
    except:
        print("Не удалось создать граф с помощью входного файла.")
        return 0
    
    graph = get_graph_from_json("tmp.json")
    os.remove("tmp.json")
    lin_interpretation = get_prefix_func(graph)

    try:
        with open(operations_path, 'r') as file:
            operations_dict = file.read()
        operations_dict = eval(operations_dict)
        result = evaluate_graph(lin_interpretation, operations_dict)
        with open(output, 'w') as file:
            file.write(str(result))
        print(f"Значение функции, построенной по графу {graph_input} и файлу" +
            f" {operations_path} сохранено в {output}.")
    except:
        print("Ошибка сопоставления операций с описанием графа!")
        return 0
    

if __name__ == "__main__":
    graphs = []
    main()