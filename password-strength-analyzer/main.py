import re
import string


def evaluate_password(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    # Special Character Check
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    # Strength Rating
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, feedback


def generate_suggestion(password):
    suggestion = password

    if not re.search(r"[A-Z]", suggestion):
        suggestion += "A"

    if not re.search(r"[a-z]", suggestion):
        suggestion += "a"

    if not re.search(r"\d", suggestion):
        suggestion += "1"

    if not any(char in string.punctuation for char in suggestion):
        suggestion += "@"

    if len(suggestion) < 12:
        suggestion += "Secure123!"

    return suggestion


def main():
    print("=" * 50)
    print("      PASSWORD STRENGTH ANALYZER")
    print("=" * 50)

    password = input("Enter Password: ")

    strength, feedback = evaluate_password(password)

    print("\nPassword Strength:", strength)

    if feedback:
        print("\nSecurity Recommendations:")
        for item in feedback:
            print(f"- {item}")

        print("\nSuggested Strong Password:")
        print(generate_suggestion(password))
    else:
        print("\nExcellent! Your password meets security standards.")


if __name__ == "__main__":
    main()