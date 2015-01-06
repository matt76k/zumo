from zumo.ShantenTable import ShantenTable
import itertools

def isWanz(n):
    return n >= 0 and n < 9
def isPinz(n):
    return n >= 9 and n < 18
def isSouz(n):
    return n >= 18 and n < 27
def isJihai(n):
    return n >= 27

def isTanyao(n):
    nn = num(n)
    return (not (isJihai(n))) and (nn != 1 and nn != 9)

def num(k):
    return (k % 9) + 1

def splitKind(hand):
    ret = ([],[],[],[])
    for t in hand:
        if isWanz(t):
            ret[0].append(t)
        elif isPinz(t):
            ret[1].append(t)
        elif isSouz(t):
            ret[2].append(t)
        else:
            ret[3].append(t)
    return ret

isKoritsuL = lambda hai: hai[1] - hai[0] > 2
isKoritsuR = lambda hai: hai[1] - hai[0] > 2
isKoritsuM = lambda hai: hai[2] - hai[1] > 2 and hai[1] - hai[0] > 2

def isKoritsu(hai, i):
    if i == 0:
        return isKoritsuL(hai[0:2])
    elif i == len(hai) - 1:
        return isKoritsuR(hai[len(hai) - 2:])
    else:
        return isKoritsuM(hai[i - 1: i + 2])

def getTable(hai):
    if len(hai) < 2:
        return [(0, 0), (0, 0)]

    tiles = hai.copy()
    koritsu = map(lambda x: x[1], filter((lambda i: isKoritsu(hai, i[0])), enumerate(hai)))
    
    
    for i in koritsu:
        tiles.remove(i)
   
    key = 0
    for i in tiles:
        key += 10 ** (9 - num(i))

    [a, b, c, d] = ShantenTable[key]
    return [(a, b), (c, d)]

def calSha(x):
    [m, t] = x

    return 8 - 2 * m - min(t, 4 - m)

def calMP(x):
    m, pm = 0, 0
    for t in x:
        m += t[0]
        pm += t[1]

    return (m, pm)

def calShanten(hand):
    hW, hP, hS, hJ = splitKind(hand)
    mJ = len(list(filter(lambda t: hJ.count(t) >= 3, set(hJ))))
    pJ = len(list(filter(lambda t: hJ.count(t) == 2, set(hJ))))

    w = getTable(hW)
    p = getTable(hP)
    s = getTable(hS)
    j = [(mJ, pJ)]

    return min(map(calSha, (map(calMP, itertools.product(w, p, s, j)))))

def normal(hand):
    tiles = hand.copy()
    nJanto = calShanten(tiles)
    wJanto = []
    for jyanto in [i for i in set(hand) if hand.count(i) >= 2]:
        tiles = hand.copy()
        tiles.remove(jyanto)
        tiles.remove(jyanto)
        wJanto.append(calShanten(tiles) - 1)

    wJanto.append(nJanto)

    return min(wJanto)

def chitoi(hand):
    kinds = list(set(hand))
    kind  = len(kinds)
    toitsu = len(list(filter(lambda t: hand.count(t) >= 2, kinds)))

    return 6 - toitsu + max((7 - kind), 0)
   
def kokushi(hand):
    yaochu = list(filter(lambda x: not(isTanyao(x)), hand))
    kinds = list(set(yaochu)) 
    kind = len(kinds)
    toitsu = len(list(filter(lambda t: yaochu.count(t) >= 2, kinds)))

    return 13 - kind - min(1, toitsu)

def shanten(hand):
    return min(normal(hand), kokushi(hand), chitoi(hand))

'''
files = open('p_koku_10000.txt').readlines()

#hand = [0, 4, 5, 5, 7, 7, 11, 17, 20, 20, 24, 30, 33, 33]

#print(normal(hand))

for l in files:
    la = list(map(int, l.split()))
    hand = la[0:14]
    n = la[14]
    k = la[15]
    c = la[16]
    nn = normal(hand)
    kk = kokushi(hand)
    cc = chitoi(hand)

    if n != nn or k != kk or c != cc:
        print(hand)
'''
