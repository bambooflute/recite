#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import time

# 格式化成2021-03-14 11:45:39形式
today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 将格式字符串转换为时间戳
time_stamp = time.mktime(time.strptime(today, "%Y-%m-%d %H:%M:%S"))
time_stamp = int(time_stamp)

# -----------------------------------------------------------------------------==
# 读取单词文件: 字典表
# -----------------------------------------------------------------------------==
data = xlrd.open_workbook('./data/00-dict.xls')   # 打开xls文件 
table = data.sheets()[0]  # 打开第一张表

# -----------------------------------------------------------------------------==
# 从excel表格中加载数据
# -----------------------------------------------------------------------------==
word_list = {}   # 单词表
word_record = {} # 每个单词的背诵情况 
# [group, status, excersice, passed, error]

nrows = table.nrows # 获取数据表的行数
for i in range(1, nrows):
    word = table.row_values(i)[2]
    word_list[word] = table.row_values(i)[3]
    word_record[word] = {'group' : table.row_values(i)[0], 'status' : table.row_values(i)[4], 'exercise': 0, 'passed': 0, 'error': 0, 'new': 'N', 'ReviewTime':0}
            
# -----------------------------------------------------------------------------==
# 从文件读取单词背诵记录
# -----------------------------------------------------------------------------==
try:
    f = open(r'./data/record.txt')
    for line in f.readlines():
#        print(line)
        values = line.split('\t' )
#        print(values[0])
#        print(values[1])
        a = values[1]
        b = a[1:-2]
        c = b.split(', ') 
        word_record[values[0]]['exercise'] = int(c[2].split(':')[1])
        word_record[values[0]]['passed'] = int(c[3].split(':')[1])
        word_record[values[0]]['error'] = int(c[4].split(':')[1])
        word_record[values[0]]['new'] = c[5].split(':')[1][2:-1]
        word_record[values[0]]['ReviewTime'] = int(c[6].split(':')[1][1:])
finally:
    f.close()

#print(word_record['different'])

# -----------------------------------------------------------------------------==
# 从文件中读取要背诵单词列表
# -----------------------------------------------------------------------------==
try:
    f = open(r'./data/new.txt')
    for line in f.readlines():
    #    print(line)
        new_word = line.strip()
        word_record[new_word]['status'] = 'todo-new'
#        print(values[0])
#        print(values[1])
finally:
    f.close()


# -----------------------------------------------------------------------------==
# 开始背单词
# -----------------------------------------------------------------------------==

while(True):
    print('\n')
    print('='*80)
    print('请选择学习模式')
    print('\t0: 退出')
    print('\t1: TODO：待背单词 ==> 拼写new.txt中的单词')
    print('\t2: TODO：待背单词 ==> 单词拼写')
    print('\t3: TODO：待背单词 ==> 词义回想')
    print('\t4: DONE：已背单词 ==> 重点记忆')
    print('\t5: DONE：已背单词 ==> 词义回想')
    print('\t6: 录入：未背单词 ==> 每天10个以上')
    print('-'*80)
    mode = input('输入学习模式：')
    print('='*80)
    print('\n')

    if(mode == '0'):
        break

    elif(mode == '1'):
        number = int(input('要练习的单词数：'))
        for key in word_list:
            if(word_record[key]['status']=='todo-new' and number > 0):
            # 显示单词
                print('\n\n')
                print('='*80)
                # print('\t\t' + key)
                # print('-'*80)
                print(word_list[key])
                print('='+'-'*78+'=')
                # 如练习次数太少，则要求拼写单词
                if(word_record[key]['exercise'] < 5):
                    word = input('【拼写练习】请输入单词：')
                    while(word != key):
                        word = input('拼写错误，请重新输入单词：')

                # 记录单词的练习情况
                word_record[key]['exercise'] += 1;
                word_record[key]['ReviewTime'] = time_stamp;
                number -= 1

                # 是否练习下一个，如练习下一个，这直接回车
                if(number > 0):
                    a = input('下一个？【Enter/N】')
                    if (a == 'N' or a == 'n'):
                        number = 0 

    elif(mode == '2'):
        number = int(input('要练习的单词数：'))
        for key in word_list:
            if(word_record[key]['status']=='todo' and number > 0):
                # 显示单词
                print('\n\n')
                print('='*80)
                print('\t\t' + key)
                print('-'*80)
                print(word_list[key])
                print('='+'-'*78+'=')
                
                # 如练习次数太少，则要求拼写单词
                if(word_record[key]['exercise'] < 5):
                    word = input('【拼写练习】请输入单词：')
                    while(word != key):
                        word = input('拼写错误，请重新输入单词：')

                # 记录单词的练习情况
                word_record[key]['exercise'] += 1;
                word_record[key]['ReviewTime'] = time_stamp;
                number -= 1

                # 是否练习下一个，如练习下一个，这直接回车
                if(number > 0 ):
                    a = input('下一个？【Enter/N】')
                    if (a == 'N' or a == 'n'):
                        number = 0 

    elif(mode == '3' ):        
        number = int(input('要练习的单词数：'))
        error_number = int(input('要练习的错过几次以上的单词：'))
        
        error_n = 0
        for key in word_record:
            if(word_record[key]['error'] >=error_number):
                error_n += 1

        if(error_n < number):
            print('注意：')
            print('\t想复习的单词数为：{}，错过{}次以上的单词数为：{}'.format(number, error_number, error_n))
            print('\t本次复习的单词数为：{}'.format(error_n))
            number = error_n

        for key in word_list:
            if(number>0 and word_record[key]['error'] >= error_number):
                if(word_record[key]['status']=='todo'):
                    # 显示单词
                    print('\n\n')
                    print('='*80)
                    print('\t' + key )
                    print('='+'-'*78+'=')
                    # 显示词义
                    a = input('\n\t显示词义【Enter】')
                    print('='+'-'*78+'=')
                    print( word_list[key] )
                    print('='*80)
                    # 是否显示下一个
                    a = input('\t下一个？【Y/N】')
                    if (a == 'N' or a == 'n'):
                        number = 0
                    #
                    word_record[key]['exercise'] += 1;
                    word_record[key]['ReviewTime'] = time_stamp;
                    number = number-1

    elif(mode == '4' ):
        group = int(input('组号：'))
        number = int(input('要复习的单词数：'))
        error_number = int(input('要复习的错过几次以上的单词：'))
        error_n = 0
        
        for key in word_record:
            if(word_record[key]['error'] >=error_number):
                error_n += 1

        if(error_n < number):
            print('注意：')
            print('\t想复习的单词数为：{}，错过{}次以上的单词数为：{}'.format(number, error_number, error_n))
            print('\t本次复习的单词数为：{}'.format(error_n))
            number = error_n

        for key in word_list:
            if(word_record[key]['group']==group and number>0 and word_record[key]['error'] >= error_number):
                if(word_record[key]['status']=='done'):
                    print('='+'-'*78+'=')
                    print( word_list[key] )
                    print('='+'-'*80+'=')

                    word = input('请输入单词：')
                    if(word == key):
                        word_record[key]['passed'] += 1;
                        print('\n\n')
                        print('-'*80)
                        print('\t\t正确! ')
                        print('-'*80)
                        print('\n\n')
                    else:
                        word_record[key]['error'] += 1;
                        print('\n\n')
                        print('-'*80)
                        print('\t\t错误！')
                        print('请重点记忆:\t', key )
                        print('-'*80)
                        print('\n\n')                    
                    word_record[key]['exercise'] += 1;
                    word_record[key]['ReviewTime'] = time_stamp;
                    number = number-1
                    
    elif(mode == '5' ):
        group = int(input('组号：'))
        number = int(input('要复习的单词数：'))
        error_number = int(input('要复习的错过几次以上的单词：'))
        error_n = 0
        
        for key in word_record:
            if(word_record[key]['error'] >=error_number):
                error_n += 1

        if(error_n < number):
            print('注意：')
            print('\t想复习的单词数为：{}，错过{}次以上的单词数为：{}'.format(number, error_number, error_n))
            print('\t本次复习的单词数为：{}'.format(error_n))
            number = error_n

        for key in word_list:
            if(word_record[key]['group']==group and number>0 and word_record[key]['error'] >= error_number):
                if(word_record[key]['status']=='done'):
                    print('\n\n')
                    print('='*80)
                    print('\t' + key )
                    print('='+'-'*78+'=')

                    a = input('\n\t显示词义【Enter】')
                    print('='+'-'*78+'=')
                    print( word_list[key] )
                    print('='*80)
                    
                    a = input('\t下一个？【Y/N】')
                    if (a == 'N' or a == 'n'):
                        number = 0
                    
                    word_record[key]['exercise'] += 1;
                    word_record[key]['ReviewTime'] = time_stamp;
                    number = number-1

    elif(mode == '6' ):
        number_done = 0
        for key in word_record:
            if(word_record[key]['status']=='done' or word_record[key]['new']=='Y'):
                number_done +=1

        print('='+'-'*78+'=')
        print('\t已背{}个单词'.format(number_done))
        print('='+'-'*78+'=')
        number = 0

        while(True):
            word=input('\n\n ==> 请录入新背诵的单词:  ')
            try:
                if(word_record[word]['status']=='done' or word_record[word]['new']=='Y'):
                    print('\n这是一个已背单词')
                    print('='*80)
                    print(word )
                    print('='+'-'*78+'=')
                    print(word_list[word] )
                    print('='*80)
                else:
                    print('\n这是一个新单词')
                    word_record[word]['new']='Y'
                    print('='*80)
                    print(word )
                    print('='+'-'*78+'=')
                    print( word_list[word] )
                    print('='*80)
                    number += 1
            except KeyError:
                print('\n\n=' + '-'*78 + '=')
                print('单词 {} 不在列表内'.format(word))
                print('=' + '-'*78 + '=')
            except:
                print('其他没有考虑到的异常，请找爸爸')
                
            a = input('已录入 {} 个单词，下一个？【Y/N】'.format(number))
            if (a == 'N' or a == 'n'):
                break
    else:
        print('输入正确的模式！\n')

# -----------------------------------------------------------------------------==
# 保存单词背诵记录
# -----------------------------------------------------------------------------==
try:
    f = open(r'./data/record.txt', 'w')
    for key in word_record:
        str_to_print = key + '\t'  + str(word_record[key]) + '\n' 
        f.writelines(str_to_print)

finally:
    f.close()
