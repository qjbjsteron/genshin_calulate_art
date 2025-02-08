import numpy
import pandas as pd
from sympy import symbols, solve, Eq
import itertools
#
# data = pd.read_excel('噎羊提供的计算表格.xlsx',sheet_name='最优函数计算')
# print(data)
#
# a = data.values[0,1]
# print(a)
# b = data.values[1,1]
# print(b)
# A = data.values[2,1]
# print(A)
# B = data.values[3,1]
# print(B)
# SumAB = int(data.values[4,1])
# print(SumAB)
# FSum = []
# for i in (range(SumAB)):
#     FSum.append((a+i*A)*(b+(SumAB-i)*B))
# print(FSum)
# for i in (FSum):
#     a = 0
#     if i == max(FSum):
#         print(i,'\n',a)
#         a+=1
#
# #技能倍率/基础攻击/攻击百分比加成/暴击率/暴击伤害/伤害加成/元素精通/抗性/减防数值/无视防御百分比/怪物等级/固定数值加成/基础加成次数/基础加成/独立乘区
# skillMultiplier = 16.971
# baseAttack = 883.85
# attackBonusPercentage = 0.85
# critRate = 0.27
# critDamage = 0.884
# damageBonus = 3.262
# elementalMastery = 0
# resistance = -0.75
# defenseReduction = 0
# ignoreDefensePct = 0
# enemyLevel = 100
# flatBonus = 4311.48
# baseBonusCount = 1
# baseBonus = 3012
# independentMultiplier = 1
# #基础区/增伤区/增幅区/双爆区/承伤区/独立区
# baseMultiplier = 1
# damageBonusZone = 1
# amplificationZone = 1
# critZone = 1
# damageTakenZone = 1
# independentZone = 1
#

class CharacterStats:
    def __init__(self, skillMultiplier, baseAttack, attackBonusPercentage, critRate, critDamage,
                 damageBonus, elementalMastery, resistance, defenseReduction, ignoreDefensePct,
                 enemyLevel, flatBonus, baseBonusCount, baseBonus, independentMultiplier,
                 baseMultiplier, damageBonusZone, amplificationZone, critZone, damageTakenZone,
                 independentZone,eleRate):
        # 技能倍率、基础攻击等属性初始化
        self.skillMultiplier = skillMultiplier
        self.baseAttack = baseAttack
        self.attackBonusPercentage = attackBonusPercentage
        self.critRate = critRate
        self.critDamage = critDamage
        self.damageBonus = damageBonus
        self.elementalMastery = elementalMastery
        self.resistance = resistance
        self.defenseReduction = defenseReduction
        self.ignoreDefensePct = ignoreDefensePct
        self.enemyLevel = enemyLevel
        self.flatBonus = flatBonus
        self.baseBonusCount = baseBonusCount
        self.baseBonus = baseBonus
        self.independentMultiplier = independentMultiplier

        # 基础区、增伤区等区域相关属性初始化
        self.baseMultiplier = baseMultiplier
        self.damageBonusZone = damageBonusZone
        self.amplificationZone = amplificationZone
        self.critZone = critZone
        self.damageTakenZone = damageTakenZone
        self.independentZone = independentZone
        self.eleRate = eleRate

    # 可以定义一些方法来计算最终伤害等，具体可以根据需要实现
    def calculate_total_attack(self):
        return self.baseAttack * (1 + self.attackBonusPercentage) + self.flatBonus

    def calculate_crit_damage(self):
        return self.critRate * self.critDamage


#------------------------------------------------------------------------------------------------------------------------------------
#7412366/
# 更多方法可以根据需求添加
# 输入的数据(除圣遗物可变词条数据)
#技能倍率/基础攻击/攻击百分比加成/暴击率/暴击伤害/伤害加成/元素精通/抗性/减防数值/无视防御百分比/怪物等级/固定数值加成/基础加成次数/基础加成/独立乘区
skillMultiplier = 18.05         #技能倍率
baseAttack = 883.855            #基础攻击
attackBonusPercentage = 0.85   #攻击百分比加成(不计入圣遗物副词条)
critRate = 0.711                    #暴击率(不计入圣遗物副词条)
critDamage = 1.748              #暴击伤害(不计入圣遗物副词条)
damageBonus = 3.334             #伤害加成
elementalMastery = 1174          #元素精通(不计入圣遗物副词条)
resistance = -1.15             #怪物抗性
defenseReduction = 0          #减防数值
ignoreDefensePct = 0            #无视防御数值
enemyLevel = 100                #怪物等级
flatBonus = 683                 #固定数值加成(如固定攻击)
baseBonusCount = 1              #基础数值加成次数
baseBonus = 3540                #基础加成(如申鹤羽毛)
independentMultiplier = 1       #独立乘区

baseMultiplier = 1              #基础数值乘区
damageBonusZone = 1             #伤害加成乘区
amplificationZone = 1           #反应系数乘区
critZone = 1                    #双爆系数乘区
damageTakenZone = 1             #伤害承受乘区
independentZone = 1             #独立乘区
eleRate = 2.0                   #反应系数设置(蒸发/融化)

#定义圣遗物词条数
artifactStatCount = 42
#单词条/双爆上限
onelimiteCount = 24             #单个副词条词条数上限
critlimiteCount = 32            #双爆词条上限(一般不超过34)

#-----------------------------------------------------------------------------------------------------------------------------------






# 创建一个 CharacterStats 对象
character = CharacterStats(skillMultiplier, baseAttack, attackBonusPercentage, critRate, critDamage,
                           damageBonus, elementalMastery, resistance, defenseReduction, ignoreDefensePct,
                           enemyLevel, flatBonus, baseBonusCount, baseBonus, independentMultiplier,
                           baseMultiplier, damageBonusZone, amplificationZone, critZone, damageTakenZone,
                           independentZone,eleRate)

# # 访问对象的属性
# print(character.baseAttack)  # 输出: 883.85
# print(character.attackBonusPercentage)  # 输出: 0.85
# print(character.calculate_total_attack())  # 计算总攻击（例如：基础攻击 + 攻击加成 + 固定加成）
# print(character.calculate_crit_damage())  # 计算暴击伤害

#定义可变变量
ChangeskillMultiplier = character.skillMultiplier
ChangebaseAttack = character.baseAttack
ChangeattackBonusPercentage = character.attackBonusPercentage
ChangecritRate = character.critRate
ChangecritDamage = character.critDamage
ChangedamageBonus = character.damageBonus
ChangeelementalMastery = character.elementalMastery
Changeresistance = character.resistance
ChangedefenseReduction = character.defenseReduction
ChangeignoreDefensePct = character.ignoreDefensePct
ChangeenemyLevel = character.enemyLevel
ChangeflatBonus = character.flatBonus
ChangebaseBonusCount = character.baseBonusCount
ChangebaseBonus = character.baseBonus
ChangeindependentMultiplier = character.independentMultiplier

ChangebaseMultiplier = character.baseMultiplier
ChangedamageBonusZone = character.damageBonusZone
ChangeamplificationZone = character.amplificationZone
ChangecritZone = character.critZone
ChangedamageTakenZone = character.damageTakenZone
ChangeindependentZone = character.independentZone
ChangeeleRate = character.eleRate
#定义圣遗物词条数
# artifactStatCount = 30
# artifactAtk, artifactCritRate, artifactCritDamge, artifactEle = symbols('artifactAtk, artifactCritRate, artifactCritDamge, artifactEle')

#定义圣遗物词条函数的约束条件
# f = artifactAtk + artifactCritRate + artifactCritDamge + artifactEle #目标函数
# constraint = Eq(artifactAtk + artifactCritRate + artifactCritDamge + artifactEle, artifactStatCount) #约束条件



def sum1t(AttackBonusPercentage,CritRate,CritDamage,ElementalMastery,artifactAtk, artifactCritRate, artifactCritDamge, artifactEle):
    changeAttackBonusPercentage = artifactAtk*0.05 + AttackBonusPercentage
    changeCritRate = artifactCritRate*0.033 + CritRate
    changeCritDamage = artifactCritDamge*0.066 + CritDamage
    changeElementalMastery = artifactEle*20 + ElementalMastery

    return changeAttackBonusPercentage,changeCritRate,changeCritDamage,changeElementalMastery











#基础区计算
def calculateBaseMultiplier(ChangeskillMultiplier,ChangebaseAttack,ChangeattackBonusPercentage,ChangeflatBonus,ChangebaseBonusCount,ChangebaseBonus):
    ChangeBaseMultiplier = ChangeskillMultiplier*(ChangebaseAttack*(1+ChangeattackBonusPercentage)+ChangeflatBonus      +2.72*ChangeelementalMastery
                                                  )+ChangebaseBonusCount*ChangebaseBonus
    return ChangeBaseMultiplier

#增伤区计算
def calculateDamageBonusZone(ChangedamageBonus):
    ChangeDamageBonusZone = ChangedamageBonus+1
    return ChangeDamageBonusZone

#增幅区计算(精通/反应类型(1.5or2.0))
def calculateAmplificationZone(ReactionType,ChangeelementalMastery):
    ChangeAmplificationZone = ReactionType*(1+(2.78*ChangeelementalMastery)/(1400+ChangeelementalMastery)+0)
    return ChangeAmplificationZone

#双爆区计算
def calculateCritMultiplierZone(ChangecritRate,ChangecritDamage):
    if ChangecritRate <= 1:
        ChangeCritZone = ChangecritRate*(ChangecritDamage+1)
        return ChangeCritZone
    if ChangecritRate > 1:
        ChangeCritZone = ChangecritDamage+1
        return  ChangeCritZone


#承伤区计算(抗性/怪物等级/减防数值/无视防御百分比)
def calculateDamageTakenZone(Changeresistance,ChangedefenseReduction,ChangeignoreDefensePct,ChangeenemyLevel):
    if Changeresistance < 0:
        ChangeDamageTakenZone = (90+100)/((90+100)+(1-ChangedefenseReduction)*(1-ChangeignoreDefensePct)*(ChangeenemyLevel+100))*(1-(Changeresistance)/2)
        return ChangeDamageTakenZone
    if resistance >= 0 and resistance < 0.75:
        ChangeDamageTakenZone = (90+100)/((90+100)+(1-ChangedefenseReduction)*(1-ChangeignoreDefensePct)*(ChangeenemyLevel+100))*(1-Changeresistance)
        return ChangeDamageTakenZone
    if resistance >= 0.75:
        ChangeDamageTakenZone = (90+100)/((90+100)+(1-ChangedefenseReduction)*(1-ChangeignoreDefensePct)*(ChangeenemyLevel+100))*(1/(1+Changeresistance*4))
        return ChangeDamageTakenZone

#独立区计算
def calculateIndependentZone(ChangeindependentMultiplier):
    return ChangeindependentMultiplier

#最终伤害计算
def calculateFinalDamage(ChangebaseMultiplier,ChangedamageBonusZone,ChangeamplificationZone,ChangecritZone,ChangedamageTakenZone,ChangeindependentZone):
    ChangeFinalDamage = ChangebaseMultiplier*ChangedamageBonusZone*ChangeamplificationZone*ChangecritZone*ChangedamageTakenZone*ChangeindependentZone
    return ChangeFinalDamage



#暴力穷举破解
max_result = float('-inf')
best_solution = None
best_5= None
for x,y,z,w in itertools.product(range(onelimiteCount),repeat=4):
    if x + y + z + w == artifactStatCount and y + z <= critlimiteCount:
        ChangeattackBonusPercentage,ChangecritRate,ChangecritDamage,ChangeelementalMastery = sum1t(character.attackBonusPercentage,character.critRate,character.critDamage,character.elementalMastery,x,y,z,w)
        ChangebaseMultiplier = calculateBaseMultiplier(ChangeskillMultiplier,ChangebaseAttack,ChangeattackBonusPercentage,ChangeflatBonus,ChangebaseBonusCount,ChangebaseBonus)
        ChangedamageBonusZone = calculateDamageBonusZone(character.damageBonus)
        ChangeamplificationZone = calculateAmplificationZone(character.eleRate,ChangeelementalMastery)
        ChangecritZone = calculateCritMultiplierZone(ChangecritRate,ChangecritDamage)
        ChangedamageTakenZone = calculateDamageTakenZone(Changeresistance,ChangedefenseReduction,ChangeignoreDefensePct,ChangeenemyLevel)
        ChangeindependentZone = calculateIndependentZone(ChangeindependentMultiplier)
        result = calculateFinalDamage(ChangebaseMultiplier,ChangedamageBonusZone,ChangeamplificationZone,ChangecritZone,ChangedamageTakenZone,ChangeindependentZone)
        if result > max_result:
            max_result = result
            best_solution = (x, y, z, w)
            best_5 = (ChangebaseMultiplier,ChangedamageBonusZone,ChangeamplificationZone,ChangecritZone,ChangedamageTakenZone,ChangeindependentZone)
            maxatk = (x*0.05+ChangeattackBonusPercentage+1)*ChangebaseAttack+character.flatBonus
            maxcritRate = ChangecritRate
            maxcritDamge = ChangecritDamage
            maxEle = ChangeelementalMastery
            maxBonus = ChangedamageBonusZone-1
            maxBounsList = (f"{maxatk:.3f}",maxcritRate,maxcritDamge,maxEle,maxBonus)

            #词条收益计算
            ChangeattackBonusPercentage1, ChangecritRate1, ChangecritDamage1, ChangeelementalMastery1 = sum1t(
                character.attackBonusPercentage, character.critRate, character.critDamage, character.elementalMastery,
                x+1, y, z, w)
            ChangebaseMultiplier1 = calculateBaseMultiplier(ChangeskillMultiplier, ChangebaseAttack,
                                                           ChangeattackBonusPercentage1, ChangeflatBonus,
                                                           ChangebaseBonusCount, ChangebaseBonus)
            ChangedamageBonusZone1 = calculateDamageBonusZone(character.damageBonus)
            ChangeamplificationZone1 = calculateAmplificationZone(character.eleRate, ChangeelementalMastery1)
            ChangecritZone1 = calculateCritMultiplierZone(ChangecritRate1, ChangecritDamage1)
            ChangedamageTakenZone1 = calculateDamageTakenZone(Changeresistance, ChangedefenseReduction,
                                                             ChangeignoreDefensePct, ChangeenemyLevel)
            ChangeindependentZone1 = calculateIndependentZone(ChangeindependentMultiplier)
            result1 = calculateFinalDamage(ChangebaseMultiplier1, ChangedamageBonusZone1, ChangeamplificationZone1,
                                          ChangecritZone1, ChangedamageTakenZone1, ChangeindependentZone1)
            xRies = (result1-max_result)/max_result




            ChangeattackBonusPercentage2, ChangecritRate2, ChangecritDamage2, ChangeelementalMastery2 = sum1t(
                character.attackBonusPercentage, character.critRate, character.critDamage, character.elementalMastery,
                x , y+1, z, w)
            ChangebaseMultiplier2 = calculateBaseMultiplier(ChangeskillMultiplier, ChangebaseAttack,
                                                            ChangeattackBonusPercentage2, ChangeflatBonus,
                                                            ChangebaseBonusCount, ChangebaseBonus)
            ChangedamageBonusZone2 = calculateDamageBonusZone(character.damageBonus)
            ChangeamplificationZone2 = calculateAmplificationZone(character.eleRate, ChangeelementalMastery2)
            ChangecritZone2 = calculateCritMultiplierZone(ChangecritRate1, ChangecritDamage2)
            ChangedamageTakenZone2 = calculateDamageTakenZone(Changeresistance, ChangedefenseReduction,
                                                              ChangeignoreDefensePct, ChangeenemyLevel)
            ChangeindependentZone2 = calculateIndependentZone(ChangeindependentMultiplier)
            result1 = calculateFinalDamage(ChangebaseMultiplier2, ChangedamageBonusZone2, ChangeamplificationZone2,
                                           ChangecritZone2, ChangedamageTakenZone2, ChangeindependentZone2)
            yRies = (result1 - max_result) / max_result




            ChangeattackBonusPercentage3, ChangecritRate3, ChangecritDamage3, ChangeelementalMastery3 = sum1t(
                character.attackBonusPercentage, character.critRate, character.critDamage, character.elementalMastery,
                x, y, z+1, w)
            ChangebaseMultiplier3 = calculateBaseMultiplier(ChangeskillMultiplier, ChangebaseAttack,
                                                            ChangeattackBonusPercentage3, ChangeflatBonus,
                                                            ChangebaseBonusCount, ChangebaseBonus)
            ChangedamageBonusZone3 = calculateDamageBonusZone(character.damageBonus)
            ChangeamplificationZone3 = calculateAmplificationZone(character.eleRate, ChangeelementalMastery3)
            ChangecritZone3 = calculateCritMultiplierZone(ChangecritRate1, ChangecritDamage3)
            ChangedamageTakenZone3 = calculateDamageTakenZone(Changeresistance, ChangedefenseReduction,
                                                              ChangeignoreDefensePct, ChangeenemyLevel)
            ChangeindependentZone3 = calculateIndependentZone(ChangeindependentMultiplier)
            result1 = calculateFinalDamage(ChangebaseMultiplier3, ChangedamageBonusZone3, ChangeamplificationZone3,
                                           ChangecritZone3, ChangedamageTakenZone3, ChangeindependentZone3)
            zRies = (result1 - max_result) / max_result




            ChangeattackBonusPercentage4, ChangecritRate4, ChangecritDamage4, ChangeelementalMastery4 = sum1t(
                character.attackBonusPercentage, character.critRate, character.critDamage, character.elementalMastery,
                x, y, z, w+1)
            ChangebaseMultiplier4 = calculateBaseMultiplier(ChangeskillMultiplier, ChangebaseAttack,
                                                            ChangeattackBonusPercentage4, ChangeflatBonus,
                                                            ChangebaseBonusCount, ChangebaseBonus)
            ChangedamageBonusZone4 = calculateDamageBonusZone(character.damageBonus)
            ChangeamplificationZone4 = calculateAmplificationZone(character.eleRate, ChangeelementalMastery4)
            ChangecritZone4 = calculateCritMultiplierZone(ChangecritRate1, ChangecritDamage4)
            ChangedamageTakenZone4 = calculateDamageTakenZone(Changeresistance, ChangedefenseReduction,
                                                              ChangeignoreDefensePct, ChangeenemyLevel)
            ChangeindependentZone4 = calculateIndependentZone(ChangeindependentMultiplier)
            result1 = calculateFinalDamage(ChangebaseMultiplier4, ChangedamageBonusZone4, ChangeamplificationZone4,
                                           ChangecritZone4, ChangedamageTakenZone4, ChangeindependentZone4)
            wRies = (result1 - max_result) / max_result




            ChangeattackBonusPercentage5, ChangecritRate5, ChangecritDamage5, ChangeelementalMastery5 = sum1t(
                character.attackBonusPercentage, character.critRate, character.critDamage, character.elementalMastery,
                x, y, z, w )
            ChangebaseMultiplier5 = calculateBaseMultiplier(ChangeskillMultiplier, ChangebaseAttack,
                                                            ChangeattackBonusPercentage5, ChangeflatBonus,
                                                            ChangebaseBonusCount, ChangebaseBonus)
            ChangedamageBonusZone5 = calculateDamageBonusZone(character.damageBonus+0.05)
            ChangeamplificationZone5 = calculateAmplificationZone(character.eleRate, ChangeelementalMastery5)
            ChangecritZone5 = calculateCritMultiplierZone(ChangecritRate1, ChangecritDamage4)
            ChangedamageTakenZone5 = calculateDamageTakenZone(Changeresistance, ChangedefenseReduction,
                                                              ChangeignoreDefensePct, ChangeenemyLevel)
            ChangeindependentZone5 = calculateIndependentZone(ChangeindependentMultiplier)
            result1 = calculateFinalDamage(ChangebaseMultiplier5, ChangedamageBonusZone5, ChangeamplificationZone5,
                                           ChangecritZone5, ChangedamageTakenZone5, ChangeindependentZone5)
            vRies = (result1 - max_result) / max_result




            sumRies = (f"{xRies:.2%}", f"{yRies:.2%}", f"{zRies:.2%}", f"{wRies:.2%}",f"{ vRies:.2%}")


    #重新初始化

print("当前配队: 仆希茜万 目前圣遗物词条数:",artifactStatCount)
print('最优解(攻击/暴击/爆伤/精通):',best_solution)
print("沙漏/杯子/头部: 精通/精通/爆伤")
print('当前面板(攻击/暴击/爆伤/精通/增伤):',maxBounsList)
print('大招伤害期望最大值:',max_result)
print('乘区情况:',best_5)
print('词条提升率(攻击/暴击/爆伤/精通/增伤:',sumRies)
print('目前设定双爆上限:',critlimiteCount,'\n目前设定单词条上限',onelimiteCount)


