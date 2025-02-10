import itertools
import copy
import time


class CharacterStats:
    def __init__(self,
                 # 基础属性
                 skill_multiplier=34.61,     #可反应倍率
                 normal_skill_multiplier=24.5,#正常倍率
                 base_attack=1300,         #基础攻击
                 attack_bonus_pct=1.74,      #百分比攻击加成
                 crit_rate=0.68,           #暴击率
                 crit_damage=1.584,         #爆伤
                 damage_bonus=1.13,        #增伤
                 elemental_mastery=1,   #元素精通

                 # 防御属性
                 enemy_resistance=-1.15,    #抗性
                 defense_reduction=0.3,     #减防数值
                 ignore_defense_pct=0.0,    #无视防御数值
                 enemy_level=100,           #敌人等级
                 char_level=90,             #角色等级

                 # 特殊加成
                 flat_bonus=683.0,          #固定攻击加成(包含羽毛主词条等)
                 base_bonus=0,              #固定基础加成(如申鹤羽毛)
                 base_bonus_count=0,        #固定基础加成次数

                 #反应乘区
                 reaction_type='amplify',   #反应类型"增幅amplify""超激化aggravate""蔓激化spread"
                 quichen_count = 30,         #激化触发次数
                 reaction_rate=2.0,         #增幅反应系数
                 reaction_bonus = 0.0,        #反应伤害提升(如魔女套15%)
                 #独立乘区
                 independent_multiplier=1.0,#独立乘区

                 #特殊参数,赤沙之杖的精通转攻击为例
                 weapon_em_to_atk_ratio=0,   #精通转攻击比例
                 ):
        # 初始化属性（无圣遗物主词条）
        self.skill_multiplier = skill_multiplier
        self.normal_skill_multiplier = normal_skill_multiplier
        self.base_attack = base_attack
        self.attack_bonus_pct = attack_bonus_pct
        self.crit_rate = crit_rate
        self.crit_damage = crit_damage
        self.damage_bonus = damage_bonus
        self.elemental_mastery = elemental_mastery
        

        # 防御属性
        self.enemy_resistance = enemy_resistance
        self.defense_reduction = defense_reduction
        self.ignore_defense_pct = ignore_defense_pct
        self.enemy_level = enemy_level
        self.char_level = char_level

        # 特殊加成
        self.flat_bonus = flat_bonus
        self.base_bonus_count = base_bonus_count
        self.base_bonus = base_bonus
        self.independent_multiplier = independent_multiplier
        self.quichen_count = quichen_count
        self.reaction_bonus = reaction_bonus

        # 武器反应参数
        self.weapon_em_to_atk_ratio = weapon_em_to_atk_ratio
        self.reaction_type = reaction_type
        self.reaction_rate = reaction_rate

    def valid_check(self):
        """属性有效性检查"""
        self.crit_rate = min(max(self.crit_rate, 0.0), 1.0)
        self.crit_damage = max(self.crit_damage, 0.0)
        self.elemental_mastery = max(self.elemental_mastery, 0.0)
        return self

    def weapon_attack_bonus(self):
        """武器特效攻击加成"""
        return min(
            self.elemental_mastery * self.weapon_em_to_atk_ratio,
            self.base_attack * 5.0
        )

    def total_attack(self):
        """总攻击力计算"""
        return (self.base_attack * (1 + self.attack_bonus_pct)
                + self.flat_bonus
                + self.weapon_attack_bonus()    #这条是赤沙的精通转攻击
                )
    
    


class DamageCalculator:
    @staticmethod
    def calculate_damage(char: object) -> object:
        """综合伤害计算"""
        # 基础区计算
        baseMultiplier1 = char.skill_multiplier * char.total_attack() + char.base_bonus#可反应倍率
        baseMultiplier2 = char.normal_skill_multiplier * char.total_attack() + char.base_bonus#普通倍率

        # 增伤区计算
        damageBonusZone = 1 + char.damage_bonus

        # 双爆区计算
        critMultiplierZone = 1 + min(char.crit_rate, 1.0) * char.crit_damage

        # 防御区计算
        defense = (char.enemy_level + 100) * (1 - char.defense_reduction) * (1 - char.ignore_defense_pct)
        defense_multiplier = (char.char_level + 100) / (char.char_level + 100 + defense)

        # 抗性区
        resist = char.enemy_resistance
        if resist < 0:
            resist_multiplier = 1 - resist / 2
        elif resist < 0.75:
            resist_multiplier = 1 - resist
        else:
            resist_multiplier = 1 / (1 + 4 * resist)

        # 反应区
        if char.reaction_type == 'amplify':     #增幅反应
            mastery_factor = (2.78 * char.elemental_mastery) / (1400 + char.elemental_mastery)+char.reaction_bonus
            reaction_multiplier = char.reaction_rate * (1 + mastery_factor)
        else:
            reaction_multiplier = 1.0
        
        if char.reaction_type == 'aggravate':   #超激化反应
            quichen_base = 1446.853458*1.15*(1+(5*char.elemental_mastery)/(char.elemental_mastery+1200)+char.reaction_bonus)
            baseMultiplier1 += quichen_base*char.quichen_count
        elif char.reaction_type == 'spread':    #蔓激化反应
            quichen_base = 1446.853458*1.25*(1+(5*char.elemental_mastery)/(char.elemental_mastery+1200)+char.reaction_bonus)
            baseMultiplier1 += quichen_base*char.quichen_count
        else:
            baseMultiplier1 = baseMultiplier1



        # 可反应伤害
        dmg1 =  (baseMultiplier1#这里是基础区
                 *reaction_multiplier#增幅区
                 *damageBonusZone#这是增伤区
                 *critMultiplierZone#双爆区
                 *defense_multiplier#防御区
                 *resist_multiplier#抗性区
                 *char.independent_multiplier#独立区                            
                )
        # 普通伤害
        dmg2 = (baseMultiplier2#这里是基础区
                 *damageBonusZone#这是增伤区
                 *critMultiplierZone#双爆区
                 *defense_multiplier#防御区
                 *resist_multiplier#抗性区
                 *char.independent_multiplier#独立区                            
                )

        return (
            dmg1
            +dmg2               
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
                    temp_char.attack_bonus_pct += value
                elif attr == 'em':
                    temp_char.elemental_mastery += value
                elif attr == 'dmg_bonus':
                    temp_char.damage_bonus += value
                elif attr == 'cd':
                    temp_char.crit_damage += value
                elif attr == 'cr':
                    temp_char.crit_rate += value
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
                temp_char.attack_bonus_pct += atk * 0.05
                temp_char.crit_rate += cr * 0.033
                temp_char.crit_damage += cd * 0.066
                temp_char.elemental_mastery += em * 20
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
        temp.attack_bonus_pct += 0.05
        gains['atk'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 暴击词条
        temp = copy.deepcopy(final_char)
        temp.crit_rate += 0.033
        gains['cr'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 暴伤词条
        temp = copy.deepcopy(final_char)
        temp.crit_damage += 0.066
        gains['cd'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 精通词条
        temp = copy.deepcopy(final_char)
        temp.elemental_mastery += 20
        gains['em'] = (DamageCalculator.calculate_damage(temp) - base_dmg) / base_dmg

        # 增伤词条（理论值）
        temp = copy.deepcopy(final_char)
        temp.damage_bonus += 0.05
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
                final_char.attack_bonus_pct += sub_allocation[0] * 0.05
                final_char.crit_rate += sub_allocation[1] * 0.033
                final_char.crit_damage += sub_allocation[2] * 0.066
                final_char.elemental_mastery += sub_allocation[3] * 20
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
暴击率：{c.crit_rate:.1%}
暴击伤害：{c.crit_damage:.1%}
元素精通：{c.elemental_mastery}
伤害加成：{c.damage_bonus:.1%}
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