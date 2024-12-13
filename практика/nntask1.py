import sys,re
import json

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


def args_parser(argv : list) -> None:
    global graphs
    in1, in2, out1, out2 = None, None, None, None
    for el in argv:
        if "input1=" in el:
            in1 = el[el.find("=") + 1:]
        elif "input2=" in el:
            in2 = el[el.find("=") + 1:]
        elif "output1=" in el:
            out1 = el[el.find("=") + 1:]
        elif "output2=" in el:
            out2 = el[el.find("=") + 1:]
    if (in1 is None) and (in2 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " для ввода и вывода.\n"
              "Пример: input1=in.txt output1=out.json\n")
        return False
    if in1 is not None:
        if out1 is None:
            out1 = f"output1.json"
            print(f"Файл для вывода не был введен.\n"
                f"Поэтому был установлен файл по умолчанию ({out1})")
        graphs.append(GraphCreation(in1, out1))
    if in2 is not None:
        if out2 is None:
            out2 = f"output2.json"
            print(f"Файл для вывода не был введен.\n"
                f"Поэтому был установлен файл по умолчанию ({out2})")
        graphs.append(GraphCreation(in2, out2)) 
    return True


def main() -> None:
    args_parser(sys.argv)
    for g in graphs:
        g.graph_creation()

if __name__ == "__main__":
    graphs = []
    main()