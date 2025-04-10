try:
    int("a")
except ValueError as e:
    print("Oops! That was not a number.", e)

print("This is the end of the program.")