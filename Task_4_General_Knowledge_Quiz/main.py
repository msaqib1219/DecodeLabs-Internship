def main():
    score = 0

    print("=" * 50)
    print("Welcome to the General Knowledge Quiz!")
    print("=" * 50)
    print()

    # Question 1
    print("Question 1: What is the capital of Pakistan?")
    answer1 = input("Your answer: ").strip().lower()

    if answer1 == "islamabad":
        print("✓ Correct!\n")
        score = score + 1
    else:
        print("✗ Wrong! The correct answer is Islamabad.\n")

    # Question 2
    print("Question 2: What is the national sports of Pakistan?")
    answer2 = input("Your answer: ").strip().lower()

    if answer2 == "hockey":
        print("✓ Correct!\n")
        score = score + 1
    else:
        print("✗ Wrong! The correct answer is Hockey.\n")

    # Question 3
    print("Question 3: Pakistan total area is how many square kilometers'?")
    answer3 = input("Your answer: ").strip().lower()

    if answer3 == "881,913":
        print("✓ Correct!\n")
        score = score + 1
    else:
        print("✗ Wrong! The correct answer is 881,913 square kilometers as per Wikipedia sources.\n")

    print("=" * 50)
    print(f"Final Score: {score}/3")
    print("=" * 50)


if __name__ == "__main__":
    main()
