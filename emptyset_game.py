import pygame
from pygame.locals import *
import sys
from fractions import Fraction
import math
import random
import time
import copy
import itertools
import sys
from operator import itemgetter
import statistics as st
import statistics
from time import sleep




#約分する関数
def about_minutes(x, y):
    if y >= 2:
        if isinstance(x, int):
            while math.sqrt(x).is_integer() and y >= 2:
                x = int(math.sqrt(x))
                y = int(y/2)
        else:
            while math.sqrt(x.numerator).is_integer() and math.sqrt(x.denominator).is_integer() and y >= 2:
                x = Fraction(int(math.sqrt(x.numerator)),
                             int(math.sqrt(x.denominator)))
                y = int(y/2)
    if isinstance(x,Fraction) and x.denominator == 1:
        x = int(x)
    return x, y


#集合を一意にする関数
def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]


#盤面更新の関数
def board_update(my, your, our):
    my += our
    your += our

    #約分
    for i in range(len(my)):
        (my[i][0], my[i][1]) = about_minutes(my[i][0], my[i][1])

    for i in range(len(your)):
        (your[i][0], your[i][1]) = about_minutes(your[i][0], your[i][1])

    #集合を一意にする
    my = get_unique_list(my)
    your = get_unique_list(your)

    #A,Bから共通集合をつくる
    remove_list = []
    our = []
    for i in my:
        if i in your:
            our.append(i)
            remove_list.append(i)

    for i in remove_list:
        my.remove(i)
        your.remove(i)

    our = get_unique_list(our)

    return my, your, our


def number_return(number):
    if number == 0: return [1,1]
    if number == 1: return [2,1]
    if number == 2: return [3,1]
    if number == 3: return [Fraction(1, 2),1]
    if number == 4: return [Fraction(1, 3),1]
    if number == 5: return [Fraction(2, 3),1]
    if number == 6: return [2,2]
    if number == 7: return [3,2]




def multiply(Pointer, set, number):
    if set[Pointer][1] == number[1]:
        set[Pointer][0] = Fraction(set[Pointer][0]*number[0])
    if set[Pointer][1] > number[1]:
        set[Pointer][0] = Fraction(set[Pointer][0]*(number[0]**Fraction(set[Pointer][1]/number[1])))
    if set[Pointer][1] < number[1]:
        set[Pointer][0] = Fraction(number[0]*(set[Pointer][0]**Fraction(number[1]/set[Pointer][1])))
        set[Pointer][1] = number[1]

def inverse(f):return Fraction(f.denominator, f.numerator)

def division(Pointer, set, number):
    if set[Pointer][1] == number[1]:
        set[Pointer][0] = Fraction(set[Pointer][0]*inverse(number[0]))
    if set[Pointer][1] > number[1]:
        set[Pointer][0] = Fraction(set[Pointer][0]*inverse(number[0]**Fraction(set[Pointer][1]/number[1])))
    if set[Pointer][1] < number[1]:
        set[Pointer][0] = Fraction(inverse(number[0])*(set[Pointer][0]**Fraction(number[1]/set[Pointer][1])))
        set[Pointer][1] = number[1]

def isLegal(checker, pointer):
    #インデックスエラー対策のため、０枚や、３枚以上選択されている場合をはじく
    if len(checker) >= 3 or len(checker) == 0:
        return 1

    #選択されている枚数が１枚または２枚のとき、合法手かどうか判定する
    else:

        #選択枚数が１枚のとき
        if len(checker) == 1:

            #二乗とルートのカードの時以外エラーと処理
            #二乗とルートのカードのときでも、数字が選択されていないときはエラー
            if not (checker[0] == 11 or checker[0] == 12):
                return 1
            else:
                if pointer >= 200:
                    return 1

        #選択枚数が２枚のとき
        if len(checker) == 2:

            #無限集合カードのときを処理
            #２枚目のカードが and か \ のとき以外エラーと処理
            # and \ であっても集合が選択されていないときはエラー
            if checker[0] == 19 or checker[0] == 18 or checker[0] == 17:
                if not (checker[1] == 9 or checker[1] == 10):
                    return 1
                else:
                    if not (pointer == 200 or pointer == 300):
                        return 1

            # B のときを処理
            # or and \ のとき以外エラーと処理
            #対象とする集合がAじゃないとき、エラーと処理
            if checker[0] == 16:
                if not (checker[1] == 8 or checker[1] == 9 or checker[1] == 10):
                    return 1
                else:
                    if pointer != 200:
                        return 1

            # A のときを処理
            # or and \ のとき以外エラーと処理
            #対象とする集合がBじゃないとき、エラーと処理
            if checker[0] == 15:
                if not (checker[1] == 8 or checker[1] == 9 or checker[1] == 10):
                    return 1
                else:
                    if pointer != 300:
                        return 1

            # ×　÷　のときを処理
            #２枚目のカードが数字じゃないときエラーと処理
            #pointerで数字がえらばれていないとエラーと処理
            if checker[0] == 13 or checker[0] == 14:
                if checker[1] >= 8:
                    return 1
                else:
                    if pointer >= 200:
                        return 1

            if checker[0] == 11 or checker[0] == 12:
                return 1

            # \ を処理
            #２枚目のカードが数字じゃないときエラーと処理
            #pointerで集合が選択されていないときエラーと処理

            # 重要！！！
            #　盤面にないカードを抜こうとすると、単純に２枚捨てたのと同じ効果になりますが、汚いのでエラー処理にしますか？
            if checker[0] == 10:
                if checker[1] >= 8:
                    return 1
                else:
                    if not (pointer == 200 or pointer == 300):
                        return 1

            # and カードが１枚目のときはエラー
            if checker[0] == 9:
                return 1

            # or カードのときの処理
            # or カード２枚のときはエラー
            # 集合が選択されていないときはエラー

            # 重要！！！
            #　盤面にあるカードを追加しようとすると、単純に２枚捨てたのと同じ効果になりますが、汚いのでエラー処理にしますか？
            if checker[0] == 8:
                if checker[1] == 8:
                    return 1
                else:
                    if not (pointer == 200 or pointer == 300):
                        return 1

            #数字だけしか選択していないときはエラー
            if checker[0] <= 7:
                return 1

    return 0

def return_Legal_move(my_life, our_life, your_life, cards):
    able_list = []
    for i in range(len(my_life)):
        for j in cards:
            check_list = []
            check_list.append(j)
            if isLegal(check_list, i) == 0:
                check_list.append(i)
                able_list.append(check_list)

        for j in cards:
            for k in cards:
                check_list = []
                check_list.append(j)
                check_list.append(k)
                check_list.sort(reverse=True)
                if isLegal(check_list, i) == 0:
                    check_list.append(i)
                    able_list.append(check_list)

    for i in range(len(our_life)):
        for j in cards:
            check_list = []
            check_list.append(j)
            if isLegal(check_list, i+50) == 0:
                check_list.append(i+50)
                able_list.append(check_list)

        for j in cards:
            for k in cards:
                check_list = []
                check_list.append(j)
                check_list.append(k)
                check_list.sort(reverse=True)
                if isLegal(check_list, i+50) == 0:
                    check_list.append(i+50)
                    able_list.append(check_list)

    for i in range(len(your_life)):
        for j in cards:
            check_list = []
            check_list.append(j)
            if isLegal(check_list, i+100) == 0:
                check_list.append(i+100)
                able_list.append(check_list)

        for j in cards:
            for k in cards:
                check_list = []
                check_list.append(j)
                check_list.append(k)
                check_list.sort(reverse=True)
                if isLegal(check_list, i+100) == 0:
                    check_list.append(i+100)
                    able_list.append(check_list)

    for j in cards:
        for k in cards:
            check_list = []
            check_list.append(j)
            check_list.append(k)
            check_list.sort(reverse=True)
            if isLegal(check_list, 200) == 0:
                check_list.append(200)
                able_list.append(check_list)
    for j in cards:
        for k in cards:
            check_list = []
            check_list.append(j)
            check_list.append(k)
            check_list.sort(reverse=True)
            if isLegal(check_list, 300) == 0:
                check_list.append(300)
                able_list.append(check_list)

    able_list = get_unique_list(able_list)
    return able_list

def isEmpty(set,our):
    if len(set) == 0 and len(our) == 0:
        return True
    else:
        return False

def do_move(my, our, your, move, pointer):
    my_life = copy.deepcopy(my)
    our_life = copy.deepcopy(our)
    your_life = copy.deepcopy(your)
    checker = [] #選択されているカードを格納するリスト
    # print(my,our,your)
    # print(my_life,our_life, your_life)

    #選択されているカードをcheckerに格納し、降順に並びかえ
    for i in move:
        checker.append(i)
    checker.sort(reverse=True)


    if len(checker) == 0:
        return my_life, our_life, your_life

    
    #１枚目が無理数、有理数、自然数のときの処理
    if checker[0] == 19 or checker[0] == 18 or checker[0] == 17:
        if pointer == 200:
            if checker[1] == 10:
                remove_list = []
                for i in my_life:
                    if (i[1] >= 2 and checker[0] == 19) or (i[1] == 1 and checker[0] == 18) or (i[1] == 1 and isinstance(i[0], int) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    my_life.remove(i)
                remove_list = []
                for i in our_life:
                    if (i[1] >= 2 and checker[0] == 19) or (i[1] == 1 and checker[0] == 18) or (i[1] == 1 and isinstance(i[0], int) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    our_life.remove(i)

            if checker[1] == 9:
                remove_list = []
                for i in my_life:
                    if (i[1] == 1 and checker[0] == 19) or (i[1] >= 2 and checker[0] == 18) or ((i[1] >= 2 or (i[1] == 1 and isinstance(i[0], Fraction))) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    my_life.remove(i)
                remove_list = []
                for i in our_life:
                    if (i[1] == 1 and checker[0] == 19) or (i[1] >= 2 and checker[0] == 18) or ((i[1] >= 2 or (i[1] == 1 and isinstance(i[0], Fraction))) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    our_life.remove(i)

        if pointer == 300:
            if checker[1] == 10:
                remove_list = []
                for i in your_life:
                    if (i[1] >= 2 and checker[0] == 19) or (i[1] == 1 and checker[0] == 18) or (i[1] == 1 and isinstance(i[0], int) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    your_life.remove(i)
                remove_list = []
                for i in our_life:
                    if (i[1] >= 2 and checker[0] == 19) or (i[1] == 1 and checker[0] == 18) or (i[1] == 1 and isinstance(i[0], int) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    our_life.remove(i)
            if checker[1] == 9:
                remove_list = []
                for i in your_life:
                    if (i[1] == 1 and checker[0] == 19) or (i[1] >= 2 and checker[0] == 18) or ((i[1] >= 2 or (i[1] == 1 and isinstance(i[0], Fraction))) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    your_life.remove(i)
                remove_list = []
                for i in our_life:
                    if (i[1] == 1 and checker[0] == 19) or (i[1] >= 2 and checker[0] == 18) or ((i[1] >= 2 or (i[1] == 1 and isinstance(i[0], Fraction))) and checker[0] == 17):
                        remove_list.append(i)
                for i in remove_list:
                    our_life.remove(i)

                
    #１枚目がBのとき処理
    if checker[0] == 16:
        if pointer == 200:
            if checker[1] == 10: our_life = []
            if checker[1] == 9: my_life = []
            if checker[1] == 8:
                our_life += your_life
                your_life = []

    #１枚目がAのとき処理
    if checker[0] == 15:
        if pointer == 300:
            if checker[1] == 10: our_life = []
            if checker[1] == 9: your_life = []
            if checker[1] == 8: 
                our_life += my_life
                my_life = []

    #１枚目（１枚が）÷のとき処理
    if checker[0] == 14:
        if 0 <= pointer <= 49: division(pointer, my_life, number_return(checker[1]))
        if 50 <= pointer <= 99: division(pointer-50, our_life, number_return(checker[1]))
        if 100 <= pointer <= 149: division(pointer-100, your_life, number_return(checker[1]))

    #１枚目が×のとき処理
    if checker[0] == 13:
        if 0 <= pointer <= 49: multiply(pointer, my_life, number_return(checker[1]))
        if 50 <= pointer <= 99: multiply(pointer-50, our_life, number_return(checker[1]))
        if 100 <= pointer <= 149: multiply(pointer-100, your_life, number_return(checker[1]))
            
    #１枚目が√のとき処理
    if checker[0] == 12:
        if 0 <= pointer <= 49:
            my_life[pointer][1] = my_life[pointer][1]*2
        if 50 <= pointer <= 99:
            our_life[pointer-50][1] = our_life[pointer-50][1]*2
        if 100 <= pointer <= 149:
            your_life[pointer-100][1] = your_life[pointer-100][1]*2

    #１枚目が二乗のとき処理
    if checker[0] == 11:
        if 0 <= pointer <= 49:
            my_life[pointer][0] = my_life[pointer][0]**2
        if 50 <= pointer <= 99:
            our_life[pointer-50][0] = our_life[pointer-50][0]**2
        if 100 <= pointer <= 149:
            your_life[pointer-100][0] = your_life[pointer-100][0]**2
    
    #１枚目が \ のとき処理
    if checker[0] == 10:
        if pointer == 200:
            if number_return(checker[1]) in my_life or number_return(checker[1]) in our_life:
                if number_return(checker[1]) in my_life: my_life.remove(number_return(checker[1]))
                if number_return(checker[1]) in our_life: our_life.remove(number_return(checker[1]))
                
        if pointer == 300:
            if number_return(checker[1]) in your_life or number_return(checker[1]) in our_life:
                if number_return(checker[1]) in your_life: your_life.remove(number_return(checker[1]))
                if number_return(checker[1]) in our_life: our_life.remove(number_return(checker[1]))

    #１枚目が or のとき処理
    if checker[0] == 8:
        if pointer == 200: my_life.append(number_return(checker[1]))
        if pointer == 300: your_life.append(number_return(checker[1]))

    #ボードを綺麗にする
    (my_life, your_life, our_life) = board_update(my_life, your_life, our_life)

    return my_life, our_life , your_life



def how_much_card(my):
    counter = [0,0,0]
    for i in my:
        if i[1] == 1 and isinstance(i[0],int) and counter[0] == 0:
            counter[0] += 1
        if i[1] == 1 and isinstance(i[0], Fraction) and counter[1] == 0:
            counter[1] += 1
        if i[1] >= 2 and counter[2] == 0:
            counter[2] += 1
    return sum(counter)

# def how_easy_extract(my, status_point):
#     check_list = [[Fraction(1, 81), 1], [Fraction(1, 36), 1], [Fraction(1, 27), 1], [Fraction(4, 81), 1], [Fraction(1, 18), 1], [Fraction(1, 16), 1], [Fraction(2, 27), 1], [Fraction(1, 12), 1], [Fraction(1, 9), 1], [Fraction(1, 8), 1], [Fraction(4, 27), 1], [Fraction(1, 6), 1], [Fraction(16, 81), 1], [Fraction(2, 9), 1], [Fraction(1, 4), 1], [Fraction(8, 27), 1], [Fraction(1, 3), 1], [Fraction(3, 8), 1], [Fraction(4, 9), 1], [Fraction(1, 2), 1], [Fraction(9, 16), 1], [Fraction(2, 3), 1], [Fraction(3, 4), 1], [Fraction(8, 9), 1], [1, 1], [Fraction(9, 8), 1], [Fraction(4, 3), 1], [Fraction(3, 2), 1], [Fraction(16, 9), 1], [2, 1], [Fraction(9, 4), 1], [Fraction(8, 3), 1], [3, 1], [4, 1], [Fraction(9, 2), 1], [6, 1], [Fraction(27, 4), 1], [8, 1], [9, 1], [12, 1], [Fraction(27, 2), 1], [16, 1], [18, 1], [Fraction(81, 4), 1], [27, 1], [36, 1], [81, 1], [Fraction(1, 243), 2], [Fraction(1, 162), 2], [Fraction(1, 108), 2], [Fraction(1, 72), 2], [Fraction(4, 243), 2], [Fraction(1, 54), 2], [Fraction(1, 48), 2], [Fraction(2, 81), 2], [Fraction(1, 32), 2], [Fraction(1, 27), 2], [Fraction(1, 24), 2], [Fraction(1, 18), 2], [Fraction(16, 243), 2],
#      [Fraction(2, 27), 2], [Fraction(1, 12), 2], [Fraction(8, 81), 2], [Fraction(1, 8), 2], [Fraction(4, 27), 2], [Fraction(1, 6), 2], [Fraction(3, 16), 2], [Fraction(2, 9), 2], [Fraction(9, 32), 2], [Fraction(8, 27), 2], [Fraction(1, 3), 2], [Fraction(3, 8), 2], [Fraction(32, 81), 2], [Fraction(1, 2), 2], [Fraction(16, 27), 2], [Fraction(2, 3), 2], [Fraction(3, 4), 2], [Fraction(8, 9), 2], [Fraction(9, 8), 2], [Fraction(4, 3), 2], [Fraction(3, 2), 2], [Fraction(27, 16), 2], [2, 2], [Fraction(8, 3), 2], [3, 2], [Fraction(27, 8), 2], [Fraction(32, 9), 2], [Fraction(9, 2), 2], [Fraction(16, 3), 2], [6, 2], [Fraction(27, 4), 2], [8, 2], [Fraction(81, 8), 2], [12, 2], [Fraction(27, 2), 2], [Fraction(243, 16), 2], [18, 2], [24, 2], [27, 2], [32, 2], [Fraction(81, 2), 2], [48, 2], [54, 2], [Fraction(243, 4), 2], [72, 2], [108, 2], [162, 2], [243, 2], [Fraction(2, 81), 4], [Fraction(1, 27), 4], [Fraction(1, 8), 4], [Fraction(3, 16), 4], [Fraction(2, 9), 4], [Fraction(1, 3), 4], [Fraction(1, 2), 4], [Fraction(3, 4), 4], [2, 4], [3, 4], [Fraction(81, 8), 4], [Fraction(243, 16), 4], [32, 4], [48, 4], [162, 4], [243, 4]]
#     counter = 0
#     for i in my:
#         for j in range(124):
#             if i == check_list[j]:
#                 counter += status_point[j]
    
#     return counter


def how_easy_extract(my):
    counter = 0
    for i in my:
        if i == [1, 1] or i == [2, 1] or i == [3, 1] or i == [Fraction(1, 2), 1] or i == [Fraction(1, 3), 1] or i == [Fraction(2, 3), 1] or i == [2, 2] or i == [3, 2]:
            counter += 1
    
    counter = len(my)  - counter
    return counter

def return_card_point(card_point, card, trash):
    check_list = [[0,9], [1,9], [2,9], [3,9], [4,9], [5,9], [6,9], [7,9],
                  [0,10], [1,10], [2,10], [3,10], [4,10], [5,10], [6,10], [7,10], [10,17], [10,18], [10, 19],
                  [1,13], [2,13], [3,13], [4,13], [5,13], [6,13], [7,13],
                  [1,14], [2,14], [3,14], [4,14], [5,14], [6,14], [7,14],
                  [8,17], [8,18], [8,19]]
    counter = 0
    for i in card:
        counter += card_point[i]
    

    for i in itertools.combinations(card, 2):
        i = list(i)
        i.sort()
        for j in range(36):
            if i == check_list[j]:
                counter += card_point[j+20]
    
    if len(card) != 7:
        Cards = [0,0,0,1,1,1,1,2,2,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8,8,8,8,8,9,9,10,10,10,10,10,10,10,11,11,11,12,12,12,13,13,13,13,14,14,14,14,15,16,17,18,19]
        average = 0
        for i in trash:
            Cards.remove(i)
        for i in Cards:
            average += card_point[i]
        average = round(average/len(Cards), 4)
        counter += average*(7 - len(card))

    return counter


def Evaluation_function(vector, card_point, status, my, our, your, card, trash):
    if isEmpty(your, our) and isEmpty(my, our):
        return -10000
    elif isEmpty(your, our):
        return 10000

    return (vector[0] * return_card_point(card_point, card, trash)
            + vector[1] * (len(my) - len(your))
            + vector[2] * (status[how_much_card(my)*16 +
                                  how_much_card(our)*4 + how_much_card(your)])
            + vector[3] * (how_easy_extract(my) - how_easy_extract(your))
            + vector[4] * (how_easy_extract(our))
            )



def return_best_move(vector, card_point, status, my_life, our_life, your_life, my_cards, turn2, trash):
    return_move = [400]
    ok_flag = [0]
    Evaluation_function_point = -10000

    for i in return_Legal_move(my_life, our_life, your_life, my_cards):
        i2 = copy.copy(i)
        pointer = i2[-1]
        del(i2[-1])
        do_move_list = do_move(my_life, our_life, your_life, i2, pointer)
        my_cards2 = copy.copy(my_cards)
        for j in i2:
            my_cards2.remove(j)

        if (turn2 == 0 and Evaluation_function_point < Evaluation_function(vector, card_point, status, do_move_list[0], do_move_list[1], do_move_list[2], my_cards2, trash)) or (turn2 == 1 and Evaluation_function_point < Evaluation_function(vector, card_point, status, do_move_list[2], do_move_list[1], do_move_list[0], my_cards2, trash)):

            if turn2 == 0:
                Evaluation_function_point = Evaluation_function(
                    vector, card_point, status, do_move_list[0], do_move_list[1], do_move_list[2], my_cards2, trash)
            if turn2 == 1:
                Evaluation_function_point = Evaluation_function(
                    vector, card_point, status, do_move_list[2], do_move_list[1], do_move_list[0], my_cards2, trash)

            return_move = copy.copy(i2)
            return_move.append(pointer)

    for i in range(8):
        for j in itertools.combinations(my_cards, i):
            j = list(j)

            if (turn2 == 0 and Evaluation_function_point < Evaluation_function(vector, card_point, status, my_life, our_life, your_life, j, trash)) or (turn2 == 1 and Evaluation_function_point < Evaluation_function(vector, card_point, status, your_life, our_life, my_life, j, trash)):
                if turn2 == 0:
                    Evaluation_function_point = Evaluation_function(
                        vector, card_point, status,my_life, our_life, your_life, j, trash)
                if turn2 == 1:
                    Evaluation_function_point = Evaluation_function(
                        vector, card_point, status,your_life, our_life, my_life, j, trash)
                ok_flag[0] = 1
                return_move = j

    ok_flag += return_move
    return ok_flag

   
    
    


def main():

    (w, h) = (800, 600)  # 画面サイズ
    pygame.init()       # pygame初期化
    pygame.display.set_mode((w, h), 0, 32)  # 画面設定
    screen = pygame.display.get_surface()

    
    title_flag = 1
    (mouse_x, mouse_y) = (0, 0)
    mouse_button = 0
    lose_flag = 0
    lose_flag2 = 0

    lose_counter2 = 0
    win_flag = 0
    win_counter = 0


    
    while (1):
        lose_flag = 0
        pygame.display.update()  
        pygame.time.wait(30)        
        screen.fill((255,255,255)) 
        pygame.draw.circle(screen, (0, 0, 0), (400, 200), 100)
        pygame.draw.circle(screen, (255, 255, 255), (400, 200), 90)
        pygame.draw.line(screen, (0, 0, 0), (300, 300), (500, 100),10)
        font_level = pygame.font.Font(None, 40)
        pygame.draw.rect(screen, (0, 0, 0), Rect(200, 400, 400, 40),5)
        level_message = font_level.render("start" , True, (255, 0, 0))
        screen.blit(level_message, [360, 407])

        
        if 200 < mouse_x < 600 and 400 < mouse_y < 440  and mouse_button == 1:
            mouse_button = 0
            title_flag = 2
            
    

        
        if lose_flag2 == 1 and lose_counter2 <= 80:
            screen.fill((255, 255, 255))
            font_lose = pygame.font.Font(None, 150)
            lose_message = font_lose.render("YOU LOSE", True, (255, 0, 0))
            screen.blit(lose_message, [100, 200])
            lose_counter2 += 1
            if lose_counter2 == 80:
                lose_flag2 = 0

        if win_flag == 1 and win_counter <= 80:
            screen.fill((255, 255, 255))
            font_lose = pygame.font.Font(None, 150)
            lose_message = font_lose.render("YOU WIN", True, (255, 0, 0))
            screen.blit(lose_message, [100, 200])
            win_counter += 1
            if win_counter == 80:
                win_flag = 0

        


                
            

        # 終了用のイベント処理
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_button = 1
            # 閉じるボタンが押されたとき
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キーを押したとき
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()
            
            




        if title_flag == 2:

            (mouse_x, mouse_y) = (0, 0)
            check_flag = [0, 0, 0, 0, 0, 0, 0]
            go_flag = 0
            mouse_button = 0
            pointer = 400
            orange = (255, 165, 0)
            black = (0, 0, 0)
            white = (255, 255, 255)
            color_A = black
            color_B = black
            turn = 0


            
            font = pygame.font.Font(None, 50)
            font2 = pygame.font.Font(None, 40)
            errorflag = 0
            error_flag_counter = 0
            your_go_card = []
            my_go_life = []
            our_go_life = []
            your_go_life = []
            your_original_card = []

            your_go_card_flag = 0
            your_go_card_flag_counter = 0

            
            vector = [1, 2.2364, 5.7272, 2.3496, -0.0189]
            card_point = [0.0122, 0.0068, -0.0203, -0.0011, -0.1591, 0.0833, -0.0676, -0.0424, 0.0856, 0.0047, -0.0203, 0.0012, 0.0051, 0.0091, -0.0356, 0.1694, 0.0805, 0.4056, 0.4292, -0.1973, -0.2814, 0.003, -0.0001, 0.3624, 0.0033, -0.3043, -0.02,
                            0.2284, 0.0025, -0.0433, -0.0959, -0.0031, 0.0113, -0.27, -0.0041, -0.013, -0.0394, -0.0003, 0.2244, 0.0124, -0.0053, -0.06, 0.0313, 0.1532, -0.0032, -0.0226, -0.0343, -0.0028, 0.002, 0.0416, 0.0022, -0.0014, 0.0021, 0.0049, 0.0709, 0.0133]
            status = [0.0, 0.0, 0.0, 0.0, -0.0123, -0.055, 0.2779, 0.1289, 0.0492, 0.2222, 0.0534, -0.005, 0.2293, 0.073, 0.1438, -0.0001, 0.0, -0.2869, 0.222, -0.0052, 0.0494, 0.3418, 0.165, -0.0001, 0.0398, 0.2808, -0.0245, 0.1076, -0.0156, 0.0068, -0.0293, 0.0465,
                        0.0, -0.0978, 0.0127, -0.1033, -0.003, -0.2469, 0.0789, 0.2536, 0.0954, -0.0631, 0.0065, 0.0014, -0.321, -0.0815, -0.0056, 0.255, 0.0, -0.0021, 0.0496, -0.0134, 0.0181, 0.0063, -0.0089, 0.0219, -0.0092, 0.0055, -0.1714, -0.0088, -0.0084, 0.0071, 0.0227, -0.1487]
        
        
            # vector = [1, 83.8, 10.4, 0.57]
            # card_point = [1, 14.8, 70.3, 35, -0.58, 114, 36.3]
            #   手動
            # vector = [2, 1.5, 1.2, 0.5]
            # card_point = [1, 1.1, 1.8, 1, 0.8, 3, 2.2]
            #機械1
            # vector = [1, 142.07, 28.82, 11.73]
            # card_point = [1, 100.67, 36.55, 34.86, -5.82, -20.52, 44.38]
            #機械2
            
            my_cards = []
            text_cards = {}
            text_cards2 = {}
            cards = [0,0,0,1,1,1,1,2,2,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8,8,8,8,8,9,9,10,10,10,10,10,10,10,11,11,11,12,12,12,13,13,13,13,14,14,14,14,15,16,17,18,19]
            for i in range(7):
                j = random.choice(cards)
                my_cards.append(j)
                cards.remove(j)
            my_cards.sort()

            your_cards = []
            for i in range(7):
                j = random.choice(cards)
                your_cards.append(j)
                cards.remove(j)
            your_cards.sort()

            my_life = []
            my_life.append(number_return(random.randrange(2)))
            my_life.append(number_return(random.randrange(3,5,1)))
            my_life.append(number_return(random.randrange(6,7,1)))

            your_life = []
            your_life.append(number_return(random.randrange(2)))
            your_life.append(number_return(random.randrange(3,5,1)))
            your_life.append(number_return(random.randrange(6,7,1)))

            our_life = []

            (my_life, your_life, our_life) = board_update(my_life, your_life, our_life)

            trash = []

            # 描画する文字列の設定
            text_cards[0] = font.render("1", True, black)
            text_cards[1] = font.render("2", True, black)
            text_cards[2] = font.render("3", True, black)
            text_cards[3] = font2.render("1/2", True, black)
            text_cards[4] = font2.render("1/3", True, black)
            text_cards[5] = font2.render("2/3", True, black)
            text_cards[6] = font2.render("√2", True, black)
            text_cards[7] = font2.render("√3", True, black)
            text_cards[8] = font2.render("U", True, black)
            text_cards[9] = font2.render("U", True, black)
            text_cards[9] = pygame.transform.rotate(text_cards[9], 180)
            text_cards[10] = font2.render('\\', True, black)
            text_cards[11] = font2.render("x", True, black)
            text_cards[12] = font2.render("√", True, black)
            text_cards[13] = font2.render("×", True, black)
            text_cards[14] = font2.render("÷", True, black)
            text_cards[15] = font2.render("A", True, black)
            text_cards[16] = font2.render("B", True, black)
            text_cards[17] = font2.render("N", True, black)
            text_cards[18] = font2.render("Q", True, black)
            font_ir = pygame.font.Font(None, 35)
            text_cards[19] = font_ir.render("R\\Q", True, black)
            font_up = pygame.font.Font(None, 20)
            text_cards[20] = font_up.render("2", True, black)
            

            text_cards2[0] = "1"
            text_cards2[1] = "2"
            text_cards2[2] = "3"
            text_cards2[3] = "1/2"
            text_cards2[4] = "1/3"
            text_cards2[5] = "2/3"
            text_cards2[6] = "√2"
            text_cards2[7] = "√3"
            text_cards2[8] = "U"
            text_cards2[9] = "U"
            text_cards2[10] ='\\'
            text_cards2[11] ="x"
            text_cards2[12] ="√"
            text_cards2[13] ="×"
            text_cards2[14] ="÷"
            text_cards2[15] = "A"
            text_cards2[16] = "B"
            text_cards2[17] = "N"
            text_cards2[18] = "Q"
            text_cards2[19] = "R\\Q"

            

            while not(isEmpty(my_life, our_life) or isEmpty(your_life, our_life)):
                if turn == 2:
                    turn = 1
                if turn == 3:
                    turn = 0


                if turn == 1:
                    if your_go_card_flag == 0:
                        move = return_best_move(
                            vector, card_point, status, my_life, our_life, your_life, your_cards, 1, trash)
                        
                        if move[0] == 0:
                            move3 = copy.copy(move)
                            del (move3[0])
                            pointer = move3[-1]
                            del (move3[-1])
                            if isEmpty(do_move(my_life,our_life,your_life,move3,pointer)[0],do_move(my_life,our_life,your_life,move3,pointer)[1]):
                                lose_flag = 1

                        your_go_card = copy.copy(move)
                        my_go_life = copy.copy(my_life)
                        our_go_life = copy.copy(our_life)
                        your_go_life = copy.copy(your_life)
                        your_original_card = copy.copy(your_cards)

                        your_go_card_flag = 1
                        your_go_card_flag_counter = 0

                    if your_go_card_flag == 3:
                        if move[0] == 0:
                            move2 = copy.copy(move)
                            del (move2[0])
                            pointer = move2[-1]
                            del (move2[-1])
                            (my_life, our_life, your_life) = do_move(my_life,our_life,your_life,move2,pointer)
                            for i in move2:
                                your_cards.remove(i)
                                trash.append(i)
                            for i in range(7-len(your_cards)):
                                if len(cards)==0:
                                    cards = [0,0,0,1,1,1,1,2,2,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8,8,8,8,8,9,9,10,10,10,10,10,10,10,11,11,11,12,12,12,13,13,13,13,14,14,14,14,15,16,17,18,19]
                                    trash = []
                                    for j in my_cards:
                                        cards.remove(j)
                                    for j in your_cards:
                                        cards.remove(j)
                                j = random.choice(cards)
                                your_cards.append(j)
                                cards.remove(j)
                            your_cards.sort()
                            pointer = 400
                            

                        if move[0] == 1:
                            move2 = copy.copy(move)
                            del (move2[0])
                            for i in your_cards:
                                trash.append(i)
                            your_cards = []
                            your_cards += move2
                            for i in move2:
                                trash.remove(i)
                            

                            for i in range(7-len(your_cards)):
                                if len(cards)==0:
                                    cards = [0,0,0,1,1,1,1,2,2,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8,8,8,8,8,9,9,10,10,10,10,10,10,10,11,11,11,12,12,12,13,13,13,13,14,14,14,14,15,16,17,18,19]
                                    trash = []
                                    for j in my_cards:
                                        cards.remove(j)
                                    for j in your_cards:
                                        cards.remove(j)
                                j = random.choice(cards)
                                your_cards.append(j)
                                cards.remove(j)
                            your_cards.sort()
                            pointer = 400
                        your_go_card_flag = 0
                        your_go_card_flag_counter = 0
                        turn = 3

                if turn == 0:
                    if go_flag == 1:
                        ok_flag = 0  # 合法手かどうか判定するフラグ
                        checker = []  # 選択されているカードを格納するリスト

                        for i in range(7):
                            if check_flag[i] == 1:
                                checker.append(my_cards[i])

                        checker.sort(reverse=True)
                        ok_flag = isLegal(checker, pointer)

                        if ok_flag == 0:
                            (my_life,our_life,your_life) = do_move(my_life, our_life, your_life, checker, pointer)
                            (my_life, your_life, our_life) = board_update(
                                my_life, your_life, our_life)
                            for i in range(len(checker)):
                                if len(cards)==0:
                                    cards = [0,0,0,1,1,1,1,2,2,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8,8,8,8,8,9,9,10,10,10,10,10,10,10,11,11,11,12,12,12,13,13,13,13,14,14,14,14,15,16,17,18,19]
                                    trash = []
                                    for j in my_cards:
                                        cards.remove(j)
                                    for j in your_cards:
                                        cards.remove(j)
                                j = random.choice(cards)
                                    
                                my_cards.append(j)
                                cards.remove(j)
                            for i in checker:
                                my_cards.remove(i)
                                trash.append(i)
                            for i in range(7):check_flag[i] = 0
                            pointer = 400
                            my_cards.sort()
                            turn = 2


                        if ok_flag == 1:
                            errorflag = 1
                            error_flag_counter = 0
                        

                    if go_flag == 2:
                        counter = 0
                        checker = []
                        for i in range(7):
                            if check_flag[i] == 1:
                                checker.append(my_cards[i])
                                check_flag[i] = 0
                                counter += 1
                        for i in checker:
                            my_cards.remove(i)
                            trash.append(i)
                        for i in range(counter):
                            if len(cards)==0:
                                cards = [0,0,0,1,1,1,1,2,2,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8,8,8,8,8,9,9,10,10,10,10,10,10,10,11,11,11,12,12,12,13,13,13,13,14,14,14,14,15,16,17,18,19]
                                trash = []
                                for j in my_cards:
                                    cards.remove(j)
                                for j in your_cards:
                                    cards.remove(j)
                            j = random.choice(cards)
                            my_cards.append(j)
                            cards.remove(j)
                        my_cards.sort()
                        pointer = 400
                        turn = 2
                    #Trash時の演算

                    









                pygame.display.update()     # 画面更新
                pygame.time.wait(30)        # 更新時間間隔

                screen.fill(white)  # 背景真っ白にする

                #背景描画
                #集合描画
                color_A = black
                color_B = black
                if pointer == 200:
                    color_A = orange
                if pointer == 300:
                    color_B = orange
                pygame.draw.ellipse(screen, color_A, (50, 50, 450, 350), 5)
                pygame.draw.ellipse(screen, color_B, (300, 50, 450, 350), 5)
                pygame.draw.rect(screen, white, Rect(235, 10, 80, 80))
                text_A = font.render("A", True, color_A)
                screen.blit(text_A, [265, 40])
                pygame.draw.rect(screen, white, Rect(485, 10, 80, 80))
                text_B = font.render("B", True, color_B)
                screen.blit(text_B, [515, 40])
                #ここまで集合描画
                #カード描画
                for i in range(7):
                    if check_flag[i] == 1:
                        pygame.draw.rect(screen, orange, Rect(90+i*90, 480, 80, 100))
                for i in range(7):
                    pygame.draw.rect(screen, black, Rect(90+i*90, 480, 80, 100), 2)
                if go_flag == 1:
                    pygame.draw.rect(screen, (255, 0, 0), Rect(720, 495, 70, 70))
                    go_flag = 0

                if go_flag == 2:
                    pygame.draw.rect(screen, (255, 0, 0), Rect(10, 495, 70, 70))
                    go_flag = 0
                    #ここまでカード描画
                    #Go描画
                pygame.draw.rect(screen, black, Rect(720, 495, 70, 70), 2)
                text_Go = font2.render("Go", True, black)
                screen.blit(text_Go, [737, 518])
                #ここまでGo描画
                #Trash描画
                font_trash = pygame.font.Font(None, 35)
                pygame.draw.rect(screen, black, Rect(10, 495, 70, 70), 2)
                text_Go = font_trash.render("Trash", True, black)
                screen.blit(text_Go, [14, 518])
                #ここまでTrash描画
                #ここまで背景描画

                #テクスト描画
                #カード描画
                for i in range(7):
                    if my_cards[i] == 11:
                        screen.blit(text_cards[20], [135 + 90*i, 505])
                    screen.blit(text_cards[my_cards[i]], [120 + 90*i, 510])
                    #ここまでカード描画

                    #集合内の文字描画
                    #A
                for i in range(len(my_life)):
                    if pointer != i:
                        color = black
                    else:
                        color = orange
                    if my_life[i][1] == 1:
                        my_life_text = font2.render(str(my_life[i][0]), True, color)
                    elif my_life[i][1] >= 2:
                        my_life_text = font2.render(
                            "√"+str(my_life[i][0]), True, color)
                    if my_life[i][1] >= 3:
                        font3 = pygame.font.Font(None, 20)
                        my_life_text2 = font3.render(str(my_life[i][1]), True, color)
                        screen.blit(my_life_text2, [
                                    100+(i//3)*80, 140+i*50-(i//3)*150])
                    screen.blit(my_life_text, [100+(i//3)*80, 150+i*50-(i//3)*150])
                    #ここまでA

                    #B
                for i in range(len(your_life)):
                    if pointer != i+100:
                        color = black
                    else:
                        color = orange
                    if your_life[i][1] == 1:
                        your_life_text = font2.render(
                            str(your_life[i][0]), True, color)
                    elif your_life[i][1] >= 2:
                        your_life_text = font2.render(
                            "√"+str(your_life[i][0]), True, color)
                    if your_life[i][1] >= 3:
                        font3 = pygame.font.Font(None, 20)
                        your_life_text2 = font3.render(
                            str(your_life[i][1]), True, color)
                        screen.blit(your_life_text2, [
                                    510+(i//3)*80, 140+i*50-(i//3)*150])
                    screen.blit(your_life_text, [510+(i//3)*80, 150+i*50-(i//3)*150])
                    #ここまでB

                    #共通部分
                for i in range(len(our_life)):
                    if pointer != i+50:
                        color = black
                    else:
                        color = orange
                    if our_life[i][1] == 1:
                        our_life_text = font2.render(str(our_life[i][0]), True, color)
                    elif our_life[i][1] >= 2:
                        our_life_text = font2.render(
                            "√"+str(our_life[i][0]), True, color)
                    if our_life[i][1] >= 3:
                        font3 = pygame.font.Font(None, 20)
                        our_life_text2 = font3.render(str(our_life[i][1]), True, color)
                        screen.blit(our_life_text2, [380, 110+i*50])
                    screen.blit(our_life_text, [380, 120+i*50])
                    #ここまで共通部分

                # test = font.render(str(pointer), True, black)
                # screen.blit(test, [0, 0])


                
                if errorflag == 1 and error_flag_counter <= 60:
                    font_error = pygame.font.Font(None, 100)
                    error_message = font_error.render("Error", True, (255, 0, 0))
                    screen.blit(error_message, [300, 200])
                    error_flag_counter += 1

                

                
                
                
                
                if your_go_card_flag == 1:
                    pointer_message = 400
                    trash_message = your_go_card[0]
                    if trash_message == 0:
                        pointer_message = your_go_card[-1]
                    if trash_message == 1:
                        icard = copy.copy(your_original_card)
                        for i in range(len(your_go_card)-1):
                            icard.remove(your_go_card[i+1])
                        your_go_card = copy.copy(icard)

                    your_go_card_flag = 2

                if your_go_card_flag == 2 and your_go_card_flag_counter <= 80:
                    font_error = pygame.font.Font(None, 60)
                    go_message = [0, 0, 0, 0, 0, 0, 0]
                    if 0 <= pointer_message <= 49:
                        if my_go_life[pointer_message][1] == 1:
                            pointer_message2 = font_error.render(str(my_go_life[pointer_message][0]), True, (0,0,0))
                        elif my_go_life[pointer_message][1] >= 2:
                            pointer_message2 = font_error.render(
                                "√"+str(my_go_life[pointer_message][0]), True, (0,0,0))
                        if my_go_life[pointer_message][1] >= 3:
                            font3 = pygame.font.Font(None, 20)
                            pointer_message3 = font3.render(str(my_go_life[pointer_message][1]), True, (0,0,0))
                            screen.blit(pointer_message3, [
                                        50, 390])
                        screen.blit(pointer_message2, [50, 420])

                    if 50 <= pointer_message <= 99:
                        if our_go_life[pointer_message-50][1] == 1:
                            pointer_message2 = font_error.render(str(our_go_life[pointer_message-50][0]), True, (0,0,0))
                        elif our_go_life[pointer_message-50][1] >= 2:
                            pointer_message2 = font_error.render(
                                "√"+str(our_go_life[pointer_message-50][0]), True, (0,0,0))
                        if our_go_life[pointer_message-50][1] >= 3:
                            font3 = pygame.font.Font(None, 20)
                            pointer_message3 = font3.render(str(our_go_life[pointer_message-50][1]), True, (0,0,0))
                            screen.blit(pointer_message3, [
                                        50, 390])
                        screen.blit(pointer_message2, [50, 420])
                        

                    if 100 <= pointer_message <= 149:
                        if your_go_life[pointer_message-100][1] == 1:
                            pointer_message2 = font_error.render(str(your_go_life[pointer_message-100][0]), True, (0,0,0))
                        elif your_go_life[pointer_message-100][1] >= 2:
                            pointer_message2 = font_error.render(
                                "√"+str(your_go_life[pointer_message-100][0]), True, (0,0,0))
                        if your_go_life[pointer_message-100][1] >= 3:
                            font3 = pygame.font.Font(None, 20)
                            pointer_message3 = font3.render(str(your_go_life[pointer_message-100][1]), True, (0,0,0))
                            screen.blit(pointer_message3, [
                                        50, 390])
                        screen.blit(pointer_message2, [50, 420])





                    if pointer_message == 200:
                        pointer_message2 = font_error.render("A", True, (0, 0, 0))
                        screen.blit(pointer_message2, [50, 420])
                    if pointer_message == 300:
                        pointer_message2 = font_error.render("B", True, (0, 0, 0))
                        screen.blit(pointer_message2, [50, 420])

                    if trash_message == 0:
                        trash_message2 = font_error.render("<----", True, (0, 0, 0))
                        screen.blit(trash_message2, [120, 415])
                        for i in range(len(your_go_card)-2):
                            go_message[i] = font_error.render(str(text_cards2[your_go_card[i+1]]), True, (0, 0, 0))
                            if your_go_card[i+1] == 9:
                                go_message[i] = pygame.transform.rotate(go_message[i], 180)
                            if your_go_card[i+1] == 11:
                                screen.blit(text_cards[20], [260 + i * 80, 410])
                            screen.blit(go_message[i], [240 + i * 80, 415])
                    
                    if trash_message == 1:
                        trash_message2 = font_error.render("Trash", True, (0, 0, 0))
                        screen.blit(trash_message2, [50, 415])
                        for i in range(len(your_go_card)-1):
                            go_message[i] = font_error.render(str(text_cards2[your_go_card[i+1]]), True, (0, 0, 0))
                            if your_go_card[i+1] == 9:
                                go_message[i] = pygame.transform.rotate(go_message[i], 180)
                            if your_go_card[i+1] == 11:
                                screen.blit(text_cards[20], [260 + i * 80, 410])
                            screen.blit(go_message[i], [240 + i * 80, 415])
                    

                    
                    your_go_card_flag_counter += 1
                    if your_go_card_flag_counter == 80:
                        your_go_card_flag = 3
                    
                    
                    if lose_flag == 1:
                        font_lose = pygame.font.Font(None, 150)
                        lose_message = font_lose.render("YOU LOSE", True, (255, 0, 0))
                        screen.blit(lose_message, [100, 200])
                        title_flag = 1
                    


                    
                if isEmpty(your_life,our_life) and isEmpty(my_life,our_life):
                    lose_flag2 = 1
                    lose_counter2 = 0
                if isEmpty(your_life, our_life) and not(isEmpty(my_life, our_life)):
                    win_flag = 1
                    win_counter = 0

                




                #ここまで集合内の文字描画

                # for i in range(7):
                #     screen.blit(text_cards[your_cards[i]], [400 + 60*i, 0])
                #ここまでテクスト描画


                if your_go_card_flag == 0:
                    #あたり判定系統
                        #カードのあたり判定
                    for i in range(7):
                        if 90+i*90 < mouse_x < 170+i*90 and 480 < mouse_y < 580 and mouse_button == 1 and check_flag[i] == 0:
                            check_flag[i] = 1
                            mouse_button = 0
                        if 90+i*90 < mouse_x < 170+i*90 and 480 < mouse_y < 580 and mouse_button == 1 and check_flag[i] == 1:
                            check_flag[i] = 0

                    if 720 < mouse_x < 790 and 495 < mouse_y < 565 and mouse_button == 1:
                            go_flag = 1

                    if 10 < mouse_x < 80 and 495 < mouse_y < 565 and mouse_button == 1:
                            go_flag = 2
                        #ここまでカードのあたり判定

                        #文字のあたり判定
                    for i in range(len(my_life)):
                        if 100+(i//3)*80 < mouse_x < 160+(i//3)*80 and 150+i*50-(i//3)*150 < mouse_y < 180+i*50-(i//3)*150 and mouse_button == 1:
                            pointer = i
                    for i in range(len(your_life)):
                        if 510+(i//3)*80 < mouse_x < 570+(i//3)*80 and 150+i*50-(i//3)*150 < mouse_y < 180+i*50-(i//3)*150 and mouse_button == 1:
                            pointer = i+100
                    for i in range(len(our_life)):
                        if 380 < mouse_x < 440 and 120+i*50 < mouse_y < 150+i*50 and mouse_button == 1:
                            pointer = i+50

                    if 235 < mouse_x < 315 and 10 < mouse_y < 90 and mouse_button == 1:
                        pointer = 200
                    if 485 < mouse_x < 565 and 10 < mouse_y < 90 and mouse_button == 1:
                        pointer = 300

                        #ここまで文字のあたり判定

                    mouse_button = 0
                    #ここまであたり判定

                # 終了用のイベント処理
                for event in pygame.event.get():
                    if event.type == MOUSEMOTION:
                        mouse_x, mouse_y = event.pos

                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        mouse_button = 1
                    # 閉じるボタンが押されたとき
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    # キーを押したとき
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:   # Escキーが押されたとき
                            pygame.quit()
                            sys.exit()

            title_flag = 1


if __name__ == "__main__":
    main()



    
    
    

    
    
        
        
                
