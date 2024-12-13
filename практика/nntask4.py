import autograd.numpy as np
import json, sys

class FeedForward:


    def __init__(self, ws) -> None:
        self.ws = ws
        self.n = len(ws)


    def sigmoid(self, x : float) -> float:
            return 1.0 / (1.0 + np.exp(-x))


    def go_forward(self, x : list) -> (list, list):
        try:
            sum = np.dot(self.ws[0], x)
            y = np.array([self.sigmoid(x) for x in sum])
        except ValueError as e:
            print(f"{e}: проверьте размерность слоя #1 и вектора х!\n"
                  f"Умножение выполнить не удалось из-за некорректно заданных размерностей"
                  f" слоя #1 и вектора x.")
            return [-1]
        for i in range(1, self.n):
            try:
                sum = np.dot(self.ws[i], y)
                y = np.array([self.sigmoid(x) for x in sum])
            except ValueError as e:
                print(f"{e}: проверьте размерность слоя #{i + 1} и вектора y!\n"
                  f"Умножение выполнить не удалось из-за некорректно заданных размерностей"
                  f" слоя #{i + 1} и вектора y.")
                return [-1]
        return y


    def get_result(self, xs : list):
        ys = []
        for x in xs:
            new_val = list(self.go_forward(np.array(x)))
            if new_val == [-1]:
                ys.clear()
                break
            ys.append(new_val)
        return ys


def read_json_file(name) -> dict:
    try:
        f = open(name)
        data = json.load(f)
        f.close()
    except:
        print(f"Файла `{name}` не существует. "
              "Проверьте корректность имени файла.")
        exit(0)
    return data


def args_parser(argv : list) -> None:
    in1, in2, out = None, None, None
    for el in argv:
        if "matrix=" in el:
            in1 = el[el.find("=") + 1:]
        elif "vector=" in el:
            in2 = el[el.find("=") + 1:]
        elif "out=" in el:
            out = el[el.find("=") + 1:]
        
    if (in1 is None) or (in2 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " формата JSON для следующих параметров:\n"
              "matrix= -- файл, где лежат матрицы весов\n"
              "vector= -- файл с входными параметрами\n")
        exit(0)
    return in1, in2, out


def write_to_file(data, filename) -> bool:
        try:
            with open(filename, 'w') as f:
                json.dump(data, f)
        except:
            print(f'Ошибка записи данных в файл `{filename}`')
            exit(0)
        else:
            print(f'Данные были успешно записаны в файл `{filename}`')


def main():
    mtrx, vec, out = args_parser(sys.argv)
    if out is None:
        print("Отсутствует название файла для вывода.\n"
              "Файл для вывода был выбран по умолчанию (output.txt)")
        out = "output.txt"
    WS = read_json_file(mtrx)
    XS = read_json_file(vec)
    ws = []
    if "W" not in WS.keys():
        print('\nНекорректный ввод данных')
        return
    if "x" not in XS.keys():
        print('\nНекорректный ввод данных')
        return
    for w in WS['W']:
        ws.append(np.array(w))
    c = FeedForward(ws)
    ys = c.get_result(XS['x'])
    if ys != []:
        write_to_file({'y' : ys}, out)


if __name__ == '__main__':
    main()