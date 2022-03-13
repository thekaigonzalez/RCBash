# Copyright 2022 kaigonzalez
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NVBasic uses a simpler interpreter,
# instead of compiling the entire statement, it'll compile a statement, with the first word being used as an alias for 
# the statement to compile.

from pathlib import Path

"""

Example:

10 PRINTF "hello"

{goto: "10", "statement": "PRINTF \"hello\""}

"""

builtins ={}
gotos ={}

class NVBasicException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NVBasicLexerException(NVBasicException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NVBasicUnknownParseException(NVBasicException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NVBasicGroupExistanceException(NVBasicException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def __nvb_compile(chunk):
    """ The COMPILER, not TRANSLATOR """

    # this compiles raw statements into raw code

    '''DECLARATIONS'''
    state = 0
    func=""
    zbuffd=""
    args=[]

    '''INITIAL LEXER'''
    if type(chunk)==str:
        for char in chunk:
            zbuffd = zbuffd # clean it
            if (char == ' ' and state == 0): state = 1;func=zbuffd;zbuffd=""
            elif (char == '"' and state == 1): state = 10;zbuffd="";
            elif (char == ' ' and state == 1): 
                if (zbuffd.strip()!=""): args.append(zbuffd);zbuffd=""
            elif (char == '"' and state == 10): state = 1;
            else: zbuffd += char

    zbuffd = zbuffd.strip()

    """ BUFFER CHECKS """
    
    if (len(chunk)!=0 and state==10): 
        raise NVBasicLexerException("Unfinished string (Strings must have TWO `\"')")
    if (len(chunk)!=0 and state == 1): 
        args.append(zbuffd.strip())
    if (len(chunk)!=0 and state == 0): 
        func = zbuffd.strip()
    '''FUNCTION CHECK'''
    #if gotos.get(func)!=None:__nvb_compile(gotos[func]["value"])
    if builtins.get(func)!=None: builtins[func](args);

def __nvb_addfunc(name, data):
    if builtins.get(name) != None:
        raise NVBasicGroupExistanceException("the name with the type you are trying to register already exists. (in __nvb_adfunc there is not allowed to be two same type names.")
    builtins[name] = data


def __nvb_translate(chunk):
    """ The TRANSLATOR, not COMPILER """

    # translates code into statements and gotos

    """DECLARATIONS"""
    zbuffd = ""
    goto=""
    state=0

    """INITIAL LEXER"""

    for char in chunk:
        if char == " " and state == 0:
            state = 1
            goto = zbuffd.strip()
            zbuffd = ""
        else:
            zbuffd+=char
    gotos[goto] = { "value":zbuffd}

def __nvb_build(stat):
    __nvb_translate(stat)
    for dict in gotos:
        __nvb_compile(gotos[dict]['value'])

def __nvb_GOTO(args):
    if (gotos.get(args[0]) != None):
        __nvb_compile(gotos[args[0]]['value'])

def __nvb_PRINT(args):
    if (len(args) >= 1):
        print(args[0])

# low-to-high functions
def nvb_globalfuncs():
    __nvb_addfunc("GOTO", __nvb_GOTO)
    __nvb_addfunc("PRINT", __nvb_PRINT)

def nvbCompile(stat): 
    try:
        return __nvb_compile(stat)
    except NVBasicGroupExistanceException as e:
        print(str(e))
    except NVBasicLexerException as e:
        print(str(e))
    except NVBasicUnknownParseException as e:
        print(str(e))

def nvbBuild(stat): return __nvb_build(stat)

def nvbTranslate(stat): return __nvb_translate(stat)

def nvdAddfunc(n, dat): __nvb_addfunc(n, dat)

def Interpreter():
    #import nvbasic as nvbasic
    import platform
    if (platform.system()=="Linux"):import readline

    nvb_globalfuncs()

    print("Welcome to the NVBasic Interpreter (Requires the NVBasic Lib to be linked!")
    print("Type HELP if you need help with using it.")

    def std_HELP(args):
        print("NVBasic Interpreter is a programming language which aims to be a performant-subset of the QBasic programming language.")
        print("Functions I can see:")
        for fnc in builtins:
            print("- " + fnc)
            print("\tRun " + fnc + " <args>")
        print("Refer to the NVBasic README for help.")

    nvdAddfunc("HELP", std_HELP)

    while True:
        chn = input(">>>")
        nvbBuild(chn)

# RCBash Support

def pluginInit(env):
    if Path("./rcbrc.nvbas").exists():
        chunk = open("./rcbrc.nvbas", "r")
        text = chunk.read()

        for m in text.split("\n"):
            nvbBuild(m)
        
        chunk.close()

def exitPlugin():
    pass # for no exit print.