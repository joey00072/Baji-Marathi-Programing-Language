import main
import sys

try:
    Debug=sys.argv[1]
except:
    Debug=True

while True:
    text = input("बाजी >")
    text = text.strip()
    if len(text)==0:
        continue
    result, error = main.run("<STDIN>", text, debug=Debug)
    if error:
        print(error.as_string())
    elif result:
        print(result)
