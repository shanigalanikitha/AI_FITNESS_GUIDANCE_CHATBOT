import streamlit as st

from utils.validations import validate_user_input
from main import generate_fitness_response

# ================= PAGE SETTINGS =================

st.set_page_config(
    page_title="AI Fitness Guidance Chatbot",
    page_icon="💪",
    layout="wide"
)

# ================= CUSTOM CSS =================

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

h1 {
    color: #ff4b4b;
    text-align: center;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 220px;
    font-size: 16px;
    border: none;
}

.stButton>button:hover {
    background-color: #ff1e1e;
    color: white;
}

section[data-testid="stSidebar"] {
    width: 260px !important;
}

.stTextInput input {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= CHAT HISTORY =================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================= SIDEBAR =================

st.sidebar.title("💪 Fitness Menu")
st.sidebar.subheader("🕘 Recent Questions")

if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history[-5:]):
        st.sidebar.caption(f"• {chat}")

# ================= TITLE =================

st.title("💪 AI Fitness Guidance Chatbot")
st.caption("AI-powered personalized fitness guidance using LangChain + Groq")

# ================= TABS =================

tab1, tab2, tab3 = st.tabs(
    [
        "💬 Fitness Chatbot",
        "⚖️ AI BMI Guidance",
        "🔥 AI Calorie Guidance"
    ]
)

# ================= COMMON FUNCTION =================

def display_ai_response(question, fitness_level):

    is_valid, message = validate_user_input(question)

    if not is_valid:
        st.warning(message)

    else:
        result = generate_fitness_response(
            question,
            fitness_level
        )

        st.session_state.chat_history.append(question)

        st.subheader(f"🏋️ {result.title}")

        if isinstance(result.response, list):
            st.success("\n\n".join(result.response))
        else:
            st.success(result.response)

        st.caption(f"Category: {result.category}")


# ================= TAB 1: FITNESS CHATBOT =================

with tab1:

    st.markdown("""
### 💡 Try Asking:

- Best workout plan for beginners
- How to lose weight safely
- Protein foods for muscle gain
- Best exercises for abs
- BMI understanding
- Daily calorie recommendations
- Best hydration tips
""")

    question = st.text_input(
        "",
        placeholder="Ask your fitness question here..."
    )

    fitness_level = st.selectbox(
        "Select Your Fitness Level",
        ["Beginner", "Intermediate", "Advanced"],
        key="chat_level"
    )

    if st.button("Get AI Guidance"):
        display_ai_response(question, fitness_level)


# ================= TAB 2: AI BMI GUIDANCE =================

with tab2:

    st.subheader("⚖️ AI BMI Guidance")

    weight = st.number_input(
        "Enter your weight in kg",
        min_value=1.0,
        key="bmi_weight"
    )

    height = st.number_input(
        "Enter your height in meters",
        min_value=0.1,
        key="bmi_height"
    )

    fitness_level = st.selectbox(
        "Select Your Fitness Level",
        ["Beginner", "Intermediate", "Advanced"],
        key="bmi_level"
    )

    if st.button("Generate AI BMI Guidance"):

        bmi_question = (
            f"My weight is {weight} kg and my height is {height} meters. "
            f"Calculate and explain my BMI. Also give safe fitness advice."
        )

        display_ai_response(bmi_question, fitness_level)


# ================= TAB 3: AI CALORIE GUIDANCE =================

with tab3:

    st.subheader("🔥 AI Calorie Guidance")

    age = st.number_input(
        "Enter your age",
        min_value=10,
        max_value=100,
        key="calorie_age"
    )

    gender = st.selectbox(
        "Select gender",
        ["Male", "Female"],
        key="calorie_gender"
    )

    weight = st.number_input(
        "Enter weight in kg",
        min_value=1.0,
        key="calorie_weight"
    )

    height = st.number_input(
        "Enter height in meters",
        min_value=0.1,
        key="calorie_height"
    )

    goal = st.selectbox(
        "Select your goal",
        ["Weight Loss", "Maintain Weight", "Muscle Gain"],
        key="calorie_goal"
    )

    fitness_level = st.selectbox(
        "Select Your Fitness Level",
        ["Beginner", "Intermediate", "Advanced"],
        key="calorie_level"
    )

    if st.button("Generate AI Calorie Guidance"):

        calorie_question = (
            f"I am {age} years old, {gender}, my weight is {weight} kg, "
            f"height is {height} meters, and my goal is {goal}. "
            f"Suggest daily calorie intake and fitness nutrition guidance."
        )

        display_ai_response(calorie_question, fitness_level)


# ================= FOOTER =================

st.markdown("---")

st.markdown(
    "💪 AI Fitness Guidance Chatbot | Powered by LangChain + Groq"
)