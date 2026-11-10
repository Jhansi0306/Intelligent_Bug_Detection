from code_optimizer import optimize_code
from unified_analyzer import analyze_code
from llm_explainer import explain_bug


FILE_PATH = "code/sample.py"


def run_complete_analysis():

    print("======================================")
    print(" INTELLIGENT BUG DETECTION SYSTEM")
    print("======================================")

    # Step 1: Detect code issues
    print("\nStep 1: Running static code analysis...")

    result = analyze_code(FILE_PATH)

    if result["status"] != "success":
        print("Analyzer Error:", result["message"])
        return

    print("Total Issues Detected:", result["total_issues"])

    if result["total_issues"] == 0:
        print("No code issues detected!")
        return

    # Step 2: Read source code
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        source_code = file.read()

    # Step 3: Prepare all detected issues
    issues_text = ""

    for number, issue in enumerate(result["issues"], start=1):

        issues_text += (
            f"\nIssue {number}:\n"
            f"Type: {issue['type']}\n"
            f"Message: {issue['message']}\n"
            f"Line: {issue['line']}\n"
            f"Severity: {issue['severity']}\n"
            f"Code: {issue['code']}\n"
        )

    print("\nStep 2: Detected issues prepared.")
    print("\nStep 3: Sending issues to Gemini AI...")

    # Step 4: Get AI explanation
    explanation = explain_bug(source_code, issues_text)

    print("\n======================================")
    print(" GEMINI AI ANALYSIS AND SOLUTIONS")
    print("======================================")

    print(explanation)
    # Step 5: Optimize the source code
    print("\n======================================")
    print(" AI CODE OPTIMIZATION")
    print("======================================")

    print("\nOptimizing source code...")

    optimization = optimize_code(source_code)

    print("\nOPTIMIZATION RESULTS")
    print("--------------------")
    print(optimization)


if __name__ == "__main__":
    run_complete_analysis()
