import streamlit as st
from datetime import date, timedelta
import math
import json

# Optional AI library
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Roadmap Planner",
    page_icon="🗺️",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.phase {
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin: 10px 0;
}

.small-text {
    color: #666;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">🗺️ AI Roadmap Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Create a personalized learning roadmap based on your time, goal and deadline.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Your Learning Plan")

course = st.sidebar.text_input(
    "What do you want to learn?",
    placeholder="Example: Python, MERN Stack, Data Science"
)

goal = st.sidebar.text_area(
    "What is your final goal?",
    placeholder="Example: Become a Full Stack Developer"
)

level = st.sidebar.selectbox(
    "Current Level",
    ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=date.today()
)

end_date = st.sidebar.date_input(
    "Last Date / Deadline",
    value=date.today() + timedelta(days=90)
)

hours_per_day = st.sidebar.number_input(
    "Available hours per day",
    min_value=0.5,
    max_value=24.0,
    value=3.0,
    step=0.5
)

days_per_week = st.sidebar.slider(
    "Available study days per week",
    min_value=1,
    max_value=7,
    value=6
)

preferred_time = st.sidebar.text_input(
    "Preferred study time",
    placeholder="Example: 8 AM - 12 PM"
)

learning_style = st.sidebar.selectbox(
    "How do you prefer to learn?",
    [
        "Theory + Practice",
        "Mostly Practical",
        "Projects First",
        "Video + Practice",
        "Reading + Practice"
    ]
)


# =========================================================
# VALIDATION
# =========================================================

if end_date <= start_date:
    st.error("⚠️ Last date must be after the start date.")
    st.stop()


# =========================================================
# CALCULATIONS
# =========================================================

total_days = (end_date - start_date).days + 1

weeks = math.ceil(total_days / 7)

study_days = math.floor(
    (total_days / 7) * days_per_week
)

total_hours = study_days * hours_per_day


# =========================================================
# DASHBOARD
# =========================================================

st.subheader("📊 Your Available Learning Time")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Days", total_days)

with col2:
    st.metric("Study Days", study_days)

with col3:
    st.metric("Hours / Day", hours_per_day)

with col4:
    st.metric("Total Hours", round(total_hours, 1))


# =========================================================
# ROADMAP GENERATOR
# =========================================================

def generate_basic_roadmap(course, goal, level, weeks, total_hours):

    if level == "Complete Beginner":
        phases = [
            ("Foundation", 0.20),
            ("Core Concepts", 0.25),
            ("Practice", 0.20),
            ("Projects", 0.25),
            ("Revision & Final Project", 0.10)
        ]

    elif level == "Beginner":
        phases = [
            ("Foundation & Review", 0.15),
            ("Core Skills", 0.30),
            ("Practice", 0.20),
            ("Projects", 0.25),
            ("Revision", 0.10)
        ]

    elif level == "Intermediate":
        phases = [
            ("Skill Review", 0.10),
            ("Advanced Concepts", 0.30),
            ("Practical Development", 0.25),
            ("Real Projects", 0.25),
            ("Final Revision", 0.10)
        ]

    else:
        phases = [
            ("Advanced Concepts", 0.25),
            ("Specialization", 0.25),
            ("Advanced Practice", 0.20),
            ("Portfolio Projects", 0.20),
            ("Final Revision", 0.10)
        ]

    roadmap = []

    for name, percentage in phases:

        phase_hours = round(total_hours * percentage, 1)

        phase_weeks = max(
            1,
            round(weeks * percentage)
        )

        roadmap.append({
            "name": name,
            "weeks": phase_weeks,
            "hours": phase_hours
        })

    return roadmap


roadmap = generate_basic_roadmap(
    course,
    goal,
    level,
    weeks,
    total_hours
)


# =========================================================
# AI ROADMAP
# =========================================================

def generate_ai_roadmap():

    if not GROQ_AVAILABLE:
        return None

    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")

        if not api_key:
            return None

        client = Groq(api_key=api_key)

        prompt = f"""
You are an expert learning-roadmap planner.

Create a realistic personalized learning roadmap.

COURSE:
{course}

FINAL GOAL:
{goal}

CURRENT LEVEL:
{level}

START DATE:
{start_date}

DEADLINE:
{end_date}

TOTAL DAYS:
{total_days}

AVAILABLE HOURS PER DAY:
{hours_per_day}

AVAILABLE STUDY DAYS PER WEEK:
{days_per_week}

TOTAL AVAILABLE HOURS:
{total_hours}

PREFERRED TIME:
{preferred_time}

LEARNING STYLE:
{learning_style}

Create:

1. Learning phases
2. Weekly roadmap
3. Daily study structure
4. Important topics in correct order
5. Practice tasks
6. Projects
7. Revision plan
8. Final project
9. What the student should achieve by the deadline

IMPORTANT:
- Do not overload the student.
- Respect the available hours.
- Keep the roadmap realistic.
- Arrange topics from easy to difficult.
- Include practical work.
- Include revision.
- Use simple language.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educational roadmap planner."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=5000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI generation failed: {str(e)}"


# =========================================================
# GENERATE BUTTON
# =========================================================

st.markdown("---")

generate = st.button(
    "🚀 Generate My Roadmap",
    type="primary",
    use_container_width=True
)


if generate:

    if not course.strip():
        st.warning("Please enter the course or skill you want to learn.")

    elif not goal.strip():
        st.warning("Please enter your final goal.")

    else:

        st.success("Your personalized roadmap is ready! 🎉")

        # -------------------------------------------------
        # BASIC PLAN
        # -------------------------------------------------

        st.subheader("🎯 Your Learning Summary")

        st.write(f"**Course:** {course}")
        st.write(f"**Goal:** {goal}")
        st.write(f"**Current Level:** {level}")
        st.write(f"**Deadline:** {end_date}")
        st.write(f"**Available Time:** {hours_per_day} hours/day")
        st.write(f"**Study Days:** {days_per_week} days/week")
        st.write(f"**Estimated Total Learning Time:** {round(total_hours, 1)} hours")

        # -------------------------------------------------
        # PHASE ROADMAP
        # -------------------------------------------------

        st.subheader("🛣️ Learning Roadmap")

        for i, phase in enumerate(roadmap, start=1):

            st.markdown(
                f"""
                <div class="phase">
                <h3>Phase {i}: {phase['name']}</h3>
                <p><b>Estimated Duration:</b> {phase['weeks']} week(s)</p>
                <p><b>Allocated Time:</b> {phase['hours']} hours</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # WEEKLY PLAN
        # -------------------------------------------------

        st.subheader("📅 Weekly Study Structure")

        weekly_hours = hours_per_day * days_per_week

        weekly_plan = {
            "Learning New Concepts": round(weekly_hours * 0.40, 1),
            "Practice": round(weekly_hours * 0.25, 1),
            "Projects": round(weekly_hours * 0.25, 1),
            "Revision": round(weekly_hours * 0.10, 1)
        }

        for task, hours in weekly_plan.items():
            st.write(f"**{task}:** {hours} hours/week")

        # -------------------------------------------------
        # DAILY PLAN
        # -------------------------------------------------

        st.subheader("🕒 Suggested Daily Structure")

        daily_learning = round(hours_per_day * 0.40, 1)
        daily_practice = round(hours_per_day * 0.25, 1)
        daily_project = round(hours_per_day * 0.25, 1)
        daily_revision = round(hours_per_day * 0.10, 1)

        daily_plan = [
            ("📚 Learn", daily_learning),
            ("💻 Practice", daily_practice),
            ("🛠️ Project", daily_project),
            ("🔄 Revision", daily_revision)
        ]

        for task, hours in daily_plan:
            st.write(f"**{task}:** {hours} hours")

        # -------------------------------------------------
        # AI PLAN
        # -------------------------------------------------

        st.markdown("---")
        st.subheader("🤖 AI-Powered Personalized Roadmap")

        with st.spinner("AI is creating your detailed roadmap..."):

            ai_plan = generate_ai_roadmap()

        if ai_plan:

            st.markdown(ai_plan)

        else:

            st.info(
                "AI API key is not configured, so the app is showing "
                "the built-in roadmap planner."
            )

            st.write(
                "For AI-powered personalized course topics, add your "
                "Groq API key to Streamlit Secrets."
            )

        # -------------------------------------------------
        # DAILY CONSISTENCY
        # -------------------------------------------------

        st.markdown("---")

        st.subheader("🔥 Consistency Rule")

        st.write(
            f"""
            You have approximately **{total_hours:.1f} total hours**
            available before your deadline.

            Try to study approximately **{hours_per_day} hours per day**
            on your selected study days.

            If you miss a day, do not try to study double the next day.
            Instead, redistribute the missed work across the remaining
            days.
            """
        )

        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        roadmap_text = f"""
AI ROADMAP PLANNER

Course: {course}
Goal: {goal}
Current Level: {level}

Start Date: {start_date}
Deadline: {end_date}

Hours Per Day: {hours_per_day}
Study Days Per Week: {days_per_week}

Estimated Total Learning Hours: {round(total_hours, 1)}

ROADMAP
"""

        for i, phase in enumerate(roadmap, start=1):
            roadmap_text += (
                f"\nPhase {i}: {phase['name']}"
                f"\nDuration: {phase['weeks']} week(s)"
                f"\nHours: {phase['hours']}\n"
            )

        st.download_button(
            label="📥 Download Basic Roadmap",
            data=roadmap_text,
            file_name="my_learning_roadmap.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🗺️ AI Roadmap Planner — Plan your learning according to your time."
)
