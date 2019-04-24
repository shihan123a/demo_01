#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pandas as pd
import glob
import csv


def merge_csv(file_address):
    csv_list = glob.glob(file_address + '*.csv')
    print('该文件下下一共有', len(csv_list), '个csv文件需要合并')
    for one_csv in csv_list:
        print(one_csv)
    # read方法是以字符串形式获取内容
    one_open = open(one_csv, 'r').read()
    with open('D:/try/merge_result.csv', 'a') as f:
        f.write(one_open)
    print('合并{}个文件完成'.format(len(csv_list)))
    return 'D:/try/merge_result.csv'


def drop_duplicate(file):
    df = pd.read_csv(file)
    datalist = df.drop_duplicates()
    datalist.to_csv(file, header=False)
    print('去重操作完成')


if __name__ == '__main__':
    file_address = 'D:\\test_accounts1\\'
    merge_result = merge_csv(file_address)
    drop_duplicate(merge_result)
