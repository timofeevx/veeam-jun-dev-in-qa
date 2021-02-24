import math
import os.path
import subprocess


with open(file='file', mode='rt') as file:
    mypath = file.read().split()[0]  # Чтение файла;  .split()[0] - для избегания пустых строк
    if os.path.exists(mypath):  # Проверка на наличие пути
        lsblk = subprocess.Popen(['lsblk',  # Тянем данные субпроцессом из терминала (сразу декодируем его и разделим)
                                  '-o', 'PATH,TYPE,SIZE,FSAVAIL,FSTYPE,MOUNTPOINT', '--bytes', '--pair', mypath],
                                 stdout=subprocess.PIPE).stdout.read().decode().split()

        path = lsblk[0].split('"')[1]  # Проверяемый путь
        dtype = lsblk[1].split('"')[1]  # Тип устройста
        size = lsblk[2].split('"')[1]  # Объем диска - raw
        size = str(math.ceil(int(size) / 1073741824)) + 'G'  # Объем диска в Гигабайтах

        if dtype != 'disk':  # Проверка на устройство
            savail = lsblk[3].split('"')[1]  # Свободный объем - raw

            if savail != '':  # Проверка на пустое значение (если да, значит диск не прочитать)
                savail = str(math.ceil(int(savail) / 1048576)) + 'M'  # Свободный объем в Мегабайтах
            else:
                savail = 'not_available'  # Неиспользуемый раздел (напр. другая ОС)

            ftype = lsblk[4].split('"')[1]  # Тип фаловой системы
            mountpoint = lsblk[5].split('"')[1]  # Точка монтирования

        else:
            savail = ftype = mountpoint = ''  # Сброс значений если disk

        print(path, dtype, size, savail, ftype, mountpoint)  # Вывод

    else:
        print("Указанного пути не существует!")  # Вывод если ложный путь
