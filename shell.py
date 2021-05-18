import main

while True:
    text = input("मराठी >")
    result, error = main.run("<STDIN>", text, debug=True)
    if error:
        print(error.as_string())
    elif result:
        print(result)
