
import ast
import subprocess
import sys
import json


def analyze_code(file_path):

    try:
        # Step 1: Read source code
        with open(file_path, "r", encoding="utf-8-sig", newline=None) as file:
            source_code = file.read()

        # Step 2: Check syntax
        try:
            ast.parse(source_code)

        except SyntaxError as error:
            return {
                "status": "success",
                "file": file_path,
                "total_issues": 1,
                "issues": [
                    {
                        "type": "syntax",
                        "message": error.msg,
                        "file": file_path,
                        "line": error.lineno,
                        "column": error.offset,
                        "severity": "error",
                        "code": "E-SYNTAX"
                    }
                ]
            }

        # Step 3: Run Pylint
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pylint",
                "--output-format=json",
                "--enable=unused-variable",
                file_path
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Step 4: Read Pylint results
        pylint_issues = json.loads(result.stdout or "[]")

        bug_reports = []

        for issue in pylint_issues:

            issue_type = issue["type"]

            if issue_type in ["error", "fatal"]:
                severity = "error"
            elif issue_type == "warning":
                severity = "warning"
            else:
                severity = "info"

            bug_reports.append({
                "type": issue_type,
                "message": issue["message"],
                "file": issue["path"],
                "line": issue["line"],
                "column": issue["column"],
                "severity": severity,
                "code": issue["message-id"]
            })

        return {
            "status": "success",
            "file": file_path,
            "total_issues": len(bug_reports),
            "issues": bug_reports
        }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


if __name__ == "__main__":

    file_path = "modules/sample.py"

    print("======================================")
    print(" INTELLIGENT BUG DETECTION SYSTEM")
    print("======================================")

    result = analyze_code(file_path)

    print("Status:", result["status"])

    if result["status"] == "success":

        print("File:", result["file"])
        print("Total Issues:", result["total_issues"])

        for issue in result["issues"]:

            print("\n------------------------------")
            print("Type:", issue["type"])
            print("Message:", issue["message"])
            print("Line:", issue["line"])
            print("Severity:", issue["severity"])
            print("Code:", issue["code"])

    else:
        print("Error:", result["message"])
