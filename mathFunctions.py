from sympy import *
import math
import random

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

def fixRange(ranges): #범위들을 복잡하지 않게 단순화하여 반환다. -> 합집합 한다.
    fixed_range = []
    size = len(ranges)
    index = 0
    while index < size:
        std = ranges[index]
        i = index + 1
        while i < size:
            if std[0] <= ranges[i][0] and ranges[i][0] <= std[1] or std[0] <= ranges[i][1] and ranges[i][1] <= std[1]:
                l = [*std, *ranges[i]]
                a = min(l)
                b = max(l)
                std = (a, b)
                del ranges[i]
                size -= 1
            i += 1
        fixed_range.append(std)
        index += 1
    fixed_range.sort(key=lambda x:x[0])

    return fixed_range

def intersectRanges(ranges1, ranges2):
    fixed_range = []
    size = len(ranges1)
    index = 0
    for r1 in ranges1:
        for r2 in ranges2:
            if r1[0] <= r2[0] and r2[0] <= r1[1] or r1[0] <= r2[1] and r2[1] <= r1[1]:
                a = (r1[0]) if r1[0]>r2[0] else (r2[0])
                b = (r1[1]) if r1[1]<r2[1] else (r2[1])
                #fixed_range.remove(r2)
                fixed_range.append((a, b))

    return fixRange(fixed_range)

def cyclifyRange(ranges, cycle):
    ranges = fixRange(ranges)
    fixed_ranges = []
    for r in ranges:
        a = r[0] % cycle
        b = r[1] % cycle
        if a <= b:
            fixed_ranges.append((a, b))
        else:
            fixed_ranges.append((a, cycle))
            fixed_ranges.append((0, b))

    return fixRange(fixed_ranges)

def randomRange(ranges): #여러 범위가 들어간 리스트에서 동일한 확률로 무작위 실수를 반환한다.
    counts = ([r[1]-r[0] for r in ranges])
    count_sum = sum(counts)
    rand1 = random.uniform(0, count_sum)
    pos = 0
    for i in range(0, len(ranges)):
        if pos > rand1:
            return random.uniform(*ranges[i-1])
        pos += counts[i]

    return random.uniform(*ranges[-1])



