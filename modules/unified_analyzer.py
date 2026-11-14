
import ast
import subprocess
import sys
import json
import os
import tempfile


def analyze_code(file_path):

    try:
        # Step 1: Read source code and normalize line endings
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=None
        ) as file:
            source_code = file.read()

        source_code = source_code.replace("\r\n", "\n")
        source_code = source_code.replace("\r", "\n")

        # Step 2: Check Python syntax
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

        # Step 3: Create a temporary file with clean LF line endings
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            encoding="utf-8",
            newline="\n",
            delete=False
        ) as temp_file:

            temp_file.write(source_code)
            clean_file_path = temp_file.name

        try:
            # Step 4: Run Pylint on normalized source code
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    "--output-format=json",
                    "--enable=unused-variable",
                    clean_file_path
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30
            )

            # Step 5: Read Pylint results
            try:
                pylint_issues = json.loads(result.stdout or "[]")
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "message": "Unable to read Pylint analysis results."
                }

            bug_reports = []

            for issue in pylint_issues:

                issue_type = issue.get("type", "info")

                if issue_type in ["error", "fatal"]:
                    severity = "error"
                elif issue_type == "warning":
                    severity = "warning"
                else:
                    severity = "info"

                bug_reports.append({
                    "type": issue_type,
                    "message": issue.get("message", ""),
                    "file": file_path,
                    "line": issue.get("line", 0),
                    "column": issue.get("column", 0),
                    "severity": severity,
                    "code": issue.get("message-id", "")
                })

            return {
                "status": "success",
                "file": file_path,
                "total_issues": len(bug_reports),
                "issues": bug_reports
            }

        finally:
            # Step 6: Remove temporary file
            if os.path.exists(clean_file_path):
                os.remove(clean_file_path)

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
