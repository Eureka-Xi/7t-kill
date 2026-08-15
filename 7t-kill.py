"""
化学杀 7t-kill.py
作者: eureka (SSOJ)
<配置文件(userdata与7t-kill.py平行)>
userdata\
│
├─builds\
│  ├─build1\
│  │  └─ca1.txt; ca2.txt; ca3.txt; ca4.txt; ca5.txt; ca6.txt; ca7.txt; ca8.txt; ca9.txt; ca10.txt; ca11.txt; ca12.txt; ca13.txt; ca14.txt; ca15.txt; ca16.txt; ca17.txt; ca18.txt; ca19.txt; ca20.txt
│  ├─build2\
│  │  └─ca1.txt; ca2.txt; ca3.txt; ca4.txt; ca5.txt; ca6.txt; ca7.txt; ca8.txt; ca9.txt; ca10.txt; ca11.txt; ca12.txt; ca13.txt; ca14.txt; ca15.txt; ca16.txt; ca17.txt; ca18.txt; ca19.txt; ca20.txt
│  └─build3\
│      └─ca1.txt; ca2.txt; ca3.txt; ca4.txt; ca5.txt; ca6.txt; ca7.txt; ca8.txt; ca9.txt; ca10.txt; ca11.txt; ca12.txt; ca13.txt; ca14.txt; ca15.txt; ca16.txt; ca17.txt; ca18.txt; ca19.txt; ca20.txt
│
├─items\
│  ├─ca_H2.txt; ca_O2.txt; ca_H2O.txt; ca_C.txt; ca_CO2.txt; ca_CO.txt; ca_Bunsen_Burner.txt; ca_Ventilate_.txt
│  └─pack_1_rds_命运之开端.txt
│
├─first_log_in.txt
├─last_log_in.txt
├─log_in_data.txt
├─new_build.txt
├─new_duel.txt
├─points.txt
└─user_name.txt
Habit
    所有文字输出都用input来让玩家回车继续，
    所有输入都要有提示符“>>> ”。
Caution
    1.列表索引从0开始
    2.注意路径绑定问题，记住copy.deepcopy()
Changelog
    8.14.整装待发。~什么(O_o)??要三个双引号？
    8.11.修复H2O和人机开窗通风的问题。
    8.10.修复已知问题，修改概率的失败语句。
    8.5.把文件结构写在注释里了，非常清晰。另外，给代码加了注释。
    8.4.清除用户数据部分。
    8.3.在集训时做了一些改动，不知能否保存。
    8.1.迁移至GitHub。
    7.30.将(UR)CO(毒)的概率从0.7增强到0.75，同时，由于正在做主页，暂时关闭对战。
    7.29.正在做用户主页，好多东西要弄啊！！
    7.27.全面清除了“【反应】”以外的“【】”。修改教程文本。
    7.26.优化了UI。加入了“Changelog”内容。
"""

import random
import copy #用于复制列表内容
from time import time
from datetime import date #用于登录信息

class Cards(object): #每张卡片的基本属性和行为
    def __init__(self, name, en_name, ch_name, text, rarity):
        self.name = name #名称，用于观看
        self.en_name = en_name #英文名
        self.ch_name = ch_name #中文名
        self.text = text #卡牌文本，介绍和效果
        self.rarity = rarity #卡牌稀有度

    #obj_fx的键是一个对象的地址，现在要将其改为对象本身。确保深拷贝的对象也能映射。
    def __eq__(self, other):
        if isinstance(other, Cards):
            return self.name == other.name
        return False
    def __hash__(self):
        return hash(self.name)

    def view(self): #玩家随时要查看卡牌的详细信息
        input(f'┌─────────\n│{self.ch_name}\n│{self.en_name}\n│{self.text}\n│{self.rarity}\n└─────────')
    def activate(self, player, target): #某张卡的发动，入连锁（栈）的过程
        #（未写）氯气之类的检测
        if stack: #如果连锁某个东西发动，也就是说是C2+，一般指定已有连锁作对象，有时可以指定玩家为对象（？暂时不理解什么时候）
            stack.append([self, target]) #以对象形式入栈
            hand_card[player].remove(self.name) #出手牌
            input(f'玩家{player}连锁c{target}发动了{self.name}。')
        else: #如果是不入连锁自发（C1），指定玩家为对象
            stack.append([self, target])
            hand_card[player].remove(self.name)
            input(f'玩家{player}以玩家{target[1]}为对象发动了{self.name}。')
            stack_chain(player) #在某个玩家桌面上开始连锁（是：对某个玩家询问连锁）
class Substances(Cards):
    def __init__(self, name, en_name, ch_name, text, rarity):
        super(Substances, self).__init__(name, en_name, ch_name, text, rarity)
        self.type = '物质卡'
class Gas(Substances):
    def __init__(self, name, en_name, ch_name, text, rarity):
        super(Gas, self).__init__(name, en_name, ch_name, text, rarity)
        self.subtype = '气体'
class Spells(Cards):
    def __init__(self, name, en_name, ch_name, text, rarity):
        super(Spells, self).__init__(name, en_name, ch_name, text, rarity)
        self.type = '魔法卡' #也称作函数卡

class Packs(object):
    def __init__(self, name, no_, cont, pro_cont):
        self.name = name
        self.no_ = no_
        self.cont = cont
        self.pro_cont = pro_cont

user_name = None
points = None
def log_in():
    global user_name
    global points
    try: #这是第一次打开文件，借此检查。
        user_name_txt = open('user_data\\user_name.txt', 'r')
        user_name = user_name_txt.read()
        user_name_txt.close()
    except FileNotFoundError:
        input('出了大问题！此程序的配套文件不存在！')
        raise FileNotFoundError
    points_txt = open('user_data\\points.txt', 'r')
    points = int(points_txt.read())
    points_txt.close()
    #判断是否是新手，对于新手，给教程。
    if not user_name:
        input('    这个游戏里的询问都会带“>>>”，没问你时按“Enter回车”可以看下一行。')
        input('《新手教程》')
        input('    这是一个名为“化学杀7t-kill”的.py纯文本卡牌游戏。')
        input('    你可以在这里构筑牌组、与人机对战、赢取积分、参加积分赛和卡包赛、开卡并收集更多的卡牌。')
        input('    这个游戏的交互全部用“input()”实现。')
        input('    《新手教程》就到这里，开始探索吧！')
        user_name = input('    哦对了，你好像还没有一个名字。\n叫什么好呢？>>> ')
        user_name_txt = open('user_data\\user_name.txt', 'w')
        user_name_txt.write(user_name)
        user_name_txt.close()
        first_log_in_txt = open('user_data\\first_log_in.txt', 'w')
        first_log_in_txt.write(str(date.today()))
        first_log_in_txt.close()
    input(f'(*^v^*)你好呀，{user_name}！\n今天是{date.today()}。')
    log_in_data_txt = open('user_data\\log_in_data.txt', 'a')
    log_in_data_txt.write(f'{user_name} 登录于 {time()}\n')
    user_name_txt.close()
    last_log_in_txt = open('user_data\\last_log_in.txt', 'r')
    last_log_in = last_log_in_txt.read()
    last_log_in_txt.close()
    if last_log_in != str(date.today()):
        last_log_in_txt = open('user_data\\last_log_in.txt', 'w')
        last_log_in_txt.write(str(date.today()))
        last_log_in_txt.close()
        input(f'这是{user_name}今天第一次玩呢！每日签到+5积分！')
        points += 5
    #不不不我还没做好。
    #first_log_in_txt = open('user_data\\first_log_in.txt', 'r')
    #first_log_in = first_log_in_txt.read()
    #first_log_in_txt.close()
    #if first_log_in == str(date.today()):
        #input(f'今天是{user_name}的生日呢！+90积分！')

#主页
def pg_main():
    while True:
        while True:
            ans = input(f'====主页================\n1.{user_name}\n2.构筑\n3.对战\n4.退出游戏\n>>> ')
            if ans == '1' or ans == '2' or ans == '3' or ans == '4':
                break
            else:
                input('请输入正确数字。')
        if ans == '1':
            pg_player()
        elif ans == '2':
            pg_building()
        elif ans == '3':
            #pg_duel()
            pass
        else:
            points_txt = open('user_data\\points.txt', 'w')
            points_txt.write(str(points))
            points_txt.close()
            exit()
#玩家页
def pg_player():
    first_log_in_txt = open('user_data\\first_log_in.txt', 'r')
    first_log_in = first_log_in_txt.read()
    first_log_in_txt.close()
    while True:
        while True:
            ans = input(f'====玩家页================\n{user_name}\n生日：{first_log_in}\n积分：{points}\n==========\n1.图鉴\n2.卡包\n3.删除所有数据\n4.返回主页\n>>> ')
            if ans == '1' or ans == '2' or ans == '3' or ans == '4':
                break
            else:
                input('请输入正确数字。')
        if ans == '1': #展示收藏
            for ca in list(str_obj.values()):
                ca_txt = open(f'user_data\\items\\ca_{ca.en_name}.txt', 'r', encoding='utf-8')
                ca_amount = ca_txt.read()
                ca_txt.close()
                print(f'{ca_amount}x')
                ca.view()
        elif ans =='2': #展示并拆开卡包
            pack_1_rds_txt = open('user_data\\items\\pack_1_rds_命运之开端.txt', 'r')
            pack_1_rds = int(pack_1_rds_txt.read())
            pack_1_rds_txt.close()
            input(f'1. rds·命运之开端 {pack_1_rds}x')
            #更多卡包……
            while True:
                ans = input('你要开什么卡包？（写数字，回车跳过）\n>>> ')
                if ans == '1': #这里还要加更多卡包
                    if ans == '1':
                        try:
                            ans = int(input('rds·命运之开端，多少包？>>> '))
                        except ValueError:
                            input('由于没有输入数字，即将返回玩家页。')
                            break
                        if 0 < ans <= pack_1_rds:
                            pack_1_rds_txt = open('user_data\\items\\pack_1_rds_命运之开端.txt', 'w')
                            pack_1_rds -= ans
                            pack_1_rds_txt.write(str(pack_1_rds))
                            input(f'已拆开{ans}包“rds·命运之开端”！')
                            for i in range(ans):
                                for j in range(4):
                                    ca = random.choice(pack_dic['rds'])
                                    ca_txt = open(f'user_data\\items\\ca_{str_obj[ca].en_name}.txt', 'r')
                                    ca_amount = int(ca_txt.read())
                                    ca_txt.close()
                                    ca_amount += 1
                                    ca_txt = open(f'user_data\\items\\ca_{str_obj[ca].en_name}.txt', 'w')
                                    ca_txt.write(str(ca_amount))
                                    ca_txt.close()
                                    input(f'{str_obj[ca].rarity} {ca}！')
                                ca = random.choice(pack_dic['rds+'])
                                ca_txt = open(f'user_data\\items\\ca_{str_obj[ca].en_name}.txt', 'r')
                                ca_amount = int(ca_txt.read())
                                ca_txt.close()
                                ca_amount += 1
                                ca_txt = open(f'user_data\\items\\ca_{str_obj[ca].en_name}.txt', 'w')
                                ca_txt.write(str(ca_amount))
                                ca_txt.close()
                                input(f'{str_obj[ca].rarity} {ca}！')
                        elif ans == 0:
                            input('sb。')
                        else:
                            input(f'你的“rds·命运之开端”只有{str(pack_1_rds)}包！')
                #elif ans == '2':……
                else:
                    input('由于没有输入数字，即将返回玩家页。')
                    break
        elif ans == '3':
            input('即将清除数据……')
            #清除用户数据部分，还没做好。
            user_name_txt = open('user_data\\user_name.txt', 'w')
            user_name_txt.write('')
            user_name_txt.close()
            points_txt = open('user_data\\points.txt', 'w')
            points_txt.write('0')
            points_txt.close()
            first_log_in_txt = open('user_data\\first_log_in_txt.txt', 'w')
            first_log_in_txt.write('')
            first_log_in_txt.close()
            last_log_in_txt = open('user_data\\last_log_in_txt.txt', 'w')
            last_log_in_txt.write('')
            last_log_in_txt.close()
            #log_in_data不要删。
            exit()
        else:
            break
#构筑页
def pg_building():
    new_build_txt = open('user_data\\new_build.txt', 'r')
    new_build = new_build_txt.read()
    new_build_txt.close()
    if not new_build:
        input('看来你是第一次构筑，下面是构筑规则。')
        input('N6张，R6张，SR5张，UR3张，合计20张整。可以下位替代。')
        input('同名卡最多3张。')
        input('编辑时每次只能输入一张卡牌。')
        new_build_txt = open('user_data\\new_build.txt', 'w')
        new_build_txt.write('True')
        new_build_txt.close()
    while True:
        ans = input(f'====构筑你的牌组吧！========\n1.构筑1\n2.构筑2\n3.构筑3\n4.返回主页>>> ')
        if ans == '1' or ans == '2' or ans == '3':
            input(f'==构筑{ans}==')
            # 导入卡表
            ca_list = []
            for i in range(1, 21):
                ca_txt = open(f'user_data\\builds\\build{ans}\\ca{i}.txt', 'r', encoding='utf-8')
                ca_list.append(ca_txt.read())
                ca_txt.close()
            # 显示卡表
            i = 0
            for ca in ca_list:
                i += 1
                input(f'{i}. {str_obj[ca].rarity} {ca}')
            # 修改卡表
        elif ans == '4':
            break
        else:
            input('请输入正确数字。')


#询问当前玩家是否要响应、行动。
def ask(player):
    while True: #让玩家指定对象
        if AImode and player == 2: #AI行动
            if stack:
                if stack[-1][0] == H2 and stack[0][1][1] == 1 and '酒精灯_' in hand_card[2]:
                    Bunsen_Burner_.activate(2, [len(stack)])
                    return True #酒精灯点对方H2
                elif stack[-1][0] == Bunsen_Burner_ and stack[0][1][1] == 1 and 'H2' in hand_card[2]:
                    H2.activate(2,[len(stack)])
                    return True #H2点对方酒精灯
                elif stack[-1] == [C, [0,1]] and '酒精灯_' in hand_card[2]:
                    Bunsen_Burner_.activate(2, [len(stack)])
                    return True #酒精灯点对方C
                elif stack[-1] == [CO, [0, 2]] and '酒精灯_' in hand_card[2]:
                    Bunsen_Burner_.activate(2, [len(stack)])
                    return True #酒精灯点自己CO
                elif isinstance(stack[-1][0], Gas) and stack[0][1][1]==2 and stack[-1][0].name!='O2' and '开窗通风_' in hand_card[2]:
                    Ventilate_.activate(2, [len(stack)])
                    return True #开窗通风
                elif isinstance(stack[-1][0], Spells) and len(stack)%2 == 1 and '无懈可击_' in hand_card[2]:
                    Negate_.activate(2, [len(stack)])
                    return True #无懈可击
            else:
                if 'H2' in hand_card[2] and '酒精灯_' in hand_card[2]:
                    H2.activate(2, [0, 1])
                    return True
                elif 'O2' in hand_card[2]:
                    O2.activate(2, [0, 2])
                    return True
                elif 'H2O' in hand_card[2]:
                    H2O.activate(2, [0, 2])
                    return True
                elif 'C' in hand_card[2]:
                    C.activate(2, [0, 2])
                    return True
                elif 'CO2' in hand_card[2]:
                    CO2.activate(2, [0, 1])
                    return True
                elif 'CO' in hand_card[2]:
                    CO.activate(2, [0, 1])
                    return True
            input('    玩家2不行动。')
            return False
        elif stack:
            input(f'    你的手牌：{hand_card[1]}')
            ans = input(f'    你要连锁{stack[-1][0].name}发动什么？>>> ')
        else:
            input(f'    你的手牌：{hand_card[1]}')
            ans = input(f'    你的回合。你要发动什么？>>> ')
        if ans in hand_card[player]:
            while True:
                target = input('    指定对象发动。>>> ')
                target = tran_target(target)
                if target:
                    break
            str_obj[ans].activate(player, target)
            return True
        elif ans == 'v':
            ans = '' #无所谓，这只是个空变量
            while not ans in str_obj:
                ans = input('    查看什么？>>> ')
            str_obj[ans].view()
        elif not ans:
            break
        else:
            input('    你手上没这张牌。')
    print(f'    玩家{player}不响应。')
    return False
#target[对象卡(0则没)，对象玩家], C几[牌,[对象卡，对象玩家]]
def tran_target(target):
    if target:
        try:
            target = [int(target)]
            if 0< target[0] <= len(stack):
                return target
        except ValueError:
            pass
        if target == 'p1' or  target == 'p2':#判断是否对玩家
            if not stack:
                return [0, int(target[-1])]
            else:
                input('    你只能应对某张牌发动，不能在连锁中攻击玩家！')
        try:
            if not '0' in target:
                target = str(target)#这句没用，只是下面的“split”标黄了很难受。
                target = [int(num) for num in target.split()]
                target.sort()
                return target
        except ValueError:
            pass
    input('    对象指定有问题。')
    return None

def draw(player):
    global deck
    global GY
    if not deck:
        deck = copy.deepcopy(GY)
        GY = []
        random.shuffle(deck)
    drawn = deck.pop(0)
    hand_card[player].append(drawn)
    if player == 1:
        input(f'玩家{player}抽到了{drawn}。')
    else:
        input(f'玩家2抽了1张牌。')
def hurt(w, target, x):
#    target = target[1]
    HP[target] -= x
    input(f'{w}使玩家{target}扣了{x}滴血。')
    if HP[target] <= 0:
        input(f'玩家{target}死亡。')
        input('结束啦！！感谢你的游玩，找我追更哦``(^o^)/')
        exit()
    else:
        input(f'    玩家{target}还有{HP[target]}滴血。')
def heal(w, target, x):
#    target = target[1]
    HP[target] += x
    input(f'{w}使玩家{target}回了{x}滴血。')
    input(f'    玩家{target}还有{HP[target]}滴血。')
#def explosion(reason, target, chance, damage):
#    if random.random <= chance:
def h2_explosion(target):
    if random.random() <= 0.5:
        hurt('氢气爆炸', target[1], 3)
    else:
        hurt('氢气"没有"爆炸', target[1], 0)
def co_explosion(target):
    if random.random() <= 0.25:
        hurt('一氧化碳爆炸', target[1], 3)
    else:
        hurt('一氧化碳"没有"爆炸', target[1], 0)

def stack_chain(player):
    _c = {1:2,2:1}
    a = _c[player]
    i = [stack[0][0].name, stack[0][1]]
    input(f'        连锁1：{i}')
    while True:#检测：当双方都不跟时，连锁结束
        if not ask(a):
            a = _c[a]
            if not ask(a):
                break
        j = 1
        k = copy.deepcopy(stack)
        for i in k:
            i[0] = i[0].name
            print(f'        连锁{j}：{i}')
            #print(f'栈：{stack}')
            j += 1
        a = _c[a]
    stack_resolve()
def stack_resolve():
    global stack
    global stack_II
    global toGY
    while stack:
        #print(stack)
        obj_fx[stack[-1][0]](stack[-1][1])
    input('==连锁处理结束==')
    GY.extend(toGY)
    toGY = []
    if stack_II:
        stack = copy.deepcopy(stack_II)
        stack_II = []
        stack_chain(whose_turn%2+1)


def react(target):
    t_input = [stack[i-1][0].name for i in target]
    t_input.append(stack[-1][0].name)
    t_input.sort()
    for reaction_list in reaction_lists:
        c_input, description, effect, c_output = reaction_list
        if t_input == c_input:
            input(description)
            if effect:
                effect(stack[0][1])
            for i in c_output:
                stack_II.insert(0, [str_obj[i],stack[target[0]-1][1]])#最难懂的部分
            for i in target:
                toGY.append(stack.pop(i)[0].name)
            return True
    input('（没有反应）')
    return False

def xg_h2(target):
    if not target[0]:
        pass
    else:
        react(target)
    toGY.append(stack.pop(-1)[0].name)
def xg_o2(target):
    if not target[0]:
        heal('O2', target[1], 1)
    else:
        react(target)
    toGY.append(stack.pop(-1)[0].name)
def xg_h2o(target):
    if not target[0]:
        if target[1] == 1:
            ans = ''
            while (not ans in GY) and GY:
                ans = input(f'    废料缸:{GY}\n    【？】选一张洗回>>> ')
            if ans in GY:
                GY.remove(ans)
                deck.insert(0, ans)
        elif target[1] == 2:
            if GY:
                deck.insert(0, GY.pop(-1))
    else:
        react(target)
    toGY.append(stack.pop(-1)[0].name)
def xg_c(target):
    #print(target)
    if not target[0]:
        draw(target[1])
    else:
        react(target)
    toGY.append(stack.pop(-1)[0].name)
def xg_co2(target):
    if not target[0]:
        hurt('CO2', target[1], 1)
    else:
        react(target)
    toGY.append(stack.pop(-1)[0].name)
def xg_co(target):
    if not target[0]:
        while random.random() >= 0.75:
            hurt('CO的毒', target[1], 1)
        input('    毒性结束。')
    else:
        react(target)
    toGY.append(stack.pop(-1)[0].name)
def xg_bunsen_burner_(target):
    if not target[0]:
        input('    拿酒精灯烧人？牛逼吗。')
        hurt('酒精灯', target[1], 0)
    else:
        react(target)
    toGY.append(stack.pop(-1)[0].name)
def xg_ventilate_(target):
    if target[0] and isinstance(stack[-2][0], Gas):
        input(f'开窗通风_使{stack[-2][0].name}无效了。')
        GY.append(stack.pop(-2)[0].name)
    else:
        input('    开窗通风打空了。')
    toGY.append(stack.pop(-1)[0].name)
def xg_negate_(target):
    if target[0] and stack[-2][0].type=='魔法卡':
        input(f'无懈可击_使{stack[-2][0].name}无效了。')
        GY.append(stack.pop(-2)[0].name)
    else:
        input('    无懈可击打空了。')
    toGY.append(stack.pop(-1)[0].name)
def xg_empty(target):
    stack.pop(-1)

def huihe(target):
    input(f'====玩家{target}的回合====')
    draw(target)
    draw(target)
    while True:
        if not ask(target):
            break
    while len(hand_card[target]) > 3:#回合结束的弃牌
        if target == 1:
            ans = ''
            while not ans in hand_card[target]:
                ans = input(f'    回合结束：你的手牌超过3张，需弃牌。\n    手牌：{hand_card[target]}\n    >>> ')
        else:
            ans = hand_card[2][0]
        hand_card[target].remove(ans)
        GY.append(ans)
    print(f'血量：{HP}')

#定义卡牌
H2 = Gas('H2','H2','氢气','还原性强。\n│#爆炸时，HP-3！', 'N')
O2 = Gas('O2','O2','氧气','氧化性强。\n│#效果：HP+1。\n│#空气里也可以燃烧物质。', 'R')
H2O = Substances('H2O','H2O','水','生命之源。\n│#效果：洗回废料缸一张物质。', 'N')
C = Substances('C','C','碳','还原性强。\n│#效果：对象玩家抽1张牌。', 'N')
CO2 = Gas('CO2','CO2','二氧化碳','本身无毒，但浓度过高会使窒息。\n│#效果：HP-1。', 'R')
CO = Gas('CO','CO','一氧化碳','既有氧化性又有还原性，有毒。\n│#效果：有75%概率HP-1，并有75%概率再来一次。\n│#爆炸时，HP-3！', 'UR')
Bunsen_Burner_ = Spells('酒精灯_','Bunsen_Burner_','酒精灯_','你知道吗？在外国化学课上多用本生灯。所以这卡中文名和英文名不一样。', 'R')
Ventilate_ = Spells('开窗通风_','Ventilate_','开窗通风_','许多实验需在通风环境下进行……什么？你没闻过HCl的味道？\n│#连锁气体发动，使其无效。', 'SR')
Negate_ = Spells('无懈可击_','Negate_','无懈可击_','三国杀你打过吧……其实这张牌还有个名字叫神之宣告。\n│#连锁魔法卡发动，使其无效。', 'UR')
_RDS = Packs('_RDS_起源之地', '_RDS', [H2, H2, O2, H2O, H2O, C, C, CO2, Bunsen_Burner_], [Ventilate_, Ventilate_, CO, Negate_])

#各种快速转换的字典
str_obj = {'H2':H2, 'O2':O2, 'H2O':H2O, 'C':C, 'CO2':CO2, 'CO':CO,
       '无懈可击_':Negate_,'酒精灯_':Bunsen_Burner_, '开窗通风_':Ventilate_}
obj_fx = {H2:xg_h2, O2:xg_o2, H2O:xg_h2o, C:xg_c, CO2:xg_co2, CO:xg_co,
          Negate_:xg_negate_, Bunsen_Burner_:xg_bunsen_burner_, Ventilate_:xg_ventilate_}
fx_obj = {v: k for k, v in obj_fx.items()}
pack_order = [None, _RDS,]

#反应
reaction_lists = [
    [['H2','酒精灯_'],'【反应】氢气在空气中燃烧生成水。\n(2)H2+O2==点燃==(2)H2O',h2_explosion,['H2O']],
        [['H2','O2','酒精灯_'],'【反应】氢气在氧气中燃烧生成水。\n(2)H2+O2==点燃==(2)H2O',h2_explosion,['H2O']],
    [['C','酒精灯_'],'【反应】碳在空气中充分燃烧生成CO2。\nC+O2==点燃==CO2',None,['CO2']],
        [['C','O2','酒精灯_'],'【反应】碳在氧气中充分燃烧生成CO2。\nC+O2==点燃==CO2',None,['CO2']],
    [['C','C','酒精灯_'],'【反应】碳在空气中不充分燃烧生成CO。\n(2)C+O2==点燃==(2)CO',None,['CO']],
        [['C', 'C','O2','酒精灯_'], '【反应】碳在氧气中不充分燃烧生成CO。\n(2)C+O2==点燃==(2)CO', None, ['CO']],
    [['CO', '酒精灯_'], '【反应】一氧化碳在空气中燃烧。\n(2)CO+O2==点燃==(2)CO2', co_explosion, ['CO2']],
        [['CO', 'O2', '酒精灯_'], '【反应】一氧化碳在氧气中燃烧。\n(2)CO+O2==点燃==(2)CO2', co_explosion, ['CO2']],
    [['C', 'CO2', '酒精灯_', '酒精灯_'], '【反应】二氧化碳在高温下被碳还原成一氧化碳。\nC+CO2==点燃==(2)CO', None, ['CO', 'CO']],
]



input('《规则》')
input('    你和AI打牌，每人5滴血，轮流抽牌、出牌。')
input('    出牌都要指定对象。')
input('    指定玩家为对象时，写“p1”（你）或“p2”（对手）。')
input('    在你行动时，可以输入“v”查阅一张牌。')
input('    你可以应对一张牌来行动，称为“连锁”。')
input('《连锁》')
input('    “连锁”作名词表示牌桌上的一个“栈”，用于处理反制卡和化学反应，')
input('    “（跟）连锁”作动词表示跟在牌后面出另一张牌，即把手牌打进“栈”中。')
input('    在连锁中，你只能指定“栈”里已有的牌作为对象。')
input('    在指定一张牌作为对象时，写一个数字表示以连锁中的第几张卡为对象。')
input('    双方轮流选择跟连锁，直到双方都不跟时，“堆栈”结束，进入“连锁处理。”')
input('    c[几]表示连锁中的第几张牌，')
input('    连锁的结构为：\n[\n连锁x：[<牌名>, <指定的对象>]\n连锁x：[<牌名>, <指定的对象>]\n连锁x：[<牌名>, <指定的对象>]\n]')
input('    连锁处理从下往上，遵循“栈”的机制。')
input('《化学反应》')
input('    用第2反应物或反应条件连锁第1个反应物即可。')
input('    当化学反应需要很多牌时，请在最后一张牌时指定多个对象。可用空格隔开多个对象。')
input('    生成物会放入新的栈中。')
input('    *“酒精灯_”在这个游戏里是“点燃、加热、高温（需2个酒精灯）”任意一个反应条件。')
input('    *游戏里默认有空气，大部分燃烧反应可以不用打出O2。')
input('    好了。规则结束了。\n')
input('欢迎来到化学杀：7t-kill！！！')
input('    玩家1 vs 玩家2（自己写的人机）')
stack = []
stack_II = []
toGY = []
GY = []
AImode = True
HP = [None,5,5]
hand_card = [None,[],[]]
turn = 0
whose_turn = 0
deck = ['H2','H2','O2','O2','H2O','C','C','CO2','CO2','CO',
        '无懈可击_','酒精灯_','酒精灯_','酒精灯_','开窗通风_','开窗通风_']
random.shuffle(deck)
input('    双方开局抽3张牌')
draw(1)
draw(1)
draw(1)
draw(2)
draw(2)
draw(2)
input('======DUEL======')
while True:
    huihe(1)
    huihe(2)
