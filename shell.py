import main
import sys

try:
    Debug=sys.argv[-1] == True
except:
    Debug=True

Debug=True

if len(sys.argv)>1:
    main.run_from_file(sys.argv[1])
else:
    while True:
        text = input("बाजी >")
        text = text.strip()
        if len(text)==0:
            continue
        
        result, error = main.run("<STDIN>", text, debug=Debug)
        if error:
            print(error.as_string())
        elif result:
            if len(result)==1:
                print(result[0])
            else:
                print(result)
