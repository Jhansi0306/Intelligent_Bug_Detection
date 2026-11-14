# Intelligent Bug Detection and Code Optimization Using LLM

## Project Overview

Intelligent Bug Detection and Code Optimization Using LLM is an AI-powered Python application that helps developers identify programming errors, understand code-quality issues, and improve their code using Large Language Models (LLMs).

The project combines traditional static code analysis techniques with Google Gemini AI to provide bug detection, beginner-friendly explanations, and code optimization suggestions through an interactive Streamlit interface.

## Key Features

- **Python Code Upload:** Upload Python files through the application.
- **Static Code Analysis:** Analyze source code using Python AST and Pylint.
- **Bug Detection:** Identify syntax errors and code-quality issues.
- **AI Bug Explanation:** Generate simple explanations and possible corrections using Gemini AI.
- **Code Optimization:** Generate optimized code suggestions using AI.
- **Interactive User Interface:** Perform analysis and optimization through a Streamlit web application.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- Python AST
- Pylint
- Git and GitHub

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
│   ├── complete_analyzer.py
│   └── check_gemini.py
│
├── code/
│   ├── sample.py
│   └── student_grade.py
│
└── tests/
    ├── gemini_test.py
    └── test.py
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Jhansi0306/Intelligent_Bug_Detection.git
cd Intelligent_Bug_Detection
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

Configure your Gemini API key using an environment variable or Streamlit secrets.

For local development, create a `.env` file in the project root if your application is configured to load it:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key to GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

## Application Workflow

1. Open the Streamlit application.
2. Upload a Python file or enter Python code.
3. Select Static Analysis to identify code issues.
4. View the detected issues.
5. Use AI Bug Explanation to understand the identified problems.
6. Select Code Optimization to generate improved code suggestions.

## Future Enhancements

- Support for additional programming languages.
- Advanced bug classification.
- Code complexity and performance analysis.
- Historical analysis reports.
- Downloadable analysis reports.
- Improved automated code correction.

## Project Information

**Project Title:** Intelligent Bug Detection and Code Optimization Using LLM

**Repository:** https://github.com/Jhansi0306/Intelligent_Bug_Detection

**Application Framework:** Streamlit

**AI Model:** Google Gemini