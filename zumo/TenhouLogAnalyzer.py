import xml.etree.ElementTree as etree
import urllib.parse
import enum

class Yaku(enum.IntEnum):
    tsumo = 0
    riichi = 1
    ippatsu = 2
    chankan = 3
    rinshan = 4
    chitoi = 22
    kokushi = 47
    kokushi13 = 48

YAKU = '''ツモ
リーチ
一発
槍槓
嶺上開花
海底撈月
河底撈魚
平和
断ヤオ
一盃口
自風牌 東
自風牌 南
自風牌 西
自風牌 北
場風牌 東
場風牌 南
場風牌 西
場風牌 北
役牌 白
役牌 發
役牌 中
ダブル立直
七対子
混全帯ヤオ
一気通貫
三色同順
三色同刻
三槓子
対々和
三暗刻
小三元
混老頭
二盃口
純全帯ヤオ
混一色
清一色
人和
天和
地和
大三元
四暗刻
四暗刻単騎
字一色
緑一色
清老頭
九連宝燈
純正九蓮宝燈
国士無双
国士無双13面待ち
四槓子
小四喜和
大四喜和
ドラ
裏ドラ
赤ドラ'''.split("\n")

class Player:
    RANKS = "新人,9級,8級,7級,6級,5級,4級,3級,2級,1級,初段,二段,三段,四段,五段,六段,七段,八段,九段,十段".split(",")
    def __init__(self, name, rank, rate):
        self.name = name
        self.rank = rank
        self.rate = rate
    
    def __str__(self):
        return "%s (レート%s, %s)" % (self.name, self.rate, self.RANKS[self.rank])

class Round:
    def __init__(self):
        self.firstHai = []
        self.firstScore = []
        self.dora = []
        self.dealer = 0
        self.wind = 0
        self.honba = 0
        self.stick = 0
        
        self.lastHai = []
        self.lastDa = 0
        self.discard = [[],[],[],[]]

        self.riichiDeclaration = []
        self.riichiSuccess = []
        self.uraDora = []
        self.finalScore = []
        self.winPlayer = None
        self.winType = None
        self.yaku = []
        self.fu = 0
        self.han = 0
        self.score = 0

class Mahjong:
    ROUND_NAMES = "東1,東2,東3,東4,南1,南2,南3,南4,西1,西2,西3,西4,北1,北2,北3,北4".split(",")
    TILES = """
        1s 2s 3s 4s 5s 6s 7s 8s 9s
        1p 2p 3p 4p 5p 6p 7p 8p 9p
        1m 2m 3m 4m 5m 6m 7m 8m 9m
        ew sw ww nw
        wd gd rd
    """.split()

    def toTile(self, l):
        return [self.TILES[i // 4] for i in l]

    def __init__(self):
        self.players = []
        self.rounds = []
        self.oneRound = None

    def setLog(self, log):
        events = etree.parse(log).getroot()
        for event in events:
            tag = event.tag
            data = event.attrib
            if "INIT" == tag:
                self.mINIT(data)
            elif "TAIKYOKU" == tag:
                continue 
            elif "DORA" == tag:
                continue 
            elif "GO" == tag:
                continue
            elif "UN" == tag:
                self.mUN(data)
            elif "AGARI" == tag:
                self.mAGARI(data)
            elif "N" == tag:
                self.mN(data)
            elif "RYUUKYOKU" == tag:
                self.mRYUUKYOKU(data)
            elif "REACH" == tag:
                self.mREACH(data)
            elif tag[0] in "TUVW":
                self.mT("TUVW".index(tag[0]), int(tag[1:]))
            elif tag[0] in "DEFG":
                self.mD("DEFG".index(tag[0]), int(tag[1:]))
        
    def mREACH(self, data):
        player = int(data["who"])
        flag = int(data["step"])
        if flag == 1:
            self.oneRound.riichiDeclaration.append(player)
        else:
            self.oneRound.riichiSuccess.append(player)

    def mRYUUKYOKU(self, data):
        r = self.oneRound
        if "type" in data:
            r.winType = data["type"]
        else:
            r.winType = 'ryuukyoku'

    def mN(self, data):
        player = int(data["who"])
        m = int(data["m"])
        hai = self.oneRound.lastHai[player]

        fromPlayer = m & 0x3
       
        tiles = self.__decodeMeld(m)
        
        hai += tiles
        
        self.oneRound.lastHai[player] = list(set(hai))

    def __decodeMeld(self, m):
        if m & 0x4:
            return self.mChi(m)
        elif m & 0x18:
            return self.mPon(m)
        elif m & 0x20:
            return self.mNuki(m)
        else:
            return self.mKan(m)


    def mChi(self, data):
        t0, t1, t2 = (data >> 3) & 0x3, (data >> 5) & 0x3, (data >> 7) & 0x3
        base = (data >> 10) // 3
        base = (base // 7) * 9 + base % 7
        return [v + 4 * (base + i) for i, v in enumerate([t0, t1, t2])]

    def mPon(self, data):
        t4 = (data >> 5) & 0x3
        t0, t1, t2 = ((1,2,3),(0,2,3),(0,1,3),(0,1,2))[t4]
        base = (data >> 9) // 3
        if data & 0x8:
            return [i + 4 * base for i in [t0, t1, t2]]
        else:
            return self.mKakan([i + 4 * base for i in [t0, t1, t2, t4]])

    def mKakan(self, tiles):
        return tiles

    def mNuki(self, data):
        raise NameError('no Nuki')
    
    def mKan(self, data):
        base = (data >> 8) // 4
        return [i + 4 * base for i in range(0, 4)]

    def mDORA(self, data):
        self.oneRound.dora.append(int(data["hai"]))

    def mAGARI(self, data):
        r = self.oneRound

        r.winPlayer = int(data["who"])
        fromPlayer = int(data["fromWho"])

        if r.winPlayer == fromPlayer:
            r.winType = "TSUMO"
        else:
            r.winType = "RON"

        for i in self.oneRound.lastHai:
            i.sort()
        
        machi = int(data["machi"])

        r.honba, r.stick = self.__decodeList(data["ba"])
        r.hu, r.score, _ = self.__decodeList(data["ten"])
       
        if "doraHaiUra" in data:
            r.uraDora = self.__decodeList(data["doraHaiUra"])

        if "yaku" in data:
            r.yaku = self.__decodeList(data["yaku"])[0::2]
            r.han = sum(self.__decodeList(data["yaku"])[1::2])
        elif "yakuman" in data:
            r.yaku = self.__decodeList(data["yakuman"])


    def mT(self, player, tile):
        self.oneRound.lastHai[player].append(tile)
     
    def mD(self, player, tile):
        self.oneRound.lastDa = tile
        self.oneRound.lastHai[player].remove(tile)
        self.oneRound.discard[player].append(tile)

    def mUN(self, data):
        rank = self.__decodeList(data['dan'])
        rate = self.__decodeList(data['rate'], dtype=float)
        for i in range(0, 4):
            name = urllib.parse.unquote(data["n%s" % i])
            self.players.append(Player(name, rank[i], rate[i]))

    def mINIT(self, data):
        r = self.oneRound = Round()
        self.rounds.append(r)
        wind, honba, stick, d0, d1, dora = self.__decodeList(data["seed"])
        r.wind = wind
        r.honba = honba 
        r.stick = stick
        r.dora.append(dora)
        r.dealer = data["oya"]
        r.firstScore = self.__decodeList(data["ten"])
        for i in range(0, 4):
            r.firstHai.append(self.__decodeList(data["hai%s" % i]))
        for i in r.firstHai:
            r.lastHai.append(list(i))

    def __decodeList(self, list, dtype = int):
        return tuple(dtype(i) for i in list.split(","))

if __name__=='__main__':
    import sys
    for path in sys.argv[1:]:
        mahjong = Mahjong()
        mahjong.setLog(open(path))
