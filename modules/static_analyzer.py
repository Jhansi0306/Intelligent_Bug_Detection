
import subprocess
import sys
import json


def analyze_code(file_path):

    try:
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
            text=True
        )

        issues = json.loads(result.stdout)

        bug_reports = []

        for issue in issues:

            bug_reports.append({
                "type": issue["type"],
                "message": issue["message"],
                "file": issue["path"],
                "line": issue["line"],
                "column": issue["column"],
                "severity": issue["type"],
                "code": issue["message-id"]
            })

        return {
            "status": "success",
            "total_issues": len(bug_reports),
            "issues": bug_reports
        }

    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Unable to read Pylint results."
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error)
        }


if __name__ == "__main__":

    result = analyze_code("modules/sample.py")

    print("INTELLIGENT STATIC CODE ANALYZER")
    print("--------------------------------")

    print("Status:", result["status"])

    if result["status"] == "success":

        print("Total Issues:", result["total_issues"])

        for issue in result["issues"]:

            print("\nIssue Type:", issue["type"])
            print("Message:", issue["message"])
            print("File:", issue["file"])
            print("Line:", issue["line"])
            print("Column:", issue["column"])
            print("Severity:", issue["severity"])
            print("Code:", issue["code"])

    else:
        print("Error:", result["message"])
