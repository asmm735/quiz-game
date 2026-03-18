import streamlit as st
import json
from typing import Dict, List, Any
from services import LLMService, GamificationEngine, ProgressStore, UserService

# ============================================================================
# Page Configuration
# ============================================================================
st.set_page_config(
    page_title="AI Quiz Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Initialize Session State
# ============================================================================
if 'llm_service' not in st.session_state:
    st.session_state.llm_service = LLMService()

if 'user_service' not in st.session_state:
    st.session_state.user_service = UserService()

if 'progress_store' not in st.session_state:
    st.session_state.progress_store = ProgressStore()

if 'gamification' not in st.session_state:
    progress_data = st.session_state.progress_store.load_progress()
    st.session_state.gamification = GamificationEngine()
    st.session_state.gamification.load_from_dict(progress_data['gamification'])

if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None

if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# ============================================================================
# Styling
# ============================================================================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .badge {
        display: inline-block;
        background: #FFD700;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-weight: bold;
    }
    .correct {
        color: #00AA00;
        font-weight: bold;
    }
    .incorrect {
        color: #AA0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Main App Function
# ============================================================================
def main():
    # =========== USER AUTHENTICATION ============
    user = st.session_state.user_service.get_current_user()
    
    if not user:
        # Show login/register page
        show_auth_page()
        return
    
    # =========== LOGGED IN - SHOW APP ===========
    st.markdown("# 🎓 AI Quiz Tutor - Learn & Level Up!")
    st.markdown("---")
    
    # Sidebar Navigation
    with st.sidebar:
        # User profile section
        st.markdown(f"### 👤 {user}")
        user_stats = st.session_state.user_service.get_user_stats()
        if user_stats:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Points", user_stats['points'])
                st.metric("Level", user_stats['level'])
            with col2:
                st.metric("Streak", user_stats.get('current_streak', 0))
                st.metric("Accuracy", f"{user_stats['accuracy']:.1f}%")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_service.logout()
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 📚 Navigation")
        page = st.radio(
            "Choose a section:",
            ["Home", "Ask the Tutor", "Generate Quiz", "Progress Dashboard", "Leaderboard"],
            key="page_selector"
        )
        
    
    # ========================================================================
    # PAGE ROUTING
    # ========================================================================
    if page == "Home":
        show_home_page()
    elif page == "Ask the Tutor":
        show_ask_tutor_page()
    elif page == "Generate Quiz":
        show_quiz_page()
    elif page == "Progress Dashboard":
        show_progress_page()
    elif page == "Leaderboard":
        show_leaderboard_page()


# ============================================================================
# HOME PAGE
# ============================================================================
def show_home_page():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💡 Ask the Tutor")
        st.markdown("Get clear explanations for any topic with real-world examples and follow-up questions.")
        st.markdown("👉 Use the **Navigation** menu on the left to get started!")
    
    with col2:
        st.markdown("### 📝 Generate Quiz")
        st.markdown("Test your knowledge with AI-generated quizzes at your preferred difficulty level.")
        st.markdown("👉 Select **Generate Quiz** from the menu →")
    
    with col3:
        st.markdown("### 📊 Dashboard")
        st.markdown("Track your progress, points, levels, and badges as you learn.")
        st.markdown("👉 View **Progress Dashboard** in the menu →")
    
    st.markdown("---")
    st.markdown("## 🎮 How It Works")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gamification System:**
        - 🎯 +10 points per correct answer
        - 🔥 +5 streak bonus every 3 correct answers
        - 📈 Level up as you earn points
        - 🏅 Earn badges for milestones
        
        **Level Progression:**
        - Level 1: 0-49 points (Quiz Starter)
        - Level 2: 50-99 points
        - Level 3: 100-199 points (Concept Master)
        - Level 4: 200-399 points
        - Level 5: 400+ points (Quiz Champion)
        """)
    
    with col2:
        st.markdown("""
        **Features:**
        ✅ Simple concept explanations
        ✅ Real-world analogies
        ✅ Structured quizzes
        ✅ Detailed feedback
        ✅ Performance tracking
        ✅ Adaptive difficulty
        
        **Start by:**
        1. Ask about a topic you're learning
        2. Take a quiz to test understanding
        3. View explanations for wrong answers
        4. Check your progress dashboard
        """)
    
    # Show recent activity
    st.markdown("---")
    st.markdown("## 📚 Your Learning Stats")
    progress_data = st.session_state.progress_store.load_progress()
    history = st.session_state.progress_store.load_quiz_history()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Points", progress_data['gamification']['points'])
    with col2:
        st.metric("Current Level", progress_data['gamification']['level'])
    with col3:
        st.metric("Quizzes Taken", len(history))
    with col4:
        accuracy = sum(1 for q in history if q.get('score', 0) >= 70) / len(history) * 100 if history else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")


# ============================================================================
# ASK THE TUTOR PAGE
# ============================================================================
def show_ask_tutor_page():
    st.markdown("## 💡 Ask the Tutor")
    st.markdown("Get clear, simple explanations for any topic with examples and follow-up questions.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic_input = st.text_input(
            "What would you like to learn about?",
            placeholder="e.g., Explain recursion simply, What is overfitting?, SQL joins with examples",
            key="topic_input"
        )
    
    with col2:
        st.write("")  # spacing
        ask_button = st.button("🎓 Get Explanation", key="ask_btn", use_container_width=True)
    
    if ask_button and topic_input:
        with st.spinner("🤔 Thinking..."):
            try:
                result = st.session_state.llm_service.explain_concept(topic_input)
                
                # Display explanation
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📌 Simple Explanation")
                    st.write(result.get('simple_explanation', 'N/A'))
                    
                    st.markdown("### 🔗 Real-World Analogy")
                    st.write(result.get('real_world_analogy', 'N/A'))
                
                with col2:
                    st.markdown("### ✨ Key Points")
                    for point in result.get('key_points', []):
                        st.write(f"• {point}")
                    
                    st.markdown("### 💭 Fun Fact")
                    st.info(result.get('fun_fact', 'N/A'))
                
                # Follow-up question
                st.markdown("---")
                st.markdown("### ❓ Check Your Understanding")
                st.write(result.get('follow_up_question', 'N/A'))
                
                if st.button("📖 Learn More About This Topic"):
                    st.success("💡 Tip: Take a quiz on this topic to deepen your understanding!")
                
            except Exception as e:
                st.error(f"Error getting explanation: {str(e)}")
                st.info("Make sure your OPENAI_API_KEY is set in the .env file")
    
    elif ask_button:
        st.warning("Please enter a topic or question!")


# ============================================================================
# QUIZ PAGE
# ============================================================================
def show_quiz_page():
    st.markdown("## 📝 Generate & Take Quiz")
    
    if st.session_state.current_quiz is None:
        # Quiz Configuration
        st.markdown("### Quiz Setup")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            topic = st.text_input(
                "Topic",
                placeholder="e.g., Python Recursion",
                key="quiz_topic"
            )
        
        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                ["easy", "medium", "hard"],
                key="quiz_difficulty"
            )
        
        with col3:
            num_questions = st.number_input(
                "Number of Questions",
                min_value=3,
                max_value=10,
                value=5,
                key="quiz_count"
            )
        
        if st.button("✨ Generate Quiz", use_container_width=True):
            if not topic:
                st.warning("Please enter a topic!")
            else:
                with st.spinner(f"🤖 Generating {num_questions} {difficulty} questions..."):
                    try:
                        quiz_data = st.session_state.llm_service.generate_quiz_questions(
                            topic, difficulty, int(num_questions)
                        )
                        
                        if quiz_data.get('questions'):
                            st.session_state.current_quiz = quiz_data
                            st.session_state.quiz_answers = {}
                            st.session_state.show_results = False
                            st.rerun()
                        else:
                            st.error("Failed to generate quiz questions. Please try again.")
                    
                    except Exception as e:
                        st.error(f"Error generating quiz: {str(e)}")
    
    else:
        # Display Quiz
        quiz = st.session_state.current_quiz
        st.markdown(f"### 📚 {quiz.get('topic', 'Quiz')}")
        st.markdown(f"**Difficulty:** {quiz.get('difficulty', 'medium').capitalize()}")
        st.markdown("---")
        
        questions = quiz.get('questions', [])
        
        for idx, q in enumerate(questions, 1):
            st.markdown(f"#### Question {idx}/{len(questions)}")
            st.write(q['question'])
            
            answer_key = f"q_{idx}"
            
            # Get previously selected answer if it exists
            prev_answer = st.session_state.quiz_answers.get(answer_key)
            initial_index = 0
            if prev_answer and prev_answer in q['options']:
                try:
                    initial_index = q['options'].index(prev_answer)
                except (ValueError, IndexError):
                    initial_index = 0
            
            selected_answer = st.radio(
                "Select your answer:",
                options=q['options'],
                key=answer_key,
                index=initial_index
            )
            
            # Store the answer text directly (not index)
            st.session_state.quiz_answers[answer_key] = selected_answer
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Submit Quiz", use_container_width=True):
                st.session_state.show_results = True
                st.rerun()
        
        with col2:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state.current_quiz = None
                st.session_state.quiz_answers = {}
                st.session_state.show_results = False
                st.rerun()
    
    # Show Results
    if st.session_state.show_results and st.session_state.current_quiz:
        show_quiz_results()


def show_quiz_results():
    """Display quiz results and feedback"""
    st.markdown("---")
    st.markdown("## 📊 Quiz Results")
    
    quiz = st.session_state.current_quiz
    questions = quiz.get('questions', [])
    answers = st.session_state.quiz_answers
    
    correct_count = 0
    total_points = 0
    wrong_answers = []
    
    for idx, q in enumerate(questions, 1):
        answer_key = f"q_{idx}"
        user_answer_text = answers.get(answer_key, "")  # Now storing answer text
        correct_idx = q['correct_answer_index']
        
        # Find the index of the user's answer
        try:
            user_answer_idx = q['options'].index(user_answer_text) if user_answer_text else -1
        except (ValueError, IndexError):
            user_answer_idx = -1
        
        is_correct = user_answer_idx == correct_idx
        if is_correct:
            correct_count += 1
            total_points += 10
        else:
            wrong_answers.append({
                'question_num': idx,
                'question': q['question'],
                'user_answer': user_answer_text if user_answer_text else "Not answered",
                'correct_answer': q['options'][correct_idx],
                'explanation': q.get('explanation', 'No explanation available')
            })
    
    # Calculate score
    score = (correct_count / len(questions)) * 100
    
    # Update gamification - global progress
    topic = quiz.get('topic', 'Unknown')
    quiz_attempt = {
        'topic': topic,
        'difficulty': quiz.get('difficulty', 'medium'),
        'questions': len(questions),
        'correct_answers': correct_count,
        'score': score
    }
    st.session_state.progress_store.save_quiz_attempt(quiz_attempt)
    
    # Update user progress - per-user points and level
    if st.session_state.user_service.get_current_user():
        st.session_state.user_service.add_quiz_attempt(
            topic=topic,
            difficulty=quiz.get('difficulty', 'medium'),
            score=score,
            correct=correct_count,
            total=len(questions)
        )
    
    # Show score
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Score", f"{correct_count}/{len(questions)}")
    with col2:
        st.metric("Percentage", f"{score:.1f}%")
    with col3:
        st.metric("Points Earned", f"+{int(score * 10)}")
    
    # Show updated user stats if logged in
    if st.session_state.user_service.get_current_user():
        user_stats = st.session_state.user_service.get_user_stats()
        with col4:
            st.metric("Total Points", user_stats['points'])
        
        st.success(f"✨ Level {user_stats['level']} | {len(user_stats['badges'])} Badge{'s' if len(user_stats['badges']) > 1 else ''}")
        if user_stats['badges']:
            st.markdown(f"**Badges:** {', '.join(user_stats['badges'])}")
    
    # Adaptive difficulty feedback
    if score < 40:
        st.warning("💡 Tip: Try an easier difficulty next time, or ask the Tutor for more explanation!")
    elif score > 80:
        st.success("🎉 Great job! Try a harder difficulty next time!")
    
    # Show questions with feedback
    st.markdown("---")
    st.markdown("### 📝 Question Review")
    
    for idx, q in enumerate(questions, 1):
        answer_key = f"q_{idx}"
        user_answer_text = answers.get(answer_key, "")  # Now storing answer text
        correct_idx = q['correct_answer_index']
        
        # Find the index of the user's answer
        try:
            user_answer_idx = q['options'].index(user_answer_text) if user_answer_text else -1
        except (ValueError, IndexError):
            user_answer_idx = -1
            
        is_correct = user_answer_idx == correct_idx
        
        expander = st.expander(
            f"{'✅' if is_correct else '❌'} Question {idx}: {'Correct' if is_correct else 'Incorrect'}",
            expanded=False
        )
        
        with expander:
            st.write(f"**Question:** {q['question']}")
            
            if is_correct:
                st.markdown(f"<div class='correct'>✅ Your answer was correct!</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='incorrect'>❌ Your answer was incorrect</div>", unsafe_allow_html=True)
                st.write(f"**Your answer:** {user_answer_text if user_answer_text else 'Not answered'}")
            
            st.write(f"**Correct answer:** {q['options'][correct_idx]}")
            st.write(f"**Explanation:** {q.get('explanation', 'No explanation available')}")
            
            # Explain wrong answer
            if not is_correct:
                if st.button(f"🤔 Explain why I got this wrong", key=f"explain_{idx}"):
                    with st.spinner("Generating detailed explanation..."):
                        explanation = st.session_state.llm_service.explain_wrong_answer(
                            q['question'],
                            user_answer_text if user_answer_text else "Not answered",
                            q['options'][correct_idx],
                            q.get('explanation', 'No explanation')
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**❌ Your misconception:**")
                            st.write(explanation.get('misconception', 'N/A'))
                            st.markdown("**💡 Mnemonic:**")
                            st.write(explanation.get('mnemonic_or_trick', 'N/A'))
                        
                        with col2:
                            st.markdown("**✅ Correct thinking:**")
                            st.write(explanation.get('correct_thinking', 'N/A'))
                            st.markdown("**📚 Next steps:**")
                            st.write(explanation.get('next_steps', 'N/A'))
    
    # Update progress
    progress_data = st.session_state.progress_store.load_progress()
    progress_data['gamification'] = st.session_state.gamification.to_dict()
    progress_data['quizzes']['attempted'] = len(st.session_state.progress_store.load_quiz_history())
    st.session_state.progress_store.save_progress(progress_data)
    
    st.markdown("---")
    if st.button("📚 Try Another Quiz", use_container_width=True):
        st.session_state.current_quiz = None
        st.session_state.quiz_answers = {}
        st.session_state.show_results = False
        st.rerun()


# ============================================================================
# PROGRESS DASHBOARD PAGE
# ============================================================================
def show_progress_page():
    st.markdown("## 📊 Progress Dashboard")
    
    # Get user stats from UserService (per-user gamification)
    user_stats = st.session_state.user_service.get_user_stats()
    
    if not user_stats:
        st.error("No user logged in")
        return
    
    # Header stats - using USER stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Total Points", user_stats['points'])
    with col2:
        st.metric("📈 Current Level", user_stats['level'])
    with col3:
        st.metric("🔥 Current Streak", user_stats.get('current_streak', 0))
    with col4:
        st.metric("🏆 Badges Earned", len(user_stats['badges']))
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Level Progress
        st.markdown("### 📊 Level Progress")
        
        level = user_stats['level']
        points = user_stats['points']
        
        # Calculate points needed for next level
        level_thresholds = {1: 1000, 2: 5000, 3: 10000}
        current_threshold = level_thresholds.get(level, 0)
        prev_threshold = level_thresholds.get(level - 1, 0)
        
        if level >= 4:
            st.success(f"🌟 Level {level} - Maximum Level Reached!")
            st.write(f"**Total Points:** {points}")
        else:
            points_in_level = points - prev_threshold
            points_needed = current_threshold - prev_threshold
            progress_pct = (points_in_level / points_needed) * 100
            st.progress(min(progress_pct / 100, 1.0))
            st.write(f"**Level {level}:** {points_in_level} / {points_needed} points to next level")
    
    with col2:
        # Best Stats
        st.markdown("### 🎖️ Best Stats")
        best_streak = user_stats.get('current_streak', 0)
        st.metric("Best Streak", f"{best_streak} 🔥")
        st.metric("Accuracy", f"{user_stats['accuracy']:.1f}%")
    
    st.markdown("---")
    
    # Quizzes & Accuracy
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Quiz Statistics")
        st.metric("Quizzes Attempted", user_stats['quizzes_attempted'])
        st.metric("Accuracy %", f"{user_stats['accuracy']:.1f}%")
    
    with col2:
        st.markdown("### 🏅 Badges Earned")
        if user_stats['badges']:
            for badge in user_stats['badges']:
                st.markdown(f"<span class='badge'>✨ {badge}</span>", unsafe_allow_html=True)
        else:
            st.info("Answer quizzes to earn badges! 🎯")
    
    st.markdown("---")
    
    # Quiz History
    st.markdown("### 📋 Quiz History")
    
    # Get quiz history from UserService
    current_username = st.session_state.user_service.get_current_user()
    if current_username and current_username in st.session_state.user_service.users:
        history = st.session_state.user_service.users[current_username].get("quiz_history", [])
    else:
        history = []
    
    if history:
        # Show last 10 quizzes
        history_data = []
        for idx, quiz in enumerate(history[-10:], 1):
            history_data.append({
                '#': idx,
                'Topic': quiz['topic'],
                'Difficulty': quiz['difficulty'].capitalize(),
                'Score': f"{quiz['correct']}/{quiz['total']}",
                'Percentage': f"{quiz['score']:.1f}%"
            })
        
        st.dataframe(history_data, use_container_width=True)
    else:
        st.info("No quizzes attempted yet. Start with the Quiz section!")


# ============================================================================
# AUTHENTICATION PAGE
# ============================================================================
def show_auth_page():
    """Login and Registration page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🎓 AI Quiz Tutor")
        st.markdown("---")
        
        auth_choice = st.radio("Choose an option:", ["Login", "Register"], horizontal=True)
        
        if auth_choice == "Login":
            st.markdown("## 🔓 Login")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", use_container_width=True):
                success, message = st.session_state.user_service.login(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        else:  # Register
            st.markdown("## 📝 Register")
            username = st.text_input("Choose a username", key="reg_user")
            password = st.text_input("Create a password", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirm password", type="password", key="reg_pass2")
            
            if st.button("Register", use_container_width=True):
                if password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = st.session_state.user_service.register(username, password)
                    if success:
                        st.success(message)
                        st.info("Now log in with your credentials")
                    else:
                        st.error(message)


# ============================================================================
# LEADERBOARD PAGE
# ============================================================================
def show_leaderboard_page():
    """Display global leaderboard"""
    st.markdown("## 🏆 Global Leaderboard")
    
    leaderboard = st.session_state.user_service.get_all_users_stats()
    
    if leaderboard:
        # Display as table
        leaders = []
        for rank, (username, stats) in enumerate(leaderboard.items(), 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}. "
            leaders.append({
                "Rank": medal,
                "Username": username,
                "Points": f"⭐ {stats['points']}",
                "Level": f"📛 {stats['level']}",
                "Accuracy": f"{stats['accuracy']:.1f}%",
                "Badges": f"🏅 {stats['badges']}"
            })
        
        st.dataframe(
            leaders,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No users yet. Register and start learning!")


# ============================================================================
# Run Main App
# ============================================================================
if __name__ == "__main__":
    main()
