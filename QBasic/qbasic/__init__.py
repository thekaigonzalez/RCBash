import os
import colorama

# QBasic Compiler

gotos = {
    
}

def QB_Cast(code):
    state = 0
    key = "";
    argv = []
    goto = "";
    buf = ""
    for i in code:
        if i == ' ' and state == 0:
            state = 1
            goto = buf;
            buf = "";
        elif i == ' ' and state == 1:
            state = 2 # forever
            key = buf
            buf = "";
        elif i == ' ' and state == 2:
            argv.append(buf);
            buf = "";
        elif i == '"' and state == 2:
            state = 999
        elif i == '"' and state == 999:
            state = 2
        else:
            buf += i
    if not len(buf.strip()) < 0 and state == 2:
        state = 0;
        argv.append(buf.strip())
    return {
        "keyword": key,
        "goto": goto,
        "args": argv
    }

funcs = {}

def qb_print(argv):
    print(argv[0])

def qb_setColor(argv):
    if argv[0] == "RED":
        print(colorama.Fore.RED, end="")
    if (argv[0] == 'RESET'):
        print(colorama.Fore.RESET, end="")

funcs["print"] = qb_print
funcs["color"] = qb_setColor
# run codes
def QB_Vrun(code): 
    ast = QB_Cast(code)
    gotos[ast["goto"]] = { "key": ast["keyword"], "args": ast["args"]}
    if (ast["keyword"].lower() == 'goto'):
        QB_Vrun(gotos[ast["args"][0]]['key'] + " " + ' '.join(ast["args"]))
    else:
        funcs[ast["keyword"].lower()](ast["args"])
    
# QB_Vrun("10 color RED")
# QB_Vrun("20 PRINT \"hello\"")
# QB_Vrun("30 color RESET")
# QB_Vrun("40 print nope")