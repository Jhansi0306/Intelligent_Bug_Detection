"""Program to calculate student grades."""


def calculate_grade(marks):
    """Return the grade based on marks."""

    if marks >= 90:
        return "A"

    if marks >= 75:
        return "B"

    if marks >= 60:
        return "C"

    if marks >= 40:
        return "D"

    return "Fail"


if __name__ == "__main__":
    student_marks = 85
    grade = calculate_grade(student_marks)

    print("Student Marks:", student_marks)
    print("Student Grade:", grade)
