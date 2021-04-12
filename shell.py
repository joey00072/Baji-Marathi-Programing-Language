import hon

while True:
    text = input('होन >')
    result , error = hon.run('<STDIN>',text)
    if error:
    	print(error.as_string())
    else:
    	print(result)