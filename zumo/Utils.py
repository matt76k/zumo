from zumo.Shanten import splitKind

def toTile(hand):
    tiles = """     
            一 二 三 四 五 六 七 八 九
            ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨
            １ ２ ３ ４ ５ ６ ７ ８ ９
            東 南 西 北 白 發 中
            """.split()
    
    return ''.join(list(map(lambda i: tiles[i], hand)))

def possibleAgari(f, hand):
    four = filter(lambda t: hand.count(t) == 4, set(hand))
    c = list(range(34))
    for i in four:
        c.remove(i)
        
    cs = list(filter(lambda t: f(sorted([t] + hand)) == -1, c))
    
    n = 0
    for t in cs:
        n += 4 - hand.count(t)
        
    return (n, cs)

def getKotsu(hand):
    m = list(filter(lambda t: hand.count(t) == 3, set(hand)))
    k = list(filter(lambda t: hand.count(t) == 4, set(hand)))
    return [[i] * 3 for i in m] + [[i] * 4 for i in k]

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

