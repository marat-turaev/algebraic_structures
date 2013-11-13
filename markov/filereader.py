#! /usr/bin/env python
# coding: utf8


def read_file(path):
    """
    Возвращает список слов из файла, находящегося по заданному пути path.
    """
    with open(path, 'r') as src:
        text = src.read().strip()
    return text.split('\n')


def read_grf():
    """
    Возвращает список слов из файла 'texts/grf_processed_6.txt',
    содержащего обработанные задачи с замененными формулами.
    """
    return read_file('texts/grf_processed_6.txt')
