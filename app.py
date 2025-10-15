import streamlit as st
import json
import datetime
from typing import Dict, List, Any, Optional, Tuple, Union

# 导入深度学习系统类
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
        return self
    
    def break_down_modules(self, modules: List[str]):
        """拆解知识模块"""
        self.knowledge_modules = modules
        return self
    
    def create_minimal_tasks(self, tasks: List[Dict]):
        """创建最小学习单元任务"""
        self.minimal_tasks = tasks
        return self
    
    def start_study_session(self, task_index: int, duration_minutes: int = 25) -> Tuple[Union[str, None], str]:
        """第二阶段：开始学习会话（番茄工作法 + 康奈尔笔记）"""
        if task_index >= len(self.minimal_tasks) or task_index < 0:
            return None, "任务索引超出范围"
            
        task = self.minimal_tasks[task_index]
        # 创建康奈尔笔记
        note_id = f"note_{task_index}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
        
        return note_id, task['name']
    
    def save_note(self, note_id: str, main_notes: str, key_questions: str, summary: str):
        """保存康奈尔笔记"""
        self.notes[note_id] = {
            'task_id': int(note_id.split('_')[1]),
            'main_notes': main_notes,
            'key_questions': key_questions,
            'summary': summary,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        self.study_sessions.append({
            'task_index': int(note_id.split('_')[1]),
            'duration': 25,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    def review_and_summarize(self, note_id: str, summary: str):
        """完成单元总结（补充康奈尔笔记的总结栏）"""
        if note_id in self.notes:
            self.notes[note_id]['summary'] = summary
            return True
        return False
    
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
    
    def evening_review(self, recall_results: Dict[str, bool], focus_points: Dict[str, str]):
        """第三阶段：睡前复习（海马体记忆法）"""
        today_notes = self._get_today_notes()
        
        if not today_notes:
            return "今天没有创建学习笔记，无需复习"
            
        # 记录需要晨间强化的重点内容
        for note_id, focus_point in focus_points.items():
            if focus_point:  # 如果用户输入了重点内容
                self._schedule_morning_review(note_id, focus_point)
        
        return "睡前复习完成，重点内容已安排晨间巩固"
    
    def morning_review(self):
        """第三阶段：晨间快速激活（海马体记忆法）"""
        today_reviews = self._get_today_morning_reviews()
        
        if not today_reviews:
            return "今天没有安排晨间复习任务"
            
        # 完成后清空今日晨间复习记录
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if today_date in self.review_schedule:
            del self.review_schedule[today_date]
        
        return "晨间复习完成，记忆已强化"
    
    def practice_testing(self, task_index: int, score: int, weak_point: str = "", blind_spot: str = ""):
        """第四阶段：实战检验（做题总结法 + 费曼学习法）"""
        if task_index >= len(self.minimal_tasks) or task_index < 0:
            return "任务索引无效"
            
        task = self.minimal_tasks[task_index]
        
        # 80分以下需记录薄弱点
        if score < 80:
            self.weak_points.append({
                'task_index': task_index,
                'task_name': task['name'],
                'weak_point': weak_point,
                'blind_spot': blind_spot,
                'practice_score': score,
                'record_time': datetime.datetime.now().isoformat()
            })
            return f"检测到未完全掌握，薄弱点已记录！建议重新学习该知识点。"
        else:
            return "得分≥80，知识点基本掌握！可定期回顾笔记巩固。"
    
    def show_weak_points(self):
        """查看所有记录的薄弱点（错题本功能）"""
        return self.weak_points
    
    def get_notes(self):
        """获取所有笔记"""
        return self.notes
    
    def get_tasks(self):
        """获取所有任务"""
        return self.minimal_tasks

# 初始化系统
@st.cache_resource
def get_study_system():
    return DeepLearningSystem()

# Streamlit应用
def main():
    st.set_page_config(page_title="深度学习系统", layout="wide")
    st.title("🎯 目标导向的深度学习循环系统")
    
    # 初始化系统
    study_system = get_study_system()
    
    # 侧边栏导航
    st.sidebar.title("学习导航")
    page = st.sidebar.radio("选择功能", [
        "🎯 设定学习目标",
        "📚 创建学习任务",
        "⏰ 开始学习会话",
        "📋 完善笔记总结",
        "🌙 睡前复习",
        "🌅 晨间复习",
        "📝 实战检验",
        "❌ 查看薄弱点",
        "📖 查看所有笔记"
    ])
    
    # 页面内容
    if page == "🎯 设定学习目标":
        st.header("🎯 设定学习目标")
        goal = st.text_input("请输入您的学习目标", "3天掌握Python基础语法")
        modules = st.text_area("请输入知识模块（每行一个）", 
                              "变量与数据类型\n条件语句\n循环结构")
        
        if st.button("设定目标"):
            if goal and modules:
                study_system.set_learning_goal(goal)
                module_list = [m.strip() for m in modules.split('\n') if m.strip()]
                study_system.break_down_modules(module_list)
                st.success(f"已设定学习目标：{goal}")
                st.success(f"已拆解 {len(module_list)} 个知识模块")
                
                # 自动生成任务
                tasks = []
                for module in module_list:
                    tasks.append({
                        "name": f"学习{module}",
                        "description": f"掌握{module}的核心概念和应用方法"
                    })
                study_system.create_minimal_tasks(tasks)
                st.success("已自动生成学习任务")
            else:
                st.warning("请填写学习目标和知识模块")
    
    elif page == "📚 创建学习任务":
        st.header("📚 创建学习任务")
        st.info("在'设定学习目标'页面中会自动生成任务，您也可以在此处手动添加任务。")
        
        task_name = st.text_input("任务名称")
        task_description = st.text_area("任务描述")
        
        if st.button("添加任务"):
            if task_name and task_description:
                study_system.minimal_tasks.append({
                    "name": task_name,
                    "description": task_description
                })
                st.success(f"已添加任务：{task_name}")
            else:
                st.warning("请填写任务名称和描述")
        
        # 显示现有任务
        if study_system.minimal_tasks:
            st.subheader("现有任务列表")
            for i, task in enumerate(study_system.minimal_tasks):
                st.markdown(f"{i+1}. **{task['name']}** - {task['description']}")
    
    elif page == "⏰ 开始学习会话":
        st.header("⏰ 开始学习会话")
        
        if not study_system.minimal_tasks:
            st.warning("请先创建学习任务")
            return
        
        # 选择任务
        task_options = [f"{i+1}. {task['name']}" for i, task in enumerate(study_system.minimal_tasks)]
        selected_task = st.selectbox("选择要学习的任务", task_options)
        
        if selected_task:
            task_index = int(selected_task.split('.')[0]) - 1
            
            # 显示任务详情
            task = study_system.minimal_tasks[task_index]
            st.info(f"**任务名称：** {task['name']}")
            st.info(f"**任务描述：** {task['description']}")
            
            # 康奈尔笔记输入
            st.subheader("📝 康奈尔笔记")
            main_notes = st.text_area("主笔记区（记录核心内容）")
            key_questions = st.text_area("左侧线索栏（记录关键问题）")
            
            if st.button("完成学习会话"):
                if main_notes and key_questions:
                    note_id, task_name_or_error = study_system.start_study_session(task_index)
                    if note_id is not None:
                        study_system.save_note(note_id, main_notes, key_questions, "")
                        st.success(f"学习会话完成！笔记已保存，ID: {note_id}")
                    else:
                        st.error(task_name_or_error)
                else:
                    st.warning("请填写主笔记和关键问题")
    
    elif page == "📋 完善笔记总结":
        st.header("📋 完善笔记总结")
        
        # 选择笔记
        note_options = [(note_id, f"任务{note['task_id']+1}: {study_system.minimal_tasks[note['task_id']]['name']}") 
                       for note_id, note in study_system.notes.items()]
        
        if not note_options:
            st.warning("暂无笔记，请先完成学习会话")
            return
        
        selected_note = st.selectbox("选择要完善的笔记", [option[1] for option in note_options])
        
        if selected_note:
            note_id = [option[0] for option in note_options if option[1] == selected_note][0]
            note = study_system.notes[note_id]
            
            # 显示笔记内容
            st.info(f"**主笔记：** {note['main_notes']}")
            st.info(f"**关键问题：** {note['key_questions']}")
            
            # 输入总结
            summary = st.text_area("总结栏（完成本单元知识总结）", note.get('summary', ''))
            
            if st.button("保存总结"):
                # 确保summary是字符串类型
                summary_str = summary if summary is not None else ""
                if study_system.review_and_summarize(note_id, summary_str):
                    st.success("总结保存成功！")
                else:
                    st.error("保存失败，请重试")
    
    elif page == "🌙 睡前复习":
        st.header("🌙 睡前复习（海马体记忆法）")
        
        # 显示当前复习计划
        st.subheader("当前复习计划")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        if tomorrow in study_system.review_schedule and study_system.review_schedule[tomorrow]:
            st.info(f"已安排的明日 ({tomorrow}) 复习计划:")
            for note_id, focus_point in study_system.review_schedule[tomorrow].items():
                if note_id in study_system.notes:
                    note = study_system.notes[note_id]
                    task_name = study_system.minimal_tasks[note['task_id']]['name']
                    st.markdown(f"- **{task_name}**: {focus_point}")
        else:
            st.info(f"暂无明日 ({tomorrow}) 复习计划")
        
        today_notes = study_system._get_today_notes()
        if not today_notes:
            st.info("今天没有创建学习笔记，无需复习")
            return
        
        recall_results = {}
        focus_points = {}
        
        st.subheader("请根据关键问题主动回忆内容")
        for note_id, note in today_notes.items():
            task = study_system.minimal_tasks[note['task_id']]
            st.markdown(f"### 复习任务: {task['name']}")
            st.info(f"**关键问题:** {note['key_questions']}")
            
            col1, col2 = st.columns(2)
            with col1:
                recall_results[note_id] = st.radio("是否能回忆起主要内容？", 
                                                  ["能回忆起", "部分回忆", "无法回忆"], 
                                                  key=f"recall_{note_id}")
            with col2:
                focus_points[note_id] = st.text_area("需要明天晨间重点复习的内容", 
                                                   key=f"focus_{note_id}")
        
        if st.button("完成睡前复习"):
            result = study_system.evening_review(recall_results, focus_points)
            st.success(result)
    
    elif page == "🌅 晨间复习":
        st.header("🌅 晨间复习（海马体记忆法）")
        
        # 显示复习计划状态
        st.subheader("复习计划状态")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        if today in study_system.review_schedule and study_system.review_schedule[today]:
            st.info(f"今日 ({today}) 复习计划:")
            for note_id, focus_point in study_system.review_schedule[today].items():
                if note_id in study_system.notes:
                    note = study_system.notes[note_id]
                    task_name = study_system.minimal_tasks[note['task_id']]['name']
                    st.markdown(f"- **{task_name}**: {focus_point}")
        else:
            st.info(f"今日 ({today}) 没有安排复习任务")
            
        if tomorrow in study_system.review_schedule and study_system.review_schedule[tomorrow]:
            st.info(f"明日 ({tomorrow}) 复习计划:")
            for note_id, focus_point in study_system.review_schedule[tomorrow].items():
                if note_id in study_system.notes:
                    note = study_system.notes[note_id]
                    task_name = study_system.minimal_tasks[note['task_id']]['name']
                    st.markdown(f"- **{task_name}**: {focus_point}")
        else:
            st.info(f"明日 ({tomorrow}) 没有安排复习任务")
        
        # 实际的晨间复习功能
        today_reviews = study_system._get_today_morning_reviews()
        if not today_reviews:
            st.info("今天没有安排晨间复习任务")
            return
        
        st.subheader("今日晨间复习任务")
        for note_id, focus_point in today_reviews.items():
            if note_id in study_system.notes:
                note = study_system.notes[note_id]
                task_name = study_system.minimal_tasks[note['task_id']]['name']
                st.markdown(f"### 复习任务: {task_name}")
                st.info(f"**重点强化:** {focus_point}")
                st.success("✅ 已完成晨间复习")
        
        if st.button("完成所有晨间复习"):
            result = study_system.morning_review()
            st.success(result)
    
    elif page == "📝 实战检验":
        st.header("📝 实战检验（做题+费曼验证）")
        
        if not study_system.minimal_tasks:
            st.warning("请先创建学习任务")
            return
        
        # 选择任务
        task_options = [f"{i+1}. {task['name']}" for i, task in enumerate(study_system.minimal_tasks)]
        selected_task = st.selectbox("选择要检验的任务", task_options)
        
        if selected_task:
            task_index = int(selected_task.split('.')[0]) - 1
            
            # 输入得分
            score = st.number_input("请输入本次练习得分（0-100）", min_value=0, max_value=100, value=85)
            
            if score < 80:
                st.warning("检测到未完全掌握，需要详细记录薄弱环节")
                weak_point = st.text_input("具体薄弱环节（如“微积分极限计算”）")
                blind_spot = st.text_input("理解盲区（如“不会用洛必达法则”）")
                
                if st.button("记录薄弱点"):
                    result = study_system.practice_testing(task_index, score, weak_point, blind_spot)
                    st.success(result)
            else:
                if st.button("确认掌握"):
                    result = study_system.practice_testing(task_index, score)
                    st.success(result)
    
    elif page == "❌ 查看薄弱点":
        st.header("❌ 薄弱点记录（错题本）")
        
        weak_points = study_system.show_weak_points()
        if not weak_points:
            st.info("目前没有记录的薄弱点，继续保持！")
            return
        
        for i, point in enumerate(weak_points, 1):
            st.markdown(f"### {i}. 任务: {point['task_name']}")
            st.markdown(f"**得分:** {point['practice_score']}")
            st.markdown(f"**薄弱环节:** {point['weak_point']}")
            st.markdown(f"**理解盲区:** {point['blind_spot']}")
            st.markdown(f"**记录时间:** {point['record_time'].split('T')[0]}")
            st.markdown("---")
    
    elif page == "📖 查看所有笔记":
        st.header("📖 所有学习笔记")
        
        notes = study_system.get_notes()
        tasks = study_system.get_tasks()
        
        if not notes:
            st.info("暂无学习笔记")
            return
        
        for note_id, note in notes.items():
            task = tasks[note['task_id']]
            st.markdown(f"### 笔记ID: {note_id}")
            st.markdown(f"**任务:** {task['name']}")
            st.markdown(f"**主笔记:** {note['main_notes']}")
            st.markdown(f"**关键问题:** {note['key_questions']}")
            st.markdown(f"**总结:** {note.get('summary', '未完成')}")
            st.markdown(f"**创建时间:** {note['created_at']}")
            st.markdown("---")

if __name__ == "__main__":
    main()