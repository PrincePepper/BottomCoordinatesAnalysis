import math

from PIL import Image

# define and const
rows = 0
cols = 0
my_list = []
min_max_list = []
name_file = "data.txt"


# вычисления максимального и минимального значения в строке
def straight_min_max(l):
    return min(l), max(l)


# чтение файла
def ReadFile(NameFIle: str):
    global cols, rows
    with open(NameFIle, "r") as file:
        # итерация по строкам
        for line in file:
            temp = line.split()
            temp = list(map(float, temp))
            my_list.append(temp)
            if cols < len(temp):
                cols = len(temp)
            rows = rows + 1
            min_max_list.append(straight_min_max(temp))


# каст значений
def remap(value, fromLow, fromHigh, toLow, toHigh):
    return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow


# формула для определения коэффициента донного рассеяния
def FormulaDeterminateBottomScatterCoefficient(data: float, speedEnvironment, sensingRange: float,
                                               heightSeabed: float, dampingFactor: float, radiationIntensity: float):
    return (8 * math.pi) / (heightSeabed * speedEnvironment) * (sensingRange ** 2 + heightSeabed ** 2) ** (3 / 2) * \
           sensingRange * math.exp(2 * dampingFactor * (sensingRange ** 2 + heightSeabed ** 2) ** (1 / 2)) * \
           (data / radiationIntensity)


# формула логарифмической фильтрации гидроакустического сигнала
def logarithmicFilter(data, max_value: float, base: int):
    return 255 * math.log(((base - 1) * data) / max_value + 1, base)


# фильтр средней строки
def middleLineFilter(data: list, cols_list, rows_list):
    middle = [0] * cols_list
    for col in range(cols_list):
        for row in range(rows_list):
            middle[col] += data[row][col]
        middle[col] /= float(rows_list)
    return middle


# фильтр логарифмический
def findByFormulaLogarithmic(data: list, cols_list, rows_list):
    new_data = [[0.0 for _ in range(cols_list)] for _ in range(rows_list)]
    # new_data = [[0.0] * cols_list] * rows_list
    for row in range(rows_list):
        for col in range(cols_list):
            new_data[row][col] = logarithmicFilter(data[row][col], min_max_list[row][1], 10)
    return new_data


# фильтр определения коэффициента донного рассеяния
def findByFormulaBottomScatterCoefficient(data: list, cols_list, rows_list):
    # new_data = [[0] * cols_list] * rows_list
    new_data = [[0.0 for _ in range(cols_list)] for _ in range(rows_list)]
    for row in range(0, rows_list):
        for col in range(0, cols_list):
            new_data[row][col] = FormulaDeterminateBottomScatterCoefficient(data[row][col], 1450, 10, 10, 1, 10)
    return new_data


def draw_image(data, name: str, cols_list: int, rows_list: int, light: int = 1, R: float = 1.0, G: float = 1.0,
               B: float = 1.0):
    image = Image.new('RGB', (cols_list, rows_list), 'white')
    for row in range(rows_list):
        for col in range(cols_list):
            c = data[row][col]
            c = light * remap(c, min_max_list[row][0], min_max_list[row][1], 0, 255)
            image.putpixel((col, row), (round(c * R), round(c * G), round(c * B), 255))

    image.save(name)


def main():
    ReadFile(name_file)
    # a = middleLineFilter(my_list, cols, rows)
    b = findByFormulaLogarithmic(my_list, cols, rows)
    c = findByFormulaBottomScatterCoefficient(b, cols, rows)
    # for i in range(0, rows):
    #     for j in range(0, cols):
    #         if a[j] == 0:
    #             continue
    #         my_list[i][j] = my_list[i][j] / a[j]
    # draw_image(my_list, 'img1.png', cols, rows, light=700)
    # draw_image(b, 'img2.png', cols, rows, light=8)
    draw_image(c, 'img3.png', cols, rows)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
