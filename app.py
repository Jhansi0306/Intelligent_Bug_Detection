
import streamlit as st
import os
import tempfile

# Load Gemini API key from Streamlit Cloud Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

from modules.unified_analyzer import analyze_code
from modules.llm_explainer import explain_bug
from modules.code_optimizer import optimize_code



st.set_page_config(
    page_title="Intelligent Bug Detection",
    page_icon="🐞",
    layout="wide"
)

st.title("🐞 Intelligent Bug Detection System")

st.write(
    "AI-powered Python bug detection and code optimization "
    "using Gemini."
)

uploaded_file = st.file_uploader(
    "Upload your Python file",
    type=["py"]
)

if uploaded_file is not None:

    source_code = uploaded_file.getvalue().decode("utf-8-sig")
    source_code = source_code.replace("\r\n", "\n").replace("\r", "\n")

    st.subheader("Uploaded Python Code")
    st.code(source_code, language="python")

    if st.button("Analyze My Code", type="primary"):

        with st.spinner("Detecting code issues..."):

            temp_path = None

            try:
                os.makedirs("uploads", exist_ok=True)

                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    newline="\n",
                    suffix=".py",
                    dir="uploads",
                    delete=False
                ) as temp_file:

                    temp_file.write(source_code)
                    temp_path = temp_file.name

                result = analyze_code(temp_path)

            except Exception as error:
                result = {
                    "status": "error",
                    "message": str(error)
                }

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

        if result["status"] != "success":

            st.error(result["message"])

        else:

            st.success("Code analysis completed!")

            st.metric(
                "Total Issues Detected",
                result["total_issues"]
            )

            if result["total_issues"] == 0:
                st.success("No issues detected!")

            for index, issue in enumerate(
                result["issues"], start=1
            ):

                with st.expander(
                    f"Issue {index}: {issue['message']}"
                ):

                    st.write("Type:", issue["type"])
                    st.write("Line:", issue["line"])
                    st.write("Severity:", issue["severity"])
                    st.write("Code:", issue["code"])

            if result["total_issues"] > 0:

                issues_text = "\n".join(
                    [
                        f"Issue: {issue['message']}, "
                        f"Line: {issue['line']}, "
                        f"Severity: {issue['severity']}"
                        for issue in result["issues"]
                    ]
                )

                st.subheader("🤖 AI Bug Explanation")

                with st.spinner("Gemini is explaining the issues..."):

                    explanation = explain_bug(
                        source_code,
                        issues_text
                    )

                if "429" in explanation or "RESOURCE_EXHAUSTED" in explanation:
                    st.warning(
                        "Gemini daily request limit reached. "
                        "Bug detection is still working. "
                        "Please try again after the quota resets."
                    )

                elif "504" in explanation or "DEADLINE_EXCEEDED" in explanation:
                    st.warning(
                        "Gemini is taking too long to respond. "
                        "Please try again later."
                    )

                elif "503" in explanation or "UNAVAILABLE" in explanation:
                    st.warning(
                        "Gemini AI is temporarily busy. "
                        "Please try again later."
                    )

                elif "Error:" in explanation or "Gemini API Error:" in explanation:
                    st.warning(explanation)

                else:
                    st.markdown(explanation)

            st.subheader("⚡ AI Code Optimization")

            with st.spinner("Gemini is optimizing your code..."):

                optimization = optimize_code(source_code)

            if "429" in optimization or "RESOURCE_EXHAUSTED" in optimization:
                st.warning(
                    "Gemini daily request limit reached. "
                    "Code optimization is temporarily unavailable. "
                    "Please try again after the quota resets."
                )

            elif "504" in optimization or "DEADLINE_EXCEEDED" in optimization:
                st.warning(
                    "Gemini optimization request timed out. "
                    "Please try again later."
                )

            elif "503" in optimization or "UNAVAILABLE" in optimization:
                st.warning(
                    "Gemini AI is temporarily busy. "
                    "Please try again later."
                )

            elif "Optimization Error:" in optimization or "Error:" in optimization:
                st.warning(optimization)

            else:
                st.markdown(optimization)

st.divider()

st.caption(
    "Intelligent Bug Detection and Code Optimization Using LLM"
)
