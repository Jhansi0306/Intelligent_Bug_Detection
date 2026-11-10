import ast


def detect_syntax_errors(source_code):

    try:
        ast.parse(source_code)

        return {
            "status": "success",
            "message": "No syntax errors detected!"
        }

    except SyntaxError as error:

        return {
            "status": "error",
            "message": error.msg,
            "line": error.lineno,
            "column": error.offset
        }


if __name__ == "__main__":

    sample_code = """
def greet()
    print("Hello, Jhansi!")

greet()
"""

    result = detect_syntax_errors(sample_code)

    print("INTELLIGENT BUG DETECTION")
    print("-------------------------")
print("Status:", result["status"])
print("Message:", result["message"])

if result["status"] == "error":
    print("Error Line:", result["line"])
    print("Error Column:", result["column"])