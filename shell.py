import main

while True:
    text = input('मराठी >')
    result , error = main.run('<STDIN>',text)
    if error:
        print(error.as_string())
    else:
        print(result)