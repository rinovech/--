import autograd.numpy as np
import json, sys

class BackPropagation:

    def __init__(self, ws, n, lrate) -> None:
        self.ws = ws
        self.len_ws = len(ws)
        self.n = n
        self.lrate = lrate
        self.messages = None

    def sigmoid(self, x : float) -> float:
        return 1.0 / (1.0 + np.exp(-x))

    def d_sigmoid(self, y : float) -> float:
        return y * (1.0 - y)

    def go_forward(self, x : list) -> (list, list):
        ys = []
        try:
            sum = np.dot(self.ws[0], x)
            y = np.array([self.sigmoid(x) for x in sum])
            ys.append(y)
        except ValueError as e:
            print(f"{e}: проверьте размерность слоя #1 и вектора х!\n"
                  f"Умножение выполнить не удалось из-за некорректно заданных размерностей"
                  f" слоя #1 и вектора x.")
            exit(0)
        for i in range(1, self.len_ws):
            try:
                sum = np.dot(self.ws[i], y)
                y = np.array([self.sigmoid(x) for x in sum])
                ys.append(y)
            except ValueError as e:
                print(f"{e}: проверьте размерность слоя #{i + 1} и вектора y!\n"
                  f"Умножение выполнить не удалось из-за некорректно заданных размерностей"
                  f" слоя #{i + 1} и вектора y.")
                exit(0)
        return ys

    def train(self, x_vec : list, y_true : list) -> None:
        m = len(x_vec)
        self.messages = []
        for it in range(1, self.n + 1):
            errors = []
            for k in range(m):
                ys = self.go_forward(np.array(x_vec[k]))
                ys = np.insert(ys, 0, np.array(x_vec[k]), axis=0)
                if len(ys[-1]) != len(y_true[k]):
                    print(f'\nРазмерность выходного значения алгоритма\n'
                          f'не совпадает с размерностью желаемого выходного состояния {y_true[k]}')
                    exit(0)
                j = len(ys) - 2
                e = ys[-1] - y_true[k]
                grad = e * self.d_sigmoid(ys[-1])  
                self.ws[-1] = self.ws[-1] - self.lrate * ys[j] * grad
                for i in range(self.len_ws - 2, -1, -1):
                    j -= 1
                    grad = self.ws[i + 1] * grad * self.d_sigmoid(ys[j + 1])
                    for t in range(len(self.ws[i])):
                        self.ws[i][t, :] = self.ws[i][t, :] - ys[j] * grad[:, t] * self.lrate
                errors.append(sum(e) / len(e))
            self.messages.append(f"При i = {it} значения функции ошибок: {sum(errors) / len(errors)}\n")

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
    in1, in2, in3, out = None, None, None, None
    for el in argv:
        if "matrix=" in el:
            in1 = el[el.find("=") + 1:]
        elif "param=" in el:
            in2 = el[el.find("=") + 1:]
        elif "train=" in el:
            in3 = el[el.find("=") + 1:]
        elif "out=" in el:
            out = el[el.find("=") + 1:]
        
    if (in1 is None) or (in2 is None) or (in3 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " формата JSON для следующих параметров:\n"
              "matrix= -- файл, где лежат матрицы весов\n"
              "param= -- файл с параметром n (количество итераций)\n"
              "train= -- файл с входными и выходными параметрами\n")
        exit(0)
    return in1, in2, in3, out


def write_inf(mes : list, filename):
    mes = "".join(mes)
    try:
        f = open(filename, 'w')
        f.write(mes)
        f.close()
    except:
        print(f'Ошибка записи данных в файл {filename}')
        exit(0)
    else:
        print(f'\nДанные успешно записаны в файл {filename}')
    
def main():
    # elements = []
    mtrx, par, train, out = args_parser(sys.argv)
    if out is None:
        print("Отсутствует название файла для вывода.\n"
              "Файл для вывода был выбран по умолчанию (output.txt)")
        out = "output.txt"
    mtrx = read_json_file(mtrx)
    par = read_json_file(par)
    train = read_json_file(train)
    if "W" not in mtrx.keys():
        print('\nНекорректный ввод данных!\n'
              'Не удалось считать матрицы весов.')
        return
    if "n" not in par.keys() or "lrate" not in par.keys():
        print('\nНекорректный ввод данных!\n'
              'Не удалось считать параметры')
        return
    if "in" not in train.keys() or "out" not in train.keys():
        print('\nНекорректный ввод данных!\n'
              'Не удалось считать входные/выходные значения')
        return
    ws = []
    for w in mtrx['W']:
        ws.append(np.array(w))
    for i in range(len(ws)):
        print(f"\nМатрица весов W{i + 1} ({i + 1}-й слой): {ws[i]}")
    print(f"\nКоличество итераций: {par['n']}")
    print(f"\nСкорость обучения: {par['lrate']}")
    bp = BackPropagation(ws, par['n'], par['lrate'])
    xs = np.array(train["in"])
    ys = np.array(train["out"])
    bp.train(xs, ys)
    write_inf(bp.messages, out)    
if __name__ == '__main__':
    main()