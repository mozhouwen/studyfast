import json
import datetime
import time
from typing import Dict, List, Any, Optional

class DeepLearningSystem:
    """目标导向的深度学习循环系统"""
    
    def __init__(self):
        self.current_goal = None
        self.knowledge_modules = []
        self.minimal_tasks = []
        self.notes = {}  # 康奈尔笔记存储
        self.weak_points = []  # 薄弱点记录
        self.study_sessions = []  # 学习会话记录
        self.review_schedule = {}  # 复习计划
        
    def set_learning_goal(self, goal: str):
        """第一阶段：设定学习目标"""
        self.current_goal = goal
        print(f"🎯 已设定核心学习目标: {goal}")
        return self
    
    def break_down_modules(self, modules: List[str]):
        """拆解知识模块"""
        self.knowledge_modules = modules
        print(f"📚 知识模块拆解完成: {len(modules)} 个模块")
        for i, module in enumerate(modules, 1):
            print(f"  {i}. {module}")
        return self
    
    def create_minimal_tasks(self, tasks: List[Dict]):
        """创建最小学习单元任务"""
        self.minimal_tasks = tasks
        print(f"📝 已创建 {len(tasks)} 个最小学习单元")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. 任务: {task['name']} | 内容: {task['description']}")
        return self
    
    def start_study_session(self, task_index: int, duration_minutes: int = 25):
        """第二阶段：开始学习会话（番茄工作法 + 康奈尔笔记）"""
        if task_index >= len(self.minimal_tasks) or task_index < 0:
            print("❌ 任务索引超出范围（请输入0到任务总数-1的数字）")
            return self
            
        task = self.minimal_tasks[task_index]
        print(f"\n⏰ 开始学习会话: {task['name']}")
        print(f"📖 内容: {task['description']}")
        
        # 模拟25分钟学习（实际使用时可注释time.sleep，直接进入笔记输入）
        print(f"🕒 专注学习 {duration_minutes} 分钟...")
        time.sleep(2)  # 仅模拟等待，实际学习时可删除
        
        # 创建康奈尔笔记（交互输入）
        note_id = f"note_{task_index}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
        self.notes[note_id] = {
            'task_id': task_index,
            'main_notes': input("📝 请在主笔记区记录核心内容: "),
            'key_questions': input("❓ 请在左侧线索栏记录关键问题: "),
            'summary': "",
            'created_at': datetime.datetime.now().isoformat()
        }
        
        print("✅ 学习会话完成，笔记已保存")
        self.study_sessions.append({
            'task_index': task_index,
            'duration': duration_minutes,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return self
    
    def review_and_summarize(self, note_id: str):
        """完成单元总结（补充康奈尔笔记的总结栏）"""
        if note_id in self.notes:
            summary = input("📋 请在总结栏完成本单元知识总结: ")
            self.notes[note_id]['summary'] = summary
            print("✅ 单元总结完成，康奈尔笔记完整")
        else:
            print("❌ 笔记ID不存在，请检查输入的note_id")
        return self
    
    def _get_today_notes(self):
        """内部方法：获取今日创建的笔记"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return {
            note_id: note 
            for note_id, note in self.notes.items() 
            if note['created_at'].startswith(today)
        }
    
    def _schedule_morning_review(self, note_id: str, focus_point: str):
        """内部方法：添加晨间复习计划"""
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow_date = tomorrow.strftime("%Y-%m-%d")
        if tomorrow_date not in self.review_schedule:
            self.review_schedule[tomorrow_date] = {}
        self.review_schedule[tomorrow_date][note_id] = focus_point
    
    def _get_today_morning_reviews(self):
        """内部方法：获取今日的晨间复习任务"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return self.review_schedule.get(today, {})
    
    def evening_review(self):
        """第三阶段：睡前复习（海马体记忆法）"""
        print("\n🌙 开始睡前黄金复习（海马体记忆强化）")
        today_notes = self._get_today_notes()
        
        if not today_notes:
            print("📭 今天没有创建学习笔记，无需复习")
            return self
            
        print("🔍 请根据关键问题主动回忆内容（不要直接看笔记）:")
        for note_id, note in today_notes.items():
            task = self.minimal_tasks[note['task_id']]
            print(f"\n📌 复习任务: {task['name']}")
            print(f"💡 关键问题: {note['key_questions']}")
            input("🧠 回忆完成后按回车继续（若想记录重点，后续会提示）: ")
            
            # 记录需要晨间强化的重点内容
            if input("❓ 是否有需要明天晨间重点复习的内容? (y/n): ").lower() == 'y':
                focus_point = input("📝 输入重点内容（如公式、定义）: ")
                self._schedule_morning_review(note_id, focus_point)
                print(f"✅ 已添加到明天晨间复习计划：{focus_point}")
        
        print("\n✅ 睡前复习完成，重点内容已安排晨间巩固")
        return self
    
    def morning_review(self):
        """第三阶段：晨间快速激活（海马体记忆法）"""
        print("\n🌅 开始晨间快速激活（强化睡前记忆）")
        today_reviews = self._get_today_morning_reviews()
        
        if not today_reviews:
            print("📭 今天没有安排晨间复习任务")
            return self
            
        for note_id, focus_point in today_reviews.items():
            note = self.notes[note_id]
            task_name = self.minimal_tasks[note['task_id']]['name']
            print(f"\n📖 复习任务: {task_name}")
            print(f"🎯 重点强化: {focus_point}")
            input("💪 快速回顾并背诵重点内容，完成后按回车: ")
        
        # 完成后清空今日晨间复习记录
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if today_date in self.review_schedule:
            del self.review_schedule[today_date]
        
        print("\n✅ 晨间复习完成，记忆已强化")
        return self
    
    def practice_testing(self, task_index: int):
        """第四阶段：实战检验（做题总结法 + 费曼学习法）"""
        if task_index >= len(self.minimal_tasks) or task_index < 0:
            print("❌ 任务索引无效，请输入0到任务总数-1的数字")
            return self
            
        task = self.minimal_tasks[task_index]
        print(f"\n📝 开始实战检验：{task['name']}（做题+费曼验证）")
        
        # 模拟做题得分（实际可替换为自动判分逻辑）
        while True:
            try:
                score = int(input("🔢 请输入本次练习得分（0-100）: "))
                if 0 <= score <= 100:
                    break
                print("❌ 得分需在0-100之间，请重新输入")
            except ValueError:
                print("❌ 请输入数字（如85、60）")
        
        # 80分以上视为基本掌握，以下需记录薄弱点
        if score < 80:
            print("\n⚠️  检测到未完全掌握，需记录薄弱点并使用费曼法验证")
            weak_point = input("1. 请描述具体薄弱环节（如“微积分极限计算”）: ")
            
            print("\n🎓 费曼学习法验证：假设向零基础者讲解这个知识点")
            explanation = input("2. 请用简单语言描述讲解内容（卡壳处直接说明）: ")
            
            if input("3. 讲解时是否遇到卡壳/理解盲区? (y/n): ").lower() == 'y':
                blind_spot = input("   请记录卡壳的具体内容（如“不会用洛必达法则”）: ")
                # 保存薄弱点到错题本
                self.weak_points.append({
                    'task_index': task_index,
                    'task_name': task['name'],
                    'weak_point': weak_point,
                    'blind_spot': blind_spot,
                    'practice_score': score,
                    'record_time': datetime.datetime.now().isoformat()
                })
                print("\n✅ 薄弱点已记录！建议重新执行“学习会话+复习”流程攻克")
        else:
            print("\n✅ 得分≥80，知识点基本掌握！可定期回顾笔记巩固")
        
        return self
    
    def show_weak_points(self):
        """查看所有记录的薄弱点（错题本功能）"""
        if not self.weak_points:
            print("\n📚 目前没有记录的薄弱点，继续保持！")
            return self
            
        print("\n❌ 已记录的薄弱点（错题本）:")
        for i, point in enumerate(self.weak_points, 1):
            print(f"\n{i}. 任务: {point['task_name']}")
            print(f"   得分: {point['practice_score']}")
            print(f"   薄弱环节: {point['weak_point']}")
            print(f"   理解盲区: {point['blind_spot']}")
            print(f"   记录时间: {point['record_time'].split('T')[0]}")
        return self


# ------------------- 以下是运行示例（可直接执行） -------------------
if __name__ == "__main__":
    print("="*50)
    print("🎯 目标导向的深度学习循环系统 启动")
    print("="*50)
    
    # 1. 初始化系统
    study_system = DeepLearningSystem()
    
    # 2. 第一阶段：设定目标+拆解模块+创建任务（示例：学习Python基础）
    study_system.set_learning_goal("3天掌握Python基础语法")
    study_system.break_down_modules(["变量与数据类型", "条件语句", "循环结构"])
    study_system.create_minimal_tasks([
        {
            "name": "Python变量与数据类型",
            "description": "掌握int/str/list类型定义、转换方法，以及变量命名规则"
        },
        {
            "name": "Python条件语句",
            "description": "理解if/elif/else语法，掌握逻辑运算符and/or/not的使用"
        },
        {
            "name": "Python循环结构",
            "description": "学会for循环（遍历列表/字符串）和while循环，以及break/continue"
        }
    ])
    
    # 3. 第二阶段：开始学习会话（以“变量与数据类型”为例，任务索引0）
    print("\n" + "-"*30)
    print("⏰ 启动第一个学习会话（番茄工作法25分钟）")
    print("-"*30)
    study_system.start_study_session(task_index=0, duration_minutes=25)
    
    # 4. 补充康奈尔笔记的总结栏
    print("\n" + "-"*30)
    print("📋 完善康奈尔笔记（补充总结栏）")
    print("-"*30)
    # 获取最新创建的笔记ID（取notes字典最后一个key）
    latest_note_id = list(study_system.notes.keys())[-1]
    study_system.review_and_summarize(note_id=latest_note_id)
    
    # 5. 第三阶段：睡前复习（模拟晚间操作）
    print("\n" + "-"*30)
    print("🌙 模拟睡前复习（海马体记忆强化）")
    print("-"*30)
    study_system.evening_review()
    
    # 6. 第三阶段：晨间复习（模拟次日操作，需手动切换日期测试，此处仅演示流程）
    print("\n" + "-"*30)
    print("🌅 模拟次日晨间复习（强化记忆）")
    print("-"*30)
    study_system.morning_review()
    
    # 7. 第四阶段：实战检验（测试“变量与数据类型”掌握情况）
    print("\n" + "-"*30)
    print("📝 实战检验（做题+费曼验证）")
    print("-"*30)
    study_system.practice_testing(task_index=0)
    
    # 8. 查看薄弱点记录
    print("\n" + "-"*30)
    print("❌ 查看薄弱点记录（错题本）")
    print("-"*30)
    study_system.show_weak_points()
    
    print("\n" + "="*50)
    print("✅ 本次学习流程演示完成！")
    print("="*50)