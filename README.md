# Intelligent Bug Detection and Code Optimization Using LLM

## Project Overview

Intelligent Bug Detection and Code Optimization Using LLM is an AI-powered Python code analysis system designed to identify programming issues, explain detected bugs, and suggest optimized code using Large Language Models (LLMs).

The system combines traditional static code analysis with Gemini AI to help developers understand code quality issues and improve their Python programs.

## Key Features

- **Python Code Upload:** Upload Python source files through a Streamlit web interface.
- **Static Code Analysis:** Detect code issues using Python AST and Pylint.
- **Bug Detection:** Identify syntax errors and code-quality issues.
- **AI Bug Explanation:** Use Gemini AI to explain detected issues and suggest corrections.
- **Code Optimization:** Generate AI-based suggestions for improving code readability and efficiency.
- **Interactive Interface:** View analysis results through a Streamlit application.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Pylint
- Python AST
- HTML/CSS (if used for future interface enhancements)

## Project Structure

```text
Intelligent_Bug_Detection/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── modules/
│   ├── bug_detector.py
│   ├── static_analyzer.py
│   ├── unified_analyzer.py
│   ├── llm_explainer.py
│   ├── code_optimizer.py
│   └── complete_analyzer.py
│
├── code/
│   ├── sample.py
│   └── student_grade.py
│
├── data/
├── database/
├── tests/
├── static/
└── uploads/
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Intelligent_Bug_Detection
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key to GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

## Application Workflow

1. Upload a Python source-code file.
2. Display the uploaded code.
3. Run static code analysis.
4. Identify and display detected issues.
5. Send detected issues to Gemini AI for explanation.
6. Generate code optimization suggestions.
7. Display the analysis and optimization results.

## Future Enhancements

- Support for additional programming languages.
- Advanced bug classification using machine learning.
- Code complexity and performance analysis.
- Historical analysis reports using a database.
- Downloadable bug reports.
- Improved code optimization and correction suggestions.

## Project Title

**Intelligent Bug Detection and Code Optimization Using LLM**

