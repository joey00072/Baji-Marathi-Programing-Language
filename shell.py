import main
import sys

try:
    Debug=sys.argv[1]
except:
    Debug=False

while True:
    text = input("बाजी >")
    result, error = main.run("<STDIN>", text, debug=Debug)
    if error:
        print(error.as_string())
    elif result:
        print(result)
