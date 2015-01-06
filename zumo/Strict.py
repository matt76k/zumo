from zumo.Shanten import splitKind

def getKotsu(hand):
    m = list(filter(lambda t: hand.count(t) == 3, set(hand)))
    return [[i] * 3 for i in m]

def getSyuntu(tehai):
    hand = sorted(list(set(tehai)))
    if len(hand) < 3:
        return []
    elif (hand[2] - hand[1] == 1) and (hand[1] - hand[0] == 1):
        t = tehai.copy()
        t.remove(hand[0])
        t.remove(hand[1])
        t.remove(hand[2])
        return [hand[0:3]] + getSyuntu(t)
    else:
        return getSyuntu(hand[1:])

def getMentsuS(f, s, hand):
    te = hand.copy()
    m = f(te)

    for i in m:
        for j in i:
            te.remove(j)

    n = s(te)

    for i in n:
        for j in i:
            te.remove(j)

    return m + n

def getMentsuG(hand):

    ks = getMentsuS(getKotsu, getSyuntu, hand)
    sk = getMentsuS(getSyuntu, getKotsu, hand)

    if len(ks) > len(sk):
        return ks
    else:
        return sk

def getMentsu(hand):
    hW, hP, hS, hJ = splitKind(hand)
    
    r = []
    for i in map(getMentsuG, [hW, hP, hS]):
        r += i

    return r + getKotsu(hJ)

def getAgari(hand):
    jyanto = list(filter(lambda t: hand.count(t) == 2, set(hand)))

    if len(jyanto) == 0:
        return []
    
    for j in jyanto:
        te = hand.copy()
        te.remove(j)
        te.remove(j)

        m = getMentsu(te)

        if len(m) == 4:
            return [[j, j]] + m

    return []

