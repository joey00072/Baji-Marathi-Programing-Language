import main

while True:
    text = input('होन >')
    result , error = main.run('<STDIN>',text)
    if error:
        print(error.as_string())
    else:
        print(result)