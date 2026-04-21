"""
Expense Tracker - Project 2
Data Accumulation & State Preservation

This program demonstrates:
- Accumulator Pattern (total = total + new_expense)
- Continuous Loop with Sentinel Value
- Defensive Coding (Try/Except for type safety)
- State Management (preserving running total)
- File Persistence (saving expenses for future view)
- Decimal Rounding (converting decimals to integers)
"""

# Phase 1: INITIALIZATION (MEMORY)
total = 0
expenses_log = []
log_file = "expenses.txt"

# Phase 2: CONTINUOUS AUDIT LOOP
while True:
    # Get user input
    user_input = input("Enter expense amount (or 'quit' to finish): ").strip()

    # Kill Switch: Sentinel Value
    if user_input.lower() == 'quit':
        break

    # Defensive Coding: Type Safety & Error Handling
    try:
        # Convert to float first to handle decimals
        expense_float = float(user_input)

        # Ensure positive values
        if expense_float < 0:
            print("Invalid: Expenses must be positive values")
            continue

        # Round decimal to nearest integer
        expense = round(expense_float)

        if expense_float != expense:
            print(f"Rounded ${expense_float} to ${expense}")

        # ACCUMULATOR PATTERN: State(new) = State(old) + Input
        total += expense
        expenses_log.append(expense)

        print(f"Added ${expense}. Running total: ${total}")

    except ValueError:
        print("Invalid Data: Please enter a valid number or 'quit' to exit")

# Phase 3: OUTPUT - Display final result & Save to file
print(f"\nFINAL TOTAL: ${total}.00")

# Save expenses to file
with open(log_file, 'w') as f:
    f.write("EXPENSE TRACKER LOG\n")
    f.write("=" * 40 + "\n\n")

    if expenses_log:
        f.write("Individual Expenses:\n")
        for i, expense in enumerate(expenses_log, 1):
            f.write(f"{i}. ${expense}\n")
        f.write("\n" + "=" * 40 + "\n")
        f.write(f"FINAL TOTAL: ${total}.00\n")
    else:
        f.write("No expenses recorded.\n")

print(f"\nExpenses saved to '{log_file}'")
