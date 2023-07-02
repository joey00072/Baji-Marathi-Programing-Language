# **बाजी (Baji)- Marathi Programing Language**
<p align="center"><a href="kalaam.io" target="_blank" rel="noopener noreferrer"><img width="300" src="./logo.svg" alt="Kalaam logo"></a></p>

बाजी (baji) high-level,dynamically typed, interpreted first Marathi programing language.

## Quick Start
### Hello World
```
दाखवा("नमस्कार विश्व")
```
### Fibonacci Series 
```
कार्य फिबोनॅकी(क)
	जर क<2 तर
		परत 1
	नाहीतर
		परत फिबोनॅकी(क-1) + फिबोनॅकी(क-2)
	शेवट
शेवट



वारंवार क=0 ते 24 तर
    दाखवा(क)
    दाखवा(" ")
	दाखवा(फिबोनॅकी(क))
	दाखवा("\n")
शेवट


दाखवा("\n")
```
Save file with `.baji` extension. 
<br>
RUN
```
baji example.baji
```
## Docs
refer [DOCS.md](./DOCS.md)

## Installation
1. Download binary from Here
    * [RELEASE](https://github.com/joey00072/Marathi-Programing-Language/releases/tag/1.0.1)

    * Windows baji.zip 

    * Linux   baji.tar

    * Mac Comming Soon...
2. 
    **Winodows**<br/>
    Unzip  baji.zip move `baji.exe` to suitable folder path 
    ```
    C:/baji/baji.exe -> recommanded
    ```
    Then set environment variables  [guide](https://support.microsoft.com/en-us/topic/how-to-manage-environment-variables-in-windows-xp-5bf6725b-655e-151c-0b55-9a8c9c7f747d)

3. **Linux/Mac**
    Download baji.tar 
    then run this command
    ```
    tar -xvf baji.tar && sudo mv .baji /bin/ && echo 'export PATH="$PATH:/bin/.baji/"' >> ~/.bashrc && source ~/.bashrc
    ```
    note : you need password to run this command also
    change bashrc to zshrc if you are using zsh shell
4. Run File
    ```
    baji example.baji
    ```

## Build
**Run With Python**
```
python3 shell.py example.baji
```
Build executable

Use [pyinstaller](https://github.com/pyinstaller/pyinstaller) to genrate executable

```
    python3 -m pyinstller shell.py -n baji
```
<br/><br/>


## Todo List

- [x] Refactor
- [ ] print function with multiple args
- [ ] Class Object 
- [ ] Replace block Structure with {}
- [ ] Web/Js Version
- [ ] syntax highlighting 

## Reporting Bugs
Create issue on github or
you can also content me on 00shxf@gmail.com


## Contributions
Any contribution is welcome, drop me a line or file a pull request.<br/>

## Licenses
Refer [LICENSE](./LICENSE)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R6R8KQTZ5)
