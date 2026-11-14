
import os
import tempfile
import streamlit as st

from modules.unified_analyzer import analyze_code
from modules.llm_explainer import explain_bug
from modules.code_optimizer import optimize_code


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Intelligent Bug Detection",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# GEMINI API KEY
# --------------------------------------------------

try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "uploaded_code": "",
    "code_input": "",
    "analysis_result": None,
    "ai_explanation": None,
    "optimization_result": None,
    "selected_file_name": "pasted_code.py",
    "active_operation": None,
    "explanation_fallback": False,
    "optimization_fallback": False,
    "last_uploaded_file_signature": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# LOCAL FALLBACK FUNCTIONS
# --------------------------------------------------

def local_bug_explanation(result):

    issues = result.get("issues", [])

    if not issues:
        return (
            "No issues were detected by the static analyzer. "
            "Continue testing your code with different inputs."
        )

    messages = []

    for index, issue in enumerate(issues, 1):

        if isinstance(issue, dict):
            message = issue.get("message", "Code quality issue")
            line = issue.get("line", "Unknown")
        else:
            message = str(issue)
            line = "Unknown"

        messages.append(
            f"**Issue {index}:** {message}\n\n"
            f"**Line:** {line}\n\n"
            "**Solution:** Review the affected line and correct the issue."
        )

    return "\n\n---\n\n".join(messages)


def local_optimization(result):

    suggestions = []

    issues = result.get("issues", [])

    if not issues:
        suggestions.append("No static-analysis issues were reported.")
    else:
        for issue in issues:
            if isinstance(issue, dict):
                message = issue.get("message", "Code quality issue")
            else:
                message = str(issue)

            suggestions.append(f"- Review: {message}")

    suggestions.extend([
        "- Use meaningful variable and function names.",
        "- Remove unnecessary calculations where safe.",
        "- Avoid repeating the same code.",
        "- Use functions for reusable operations.",
        "- Handle invalid inputs and possible exceptions.",
        "- Test the program after every code modification."
    ])

    return "\n".join(suggestions)


def is_quota_error(error_text):

    error_text = str(error_text).upper()

    return any(word in error_text for word in [
        "429",
        "503",
        "504",
        "RESOURCE_EXHAUSTED",
        "QUOTA",
        "RATE LIMIT",
        "UNAVAILABLE",
        "HIGH DEMAND",
        "DEADLINE_EXCEEDED"
    ])


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* PAGE BACKGROUND */

.stApp {
    background:
        radial-gradient(
            circle at 50% 5%,
            rgba(125, 55, 190, 0.35),
            transparent 38%
        ),
        linear-gradient(
            135deg,
            #16052D,
            #241044,
            #35135B,
            #19082F
        );

    background-attachment: fixed;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: transparent;
}


/* MAIN HEADING */

.main-heading {
    text-align: center;
    color: #FF4FD8;
    font-size: clamp(54px, 8vw, 100px);
    font-weight: 1000;
    letter-spacing: 1px;
    line-height: 1.12;
    margin-top: 22px;
    margin-bottom: 10px;
    white-space: nowrap;

    text-shadow:
        0 0 6px rgba(255, 79, 216, 0.75),
        0 0 15px rgba(255, 79, 216, 0.5),
        0 0 28px rgba(255, 79, 216, 0.25);
}


/* SUBTITLE */

.main-subtitle {
    text-align: center;
    color: #67F5FF;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 35px;
    letter-spacing: 1px;
}


/* SECTION HEADINGS */

.section-heading {
    color: #FFD166;
    font-size: 21px;
    font-weight: 800;
    margin-top: 22px;
    margin-bottom: 12px;
}


/* UPLOAD BOX */

[data-testid="stFileUploader"] {
    max-width: 560px;
    margin-left: auto;
    margin-right: auto;
    background: #38205B !important;
    border: 2px dashed #B58AFF;
    border-radius: 14px;
    padding: 12px;
    transition: none !important;
}

[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] section > div {
    background: #38205B !important;
    transition: none !important;
}

[data-testid="stFileUploader"]:hover,
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section > div:hover {
    background: #38205B !important;
}

[data-testid="stFileUploader"] button {
    background: #38205B !important;
    color: #FFFFFF !important;
    border-color: #B58AFF !important;
}

[data-testid="stFileUploader"] button:hover {
    background: #38205B !important;
    color: #FFFFFF !important;
    border-color: #B58AFF !important;
}

[data-testid="stFileUploader"] button:active {
    background: #FFFFFF !important;
    color: #38205B !important;
    border-color: #FFFFFF !important;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #FFFFFF !important;
}


/* PASTE CODE BOX */

.st-key-code_input textarea {
    background: #38205B !important;
    color: #FFFFFF !important;
    border: 2px solid #B58AFF !important;
    border-radius: 12px !important;
    min-height: 75px !important;
}


/* SMALL RED WARNING */

.input-warning {
    color: #FF4545 !important;
    font-size: 12px;
    font-weight: 700;
    margin-top: 5px;
    margin-bottom: 8px;
    text-align: left;
}


/* OPERATION BOXES */

.st-key-static_analysis_box,
.st-key-ai_explanation_box,
.st-key-code_optimization_box {
    border-radius: 12px;
    padding: 4px;
    transition: all 0.25s ease;
}


/* BUTTON BASE STYLE */

.st-key-static_analysis_box .stButton > button,
.st-key-ai_explanation_box .stButton > button,
.st-key-code_optimization_box .stButton > button {

    width: 100%;
    min-height: 46px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 900;
    padding: 6px 10px;
    opacity: 1 !important;
    visibility: visible !important;
    transition: all 0.25s ease;
}


/* STATIC ANALYSIS BUTTON */

.st-key-static_analysis_box .stButton > button {
    background-color: #36A9F5 !important;
    color: #071C36 !important;
    border: 2px solid #A5E0FF !important;
}

.st-key-static_analysis_box .stButton > button p,
.st-key-static_analysis_box .stButton > button span {
    color: #071C36 !important;
    -webkit-text-fill-color: #071C36 !important;
}

.st-key-static_analysis_box .stButton > button:hover {
    background-color: #A8E1FF !important;
    color: #071C36 !important;
    border: 2px solid #FFFFFF !important;
    box-shadow:
        0 0 8px #60BFFF,
        0 0 20px rgba(96, 191, 255, 0.8) !important;
    transform: translateY(-3px) scale(1.02);
}


/* AI EXPLANATION BUTTON */

.st-key-ai_explanation_box .stButton > button {
    background-color: #FF69B4 !important;
    color: #351044 !important;
    border: 2px solid #FFB5DA !important;
}

.st-key-ai_explanation_box .stButton > button p,
.st-key-ai_explanation_box .stButton > button span {
    color: #351044 !important;
    -webkit-text-fill-color: #351044 !important;
}

.st-key-ai_explanation_box .stButton > button:hover {
    background-color: #FFB0E8 !important;
    color: #351044 !important;
    border: 2px solid #FFFFFF !important;
    box-shadow:
        0 0 8px #F472D0,
        0 0 20px rgba(244, 114, 208, 0.8) !important;
    transform: translateY(-3px) scale(1.02);
}


/* OPTIMIZATION BUTTON */

.st-key-code_optimization_box .stButton > button {
    background-color: #35D69A !important;
    color: #063B29 !important;
    border: 2px solid #9BFFD3 !important;
}

.st-key-code_optimization_box .stButton > button p,
.st-key-code_optimization_box .stButton > button span {
    color: #063B29 !important;
    -webkit-text-fill-color: #063B29 !important;
}

.st-key-code_optimization_box .stButton > button:hover {
    background-color: #9BFFD3 !important;
    color: #063B29 !important;
    border: 2px solid #FFFFFF !important;
    box-shadow:
        0 0 8px #35D69A,
        0 0 20px rgba(53, 214, 154, 0.8) !important;
    transform: translateY(-3px) scale(1.02);
}


/* GENERAL TEXT */

.stApp p,
.stApp label {
    color: #FFFFFF;
}


/* RESULTS */

.result-box {
    background: #38205B;
    border: 1px solid #B58AFF;
    border-radius: 12px;
    padding: 18px;
    color: #FFFFFF;
    margin-top: 12px;
}

h2, h3, h4 {
    color: #FFD166 !important;
}


/* METRICS */

[data-testid="stMetric"] {
    background: #38205B;
    border: 1px solid #B58AFF;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}


/* EXPANDERS */

[data-testid="stExpander"] {
    background: #38205B;
    border: 1px solid #B58AFF;
    border-radius: 10px;
}

[data-testid="stExpander"] summary {
    color: #FFFFFF !important;
}


/* ALERTS */

[data-testid="stAlert"] {
    border-radius: 10px;
}


/* CODE BLOCKS */

[data-testid="stCodeBlock"] {
    border-radius: 12px;
}


/* MOBILE RESPONSIVE */

@media (max-width: 700px) {

    .main-heading {
        font-size: 34px;
        white-space: normal;
    }

    .main-subtitle {
        font-size: 14px;
    }

}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MAIN HEADING
# --------------------------------------------------

st.markdown("""
<div class="main-heading">
    INTELLIGENT BUG DETECTION
</div>

<div class="main-subtitle">
    Detect Errors • Understand Bugs • Optimize Code
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CODE INPUT
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📁 Upload Your Python Code</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a Python file",
    type=["py"],
    label_visibility="collapsed"
)


# --------------------------------------------------
# CORRECTLY LOAD UPLOADED FILE INTO TEXT AREA
# --------------------------------------------------

if uploaded_file is not None:

    uploaded_code = uploaded_file.getvalue().decode(
        "utf-8-sig",
        errors="replace"
    )

    file_signature = (uploaded_file.name, uploaded_code)

    if file_signature != st.session_state.last_uploaded_file_signature:

        st.session_state.last_uploaded_file_signature = file_signature

        # Synchronize uploaded code with the paste box
        st.session_state.code_input = uploaded_code
        st.session_state.uploaded_code = uploaded_code
        st.session_state.selected_file_name = uploaded_file.name

        # Clear previous results
        st.session_state.analysis_result = None
        st.session_state.ai_explanation = None
        st.session_state.optimization_result = None
        st.session_state.active_operation = None
        st.session_state.explanation_fallback = False
        st.session_state.optimization_fallback = False

else:
    st.session_state.last_uploaded_file_signature = None


st.markdown(
    '<div class="section-heading">⌨️ Paste Your Code Here</div>',
    unsafe_allow_html=True
)

pasted_code = st.text_area(
    "Paste your Python code",
    height=75,
    placeholder="Paste your Python code here...",
    label_visibility="collapsed",
    key="code_input"
)


# --------------------------------------------------
# UPDATE PASTED CODE
# --------------------------------------------------

if pasted_code != st.session_state.uploaded_code:

    st.session_state.uploaded_code = pasted_code
    st.session_state.selected_file_name = "pasted_code.py"

    # Clear previous results when code changes
    st.session_state.analysis_result = None
    st.session_state.ai_explanation = None
    st.session_state.optimization_result = None
    st.session_state.active_operation = None
    st.session_state.explanation_fallback = False
    st.session_state.optimization_fallback = False


source_code = st.session_state.uploaded_code


# Placeholder for the small red warning
warning_placeholder = st.empty()


# --------------------------------------------------
# OPERATION BUTTONS
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">⚡ Select Inspection Operation</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(key="static_analysis_box"):
        static_button = st.button(
            "🔍 Static Analysis",
            use_container_width=True,
            key="static_button"
        )

with col2:
    with st.container(key="ai_explanation_box"):
        ai_button = st.button(
            "🤖 AI Bug Explanation",
            use_container_width=True,
            key="ai_button"
        )

with col3:
    with st.container(key="code_optimization_box"):
        optimize_button = st.button(
            "⚡ Code Optimization",
            use_container_width=True,
            key="optimize_button"
        )


# --------------------------------------------------
# SHOW WARNING ONLY WHEN BUTTON IS CLICKED WITHOUT CODE
# --------------------------------------------------

if (
    not source_code.strip()
    and (static_button or ai_button or optimize_button)
):

    warning_placeholder.markdown(
        '<p class="input-warning">'
        'Please upload a file or paste your code.'
        '</p>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# STATIC ANALYSIS
# --------------------------------------------------

if static_button and source_code.strip():

    with st.spinner("Analyzing your code..."):

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                encoding="utf-8",
                delete=False,
                newline="\n"
            ) as temp_file:

                temp_file.write(source_code)
                temp_path = temp_file.name

            result = analyze_code(temp_path)

            if not isinstance(result, dict):
                result = {
                    "status": "error",
                    "issues": [],
                    "total_issues": 0,
                    "message": str(result)
                }

            st.session_state.analysis_result = result
            st.session_state.ai_explanation = None
            st.session_state.optimization_result = None
            st.session_state.active_operation = "static"

        except Exception as error:
            st.error(f"Analysis failed: {error}")

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)


# --------------------------------------------------
# AI BUG EXPLANATION
# --------------------------------------------------

if ai_button and source_code.strip():

    with st.spinner("Generating AI bug explanation..."):

        try:

            result = st.session_state.analysis_result

            if not result or result.get("status") != "success":

                temp_path = None

                try:
                    with tempfile.NamedTemporaryFile(
                        mode="w",
                        suffix=".py",
                        encoding="utf-8",
                        delete=False,
                        newline="\n"
                    ) as temp_file:

                        temp_file.write(source_code)
                        temp_path = temp_file.name

                    result = analyze_code(temp_path)
                    st.session_state.analysis_result = result

                finally:
                    if temp_path and os.path.exists(temp_path):
                        os.remove(temp_path)

            issues = result.get("issues", [])

            issue_text = "\n".join(
                str(issue) for issue in issues
            )

            try:
                explanation = explain_bug(source_code, issue_text)
            except Exception as error:
                explanation = str(error)

            if is_quota_error(explanation):

                st.session_state.ai_explanation = local_bug_explanation(result)
                st.session_state.explanation_fallback = True

            else:

                st.session_state.ai_explanation = explanation
                st.session_state.explanation_fallback = False

            st.session_state.active_operation = "ai"

        except Exception as error:
            st.error(f"AI explanation failed: {error}")


# --------------------------------------------------
# CODE OPTIMIZATION
# --------------------------------------------------

if optimize_button and source_code.strip():

    with st.spinner("Optimizing your code..."):

        try:

            try:
                optimization = optimize_code(source_code)
            except Exception as error:
                optimization = str(error)

            if is_quota_error(optimization):

                result = st.session_state.analysis_result

                if not result or result.get("status") != "success":

                    temp_path = None

                    try:
                        with tempfile.NamedTemporaryFile(
                            mode="w",
                            suffix=".py",
                            encoding="utf-8",
                            delete=False,
                            newline="\n"
                        ) as temp_file:

                            temp_file.write(source_code)
                            temp_path = temp_file.name

                        result = analyze_code(temp_path)
                        st.session_state.analysis_result = result

                    finally:
                        if temp_path and os.path.exists(temp_path):
                            os.remove(temp_path)

                optimization = local_optimization(result)
                st.session_state.optimization_fallback = True

            else:
                st.session_state.optimization_fallback = False

            st.session_state.optimization_result = optimization
            st.session_state.active_operation = "optimize"

        except Exception as error:
            st.error(f"Optimization failed: {error}")


# --------------------------------------------------
# DISPLAY STATIC ANALYSIS RESULTS
# --------------------------------------------------

if (
    st.session_state.active_operation == "static"
    and st.session_state.analysis_result
):

    result = st.session_state.analysis_result

    st.divider()
    st.header("📊 Static Analysis Results")

    if result.get("status") == "success":

        total_issues = result.get(
            "total_issues",
            len(result.get("issues", []))
        )

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric("Total Issues Detected", total_issues)

        with metric2:
            st.metric("Analysis Status", "Completed")

        issues = result.get("issues", [])

        if issues:

            for index, issue in enumerate(issues, 1):

                if isinstance(issue, dict):
                    message = issue.get("message", "Issue detected")
                    line = issue.get("line", "Unknown")
                    severity = issue.get("severity", "Review")
                else:
                    message = str(issue)
                    line = "Unknown"
                    severity = "Review"

                with st.expander(f"🐞 Issue {index}: {message}"):
                    st.write(f"**Line:** {line}")
                    st.write(f"**Severity:** {severity}")

        else:
            st.success("🎉 No bugs or code-quality issues detected!")

    else:
        st.error(result.get("message", "Unable to analyze this code."))


# --------------------------------------------------
# DISPLAY AI EXPLANATION
# --------------------------------------------------

if (
    st.session_state.active_operation == "ai"
    and st.session_state.ai_explanation
):

    st.divider()
    st.header("🤖 AI Bug Explanation")

    if st.session_state.explanation_fallback:

        st.info(
            "Gemini is temporarily unavailable. "
            "Showing local explanations and possible solutions."
        )

    st.markdown(st.session_state.ai_explanation)


# --------------------------------------------------
# DISPLAY OPTIMIZATION
# --------------------------------------------------

if (
    st.session_state.active_operation == "optimize"
    and st.session_state.optimization_result
):

    st.divider()
    st.header("⚡ Code Optimization")

    if st.session_state.optimization_fallback:

        st.info(
            "Gemini is temporarily unavailable. "
            "Showing local optimization suggestions."
        )

        st.markdown(st.session_state.optimization_result)

    else:

        st.code(
            st.session_state.optimization_result,
            language="python"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<p style="
    text-align:center;
    color:#67F5FF;
    font-weight:600;
">
    Intelligent Bug Detection and Code Optimization Using LLM
</p>
""", unsafe_allow_html=True)
