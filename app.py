import streamlit as st
import json
import textwrap

from utils.validations import validate_user_input
from main import generate_fitness_response


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Fitness Guidance Chatbot",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       REMOVE EXTRA STREAMLIT TOP SPACE
    ----------------------------------------------------- */

    header[data-testid="stHeader"] {
        background: transparent;
        height: 2rem;
    }

    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }


    /* -----------------------------------------------------
       MAIN DASHBOARD BACKGROUND
    ----------------------------------------------------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #fffafa 0%,
            #f7fbff 35%,
            #f8fff9 68%,
            #fffaf4 100%
        );
    }


    /* -----------------------------------------------------
       SIDEBAR
    ----------------------------------------------------- */

    section[data-testid="stSidebar"] {

        background: linear-gradient(
            180deg,
            #eeeaff 0%,
            #e8f1ff 45%,
            #e8f8f4 100%
        );

        border-right: 1px solid #d8dcef;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }


    /* -----------------------------------------------------
       MAIN TITLE
    ----------------------------------------------------- */

    h1 {
        text-align: center;
        font-weight: 800;
        color: #27283c;
        margin-top: 0rem;
        margin-bottom: 0.3rem;
    }


    /* -----------------------------------------------------
       METRICS
    ----------------------------------------------------- */

    div[data-testid="stMetric"] {

        background: rgba(255, 255, 255, 0.55);

        border: 1px solid rgba(220, 225, 235, 0.8);

        border-radius: 14px;

        padding: 15px;

        min-height: 105px;

        box-shadow:
            0px 3px 12px
            rgba(0, 0, 0, 0.035);
    }


    /* -----------------------------------------------------
       BUTTONS
    ----------------------------------------------------- */

    .stButton > button {

        border-radius: 10px;

        min-height: 44px;

        font-weight: 600;

        padding-left: 22px;
        padding-right: 22px;

        transition: 0.2s ease;
    }

    .stButton > button:hover {

        transform: translateY(-1px);
    }


    /* -----------------------------------------------------
       INPUTS
    ----------------------------------------------------- */

    .stTextInput input {

        border-radius: 10px;
    }

    .stNumberInput input {

        border-radius: 10px;
    }

    div[data-baseweb="select"] > div {

        border-radius: 10px;
    }


    /* -----------------------------------------------------
       TABS
    ----------------------------------------------------- */

    button[data-baseweb="tab"] {

        font-size: 15px;

        font-weight: 600;

        padding-left: 18px;
        padding-right: 18px;
    }


    /* -----------------------------------------------------
       CODE / JSON
    ----------------------------------------------------- */

    div[data-testid="stCodeBlock"] {

        border-radius: 12px;

        overflow: hidden;
    }


    /* -----------------------------------------------------
       DIVIDERS
    ----------------------------------------------------- */

    hr {

        margin-top: 1rem;
        margin-bottom: 1.2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


if "total_responses" not in st.session_state:

    st.session_state.total_responses = 0


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💪 Fitness Menu")

st.sidebar.caption(
    "Your AI-powered personalized fitness assistant"
)

st.sidebar.divider()


# ---------------- RECENT QUESTIONS ----------------

st.sidebar.subheader("🕘 Recent Questions")


if st.session_state.chat_history:

    for question in reversed(
        st.session_state.chat_history[-5:]
    ):

        st.sidebar.write(
            f"• {question}"
        )

else:

    st.sidebar.info(
        "No questions asked yet."
    )


st.sidebar.divider()


# ---------------- CLEAR HISTORY ----------------

if st.sidebar.button(
    "🗑️ Clear History",
    use_container_width=True
):

    st.session_state.chat_history = []

    st.session_state.total_responses = 0

    st.rerun()


# ---------------- TECHNOLOGY STACK ----------------

st.sidebar.subheader("⚙️ Technology Stack")

st.sidebar.write("🐍 Python")

st.sidebar.write("🔗 LangChain")

st.sidebar.write("🤖 Groq LLM")

st.sidebar.write("📊 Langfuse")

st.sidebar.write("📦 Pydantic")

st.sidebar.write("☁️ AWS EC2")


st.sidebar.divider()

st.sidebar.caption(
    "AI Fitness Guidance Chatbot"
)


# =========================================================
# MAIN TITLE
# =========================================================

st.title(
    "💪 AI Fitness Guidance Chatbot"
)

st.markdown(
    """
    <p style="
        text-align:center;
        font-size:17px;
        color:#606070;
        margin-top:0px;
    ">
        Personalized Workout • BMI • Calorie •
        Nutrition • Hydration Guidance
    </p>
    """,
    unsafe_allow_html=True
)


st.divider()


# =========================================================
# DASHBOARD OVERVIEW
# =========================================================

metric1, metric2, metric3, metric4 = st.columns(4)


with metric1:

    st.metric(
        "🤖 AI Assistant",
        "Active"
    )


with metric2:

    st.metric(
        "🏋️ Fitness Levels",
        "3"
    )


with metric3:

    st.metric(
        "📦 AI Output",
        "JSON"
    )


with metric4:

    st.metric(
        "💬 Queries",
        st.session_state.total_responses
    )


st.write("")


# =========================================================
# FEATURE OVERVIEW
# =========================================================

feature1, feature2, feature3 = st.columns(3)


with feature1:

    st.info(
        """
        **💬 Fitness Guidance**

        Personalized workout, nutrition,
        hydration and recovery guidance.
        """
    )


with feature2:

    st.success(
        """
        **⚖️ BMI Guidance**

        Calculate BMI and receive
        fitness-level based AI suggestions.
        """
    )


with feature3:

    st.warning(
        """
        **🔥 Calorie Guidance**

        Estimate BMR and receive calorie
        guidance based on fitness goals.
        """
    )


st.write("")


# =========================================================
# RESPONSE TEXT FORMATTER
# =========================================================

def format_response_text(response):

    if not response:

        return "No response generated."


    paragraphs = response.split("\n")

    formatted_parts = []


    for paragraph in paragraphs:

        paragraph = paragraph.strip()


        if paragraph:

            wrapped_text = textwrap.fill(
                paragraph,
                width=90
            )

            formatted_parts.append(
                wrapped_text
            )


    return "\n\n".join(
        formatted_parts
    )


# =========================================================
# COMMON AI RESPONSE FUNCTION
# =========================================================

def display_ai_response(
    question,
    fitness_level
):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    is_valid, message = validate_user_input(
        question
    )


    if not is_valid:

        st.warning(message)

        return


    try:

        # -------------------------------------------------
        # AI GENERATION
        # -------------------------------------------------

        with st.spinner(
            "🤖 Generating personalized fitness guidance..."
        ):

            result = generate_fitness_response(
                question,
                fitness_level
            )


        # -------------------------------------------------
        # CHAT HISTORY
        # -------------------------------------------------

        if (
            not st.session_state.chat_history
            or
            st.session_state.chat_history[-1]
            != question
        ):

            st.session_state.chat_history.append(
                question
            )


        st.session_state.total_responses += 1


        # -------------------------------------------------
        # PYDANTIC → DICTIONARY
        # -------------------------------------------------

        output = result.model_dump()


        st.success(
            "✅ AI guidance generated successfully!"
        )


        # =================================================
        # STRUCTURED RESULT
        # =================================================

        st.subheader(
            "📋 Your Personalized Fitness Guidance"
        )


        info1, info2, info3 = st.columns(3)


        with info1:

            st.write(
                "**📌 Title**"
            )

            st.info(
                output.get(
                    "title",
                    "Fitness Guidance"
                )
            )


        with info2:

            st.write(
                "**🏷️ Category**"
            )

            st.info(
                output.get(
                    "category",
                    "General Fitness"
                )
            )


        with info3:

            st.write(
                "**🏋️ Fitness Level**"
            )

            st.info(
                output.get(
                    "fitness_level",
                    fitness_level
                )
            )


        # =================================================
        # READABLE RECOMMENDATION
        # =================================================

        st.markdown(
            "### 🤖 AI Recommendation"
        )


        readable_response = format_response_text(

            output.get(
                "response",
                ""
            )

        )


        st.text(
            readable_response
        )


        # =================================================
        # JSON OUTPUT
        # =================================================

        st.markdown(
            "### 📦 Structured JSON Output"
        )


        st.code(

            json.dumps(
                output,
                indent=4,
                ensure_ascii=False
            ),

            language="json"

        )


    except Exception as error:

        st.error(
            "❌ Unable to generate AI fitness guidance."
        )


        with st.expander(
            "🔧 Technical Error Details"
        ):

            st.write(error)


# =========================================================
# APPLICATION TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(

    [

        "💬 Fitness Chatbot",

        "⚖️ BMI Guidance",

        "🔥 Calorie Guidance"

    ]

)


# =========================================================
# TAB 1 — FITNESS CHATBOT
# =========================================================

with tab1:

    st.header(
        "💬 Ask Your Fitness Question"
    )


    st.caption(
        "Ask about workouts, nutrition, hydration, "
        "weight management, muscle gain, recovery "
        "or general fitness."
    )


    # =====================================================
    # DIRECT QUESTION SUGGESTIONS
    # =====================================================

    st.subheader(
        "💡 Try These Questions"
    )


    suggestion1, suggestion2 = st.columns(2)


    with suggestion1:

        st.write(
            "🏋️ Best workout plan for beginners"
        )

        st.write(
            "⚖️ How to lose weight safely"
        )

        st.write(
            "🥚 Protein foods for muscle gain"
        )

        st.write(
            "💪 Best exercises for abs"
        )


    with suggestion2:

        st.write(
            "🔥 Daily calorie recommendations"
        )

        st.write(
            "💧 Best hydration tips"
        )

        st.write(
            "🏃 How can I improve my stamina?"
        )

        st.write(
            "🧘 Best recovery tips after workout"
        )


    st.write("")


    # =====================================================
    # USER QUESTION
    # =====================================================

    question = st.text_input(

        "Enter Your Fitness Question",

        placeholder=(
            "Example: Suggest a beginner workout plan"
        )

    )


    fitness_level = st.selectbox(

        "Select Your Fitness Level",

        [

            "Beginner",

            "Intermediate",

            "Advanced"

        ],

        key="chat_level"

    )


    if st.button(

        "✨ Generate Fitness Guidance",

        key="fitness_button"

    ):

        display_ai_response(
            question,
            fitness_level
        )


# =========================================================
# TAB 2 — BMI GUIDANCE
# =========================================================

with tab2:

    st.header(
        "⚖️ AI BMI Guidance"
    )


    st.caption(
        "Calculate your BMI and receive "
        "personalized AI fitness guidance."
    )


    bmi_col1, bmi_col2 = st.columns(2)


    with bmi_col1:

        weight = st.number_input(

            "Weight (kg)",

            min_value=1.0,

            value=60.0,

            step=0.5,

            key="bmi_weight"

        )


    with bmi_col2:

        height = st.number_input(

            "Height (meters)",

            min_value=0.1,

            value=1.65,

            step=0.01,

            key="bmi_height"

        )


    fitness_level = st.selectbox(

        "Select Your Fitness Level",

        [

            "Beginner",

            "Intermediate",

            "Advanced"

        ],

        key="bmi_level"

    )


    # =====================================================
    # BMI CALCULATION
    # =====================================================

    bmi = weight / (
        height ** 2
    )


    bmi_metric, category_metric = st.columns(2)


    with bmi_metric:

        st.metric(

            "⚖️ Your BMI",

            f"{bmi:.2f}"

        )


    # -----------------------------------------------------
    # BMI CATEGORY
    # -----------------------------------------------------

    if bmi < 18.5:

        bmi_category = "Underweight"


    elif bmi < 25:

        bmi_category = "Normal"


    elif bmi < 30:

        bmi_category = "Overweight"


    else:

        bmi_category = "Obesity Range"


    with category_metric:

        st.metric(

            "📊 BMI Category",

            bmi_category

        )


    if st.button(

        "⚖️ Generate AI BMI Guidance",

        key="bmi_button"

    ):

        bmi_question = (

            f"My weight is {weight} kg and "
            f"my height is {height} meters. "

            f"My calculated BMI is {bmi:.2f} "
            f"and my BMI category is {bmi_category}. "

            f"Explain my BMI and provide safe "
            f"fitness and nutrition guidance."

        )


        display_ai_response(
            bmi_question,
            fitness_level
        )


# =========================================================
# TAB 3 — CALORIE GUIDANCE
# =========================================================

with tab3:

    st.header(
        "🔥 AI Calorie Guidance"
    )


    st.caption(
        "Estimate your BMR and receive calorie "
        "and nutrition guidance based on your goal."
    )


    calorie_col1, calorie_col2 = st.columns(2)


    # =====================================================
    # LEFT COLUMN
    # =====================================================

    with calorie_col1:

        age = st.number_input(

            "Age",

            min_value=10,

            max_value=100,

            value=25,

            key="calorie_age"

        )


        gender = st.selectbox(

            "Gender",

            [

                "Male",

                "Female"

            ],

            key="calorie_gender"

        )


        weight = st.number_input(

            "Weight (kg)",

            min_value=1.0,

            value=65.0,

            step=0.5,

            key="calorie_weight"

        )


    # =====================================================
    # RIGHT COLUMN
    # =====================================================

    with calorie_col2:

        height = st.number_input(

            "Height (meters)",

            min_value=0.1,

            value=1.70,

            step=0.01,

            key="calorie_height"

        )


        goal = st.selectbox(

            "Fitness Goal",

            [

                "Weight Loss",

                "Maintain Weight",

                "Muscle Gain"

            ],

            key="calorie_goal"

        )


        fitness_level = st.selectbox(

            "Fitness Level",

            [

                "Beginner",

                "Intermediate",

                "Advanced"

            ],

            key="calorie_level"

        )


    # =====================================================
    # BMR CALCULATION
    # =====================================================

    height_cm = height * 100


    if gender == "Male":

        bmr = (

            10 * weight

            + 6.25 * height_cm

            - 5 * age

            + 5

        )


    else:

        bmr = (

            10 * weight

            + 6.25 * height_cm

            - 5 * age

            - 161

        )


    result_col1, result_col2 = st.columns(2)


    with result_col1:

        st.metric(

            "🔥 Estimated BMR",

            f"{bmr:.0f} kcal/day"

        )


    with result_col2:

        st.metric(

            "🎯 Fitness Goal",

            goal

        )


    if st.button(

        "🔥 Generate AI Calorie Guidance",

        key="calorie_button"

    ):

        calorie_question = (

            f"I am {age} years old and {gender}. "

            f"My weight is {weight} kg and "
            f"my height is {height} meters. "

            f"My estimated BMR is "
            f"{bmr:.0f} calories per day. "

            f"My fitness goal is {goal}. "

            f"Suggest appropriate daily calorie intake "
            f"and safe nutrition and fitness guidance."

        )


        display_ai_response(
            calorie_question,
            fitness_level
        )


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.divider()


with st.expander(
    "ℹ️ About This Project"
):

    st.write(
        """
        **AI Fitness Guidance Chatbot**

        This Generative AI application provides
        personalized fitness, BMI, calorie,
        nutrition and hydration guidance.

        **Frontend:** Streamlit

        **AI Workflow:** LangChain

        **Large Language Model:** Groq LLM

        **Structured Output:** Pydantic Output Parser

        **Prompt Management & Tracing:** Langfuse

        **Cloud Deployment:** AWS EC2
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "💪 AI Fitness Guidance Chatbot | "
    "Powered by LangChain + Groq LLM"
)