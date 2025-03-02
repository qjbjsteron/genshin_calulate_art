import itertools
import copy
import time
from concurrent.futures import ProcessPoolExecutor

class CharacterStats:
    def __init__(self, 
                 # 使用字典存储多倍率类型(可自行按照格式添加)
                 #瓦雷莎
                 skill_data={
                     1: {'multiplier': 7.344, 'base_attack': 1013.63, 'attack_pct': 0.76, 'crit_rate': 0.465, #瓦q
                         'crit_damage': 1.941, 'damage_bonus': 1.24, 'em': 0, 'flat_bonus': 685, 
                         'base_bonus': 0, 'base_count': 0, 'reaction_type': 'NONE', 
                         'quichen_count': 0, 'reaction_rate': 1, 'reaction_bonus': 0.0},
                     2: {'multiplier': 2.703, 'base_attack': 1013.63, 'attack_pct': 1.36, 'crit_rate': 0.365,  #第一个e
                         'crit_damage': 0.5, 'damage_bonus': 2.152, 'em': 0, 'flat_bonus': 685,
                         'base_bonus': 0, 'base_count': 0, 'reaction_type': 'NONE',
                         'quichen_count': 0, 'reaction_rate': 1, 'reaction_bonus': 0.0},
                     3: {'multiplier': 9.84, 'base_attack': 1013.63, 'attack_pct': 1.81, 'crit_rate': 0.365,   #瓦重击*4
                         'crit_damage': 0.941, 'damage_bonus': 2.472, 'em': 0, 'flat_bonus': 685,
                         'base_bonus': 2900, 'base_count': 3, 'reaction_type': 'NONE',
                         'quichen_count': 0, 'reaction_rate': 1, 'reaction_bonus': 0.0},
                     4: {'multiplier': 8.109, 'base_attack': 1013.63, 'attack_pct': 1.81, 'crit_rate': 0.365,  #瓦e*3
                         'crit_damage': 0.941, 'damage_bonus': 2.152, 'em': 0, 'flat_bonus': 685,
                         'base_bonus': 0, 'base_count': 0, 'reaction_type': 'NONE',
                         'quichen_count': 0, 'reaction_rate': 1, 'reaction_bonus': 0.0},
                     5: {'multiplier': 26.76, 'base_attack': 1013.63, 'attack_pct': 1.81, 'crit_rate': 0.52,  #瓦下落*4
                         'crit_damage': 3.301, 'damage_bonus': 4.772, 'em': 0, 'flat_bonus': 685,
                         'base_bonus': 100700, 'base_count': 1, 'reaction_type': 'NONE',
                         'quichen_count': 0, 'reaction_rate': 1, 'reaction_bonus': 0.0},
                     6: {'multiplier': 34.224, 'base_attack': 1013.63, 'attack_pct': 1.81, 'crit_rate': 0.52,  #瓦小q*4
                         'crit_damage': 3.301, 'damage_bonus': 5.772, 'em': 0, 'flat_bonus': 685,
                         'base_bonus': 80700, 'base_count': 1, 'reaction_type': 'NONE',
                         'quichen_count': 0, 'reaction_rate': 1, 'reaction_bonus': 0.0},
                     7: {'multiplier': 7.148, 'base_attack': 1013.63, 'attack_pct': 1.81, 'crit_rate': 0.365,  #瓦擦伤*4
                         'crit_damage': 0.941, 'damage_bonus': 2.152, 'em': 0, 'flat_bonus': 685,
                         'base_bonus': 0, 'base_count': 0, 'reaction_type': 'NONE',
                         'quichen_count': 0, 'reaction_rate': 1, 'reaction_bonus': 0.0},
                 },
                 # 公共属性
                 weapon_em_to_atk=0,
                 enemy_resist=-0.75,
                 defense_red=0,
                 ignore_def=0.0,
                 enemy_lv=100,
                 char_lv=90,
                 independent=1.0):
        
        # 初始化倍率数据
        self.skills = {k: copy.deepcopy(v) for k, v in skill_data.items()}
        
        # 武器和防御属性
        self.weapon_em_to_atk = weapon_em_to_atk
        self.enemy_resist = enemy_resist
        self.defense_red = defense_red
        self.ignore_def = ignore_def
        self.enemy_lv = enemy_lv
        self.char_lv = char_lv
        self.independent = independent

    def valid_check(self):
        """统一属性校验"""
        for sid in self.skills:
            s = self.skills[sid]
            s['crit_rate'] = max(0.0, min(s['crit_rate'], 1.0))
            s['crit_damage'] = max(s['crit_damage'], 0.0)
            s['em'] = max(s['em'], 0.0)
        return self

    def weapon_atk_bonus(self):
        """武器攻击加成"""
        total_em = sum(s['em'] for s in self.skills.values())
        return min(total_em * self.weapon_em_to_atk, 5.0 * max(s['base_attack'] for s in self.skills.values()))

    def total_attack(self, sid):
        """计算指定倍率类型的总攻击"""
        s = self.skills[sid]
        return s['base_attack'] * (1 + s['attack_pct']) + s['flat_bonus'] + self.weapon_atk_bonus()

class DamageCalculator:
    @staticmethod
    def calculate(char):
        """优化后的伤害计算"""
        # 公共乘区计算
        defense = (char.enemy_lv + 100) * (1 - char.defense_red) * (1 - char.ignore_def)
        def_mult = (char.char_lv + 100) / (char.char_lv + 100 + defense)
        
        resist = char.enemy_resist
        resist_mult = 1 - resist/2 if resist < 0 else \
                     (1 - resist) if resist < 0.75 else 1/(1+4*resist)
        
        total_dmg = 0
        
        for sid in char.skills:
            s = char.skills[sid]
            if s['multiplier'] <= 0:
                continue
            
            # 基础区
            base = s['multiplier'] * char.total_attack(sid) + s['base_bonus']
            
            # 反应处理
            react_type = s['reaction_type']
            if react_type == 'amplify':
                mastery = (2.78 * s['em']) / (1400 + s['em']) + s['reaction_bonus']
                react_mult = s['reaction_rate'] * (1 + mastery)
            elif react_type in ('aggravate', 'spread'):
                coeff = 1.15 if react_type == 'aggravate' else 1.25
                base += 1446.85 * coeff * (1 + (5*s['em'])/(s['em']+1200)+s['reaction_bonus'])*s['quichen_count']
                react_mult = 1.0
            else:
                react_mult = 1.0
            
            # 综合计算
            total_dmg += base * \
                       (1 + s['damage_bonus']) * \
                       (1 + min(s['crit_rate'],1)*s['crit_damage']) * \
                       react_mult * \
                       def_mult * \
                       resist_mult * \
                       char.independent
        
        return total_dmg

class ArtifactOptimizer:
    def __init__(self, base_char):
        self.base_char = copy.deepcopy(base_char)
        self.main_opts = [
            [{'atk_pct':0.466}, {'em':187}],  # 沙漏
            [{'atk_pct':0.466}, {'em':187}, {'dmg_bonus':0.466}],  # 杯子
            [{'atk_pct':0.466}, {'em':187}, {'cd':0.662}, {'cr':0.331}]  # 头冠
        ]
        self.sub_rules = {'total':40, 'crit_limit':32, 'stat_limits':24}
        self.sub_cache = None  # 副词条组合缓存

    def _gen_substats(self):
        """预生成有效副词条组合"""
        if self.sub_cache: return self.sub_cache
        
        valid_subs = []
        for atk, cr, cd, em in itertools.product(
            range(self.sub_rules['stat_limits']+1), repeat=4):
            
            if (atk + cr + cd + em == self.sub_rules['total'] and
                cr + cd <= self.sub_rules['crit_limit'] and
                max(atk, cr, cd, em) <= self.sub_rules['stat_limits']):
                valid_subs.append((atk, cr, cd, em))
        
        self.sub_cache = valid_subs
        return valid_subs

    def _apply_main(self, combo):
        """应用主词条组合"""
        temp = copy.deepcopy(self.base_char)
        for slot, opt_idx in enumerate(combo):
            for attr, val in self.main_opts[slot][opt_idx].items():
                for sid in temp.skills:
                    if attr == 'atk_pct':
                        temp.skills[sid]['attack_pct'] += val
                    elif attr == 'em':
                        temp.skills[sid]['em'] += val
                    elif attr == 'dmg_bonus':
                        temp.skills[sid]['damage_bonus'] += val
                    elif attr == 'cd':
                        temp.skills[sid]['crit_damage'] += val
                    elif attr == 'cr':
                        temp.skills[sid]['crit_rate'] += val
        return temp.valid_check()

    def _eval_combo(self, combo):
        """评估单个主词条组合"""
        temp_char = self._apply_main(combo)
        best_sub, max_dmg = (0,0,0,0), 0
        
        for sub in self._gen_substats():
            test_char = copy.deepcopy(temp_char)
            atk, cr, cd, em = sub
            for sid in test_char.skills:
                s = test_char.skills[sid]
                s['attack_pct'] += atk*0.05
                s['crit_rate'] += cr*0.033
                s['crit_damage'] += cd*0.066
                s['em'] += em*20
            
            dmg = DamageCalculator.calculate(test_char.valid_check())
            if dmg > max_dmg:
                max_dmg = dmg
                best_sub = sub
        
        return (combo, best_sub, max_dmg)

    def optimize(self):
        """并行优化主词条"""
        start = time.time()
        combos = list(itertools.product(*[range(len(opts)) for opts in self.main_opts]))
        
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(self._eval_combo, combos))
        
        best = max(results, key=lambda x: x[2])
        final_char = self._build_final(best[0], best[1])
        
        return {
            'damage': best[2],
            'main_combo': best[0],
            'sub_allocation': best[1],
            'gains': self._calc_margins(final_char),
            'final_char': final_char
        }

    def _build_final(self, main_combo, sub_allocation):
        """构建最终角色"""
        final = self._apply_main(main_combo)
        atk, cr, cd, em = sub_allocation
        for sid in final.skills:
            s = final.skills[sid]
            s['attack_pct'] += atk*0.05
            s['crit_rate'] += cr*0.033
            s['crit_damage'] += cd*0.066
            s['em'] += em*20
        return final.valid_check()

    def _calc_margins(self, char):
        """计算边际收益"""
        base = DamageCalculator.calculate(char)
        margins = {}
        
        # 测试各属性
        test_cases = [
            ('atk', [('attack_pct', 0.05)]),
            ('cr', [('crit_rate', 0.033)]),
            ('cd', [('crit_damage', 0.066)]),
            ('em', [('em', 20)]),
            ('dmg_bonus', [('damage_bonus', 0.05)])
        ]
        
        for name, mods in test_cases:
            temp = copy.deepcopy(char)
            for sid in temp.skills:
                for attr, delta in mods:
                    temp.skills[sid][attr] += delta
            margins[name] = (DamageCalculator.calculate(temp) - base)/base
        
        return margins

def format_main_combo(combo):
    """将主词条组合转换为可读文本"""
    parts = [
        ["攻击沙", "精通沙"],  # 部位0
        ["攻击杯", "精通杯", "增伤杯"],  # 部位1
        ["攻击头", "精通头", "暴伤头", "暴击头"]  # 部位2
    ]
    return " | ".join([parts[i][v] for i, v in enumerate(combo)])

def format_result(result):
    """格式化最终结果输出"""
    c = result['final_char']
    main_combo = result['main_combo']
    sub_alloc = result['sub_allocation']
    gains = result['gains']
    
    # 获取第一个有效倍率类型的面板数据
    sid = next(k for k in c.skills if c.skills[k]['multiplier'] > 0)
    skill_data = c.skills[sid]

    
    
    report = f"""
=== 最终优化结果 ===
总伤害：{result['damage']:,.0f}

【最优主词条配置】
{format_main_combo(main_combo)}

【最优副词条分配】
攻击词条：{sub_alloc[0]}
暴击词条：{sub_alloc[1]}
暴伤词条：{sub_alloc[2]}
精通词条：{sub_alloc[3]}

【当前面板 - 技能类型{sid}】
总攻击力：{c.total_attack(sid):.1f}
暴击率：{skill_data['crit_rate']:.1%}
暴击伤害：{skill_data['crit_damage']:.1%}
元素精通：{skill_data['em']}
伤害加成：{skill_data['damage_bonus']:.1%}
武器特效攻击：{c.weapon_atk_bonus():.0f}

【边际收益/词条】
攻击：{gains['atk']:.2%}
暴击：{gains['cr']:.2%}
暴伤：{gains['cd']:.2%}
精通：{gains['em']:.2%}
增伤：{gains['dmg_bonus']:.2%}
"""
    # 在format_result中添加
    report += "\n【详细倍率数据】\n"
    for sid, data in c.skills.items():
        if data['multiplier'] <= 0:
            continue
        report += f"类型{sid}: 倍率{data['multiplier']} 攻击{data['attack_pct']:.1%} 总攻击力：{c.total_attack(sid):.1f} "
        report += f"暴击{data['crit_rate']:.1%} 暴伤{data['crit_damage']:.1%} 增伤{data['damage_bonus']:.1%}\n"
    return report



if __name__ == "__main__":
    base = CharacterStats()
    optimizer = ArtifactOptimizer(base)
    result = optimizer.optimize()
    print(format_result(result))