import itertools
import copy
import time


class CharacterStats:
    def __init__(self,
    ############ 基础属性1 ############
                 skill_multiplier_1=34.61,     #倍率类型1
                 base_attack_1=1300,         #基础攻击
                 attack_bonus_pct_1=1.74,      #百分比攻击加成
                 crit_rate_1=0.68,           #暴击率
                 crit_damage_1=1.584,         #爆伤
                 damage_bonus_1=1.13,        #增伤
                 elemental_mastery_1=1,      #元素精通

                 # 特殊加成
                 flat_bonus_1=683.0,          #固定攻击加成(包含羽毛主词条等)
                 base_bonus_1=0,              #固定基础加成(如申鹤羽毛)
                 base_bonus_count_1=0,        #固定基础加成次数

                 #反应乘区
                 reaction_type_1='amplify',   #反应类型"增幅amplify""超激化aggravate""蔓激化spread"
                 quichen_count_1 = 30,         #激化触发次数
                 reaction_rate_1=2.0,         #增幅反应系数
                 reaction_bonus_1 = 0.0,        #反应伤害提升(如魔女套15%)

    ############ 基础属性2 ############
                 skill_multiplier_2=0,     #倍率类型2
                 base_attack_2=1300,         #基础攻击
                 attack_bonus_pct_2=1.74,      #百分比攻击加成
                 crit_rate_2=0.68,           #暴击率
                 crit_damage_2=1.584,         #爆伤
                 damage_bonus_2=1.13,        #增伤
                 elemental_mastery_2=0,      #元素精通(精通为0时不参加反应,参加反应至少为1)

                 # 特殊加成
                 flat_bonus_2=0,          #固定攻击加成(包含羽毛主词条等)
                 base_bonus_2=0,              #固定基础加成(如申鹤羽毛)
                 base_bonus_count_2=0,        #固定基础加成次数

                 #反应乘区
                 reaction_type_2='amplify',   #反应类型"增幅amplify""超激化aggravate""蔓激化spread"
                 quichen_count_2 = 0,         #激化触发次数
                 reaction_rate_2=2.0,         #增幅反应系数
                 reaction_bonus_2 = 0.0,        #反应伤害提升(如魔女套15%)

    ############ 基础属性3 ############
                 skill_multiplier_3=0,     #倍率类型3
                 base_attack_3=1300,         #基础攻击
                 attack_bonus_pct_3=1.74,      #百分比攻击加成
                 crit_rate_3=0.68,           #暴击率
                 crit_damage_3=1.584,         #爆伤
                 damage_bonus_3=1.13,        #增伤
                 elemental_mastery_3=0,      #元素精通(精通为0时不参加反应,参加反应至少为1)

                 # 特殊加成
                 flat_bonus_3=0,          #固定攻击加成(包含羽毛主词条等)
                 base_bonus_3=0,              #固定基础加成(如申鹤羽毛)
                 base_bonus_count_3=0,        #固定基础加成次数

                 #反应乘区
                 reaction_type_3='amplify',   #反应类型"增幅amplify""超激化aggravate""蔓激化spread"
                 quichen_count_3 =0,         #激化触发次数
                 reaction_rate_3=2.0,         #增幅反应系数
                 reaction_bonus_3 = 0.0,        #反应伤害提升(如魔女套15%)





                 #独立乘区
                 independent_multiplier=1.0,#独立乘区

                 #特殊参数,赤沙之杖的精通转攻击为例
                 weapon_em_to_atk_ratio=0,   #精通转攻击比例
                 
                 # 防御属性
                 enemy_resistance=-1.15,    #抗性
                 defense_reduction=0.3,     #减防数值
                 ignore_defense_pct=0.0,    #无视防御数值
                 enemy_level=100,           #敌人等级
                 char_level=90,             #角色等级
                 ):
        # 初始化属性（无圣遗物主词条）_1
        self.skill_multiplier_1 = skill_multiplier_1
        self.base_attack_1 = base_attack_1
        self.attack_bonus_pct_1 = attack_bonus_pct_1
        self.crit_rate_1 = crit_rate_1
        self.crit_damage_1 = crit_damage_1
        self.damage_bonus_1 = damage_bonus_1
        self.elemental_mastery_1 = elemental_mastery_1
        self.reaction_type_1 = reaction_type_1
        self.reaction_rate_1 = reaction_rate_1
        self.flat_bonus_1 = flat_bonus_1
        self.base_bonus_count_1 = base_bonus_count_1
        self.base_bonus_1 = base_bonus_1
        self.quichen_count_1 = quichen_count_1
        self.reaction_bonus_1 = reaction_bonus_1

        # 初始化属性（无圣遗物主词条）_2
        self.skill_multiplier_2 = skill_multiplier_2
        self.base_attack_2 = base_attack_2
        self.attack_bonus_pct_2 = attack_bonus_pct_2
        self.crit_rate_2 = crit_rate_2
        self.crit_damage_2 = crit_damage_2
        self.damage_bonus_2 = damage_bonus_2
        self.elemental_mastery_2 = elemental_mastery_2
        self.reaction_type_2 = reaction_type_2
        self.reaction_rate_2 = reaction_rate_2
        self.flat_bonus_2 = flat_bonus_2
        self.base_bonus_count_2 = base_bonus_count_2
        self.base_bonus_2 = base_bonus_2
        self.quichen_count_2 = quichen_count_2
        self.reaction_bonus_2 = reaction_bonus_2

        # 初始化属性（无圣遗物主词条）_3
        self.skill_multiplier_3 = skill_multiplier_3
        self.base_attack_3 = base_attack_3
        self.attack_bonus_pct_3 = attack_bonus_pct_3
        self.crit_rate_3 = crit_rate_3
        self.crit_damage_3 = crit_damage_3
        self.damage_bonus_3 = damage_bonus_3
        self.elemental_mastery_3 = elemental_mastery_3
        self.reaction_type_3 = reaction_type_3
        self.reaction_rate_3 = reaction_rate_3
        self.flat_bonus_3 = flat_bonus_3
        self.base_bonus_count_3 = base_bonus_count_3
        self.base_bonus_3 = base_bonus_3
        self.quichen_count_3 = quichen_count_3
        self.reaction_bonus_3 = reaction_bonus_3




        # 防御属性
        self.enemy_resistance = enemy_resistance
        self.defense_reduction = defense_reduction
        self.ignore_defense_pct = ignore_defense_pct
        self.enemy_level = enemy_level
        self.char_level = char_level

        #独立乘区
        self.independent_multiplier = independent_multiplier

        # 特殊参数
        self.weapon_em_to_atk_ratio = weapon_em_to_atk_ratio
        
    def valid_check(self):
        """属性有效性检查"""
        self.crit_rate_1 = min(max(self.crit_rate_1, 0.0), 1.0)
        self.crit_rate_2 = min(max(self.crit_rate_2, 0.0), 1.0)
        self.crit_rate_3 = min(max(self.crit_rate_3, 0.0), 1.0)
        self.crit_damage_1 = max(self.crit_damage_1, 0.0)
        self.crit_damage_2 = max(self.crit_damage_2, 0.0)
        self.crit_damage_3 = max(self.crit_damage_3, 0.0)
        self.elemental_mastery_1 = max(self.elemental_mastery_1, 0.0)
        self.elemental_mastery_2 = max(self.elemental_mastery_2, 0.0)
        self.elemental_mastery_3 = max(self.elemental_mastery_3, 0.0)
        return self

    def weapon_attack_bonus(self):
        """武器特效攻击加成"""
        return min(
            self.elemental_mastery_1 * self.weapon_em_to_atk_ratio,
            self.base_attack_1 * 5.0
        )

    def total_attack(self):
        """总攻击力计算"""
        return (self.base_attack_1 * (1 + self.attack_bonus_pct_1)
                + self.flat_bonus_1
                + self.weapon_attack_bonus()    #这条是赤沙的精通转攻击
                )
    
    


class DamageCalculator:
    @staticmethod
    def calculate_damage(char: object) -> object:
        """综合伤害计算"""
        # 基础区计算
        baseMultiplier_1 = char.skill_multiplier_1 * char.total_attack() + char.base_bonus_1#倍率_1
        baseMultiplier_2 = char.skill_multiplier_2 * char.total_attack() + char.base_bonus_2#倍率_2
        baseMultiplier_3 = char.skill_multiplier_3 * char.total_attack() + char.base_bonus_3#倍率_2

        # 增伤区计算
        damageBonusZone_1 = 1 + char.damage_bonus_1
        damageBonusZone_2 = 1 + char.damage_bonus_2
        damageBonusZone_3 = 1 + char.damage_bonus_3

        # 双爆区计算
        critMultiplierZone_1 = 1 + min(char.crit_rate_1, 1.0) * char.crit_damage_1
        critMultiplierZone_2 = 1 + min(char.crit_rate_2, 1.0) * char.crit_damage_2
        critMultiplierZone_3 = 1 + min(char.crit_rate_3, 1.0) * char.crit_damage_3

        # 防御区计算
        defense = (char.enemy_level + 100) * (1 - char.defense_reduction) * (1 - char.ignore_defense_pct)
        defense_multiplier = (char.char_level + 100) / (char.char_level + 100 + defense)

        # 反应区-------------------------------_1
        if char.reaction_type_1 == 'amplify':     #增幅反应
            mastery_factor_1 = (2.78 * char.elemental_mastery_1) / (1400 + char.elemental_mastery_1)+char.reaction_bonus_1
            reaction_multiplier_1 = char.reaction_rate_1 * (1 + mastery_factor_1)
        else:
            reaction_multiplier_1 = 1.0
        
        if char.reaction_type_1 == 'aggravate':   #超激化反应
            quichen_base_1 = 1446.853458*1.15*(1+(5*char.elemental_mastery_1)/(char.elemental_mastery_1+1200)+char.reaction_bonus_1)
            baseMultiplier_1 += quichen_base_1*char.quichen_count_1
        elif char.reaction_type_1 == 'spread':    #蔓激化反应
            quichen_base_1 = 1446.853458*1.25*(1+(5*char.elemental_mastery_1)/(char.elemental_mastery_1+1200)+char.reaction_bonus_1)
            baseMultiplier_1 += quichen_base_1*char.quichen_count_1
        else:
            baseMultiplier_1 = baseMultiplier_1

        # 反应区-------------------------------_2
        if char.reaction_type_2 == 'amplify':     #增幅反应
            mastery_factor_2 = (2.78 * char.elemental_mastery_2) / (1400 + char.elemental_mastery_2)+char.reaction_bonus_2
            reaction_multiplier_2 = char.reaction_rate_2 * (1 + mastery_factor_2)
        else:
            reaction_multiplier_2 = 1.0
        
        if char.reaction_type_2 == 'aggravate':   #超激化反应
            quichen_base_2 = 1446.853458*1.15*(1+(5*char.elemental_mastery_2)/(char.elemental_mastery_2+1200)+char.reaction_bonus_2)
            baseMultiplier_2 += quichen_base_2*char.quichen_count_2
        elif char.reaction_type_1 == 'spread':    #蔓激化反应
            quichen_base_2 = 1446.853458*1.25*(1+(5*char.elemental_mastery_2)/(char.elemental_mastery_2+1200)+char.reaction_bonus_2)
            baseMultiplier_2 += quichen_base_2*char.quichen_count_2
        else:
            baseMultiplier_2 = baseMultiplier_2
        
        # 反应区-------------------------------_3
        if char.reaction_type_3 == 'amplify':     #增幅反应
            mastery_factor_3 = (2.78 * char.elemental_mastery_3) / (1400 + char.elemental_mastery_3)+char.reaction_bonus_3
            reaction_multiplier_3 = char.reaction_rate_3 * (1 + mastery_factor_3)
        else:
            reaction_multiplier_3 = 1.0
        
        if char.reaction_type_3 == 'aggravate':   #超激化反应
            quichen_base_3 = 1446.853458*1.15*(1+(5*char.elemental_mastery_3)/(char.elemental_mastery_3+1200)+char.reaction_bonus_3)
            baseMultiplier_3 += quichen_base_3*char.quichen_count_3
        elif char.reaction_type_3 == 'spread':    #蔓激化反应
            quichen_base_3 = 1446.853458*1.25*(1+(5*char.elemental_mastery_3)/(char.elemental_mastery_3+1200)+char.reaction_bonus_3)
            baseMultiplier_3 += quichen_base_3*char.quichen_count_3
        else:
            baseMultiplier_3 = baseMultiplier_3

        # 抗性区
        resist = char.enemy_resistance
        if resist < 0:
            resist_multiplier = 1 - resist / 2
        elif resist < 0.75:
            resist_multiplier = 1 - resist
        else:
            resist_multiplier = 1 / (1 + 4 * resist)

        # 伤害倍率1
        dmg1 =  (baseMultiplier_1#这里是基础区
                 *reaction_multiplier_1#增幅区
                 *damageBonusZone_1#这是增伤区
                 *critMultiplierZone_1#双爆区
                 *defense_multiplier#防御区
                 *resist_multiplier#抗性区
                 *char.independent_multiplier#独立区                            
                )
        # 伤害倍率2
        dmg2 =  (baseMultiplier_2#这里是基础区
                 *reaction_multiplier_2#增幅区
                 *damageBonusZone_2#这是增伤区
                 *critMultiplierZone_2#双爆区
                 *defense_multiplier#防御区
                 *resist_multiplier#抗性区
                 *char.independent_multiplier#独立区                            
                )
        # 伤害倍率3
        dmg3 =  (baseMultiplier_3#这里是基础区
                 *reaction_multiplier_3#增幅区
                 *damageBonusZone_3#这是增伤区
                 *critMultiplierZone_3#双爆区
                 *defense_multiplier#防御区
                 *resist_multiplier#抗性区
                 *char.independent_multiplier#独立区                            
                )
        return (
            dmg1
            +dmg2
            +dmg3               
        )


class ArtifactOptimizer:
    '''求解主副词条最优选择'''
    def __init__(self, base_char):
        self.base_char = copy.deepcopy(base_char)
        self.main_options = [
            [  # 沙漏
                {'atk_pct': 46.6 / 100},  # 攻击
                {'em': 187}  # 精通
            ],
            [  # 杯子
                {'atk_pct': 46.6 / 100},  # 攻击
                {'em': 187},  # 精通
                {'dmg_bonus': 46.6 / 100}  # 增伤
            ],
            [  # 头冠
                {'atk_pct': 46.6 / 100},  # 攻击
                {'em': 187},  # 精通
                {'cd': 66.2 / 100},  # 暴伤
                {'cr': 33.1 / 100}  # 暴击
            ]
        ]
        self.substat_rules = {
            'total': 42,                #总词条数
            'crit_limit': 32,           #双爆词条上限
            'stat_limits': 24           #单词条上限
        }

    def _apply_main_stats(self, combination):
        """应用主词条组合"""
        temp_char = copy.deepcopy(self.base_char)
        for slot_idx, option_idx in enumerate(combination):
            option = self.main_options[slot_idx][option_idx]
            for attr, value in option.items():
                if attr == 'atk_pct':
                    temp_char.attack_bonus_pct_1 += value
                    temp_char.attack_bonus_pct_2 += value
                    temp_char.attack_bonus_pct_3 += value
                elif attr == 'em':
                    temp_char.elemental_mastery_1 += value
                    temp_char.elemental_mastery_2 += value
                    temp_char.elemental_mastery_3 += value
                elif attr == 'dmg_bonus':
                    temp_char.damage_bonus_1 += value
                    temp_char.damage_bonus_2 += value
                    temp_char.damage_bonus_3 += value
                elif attr == 'cd':
                    temp_char.crit_damage_1 += value
                    temp_char.crit_damage_2 += value
                    temp_char.crit_damage_3 += value
                elif attr == 'cr':
                    temp_char.crit_rate_1 += value
                    temp_char.crit_rate_2 += value
                    temp_char.crit_rate_3 += value
        return temp_char.valid_check()

    def _optimize_substats(self, base_char):
        """优化副词条分配"""
        max_dmg = 0
        best_sub = (0, 0, 0, 0)

        # 生成有效副词条组合
        for atk, cr, cd, em in itertools.product(
                range(self.substat_rules['stat_limits'] + 1),
                repeat=4
        ):
            if (atk + cr + cd + em == self.substat_rules['total'] and
                    cr + cd <= self.substat_rules['crit_limit'] and
                    max(atk, cr, cd, em) <= self.substat_rules['stat_limits']):

                temp_char = copy.deepcopy(base_char)
                temp_char.attack_bonus_pct_1 += atk * 0.05
                temp_char.attack_bonus_pct_2 += atk * 0.05
                temp_char.attack_bonus_pct_3 += atk * 0.05
                temp_char.crit_rate_1 += cr * 0.033
                temp_char.crit_rate_2 += cr * 0.033
                temp_char.crit_rate_3 += cr * 0.033
                temp_char.crit_damage_1 += cd * 0.066
                temp_char.crit_damage_2 += cd * 0.066
                temp_char.crit_damage_3 += cd * 0.066
                temp_char.elemental_mastery_1 += em * 20
                temp_char.elemental_mastery_2 += em * 20
                temp_char.elemental_mastery_3 += em * 20
                temp_char.valid_check()

                current_dmg = DamageCalculator.calculate_damage(temp_char)
                if current_dmg > max_dmg:
                    max_dmg = current_dmg
                    best_sub = (atk, cr, cd, em)

        return best_sub, max_dmg

    def _calculate_marginal_gains(self, final_char):
        """计算边际收益（含增伤词条）"""
        gains = {}
        base_dmg = DamageCalculator.calculate_damage(final_char)

        # 攻击词条
        temp = copy.deepcopy(final_char)
        temp.attack_bonus_pct_1 += 0.05
        temp.attack_bonus_pct_2 += 0.05
        temp.attack_bonus_pct_3 += 0.05
        gains['atk'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 暴击词条
        temp = copy.deepcopy(final_char)
        temp.crit_rate_1 += 0.033
        temp.crit_rate_2 += 0.033
        temp.crit_rate_3 += 0.033
        gains['cr'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 暴伤词条
        temp = copy.deepcopy(final_char)
        temp.crit_damage_1 += 0.066
        temp.crit_damage_2 += 0.066
        temp.crit_damage_3 += 0.066
        gains['cd'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 精通词条
        temp = copy.deepcopy(final_char)
        temp.elemental_mastery_1 += 20
        temp.elemental_mastery_2 += 20
        temp.elemental_mastery_3 += 20
        gains['em'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 增伤词条（理论值）
        temp = copy.deepcopy(final_char)
        temp.damage_bonus_1 += 0.05
        temp.damage_bonus_2 += 0.05
        temp.damage_bonus_3 += 0.05
        gains['dmg_bonus'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        return gains

    def optimize(self):
        """综合优化主词条和副词条"""
        start_time = time.time()
        global_best = {
            'damage': 0,
            'main_combo': None,
            'sub_allocation': None,
            'gains': None,
            'final_char': None
        }

        # 生成所有主词条组合（沙漏×杯子×头冠）
        main_combinations = itertools.product(
            range(len(self.main_options[0])),
            range(len(self.main_options[1])),
            range(len(self.main_options[2]))
        )

        for main_combo in main_combinations:
            # 应用主词条
            temp_char = self._apply_main_stats(main_combo)

            # 优化副词条
            sub_allocation, sub_damage = self._optimize_substats(temp_char)

            # 更新全局最优
            if sub_damage > global_best['damage']:
                # 构建最终角色
                final_char = copy.deepcopy(temp_char)
                final_char.attack_bonus_pct_1 += sub_allocation[0] * 0.05
                final_char.attack_bonus_pct_2 += sub_allocation[0] * 0.05
                final_char.attack_bonus_pct_3 += sub_allocation[0] * 0.05
                final_char.crit_rate_1 += sub_allocation[1] * 0.033
                final_char.crit_rate_2 += sub_allocation[1] * 0.033
                final_char.crit_rate_3 += sub_allocation[1] * 0.033
                final_char.crit_damage_1 += sub_allocation[2] * 0.066
                final_char.crit_damage_2 += sub_allocation[2] * 0.066
                final_char.crit_damage_3 += sub_allocation[2] * 0.066
                final_char.elemental_mastery_1 += sub_allocation[3] * 20
                final_char.elemental_mastery_2 += sub_allocation[3] * 20
                final_char.elemental_mastery_3 += sub_allocation[3] * 20
                final_char.valid_check()

                global_best.update({
                    'damage': sub_damage,
                    'main_combo': main_combo,
                    'sub_allocation': sub_allocation,
                    'gains': self._calculate_marginal_gains(final_char),
                    'final_char': final_char
                })

        print(f"优化完成，耗时：{time.time() - start_time:.2f}秒")
        return global_best


def format_main_combo(combo):
    """格式化主词条组合"""
    names = [
        ["攻击沙", "精通沙"],
        ["攻击杯", "精通杯", "增伤杯"],
        ["攻击头", "精通头", "暴伤头", "暴击头"]
    ]
    return " | ".join([names[i][v] for i, v in enumerate(combo)])


def format_result(result):
    """格式化输出结果"""
    c = result['final_char']
    report = f"""
=== 最终优化结果 ===
总伤害：{result['damage']:,.0f}

【最优主词条配置】
{format_main_combo(result['main_combo'])}

【最优副词条分配】
攻击词条：{result['sub_allocation'][0]}
暴击词条：{result['sub_allocation'][1]}
暴伤词条：{result['sub_allocation'][2]}
精通词条：{result['sub_allocation'][3]}

【当前面板】
总攻击力：{c.total_attack():.1f}
暴击率：{c.crit_rate_1:.1%}
暴击伤害：{c.crit_damage_1:.1%}
元素精通：{c.elemental_mastery_1}
伤害加成：{c.damage_bonus_1:.1%}
武器特效转攻击加成：{c.weapon_attack_bonus():,.0f}

【边际收益/词条】
攻击：{result['gains']['atk']:.2%}
暴击：{result['gains']['cr']:.2%}
暴伤：{result['gains']['cd']:.2%}
精通：{result['gains']['em']:.2%}
增伤：{result['gains']['dmg_bonus']:.2%}
"""
    return report


# 使用示例
if __name__ == "__main__":
    # 初始化基础角色（无圣遗物主词条）
    base_char = CharacterStats()

    # 执行优化
    optimizer = ArtifactOptimizer(base_char)
    result = optimizer.optimize()

    print(format_result(result))