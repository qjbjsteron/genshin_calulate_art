import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from text import CharacterStats, ArtifactOptimizer, format_result
import threading
import json
import re

# ==================== 自定义验证输入组件 ====================
class ValidatedEntry(ttk.Entry):
    """支持小数和负数的验证文本框"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vcmd = (self.register(self.validate), '%P')
        self.configure(
            validate='key',
            validatecommand=vcmd,
            width=15
        )
    
    def validate(self, new_text):
        """验证规则：允许数字、小数点和负号"""
        if not new_text:
            return True
        return re.match(r'^[-+]?[0-9]*\.?[0-9]*$', new_text) is not None

# ==================== 技能编辑器窗口 ====================
class SkillEditorWindow(tk.Toplevel):
    def __init__(self, parent, skill_data):
        super().__init__(parent)
        self.title("技能编辑器")
        self.parent = parent
        self.skill_data = skill_data
        self.current_max_id = max(skill_data.keys()) if skill_data else 0
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 表格框架
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 表头
        headers = ["技能ID", "倍率", "基础攻击", "攻击%", "暴击率%", "暴伤%", 
                  "增伤%", "元素精通", "固定加成", "基础加成", "反应类型", "操作"]
        for col, text in enumerate(headers):
            ttk.Label(table_frame, text=text, relief="ridge", anchor="center").grid(
                row=0, column=col, sticky="nsew", padx=1, pady=1
            )
            table_frame.grid_columnconfigure(col, weight=1)
        
        # 动态生成输入行
        self.entries = {}
        self._create_rows(table_frame)

        # 按钮区
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="➕ 添加技能", command=self.add_skill).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="💾 保存", command=self.save_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📥 导入JSON", command=self.import_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📤 导出JSON", command=self.export_json).pack(side=tk.LEFT, padx=5)

        # 配置网格自适应
        for col in range(len(headers)):
            table_frame.grid_columnconfigure(col, weight=1)

    def _create_rows(self, parent):
        """动态创建所有技能行"""
        # 清空旧组件
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()
        
        self.entries.clear()
        for row, (sid, data) in enumerate(self.skill_data.items(), 1):
            self._create_single_row(parent, sid, data, row)

    def _create_single_row(self, parent, sid, data, row):
        """创建单个技能行"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky="ew", pady=1)
        
        # 技能ID
        ttk.Label(frame, text=str(sid)).grid(row=0, column=0, sticky="ew")
        
        entries = []
        # 数值字段
        for col, key in enumerate([
            'multiplier', 'base_attack', 'attack_pct', 'crit_rate', 
            'crit_damage', 'damage_bonus', 'em', 'flat_bonus', 'base_bonus'
        ], 1):
            val = data.get(key, 0)
            entry = ValidatedEntry(frame)
            entry.insert(0, str(val))
            entry.grid(row=0, column=col, sticky="ew", padx=2)
            entries.append(entry)
        
        # 反应类型（普通输入框）
        reaction_entry = ttk.Entry(frame)
        reaction_entry.insert(0, data.get('reaction_type', 'NONE'))
        reaction_entry.grid(row=0, column=10, sticky="ew", padx=2)
        entries.append(reaction_entry)
        
        # 删除按钮
        del_btn = ttk.Button(
            frame, text="×", 
            command=lambda s=sid: self.delete_skill(s),
            width=3
        )
        del_btn.grid(row=0, column=11, padx=5)
        
        self.entries[sid] = entries

    def add_skill(self):
        """添加新技能"""
        self.current_max_id += 1
        new_id = self.current_max_id
        self.skill_data[new_id] = {
            'multiplier': 0.0,
            'base_attack': 0.0,
            'attack_pct': 0.0,
            'crit_rate': 0.0,
            'crit_damage': 0.0,
            'damage_bonus': 0.0,
            'em': 0.0,
            'flat_bonus': 0.0,
            'base_bonus': 0.0,
            'reaction_type': 'NONE'
        }
        self._create_rows(self.winfo_children()[0].winfo_children()[0])

    def delete_skill(self, skill_id):
        """删除技能"""
        if skill_id in self.skill_data:
            del self.skill_data[skill_id]
            self._create_rows(self.winfo_children()[0].winfo_children()[0])

    def save_data(self):
        try:
            for sid, entries in self.entries.items():
                data = {
                    'multiplier': float(entries[0].get()),
                    'base_attack': float(entries[1].get()),
                    'attack_pct': float(entries[2].get()),
                    'crit_rate': float(entries[3].get()),
                    'crit_damage': float(entries[4].get()),
                    'damage_bonus': float(entries[5].get()),
                    'em': float(entries[6].get()),
                    'flat_bonus': float(entries[7].get()),
                    'base_bonus': float(entries[8].get()),
                    'reaction_type': entries[9].get().upper()
                }
                self.skill_data[sid] = data
            messagebox.showinfo("保存成功", "技能数据已更新")
        except ValueError as e:
            messagebox.showerror("输入错误", f"数值格式错误: {str(e)}")

    def import_json(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON文件", "*.json")],
                title="选择要导入的技能文件"
            )
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    new_data = json.load(f)
                    self.skill_data.clear()
                    for k, v in new_data.items():
                        v.setdefault('flat_bonus', 0.0)
                        self.skill_data[int(k)] = v
                    self.current_max_id = max(self.skill_data.keys())
                    self._create_rows(self.winfo_children()[0].winfo_children()[0])
        except Exception as e:
            messagebox.showerror("导入失败", f"错误信息: {str(e)}")

    def export_json(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json")],
                title="保存技能数据"
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.skill_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("导出成功", f"数据已保存至: {file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"错误信息: {str(e)}")

# ==================== 主程序界面 ====================
class GenshinOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("原神圣遗物优化器")
        self.root.geometry("1200x800")
        
        # 初始化技能数据
        self.skill_data = {
            1: {'multiplier': 7.344, 'base_attack': 1013.63, 'attack_pct': 0.76, 
                'crit_rate': 0.465, 'crit_damage': 1.941, 'damage_bonus': 1.24,
                'em': 0, 'flat_bonus': 685, 'base_bonus': 0, 'reaction_type': 'NONE'},
            2: {'multiplier': 2.703, 'base_attack': 1013.63, 'attack_pct': 1.36,
                'crit_rate': 0.365, 'crit_damage': 0.5, 'damage_bonus': 2.152,
                'em': 0, 'flat_bonus': 685, 'base_bonus': 0, 'reaction_type': 'NONE'}
        }
        
        self.setup_ui()
        self.running = False

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 控制按钮区
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="📝 编辑技能数据", 
                 command=self.open_skill_editor).pack(side=tk.LEFT, padx=5)
        self.optimize_btn = ttk.Button(
            control_frame, text="⚡ 开始优化", 
            command=self.start_optimization
        )
        self.optimize_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(
            control_frame, text="🛑 停止", 
            command=self.stop_optimization, 
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # 全局参数面板
        input_frame = ttk.LabelFrame(main_frame, text="全局参数设置")
        input_frame.pack(fill=tk.X, pady=5)
        
        input_grid = ttk.Frame(input_frame)
        input_grid.pack(padx=10, pady=5)
        
        # 第一行参数
        ttk.Label(input_grid, text="敌人等级:").grid(row=0, column=0, sticky=tk.W)
        self.enemy_lv = ValidatedEntry(input_grid)
        self.enemy_lv.insert(0, "100")
        self.enemy_lv.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_grid, text="角色等级:").grid(row=0, column=2, sticky=tk.W)
        self.char_lv = ValidatedEntry(input_grid)
        self.char_lv.insert(0, "90")
        self.char_lv.grid(row=0, column=3, padx=5)
        
        ttk.Label(input_grid, text="敌人抗性:").grid(row=0, column=4, sticky=tk.W)
        self.enemy_resist = ValidatedEntry(input_grid)
        self.enemy_resist.insert(0, "-0.75")
        self.enemy_resist.grid(row=0, column=5, padx=5)
        
        # 第二行参数
        ttk.Label(input_grid, text="武器精通转攻击:").grid(row=1, column=0, sticky=tk.W)
        self.weapon_em_to_atk = ValidatedEntry(input_grid)
        self.weapon_em_to_atk.insert(0, "0")
        self.weapon_em_to_atk.grid(row=1, column=1, padx=5)
        
        ttk.Label(input_grid, text="防御区减伤:").grid(row=1, column=2, sticky=tk.W)
        self.defense_red = ValidatedEntry(input_grid)
        self.defense_red.insert(0, "0")
        self.defense_red.grid(row=1, column=3, padx=5)

        # 结果展示面板
        result_frame = ttk.LabelFrame(main_frame, text="优化结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def open_skill_editor(self):
        SkillEditorWindow(self.root, self.skill_data)

    def start_optimization(self):
        if self.running:
            return

        try:
            base_stats = CharacterStats(
                skill_data=self.skill_data,
                weapon_em_to_atk=float(self.weapon_em_to_atk.get()),
                defense_red=float(self.defense_red.get()),
                enemy_lv=float(self.enemy_lv.get()),
                char_lv=float(self.char_lv.get()),
                enemy_resist=float(self.enemy_resist.get())
            )
        except ValueError as e:
            messagebox.showerror("输入错误", f"参数格式错误: {str(e)}")
            return

        self.running = True
        self.optimize_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "正在计算中，请稍候...\n")

        self.optimizer = ArtifactOptimizer(base_stats)
        self.thread = threading.Thread(target=self.run_optimization)
        self.thread.start()

    def run_optimization(self):
        try:
            result = self.optimizer.optimize()
            self.root.after(0, self.show_result, result)
        except Exception as e:
            self.root.after(0, messagebox.showerror, "计算错误", str(e))
        finally:
            self.running = False

    def show_result(self, result):
        self.optimize_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, format_result(result))

    def stop_optimization(self):
        if self.running:
            self.running = False
            messagebox.showinfo("已停止", "优化过程已中止")

if __name__ == "__main__":
    root = tk.Tk()
    app = GenshinOptimizerGUI(root)
    root.mainloop()