from sympy import *
import math

def findExtremums(func, arg): # 함수, 변수. 단변수함수에서만 동작한다.
    dy = diff(func, arg)
    extremums = solve(dy, arg)

    return extremums

def findMinMax(func, arg, func_range, arg_range): # 함수, 변수, 함수값 범위, 변수 범위. 단변수함수에서만 동작한다.
    maybe_minmax = []

    for extr in findExtremums(func, arg):
        if arg_range[0] <= extr and extr <= arg_range[1]:
            y = func.subs(arg, extr)
            maybe_minmax.append(y)
    maybe_minmax.append(func.subs(arg, arg_range[0]))
    maybe_minmax.append(func.subs(arg, arg_range[1]))

    if maybe_minmax == []:
        return None

    min = None
    max = None

    for n in maybe_minmax:
        if n != None and not im(n):
            if n >= func_range[0] and n <= func_range[1]:
                if min == None:
                    min = n
                if max == None:
                    max = n
                elif n < min:
                    min = n
                elif n > max:
                    max = n
            else:
                if n < func_range[0]:
                    min = func_range[0]
                elif n > func_range[1]:
                    max = func_range[1]

    return (min, max)

def findExtremums2(func, args): #함수, (변수a, 변수b)
    dy1 = diff(func, args[0]) # a에 대해 편미분
    dy2 = diff(func, args[1]) # b에 대해 편미분

    extremums = solve([dy1, dy2], args)

    return extremums

def findMinMax2(func, args, func_range, arg_ranges): #함수, (변수a, 변수b), 함수값 범위, 변수 범위
    maybe_minmax = []

    extremums = findExtremums2(func, args)

    for extr in extremums:
        if arg_ranges[0][0] <= extr[0] and extr[0] <= arg_ranges[0][1] and arg_ranges[1][0] <= extr[1] and extr[1] <= arg_ranges[1][1]:
            y = func.subs({args[0]:extr[0], args[1]:extr[1]})
            maybe_minmax.append(y)

    for a_edge in arg_ranges[0]: # a의 최대 최소를 대입했을 때 함수의 최대, 최소
        f = func.subs(args[0], a_edge)
        maybe_minmax.extend(findMinMax(f, args[1], func_range, arg_ranges[1]))
    for b_edge in arg_ranges[1]: # a의 최대 최소를 대입했을 때 함수의 최대, 최소
        f = func.subs(args[1], b_edge)
        maybe_minmax.extend(findMinMax(f, args[0], func_range, arg_ranges[0]))

    if maybe_minmax == []:
        return None

    min = None
    max = None

    for n in maybe_minmax:
        if n != None and not im(n):
            if n >= func_range[0] and n <= func_range[1]:
                if min == None:
                    min = n
                if max == None:
                    max = n
                elif n < min:
                    min = n
                elif n > max:
                    max = n
            else:
                if n < func_range[0]:
                    min = func_range[0]
                elif n > func_range[1]:
                    max = func_range[1]

    return (min, max)

def tuple_to_interval(tuple):
    pass
