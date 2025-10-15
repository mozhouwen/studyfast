import streamlit as st
import json
import datetime
from typing import Dict, List, Any, Optional, Tuple, Union

# 导入深度学习系统类
# 由于在同一目录下，直接导入
from app import DeepLearningSystem

# 初始化系统
@st.cache_resource
def get_study_system():
    return DeepLearningSystem()

# 现代化UI主函数
def modern_ui():
    # 页面配置
    st.set_page_config(
        page_title="深度学习系统 - 现代化界面",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 自定义样式
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .feature-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .progress-bar {
        height: 10px;
        background: #e9ecef;
        border-radius: 5px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #45a049);
        border-radius: 5px;
    }
    
    .study-session {
        border-left: 4px solid #667eea;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    
    .review-item {
        border-left: 4px solid #ff9800;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    
    .weak-point {
        border-left: 4px solid #f44336;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    
    .cornell-note {
        display: grid;
        grid-template-columns: 3fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .cornell-main {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 5px;
    }
    
    .cornell-cue {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 5px;
    }
    
    .cornell-summary {
        grid-column: span 2;
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 5px;
        background: #f8f9fa;
    }
    
    .stats-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stats-label {
        color: #6c757d;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 初始化系统
    study_system = get_study_system()
    
    # 主标题
    st.markdown('<div class="main-header"><h1>🎯 目标导向的深度学习循环系统</h1></div>', unsafe_allow_html=True)
    
    # 顶部统计卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-number">{len(study_system.minimal_tasks)}</div>
            <div class="stats-label">学习任务</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-number">{len(study_system.notes)}</div>
            <div class="stats-label">学习笔记</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-number">{len(study_system.weak_points)}</div>
            <div class="stats-label">薄弱点</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        today_notes = study_system._get_today_notes()
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-number">{len(today_notes)}</div>
            <div class="stats-label">今日笔记</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 侧边栏导航
    with st.sidebar:
        st.title("📚 学习导航")
        
        # 学习目标显示
        if study_system.current_goal:
            st.subheader("🎯 当前目标")
            st.info(study_system.current_goal)
            
            # 进度条
            total_tasks = len(study_system.minimal_tasks)
            completed_tasks = len([note for note in study_system.notes.values() 
                                 if note['task_id'] < len(study_system.minimal_tasks)])
            progress = completed_tasks / total_tasks if total_tasks > 0 else 0
            
            st.subheader("📈 学习进度")
            st.progress(progress)
            st.caption(f"已完成 {completed_tasks}/{total_tasks} 个任务")
        
        # 导航菜单
        page = st.radio("选择功能", [
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
        
        # 快速操作
        st.subheader("⚡ 快速操作")
        if st.button("刷新页面"):
            st.rerun()
    
    # 页面内容
    if page == "🎯 设定学习目标":
        st.header("🎯 设定学习目标")
        
        with st.form("goal_form"):
            goal = st.text_input("请输入您的学习目标", 
                               study_system.current_goal or "3天掌握Python基础语法",
                               help="设定一个明确、可衡量的学习目标")
            
            modules = st.text_area("请输入知识模块（每行一个）", 
                                 "\n".join(study_system.knowledge_modules) if study_system.knowledge_modules 
                                 else "变量与数据类型\n条件语句\n循环结构",
                                 help="将学习目标拆解为具体的知识模块")
            
            submitted = st.form_submit_button("🎯 设定目标")
            
            if submitted:
                if goal and modules:
                    study_system.set_learning_goal(goal)
                    module_list = [m.strip() for m in modules.split('\n') if m.strip()]
                    study_system.break_down_modules(module_list)
                    st.success(f"✅ 已设定学习目标：{goal}")
                    st.success(f"📚 已拆解 {len(module_list)} 个知识模块")
                    
                    # 自动生成任务
                    tasks = []
                    for module in module_list:
                        tasks.append({
                            "name": f"学习{module}",
                            "description": f"掌握{module}的核心概念和应用方法"
                        })
                    study_system.create_minimal_tasks(tasks)
                    st.success("🤖 已自动生成学习任务")
                    st.rerun()
                else:
                    st.warning("⚠️ 请填写学习目标和知识模块")
    
    elif page == "📚 创建学习任务":
        st.header("📚 创建学习任务")
        
        st.info("💡 在'设定学习目标'页面中会自动生成任务，您也可以在此处手动添加任务。")
        
        with st.form("task_form"):
            task_name = st.text_input("任务名称", help="给任务起一个简洁明了的名称")
            task_description = st.text_area("任务描述", help="详细描述任务的内容和要求")
            
            submitted = st.form_submit_button("➕ 添加任务")
            
            if submitted:
                if task_name and task_description:
                    study_system.minimal_tasks.append({
                        "name": task_name,
                        "description": task_description
                    })
                    st.success(f"✅ 已添加任务：{task_name}")
                    st.rerun()
                else:
                    st.warning("⚠️ 请填写任务名称和描述")
        
        # 显示现有任务
        if study_system.minimal_tasks:
            st.subheader("📋 现有任务列表")
            for i, task in enumerate(study_system.minimal_tasks):
                st.markdown(f'''
                <div class="feature-card">
                    <h4>📝 任务 {i+1}: {task['name']}</h4>
                    <p>{task['description']}</p>
                </div>
                ''', unsafe_allow_html=True)
    
    elif page == "⏰ 开始学习会话":
        st.header("⏰ 开始学习会话")
        
        if not study_system.minimal_tasks:
            st.warning("⚠️ 请先创建学习任务")
            return
        
        # 选择任务
        task_options = [f"{i+1}. {task['name']}" for i, task in enumerate(study_system.minimal_tasks)]
        
        selected_task = st.selectbox("选择要学习的任务", task_options,
                                   help="选择您要开始学习的任务")
        
        if selected_task:
            task_index = int(selected_task.split('.')[0]) - 1
            
            # 显示任务详情
            task = study_system.minimal_tasks[task_index]
            st.markdown(f'''
            <div class="study-session">
                <h3>📘 任务详情</h3>
                <p><strong>任务名称：</strong> {task['name']}</p>
                <p><strong>任务描述：</strong> {task['description']}</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # 康奈尔笔记输入
            st.subheader("📝 康奈尔笔记")
            
            with st.form("cornell_note_form"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    main_notes = st.text_area("主笔记区（记录核心内容）", 
                                            height=200,
                                            help="在这里记录学习的核心内容和要点")
                
                with col2:
                    key_questions = st.text_area("左侧线索栏（记录关键问题）", 
                                               height=200,
                                               help="记录有助于回忆的关键问题")
                
                submitted = st.form_submit_button("✅ 完成学习会话")
                
                if submitted:
                    if main_notes and key_questions:
                        note_id, task_name_or_error = study_system.start_study_session(task_index)
                        if note_id is not None:
                            study_system.save_note(note_id, main_notes, key_questions, "")
                            st.success(f"🎉 学习会话完成！笔记已保存，ID: {note_id}")
                            st.rerun()
                        else:
                            st.error(task_name_or_error)
                    else:
                        st.warning("⚠️ 请填写主笔记和关键问题")
    
    elif page == "📋 完善笔记总结":
        st.header("📋 完善笔记总结")
        
        # 选择笔记
        note_options = [(note_id, f"任务{note['task_id']+1}: {study_system.minimal_tasks[note['task_id']]['name']}") 
                       for note_id, note in study_system.notes.items()]
        
        if not note_options:
            st.warning("⚠️ 暂无笔记，请先完成学习会话")
            return
        
        selected_note = st.selectbox("选择要完善的笔记", [option[1] for option in note_options],
                                   help="选择您要完善总结的笔记")
        
        if selected_note:
            note_id = [option[0] for option in note_options if option[1] == selected_note][0]
            note = study_system.notes[note_id]
            
            # 显示笔记内容（康奈尔笔记格式）
            st.subheader("📖 笔记内容")
            st.markdown(f'''
            <div class="cornell-note">
                <div class="cornell-main">
                    <h4>📝 主笔记区</h4>
                    <p>{note['main_notes']}</p>
                </div>
                <div class="cornell-cue">
                    <h4>❓ 线索栏</h4>
                    <p>{note['key_questions']}</p>
                </div>
                <div class="cornell-summary">
                    <h4>📋 总结栏</h4>
                    <p>{note.get('summary', '尚未完成总结')}</p>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # 输入总结
            summary = st.text_area("总结栏（完成本单元知识总结）", 
                                 note.get('summary', ''),
                                 height=150,
                                 help="总结本单元的核心知识点和学习收获")
            
            if st.button("💾 保存总结"):
                # 确保summary是字符串类型
                summary_str = summary if summary is not None else ""
                if study_system.review_and_summarize(note_id, summary_str):
                    st.success("✅ 总结保存成功！")
                    st.rerun()
                else:
                    st.error("❌ 保存失败，请重试")
    
    elif page == "🌙 睡前复习":
        st.header("🌙 睡前复习（海马体记忆法）")
        
        # 显示当前复习计划
        st.subheader("📅 复习计划预览")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**今日 ({today}) 复习计划:**")
            if today in study_system.review_schedule and study_system.review_schedule[today]:
                for note_id, focus_point in study_system.review_schedule[today].items():
                    if note_id in study_system.notes:
                        note = study_system.notes[note_id]
                        task_name = study_system.minimal_tasks[note['task_id']]['name']
                        st.markdown(f"- 📘 {task_name}: {focus_point}")
            else:
                st.info("📭 今日无复习任务")
        
        with col2:
            st.markdown(f"**明日 ({tomorrow}) 复习计划:**")
            if tomorrow in study_system.review_schedule and study_system.review_schedule[tomorrow]:
                for note_id, focus_point in study_system.review_schedule[tomorrow].items():
                    if note_id in study_system.notes:
                        note = study_system.notes[note_id]
                        task_name = study_system.minimal_tasks[note['task_id']]['name']
                        st.markdown(f"- 📗 {task_name}: {focus_point}")
            else:
                st.info("📭 明日无复习任务")
        
        today_notes = study_system._get_today_notes()
        if not today_notes:
            st.info("📭 今天没有创建学习笔记，无需复习")
            return
        
        recall_results = {}
        focus_points = {}
        
        st.subheader("🧠 主动回忆练习")
        for note_id, note in today_notes.items():
            task = study_system.minimal_tasks[note['task_id']]
            st.markdown(f'''
            <div class="review-item">
                <h3>📘 复习任务: {task['name']}</h3>
                <p><strong>关键问题:</strong> {note['key_questions']}</p>
            </div>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                recall_results[note_id] = st.radio("是否能回忆起主要内容？", 
                                                  ["能回忆起", "部分回忆", "无法回忆"], 
                                                  key=f"recall_{note_id}",
                                                  help="诚实评估您的回忆情况")
            with col2:
                focus_points[note_id] = st.text_area("需要明天晨间重点复习的内容", 
                                                   key=f"focus_{note_id}",
                                                   help="记录需要重点复习的内容")
        
        if st.button("✅ 完成睡前复习"):
            result = study_system.evening_review(recall_results, focus_points)
            st.success(result)
            st.rerun()
    
    elif page == "🌅 晨间复习":
        st.header("🌅 晨间复习（海马体记忆法）")
        
        # 显示复习计划状态
        st.subheader("📅 复习计划状态")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**今日 ({today}) 复习计划:**")
            if today in study_system.review_schedule and study_system.review_schedule[today]:
                for note_id, focus_point in study_system.review_schedule[today].items():
                    if note_id in study_system.notes:
                        note = study_system.notes[note_id]
                        task_name = study_system.minimal_tasks[note['task_id']]['name']
                        st.markdown(f"- 📘 {task_name}: {focus_point}")
            else:
                st.info("📭 今日无复习任务")
        
        with col2:
            st.markdown(f"**明日 ({tomorrow}) 复习计划:**")
            if tomorrow in study_system.review_schedule and study_system.review_schedule[tomorrow]:
                for note_id, focus_point in study_system.review_schedule[tomorrow].items():
                    if note_id in study_system.notes:
                        note = study_system.notes[note_id]
                        task_name = study_system.minimal_tasks[note['task_id']]['name']
                        st.markdown(f"- 📗 {task_name}: {focus_point}")
            else:
                st.info("📭 明日无复习任务")
        
        # 实际的晨间复习功能
        today_reviews = study_system._get_today_morning_reviews()
        if not today_reviews:
            st.info("📭 今天没有安排晨间复习任务")
            return
        
        st.subheader("⚡ 今日晨间复习任务")
        for note_id, focus_point in today_reviews.items():
            if note_id in study_system.notes:
                note = study_system.notes[note_id]
                task_name = study_system.minimal_tasks[note['task_id']]['name']
                st.markdown(f'''
                <div class="review-item">
                    <h3>📘 复习任务: {task_name}</h3>
                    <p><strong>重点强化:</strong> {focus_point}</p>
                </div>
                ''', unsafe_allow_html=True)
                st.success("✅ 已完成晨间复习")
        
        if st.button("✅ 完成所有晨间复习"):
            result = study_system.morning_review()
            st.success(result)
            st.rerun()
    
    elif page == "📝 实战检验":
        st.header("📝 实战检验（做题+费曼验证）")
        
        if not study_system.minimal_tasks:
            st.warning("⚠️ 请先创建学习任务")
            return
        
        # 选择任务
        task_options = [f"{i+1}. {task['name']}" for i, task in enumerate(study_system.minimal_tasks)]
        selected_task = st.selectbox("选择要检验的任务", task_options,
                                   help="选择您要检验掌握程度的任务")
        
        if selected_task:
            task_index = int(selected_task.split('.')[0]) - 1
            
            # 输入得分
            score = st.number_input("请输入本次练习得分（0-100）", 
                                  min_value=0, max_value=100, value=85,
                                  help="根据实际练习情况输入得分")
            
            # 显示得分评价
            if score >= 90:
                st.success(f"🏆 优秀！得分 {score} 分")
            elif score >= 80:
                st.info(f"👍 良好！得分 {score} 分")
            elif score >= 70:
                st.warning(f"⚠️ 一般！得分 {score} 分，需要加强")
            else:
                st.error(f"❌ 需要努力！得分 {score} 分，建议重新学习")
            
            if score < 80:
                st.warning("⚠️ 检测到未完全掌握，需要详细记录薄弱环节")
                
                weak_point = st.text_input("具体薄弱环节（如“微积分极限计算”）",
                                         help="描述您在哪个具体知识点上遇到困难")
                blind_spot = st.text_input("理解盲区（如“不会用洛必达法则”）",
                                         help="记录您不理解或容易混淆的地方")
                
                if st.button("📌 记录薄弱点"):
                    result = study_system.practice_testing(task_index, score, weak_point, blind_spot)
                    st.success(result)
                    st.rerun()
            else:
                if st.button("✅ 确认掌握"):
                    result = study_system.practice_testing(task_index, score)
                    st.success(result)
    
    elif page == "❌ 查看薄弱点":
        st.header("❌ 薄弱点记录（错题本）")
        
        weak_points = study_system.show_weak_points()
        if not weak_points:
            st.info("🎉 目前没有记录的薄弱点，继续保持！")
            return
        
        st.subheader(f"📋 共 {len(weak_points)} 个薄弱点")
        for i, point in enumerate(weak_points, 1):
            st.markdown(f'''
            <div class="weak-point">
                <h3>❌ {i}. 任务: {point['task_name']}</h3>
                <p><strong>得分:</strong> {point['practice_score']}</p>
                <p><strong>薄弱环节:</strong> {point['weak_point']}</p>
                <p><strong>理解盲区:</strong> {point['blind_spot']}</p>
                <p><strong>记录时间:</strong> {point['record_time'].split('T')[0]}</p>
            </div>
            ''', unsafe_allow_html=True)
    
    elif page == "📖 查看所有笔记":
        st.header("📖 所有学习笔记")
        
        notes = study_system.get_notes()
        tasks = study_system.get_tasks()
        
        if not notes:
            st.info("📭 暂无学习笔记")
            return
        
        st.subheader(f"📋 共 {len(notes)} 条笔记")
        for note_id, note in notes.items():
            task = tasks[note['task_id']]
            st.markdown(f'''
            <div class="feature-card">
                <h3>📘 笔记ID: {note_id}</h3>
                <p><strong>任务:</strong> {task['name']}</p>
                <p><strong>主笔记:</strong> {note['main_notes']}</p>
                <p><strong>关键问题:</strong> {note['key_questions']}</p>
                <p><strong>总结:</strong> {note.get('summary', '未完成')}</p>
                <p><strong>创建时间:</strong> {note['created_at']}</p>
            </div>
            ''', unsafe_allow_html=True)

if __name__ == "__main__":
    modern_ui()