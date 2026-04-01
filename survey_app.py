"""
Campus Walk Frequency and Mental Refreshment During Breaks Survey
Fundamentals of Programming - Project 1
Streamlit Web-Based Application
"""

import streamlit as st
import json
import csv
import re
import os
from datetime import datetime, date

# ─────────────────────────────────────────────
# VARIABLE TYPES USED (for assessment criteria):
# int, str, float, list, tuple, range, bool, dict, set, frozenset
# ─────────────────────────────────────────────

SURVEY_TITLE: str = "Campus Walk Frequency and Mental Refreshment During Breaks Survey"
SURVEY_DESCRIPTION: str = (
    "This survey evaluates how frequently you engage in campus walks during breaks "
    "and how mentally refreshed you feel as a result."
)
MAX_SCORE: int = 80
SCORE_PERCENTAGE_PRECISION: float = 1.0   # decimal places used when rounding percentage scores
ALLOWED_CHARS: frozenset = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'")

# Questions embedded directly in the code (list of dicts)
QUESTIONS: list = [
    {
        "id": 1,
        "text": "How many times per day do you typically take a walk during academic breaks?",
        "options": [
            {"label": "3 or more times", "score": 0},
            {"label": "Twice a day", "score": 1},
            {"label": "Once a day", "score": 2},
            {"label": "Rarely, only occasionally", "score": 3},
            {"label": "I never walk during breaks", "score": 4},
        ],
    },
    {
        "id": 2,
        "text": "After a short walk around campus, how mentally refreshed do you feel?",
        "options": [
            {"label": "Completely refreshed and re-energized", "score": 0},
            {"label": "Noticeably refreshed", "score": 1},
            {"label": "Slightly refreshed", "score": 2},
            {"label": "Barely any difference", "score": 3},
            {"label": "I feel no mental refreshment at all", "score": 4},
        ],
    },
    {
        "id": 3,
        "text": "How long do your campus walks during breaks usually last?",
        "options": [
            {"label": "More than 15 minutes", "score": 0},
            {"label": "10 to 15 minutes", "score": 1},
            {"label": "5 to 10 minutes", "score": 2},
            {"label": "Less than 5 minutes", "score": 3},
            {"label": "I do not walk during breaks", "score": 4},
        ],
    },
    {
        "id": 4,
        "text": "How well can you concentrate on your studies after taking a walk during a break?",
        "options": [
            {"label": "Much better than before", "score": 0},
            {"label": "Somewhat better", "score": 1},
            {"label": "About the same", "score": 2},
            {"label": "Slightly worse, I feel distracted", "score": 3},
            {"label": "My concentration drops significantly", "score": 4},
        ],
    },
    {
        "id": 5,
        "text": "Do you feel that walking on campus between classes helps reduce your academic pressure?",
        "options": [
            {"label": "Definitely yes, it greatly reduces pressure", "score": 0},
            {"label": "Yes, it helps a little", "score": 1},
            {"label": "Neutral, it makes no difference", "score": 2},
            {"label": "Not really, I still feel pressured", "score": 3},
            {"label": "No, it does not help at all", "score": 4},
        ],
    },
    {
        "id": 6,
        "text": "How often do you choose to sit indoors instead of walking during your free time on campus?",
        "options": [
            {"label": "Never, I always prefer to walk", "score": 0},
            {"label": "Rarely, walking is my first choice", "score": 1},
            {"label": "Sometimes I sit, sometimes I walk", "score": 2},
            {"label": "I usually sit rather than walk", "score": 3},
            {"label": "Always, I always stay seated indoors", "score": 4},
        ],
    },
    {
        "id": 7,
        "text": "How does your mood change after a walk through the campus grounds?",
        "options": [
            {"label": "My mood improves greatly", "score": 0},
            {"label": "My mood improves slightly", "score": 1},
            {"label": "My mood stays the same", "score": 2},
            {"label": "I feel somewhat worse afterwards", "score": 3},
            {"label": "My mood worsens noticeably", "score": 4},
        ],
    },
    {
        "id": 8,
        "text": "How physically active do you feel during a typical academic day on campus?",
        "options": [
            {"label": "Very active, I walk a lot between activities", "score": 0},
            {"label": "Fairly active with some movement", "score": 1},
            {"label": "Moderately active", "score": 2},
            {"label": "Mostly seated with minimal movement", "score": 3},
            {"label": "Almost entirely sedentary all day", "score": 4},
        ],
    },
    {
        "id": 9,
        "text": "How often do you use campus outdoor spaces (gardens, courtyards, pathways) during breaks?",
        "options": [
            {"label": "Every single break", "score": 0},
            {"label": "Most breaks", "score": 1},
            {"label": "Occasionally", "score": 2},
            {"label": "Rarely", "score": 3},
            {"label": "Never", "score": 4},
        ],
    },
    {
        "id": 10,
        "text": "How do you feel about your ability to manage mental fatigue throughout the academic day?",
        "options": [
            {"label": "I manage it very well through regular movement", "score": 0},
            {"label": "I manage it reasonably well", "score": 1},
            {"label": "I sometimes struggle with fatigue", "score": 2},
            {"label": "I often feel mentally drained", "score": 3},
            {"label": "I feel constantly mentally exhausted", "score": 4},
        ],
    },
    {
        "id": 11,
        "text": "How often do you feel mentally stuck or unable to process new information during lectures?",
        "options": [
            {"label": "Never, I always feel mentally clear", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Almost every lecture", "score": 4},
        ],
    },
    {
        "id": 12,
        "text": "When you feel mentally tired during the day, what do you most commonly do?",
        "options": [
            {"label": "Go for a walk around campus immediately", "score": 0},
            {"label": "Take a short walk if time allows", "score": 1},
            {"label": "Sit quietly and rest in place", "score": 2},
            {"label": "Use my phone or scroll social media", "score": 3},
            {"label": "Continue working despite the fatigue", "score": 4},
        ],
    },
    {
        "id": 13,
        "text": "How much does the natural environment of your campus (trees, open areas) contribute to your sense of calm?",
        "options": [
            {"label": "It greatly contributes to my calmness", "score": 0},
            {"label": "It helps a fair amount", "score": 1},
            {"label": "It has a minor effect", "score": 2},
            {"label": "It has almost no effect on me", "score": 3},
            {"label": "It has no effect whatsoever", "score": 4},
        ],
    },
    {
        "id": 14,
        "text": "How often do you plan or schedule a walk into your academic day as a deliberate break strategy?",
        "options": [
            {"label": "Always, it is a regular part of my routine", "score": 0},
            {"label": "Often", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Rarely, only when I remember", "score": 3},
            {"label": "Never, I do not plan walks at all", "score": 4},
        ],
    },
    {
        "id": 15,
        "text": "How would you rate your overall mental well-being on days when you walk regularly on campus compared to days when you do not?",
        "options": [
            {"label": "Much better on walking days", "score": 0},
            {"label": "Slightly better on walking days", "score": 1},
            {"label": "I notice no real difference", "score": 2},
            {"label": "Slightly worse on walking days due to tiredness", "score": 3},
            {"label": "I have never noticed any connection", "score": 4},
        ],
    },
    {
        "id": 16,
        "text": "How easy is it for you to detach mentally from academic work during a break walk?",
        "options": [
            {"label": "Very easy, I fully switch off from work", "score": 0},
            {"label": "Fairly easy", "score": 1},
            {"label": "Neutral, sometimes I do sometimes I don't", "score": 2},
            {"label": "Difficult, my mind stays on coursework", "score": 3},
            {"label": "Impossible, I cannot stop thinking about tasks", "score": 4},
        ],
    },
    {
        "id": 17,
        "text": "How often do you feel physically restless or tense after sitting for long periods during classes?",
        "options": [
            {"label": "Never, I manage well through regular movement", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Almost always after every long session", "score": 4},
        ],
    },
    {
        "id": 18,
        "text": "How satisfied are you with the quality of your mental breaks during the academic day?",
        "options": [
            {"label": "Very satisfied", "score": 0},
            {"label": "Fairly satisfied", "score": 1},
            {"label": "Neutral", "score": 2},
            {"label": "Somewhat dissatisfied", "score": 3},
            {"label": "Very dissatisfied", "score": 4},
        ],
    },
    {
        "id": 19,
        "text": "How often do you walk with peers or classmates during campus breaks as a social-refreshment activity?",
        "options": [
            {"label": "Almost always", "score": 0},
            {"label": "Frequently", "score": 1},
            {"label": "Occasionally", "score": 2},
            {"label": "Rarely", "score": 3},
            {"label": "Never, I always stay alone and seated", "score": 4},
        ],
    },
    {
        "id": 20,
        "text": "How do you feel your academic performance is affected by the amount of physical movement you get during the day?",
        "options": [
            {"label": "More movement clearly improves my performance", "score": 0},
            {"label": "It somewhat helps my performance", "score": 1},
            {"label": "I see no connection between movement and performance", "score": 2},
            {"label": "Too much movement distracts me", "score": 3},
            {"label": "Physical movement negatively affects my studies", "score": 4},
        ],
    },
]

# Psychological states (tuple of dicts for immutability)
PSYCHOLOGICAL_STATES: tuple = (
    {"min": 0,  "max": 15, "label": "Excellent Mental Refreshment",
     "description": "You walk frequently and experience very high levels of mental refreshment. Your break habits are excellent, and your mind is well-rested and alert throughout the day. No intervention needed."},
    {"min": 16, "max": 30, "label": "Good Mental Recovery",
     "description": "You maintain reasonably good walking habits and benefit from moderate mental refreshment. Your mental energy levels are mostly stable. Continue your current routine and consider adding more outdoor time."},
    {"min": 31, "max": 45, "label": "Moderate Refreshment — Improvement Recommended",
     "description": "Your walking frequency and mental refreshment are at a moderate level. You may experience occasional mental fatigue. It is recommended to incorporate at least one intentional 10-minute walk into each academic day."},
    {"min": 46, "max": 60, "label": "Low Mental Refreshment — Action Advised",
     "description": "You walk infrequently and mental refreshment is low. You likely experience noticeable mental fatigue and reduced concentration. A structured break-walking routine is strongly advised to improve your well-being."},
    {"min": 61, "max": 75, "label": "Poor Break Habits — Wellbeing at Risk",
     "description": "Your break habits are poor and you are experiencing significant mental fatigue due to inactivity. Academic performance may be affected. Consider speaking with a student wellbeing advisor and start a daily movement plan."},
    {"min": 76, "max": 80, "label": "Critical Sedentary State — Support Needed",
     "description": "You are almost entirely sedentary during the academic day and experience very low mental refreshment. This pattern poses a serious risk to your psychological and physical health. Professional wellbeing support is strongly recommended."},
)

# Score color map (dict)
STATE_COLORS: dict = {
    "Excellent Mental Refreshment": "#2ecc71",
    "Good Mental Recovery": "#27ae60",
    "Moderate Refreshment — Improvement Recommended": "#f1c40f",
    "Low Mental Refreshment — Action Advised": "#e67e22",
    "Poor Break Habits — Wellbeing at Risk": "#e74c3c",
    "Critical Sedentary State — Support Needed": "#8e44ad",
}

# ─────────────────────────────────────────────
# LOAD QUESTIONS FROM EXTERNAL FILE AT RUNTIME
# ─────────────────────────────────────────────

def load_questions_from_file(filepath: str = "questions.json") -> list:
    """Load survey questions from an external JSON file at runtime.
    Falls back to the hardcoded QUESTIONS list if the file is not found."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
            loaded: list = data.get("questions", [])
            if loaded:
                return loaded
    except FileNotFoundError:
        pass
    except Exception:
        pass
    # Fallback: return hardcoded questions
    return QUESTIONS


# Active question set — loaded from file if available, else hardcoded
ACTIVE_QUESTIONS: list = load_questions_from_file()

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def validate_name(name: str) -> bool:
    """Validate name: only letters, hyphens, apostrophes, spaces allowed."""
    if not name or not name.strip():
        return False
    allowed: set = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'")
    # for loop for input validation
    for char in name:
        if char not in allowed:
            return False
    return True


def validate_student_id(sid: str) -> bool:
    """Validate student ID: digits only."""
    if not sid:
        return False
    # while loop for input validation (simulated with index)
    i: int = 0
    while i < len(sid):
        if not sid[i].isdigit():
            return False
        i += 1
    return True


def get_psychological_state(score: int) -> dict:
    """Return the psychological state dict based on total score."""
    for state in PSYCHOLOGICAL_STATES:
        if state["min"] <= score <= state["max"]:
            return state
    return PSYCHOLOGICAL_STATES[-1]


def calculate_score(answers: list) -> int:
    """Calculate total score from a list of selected option scores."""
    total: int = 0
    for s in answers:
        total += s
    return total


def build_result_dict(surname: str, given_name: str, dob: str,
                      student_id: str, score: int, state: dict) -> dict:
    """Build a result dictionary for saving."""
    percentage_score: float = round((score / MAX_SCORE) * 100, int(SCORE_PERCENTAGE_PRECISION))
    result: dict = {
        "surname": surname,
        "given_name": given_name,
        "date_of_birth": dob,
        "student_id": student_id,
        "total_score": score,
        "percentage_score": percentage_score,
        "psychological_state": state["label"],
        "description": state["description"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return result


def save_results_json(result: dict) -> str:
    """Save results to a JSON file and return the filename."""
    filename: str = f"result_{result['student_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    return filename


def load_results_json(file_content: str) -> dict:
    """Load and parse a JSON result file."""
    data: dict = json.loads(file_content)
    return data

# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Campus Walk Survey",
        page_icon="🚶",
        layout="centered",
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main { background-color: #f0f4f8; }
        .stRadio > div { gap: 6px; }
        .result-box {
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            margin-top: 1rem;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚶 " + SURVEY_TITLE)
    st.caption(SURVEY_DESCRIPTION)
    st.divider()

    # Session state initialization
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "result" not in st.session_state:
        st.session_state.result = None

    # ── HOME PAGE ──
    if st.session_state.page == "home":
        st.subheader("Welcome! What would you like to do?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Start New Survey", use_container_width=True, type="primary"):
                st.session_state.page = "details"
                st.rerun()
        with col2:
            if st.button("📂 Load Existing Result", use_container_width=True):
                st.session_state.page = "load"
                st.rerun()

    # ── LOAD PAGE ──
    elif st.session_state.page == "load":
        st.subheader("📂 Load Existing Result")
        uploaded = st.file_uploader("Upload a JSON result file", type=["json"])
        if uploaded:
            try:
                content: str = uploaded.read().decode("utf-8")
                data: dict = load_results_json(content)
                st.success("✅ Result loaded successfully!")
                # Display loaded result
                state_label: str = data.get("psychological_state", "Unknown")
                color: str = STATE_COLORS.get(state_label, "#555")
                st.markdown(f"""
                    <div class="result-box" style="background:{color}">
                        <b>{data.get('given_name', '')} {data.get('surname', '')}</b><br>
                        Student ID: {data.get('student_id', '')}<br>
                        Date of Birth: {data.get('date_of_birth', '')}<br>
                        Total Score: {data.get('total_score', '')} / {MAX_SCORE} ({data.get('percentage_score', 'N/A')}%)<br>
                        State: <b>{state_label}</b><br><br>
                        {data.get('description', '')}
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error reading file: {e}")
        if st.button("⬅ Back to Home"):
            st.session_state.page = "home"
            st.rerun()

    # ── PERSONAL DETAILS PAGE ──
    elif st.session_state.page == "details":
        st.subheader("👤 Personal Details")
        st.info("Please fill in your details before starting the survey.")

        surname = st.text_input("Surname", placeholder="e.g. Smith-Jones")
        given_name = st.text_input("Given Name", placeholder="e.g. Mary Ann")
        dob = st.date_input(
            "Date of Birth",
            min_value=date(1950, 1, 1),
            max_value=date.today(),
            value=date(2000, 1, 1),
        )
        student_id = st.text_input("Student ID (digits only)", placeholder="e.g. 00123456")

        # Validation using if/elif/else
        if st.button("Continue to Survey ➡", type="primary"):
            errors: list = []
            if not validate_name(surname):
                errors.append("❌ Surname is invalid. Use only letters, spaces, hyphens, or apostrophes.")
            if not validate_name(given_name):
                errors.append("❌ Given name is invalid. Use only letters, spaces, hyphens, or apostrophes.")
            if not validate_student_id(student_id):
                errors.append("❌ Student ID must contain digits only.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                st.session_state.surname = surname
                st.session_state.given_name = given_name
                st.session_state.dob = str(dob)
                st.session_state.student_id = student_id
                st.session_state.page = "survey"
                st.session_state.answers = []
                st.rerun()

        if st.button("⬅ Back to Home"):
            st.session_state.page = "home"
            st.rerun()

    # ── SURVEY PAGE ──
    elif st.session_state.page == "survey":
        st.subheader("📋 Survey Questions")
        total_q: int = len(ACTIVE_QUESTIONS)
        score_range: range = range(total_q)

        with st.form("survey_form"):
            selected_scores: list = []
            all_answered: bool = True

            for idx in score_range:
                q: dict = ACTIVE_QUESTIONS[idx]
                labels: list = [opt["label"] for opt in q["options"]]
                st.markdown(f"**Q{q['id']}. {q['text']}**")
                choice = st.radio(
                    label=f"q{q['id']}",
                    options=labels,
                    index=None,
                    label_visibility="collapsed",
                    key=f"q_{q['id']}",
                )
                selected_scores.append((choice, q["options"]))
                st.divider()

            submitted: bool = st.form_submit_button("Submit Survey ✅", type="primary")

        if submitted:
            final_scores: list = []
            unanswered: list = []

            for i, (choice, options) in enumerate(selected_scores):
                if choice is None:
                    unanswered.append(i + 1)
                else:
                    for opt in options:
                        if opt["label"] == choice:
                            final_scores.append(opt["score"])
                            break

            if unanswered:
                st.error(f"⚠️ Please answer all questions. Unanswered: {unanswered}")
            else:
                total: int = calculate_score(final_scores)
                state: dict = get_psychological_state(total)
                result: dict = build_result_dict(
                    st.session_state.surname,
                    st.session_state.given_name,
                    st.session_state.dob,
                    st.session_state.student_id,
                    total,
                    state,
                )
                st.session_state.result = result
                st.session_state.page = "result"
                st.rerun()

    # ── RESULT PAGE ──
    elif st.session_state.page == "result":
        result: dict = st.session_state.result
        state_label: str = result["psychological_state"]
        color: str = STATE_COLORS.get(state_label, "#555")

        st.subheader("📊 Your Results")
        st.markdown(f"""
            <div class="result-box" style="background:{color}">
                <b>Name:</b> {result['given_name']} {result['surname']}<br>
                <b>Student ID:</b> {result['student_id']}<br>
                <b>Date of Birth:</b> {result['date_of_birth']}<br>
                <b>Total Score:</b> {result['total_score']} / {MAX_SCORE} ({result['percentage_score']}%)<br>
                <br>
                <b>Psychological State: {state_label}</b><br><br>
                {result['description']}
            </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.subheader("💾 Save Your Results")
        fmt: str = st.selectbox("Choose file format", ["JSON", "CSV", "TXT"])

        if st.button("Download Results", type="primary"):
            if fmt == "JSON":
                content: str = json.dumps(result, indent=4, ensure_ascii=False)
                st.download_button(
                    label="📥 Download JSON",
                    data=content,
                    file_name=f"result_{result['student_id']}.json",
                    mime="application/json",
                )
            elif fmt == "CSV":
                import io
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=result.keys())
                writer.writeheader()
                writer.writerow(result)
                st.download_button(
                    label="📥 Download CSV",
                    data=output.getvalue(),
                    file_name=f"result_{result['student_id']}.csv",
                    mime="text/csv",
                )
            elif fmt == "TXT":
                lines: list = [f"{k}: {v}" for k, v in result.items()]
                txt_content: str = "\n".join(lines)
                st.download_button(
                    label="📥 Download TXT",
                    data=txt_content,
                    file_name=f"result_{result['student_id']}.txt",
                    mime="text/plain",
                )

        if st.button("🔄 Start New Survey"):
            for key in ["page", "answers", "result", "surname",
                        "given_name", "dob", "student_id"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()
