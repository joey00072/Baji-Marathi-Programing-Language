import main
import sys

Debug=False

try:
    if len(sys.argv)>1:
        main.run_from_file(sys.argv[1])
    else:
        while True:
            text = input("बाजी >")
            text = text.strip()
            if len(text)==0:
                continue
            
            result, error = main.run("<मुख्य>", text, debug=Debug)
            if error:
                print(error.as_string())
            elif result:
                if len(result)==1:
                    print(result[0])
                else:
                    print(result)
except KeyboardInterrupt as e:
    print("\n--------------------")
    print("कीबोर्डद्वारे प्रोग्राम थांबविला")
    print("^^^^^^^^^^^^^^^^^^^^")
except BaseException as e:
    print("\n--------------------")
    print("प्रोग्राम चालू असताना त्रुटी आली")
    print("^^^^^^^^^^^^^^^^^^^^")
