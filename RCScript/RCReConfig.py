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

"""

RC Reconfig

ReConfiguration Reborn

Lexer:

<text> = <value> (store as recfg value)

<text>(<args>)

<statement>; <--- Semicolon

"""
import getpass
from importlib.machinery import SourceFileLoader
from platform import platform
import platform
import psutil
import os
import sys
import types
import pathlib
from typing import List

true = True
false = False
RCFGPATH=[]

""" STD LIBRARY """
def __stdprintln(args):
    """
    std:println(...) - ReConfiguration Standard Library

    Appends every argument to stdout with a space.
    """
    for m in args:
        sys.stdout.write(str(m))
    print()

def __stdassert(args):
    """
    std:assert(stat) - ReConfiguration Standard Library

    Basic assert using builtin types

    Takes only 1 argument: bool

    Will exit if "stat" is not true. "stat" can be a ReConfiguration Function however; 
    If you need specific variables then check std:assertcmp

    
    """
    if len(args) == 0: pass # undefined behaviour
    if (args[0] == True): 
        pass
    else:
        print("error: Assert failed!\nwhat(): " + str(args[0]) + " != 1")
        exit(-1)

def __stdassertcmp(args):
    """
    std:assertcmp(one, two) - ReConfiguration Standard Library

    std:assert() but instead of comparing a single return value, the comparison is done at runtime.

    """
    if len(args) != 2: pass # undefined behaviour
    if (args[0] == args[1]):
        pass
    else:
        print("error: Assert failed!\nwhat(): " + str(args[0]) + " != " + str(args[1]))
        exit(-1)

def __stdchunkit(args):
    """
    std:chunkit(func, ...) - ReConfiguration Standard Library

    Chunk and run a function programmatically with positional args (...)
    
    """
    if len(args) != 1: pass
    args[0](args[1:])

def __stdadd(args):
    # if len(args) != 2: pass
    return args[0] + args[1]

def __stdstring_sub(args: List[str]):
    """ 
    std:string:sub(str, one, two) - ReConfiguration Standard Library
    
    Get text within two characters (or indices) of a string.
    
    """
    if len(args) != 3: pass # undefined behavior
    return args[0][args[1]:args[2]]



def __stdstring_strip(args):
    """
    std:string:strip(string) - ReConfiguration Standard Library
    
    """
    return args[0].strip()

def __stdinput(args):
    """
    std:input(prompt) - ReConfiguration Standard Library

    Returns input with given prompt.
    """
    return input(args[0])

def __stdloadlib(args):
    """
    std:loadlib(lib) - ReConfiguration Standard Library

    Load a Python module's functions.

    When loading the module, it'll look for rcfg_registers and append those to the current session.

    a typical mod would look like:

    \# mod file

    def myfunc():
        print("hi!")

    rcfg_registers = {
        "func1": myfunc
    }
    
    """
    import importlib
    prev = sys.path
    sys.path = RCFGPATH
    
    try:

        mod = importlib.import_module(args[0])

        if type(mod.rcfg_registers) == dict:
            if mod.TYPE == 'full-lib':
                builtins[mod.NAME] = mod.rcfg_registers
    except Exception as e:
        print("std:lib - Failed to import library `" + args[0] + "'\nError Message: " + str(e))
    sys.path = prev

def __stdaddpath(args):
    """
    std:addpath(pathname) - ReConfiguration Standard Library

    Adds "pathname" to virtual path. Used for std:lib candidate.

    """
    RCFGPATH.append(args[0])
def __stdcmp(args):
    """
    std:cmp(one, two, func, ...) - ReConfiguration Standard Library

    Combines std:chunkit with std:asert

    if one and two are the same, then it will run "func" with any positional arguments (...)
    
    """
    if len(args) != 3: pass

    if args[0] == args[1]:
        args[2](args[3:])

def __stdbool(args):
    """ Compares arg0, and arg1. """
    if args[0] == args[1]: return True
    else: return False

def __stdlength(args):
    """ length arg0 """
    return len(args[0])

def __stdmultiply(args):
    """ arg0 * arg1 """
    return args[0] * args[1]

def __stdmacro(args):
    """
    Bind a function
    """
    strs= args[1]
    def exec(args):
        __exec_rcfg(strs)
    builtins[args[0]] = exec

def __stdfwrite(args, fsile):
    """
    Write to a file.
    """
    fsile.write(args[0])

def __stdfread(args, fsile):
    """
    Read a file's contents
    
    """
    return fsile.read()

def __stdfclose(args, file):
    file.close()

def __stdfexists(args):
    """
    std:exists(path) - ReConfiguration Standard Library 

    check if the path exists (only path)

    No std:file objects allowed currently.
    
    """
    if pathlib.Path(args[0]).exists(): return True
    else: return False

def __stdfile(args):
    """
    std:file(name, mode) - ReConfiguration Standard Library
    
    The file object

    A wrapper around the open() function in Python
    """
    fsile = open(args[0], args[1])

    def loadwrite(args):
        __stdfwrite(args, fsile)
    
    def loadread(args):
        return __stdfread(args, fsile);

    def loadclose(args):
        __stdfclose(args, fsile);
        
    return {
        'write': loadwrite,
        'read': loadread,
        'close': loadclose
    }

def __stdinfo(args):
    """
    std:info() - ReConfiguration Standard Library

    std:info returns a Information object.

    Conatins 

    Information.cpus
    Infomation.username
    Information.libcver
    Information.arch
    Information.uname
    
    """
    return {
        "cpus": os.cpu_count(),
        "username": getpass.getuser(),
        "arch": platform.architecture(),
        "libcver": platform.libc_ver(),
        'uname': platform.system()
    }

def __stdassertnil(args):
    return args[0] == None

def __stdmember(args):
    return args[0][args[1]]

def __stdexit(args):
    exit(args[0])

def __not(args):
    return args[0] == False

def __define(args):
    builtins[args[0]] = args[1]
builtins = {
    "std": {
        "addpath": __stdaddpath,
        "println": __stdprintln,
        "VERSION": '0.7',
        "assert": __stdassert,
        "assertcmp": __stdassertcmp,
        "chunkit": __stdchunkit,
        "add": __stdadd,
        "string": {
            "sub": __stdstring_sub,
            "strip": __stdstring_strip
        },
        "cmp": __stdcmp,
        "lib": __stdloadlib,
        "input": __stdinput,
        "bool": __stdbool,
        "length": __stdlength,
        "multiply": __stdmultiply,
        "macro": __stdmacro,
        "file": __stdfile,
        "info": __stdinfo,
        "exists": __stdfexists,
        "assertnil": __stdassertnil,
        "argv": sys.argv,
        "member": __stdmember,
        "exit": __stdexit
    },
    "not": __not,
    "define": __define

}

def __rcfg_absd(c):
    """
    ## Absolute Depth

    Returns the depth in builtins separated by ':'

    ### How?

    Using infinite recursion,

    as long as there is another table to fit the recursion as in, move, then move.

    Then continue that same process.

    """
    b=""
    state=0
    cs=':'
    depth = builtins
    for char in c:
        if char == cs:
            if type(depth.get(b)) == dict:
                depth = depth[b]
            else:
                return depth[b]
            b = ""
        else:
            b += char

    if len(b) != 0:
        return depth[b]
    return None


def RC_LexerErr(msg):
    print("Error When Lexing/Parsing: " + msg)

def __exec_rcfg(chu: str, rfv=False, debug=False):
    """
    ## Execute RConfig Code

    * Does Lexing, Parsing, and Executing.

    """
    if type(chu) == str:
        """DECL"""
        vb = ""
        state = 0
        db_prevstate = state
        cfunc = ""
        flag = None
        args = [] #tmp arg holder (deleted after)
        name = ""
        value = ""
        prevst = 0
        stch = ""
        STCHF=False
        COLLECTING=False
        chu = chu.strip()
        
        try:
            if type(__rcfg_absd(chu.strip())) is not None:
                return __rcfg_absd(chu.strip())

            
        except:
            pass
        try:
            if type(eval(chu)) == str or type(eval(chu)) == bool or type(eval(chu)) == int or type(eval(chu)) == dict:
                return eval(chu)
        except:
            pass
        for char in chu:
            
            if char == "(" and state == 0 and len(vb.strip())!=0:
                if debug:
                    print("[FUNCTION-CALL] for " + vb.strip())
                try:
                    if vb.strip() == "return":
                        flag = "RETURN"

                        # cfunc = "return"
                    else:
                        cfunc = __rcfg_absd(vb.strip())
                except KeyError:
                    print("error: function/object not found `" + vb.strip() + "'")

                state = 1
                vb = ""
            elif char == '"' and state == 1:
                state = 699699839381892
                vb += char
            elif char == '"' and state == 699699839381892:
                state = 1
                vb += char

            elif char == '(' and state == 1:
                state += 10
                vb += "("

            elif char == '(' and state != 1 and state != 5 and state != 69 and state != 81 and state != 6722 and state != 672 and state != 699699839381892:
                if debug:
                    print("[LEXER] Adding 10 to state because of: " + char)
                state += 10
                vb += "("
            
            elif char == "," and state == 1:
                args.append(vb)
                vb = ""
            elif char == '@' and state == 0:
                if debug:
                    print("[SPECIAL-TOKEN] macro token " + char)
                state = 43
                vb = ""
            elif char == ' ' and state == 43:
                if debug:
                    print("[MACRO] Loading macro functionality for " + vb.strip())
                if vb.strip() == 'if':
                    state =672
                    vb = ""
                else:
                    print("unknown directive macro.")
                    exit(-1)
                vb = ""
            elif char == '{' and state == 672:
                if debug:
                    print('[COMPARE] checking ' + vb.strip())
    
                state = 6722
                COLLECTING=True
                STCHF= __exec_rcfg(vb.strip(), True)
                if debug:
                    print("[COMPARE] tried once, got " + str(__exec_rcfg(vb.strip(), True)))
                vb = ""
            elif char == '}' and state == 6722:
                if debug:
                    print("[TOKEN] found end of block, loading code:\n" + stch.strip())
                state = 0

                if STCHF:
                    __exec_rcfg(stch.strip())
                vb = ""
                STCHF = False
                COLLECTING = False
                args = []
                

            elif char == ")" and state != 1 and state != 5 and state != 69 and state != 81 and state != 6722 and state != 672 and state != 699699839381892:
                if debug:
                    print("[LEXER] removing 10 from state because of " + char)
                state -= 10
                vb += ")"
            
            elif char == ')' and state == 1:
                state = 5

                
                
                
                if (len(vb) != 0 and vb.strip() != ''): args.append(vb)
                
                idx = 0
                for i in args:
                        args[idx] = __exec_rcfg(i.strip(), True)
                        idx += 1
                if debug:
                    print("[FUNCTION] executing function with args - " + str(args))
                try:
                    
                    if rfv == True:

                        return cfunc(args)
                    
                    if flag == "RETURN":
                        return args[0]
                    else:
                        cfunc(args)
                    
                except Exception as e:
                    print("Error when evaluating: Unable to load Function. Refer to above errors (if any)\nOr Refer to this message: " + str(e))

                

                vb = ""
            
            elif char == ';' or char == '\n' and state == 5 and not COLLECTING:
                if debug: print("[STATEMENT] Found newline on state: " + str(state))
                if state == 699699839381892:
                    vb += char
                    
                elif COLLECTING:
                    state = 6722
                    stch += char
                    
                else:
                    if state == 81:
                        builtins[name] = __exec_rcfg(value.strip(), True);
                    value = ""
                    state = 0
                    cfunc = None
                    vb = ""
                    args = []

            elif char == '=' and state == 0:
                state = 81
                name = vb.strip()
                vb = ""

            elif char == '\n' or char == ';' and state == 81 and state != 6722 and not COLLECTING:
                if COLLECTING:
                    state = 6722
                    stch += char
                else:
                    if debug:
                        print("[CHUNK] End of line found, old state: " + str(state) + ", Collection Status: " + str(COLLECTING))
                    if state == 81:
                        builtins[name] = __exec_rcfg(value.strip(), True);
                        
                    state = 0
                    cfunc = None
                    vb = ""
                    args = []
                    value = ""
                    
                    
                    vb = ""
                    state = 0

            elif char == '#' and state == 0:
                state = 69
                vb = ""
            elif char == '\n' and state == 69:
                if debug:
                    print("[COMEMNT] Ended comment")
                state = 0
                vb=""
            else:
                if state == 69: vb = ""
                elif state == 81: value += char
                elif state == 6722: stch += char
                else:
                    vb += char
            if db_prevstate != state and debug:
                char2 = char
                if char2 == '\n': char2 = '\\n'
                print('[STATE-CHANGED] state changed to ' + str(state) + " on `" + char2 + "' from " + str(db_prevstate))
                db_prevstate = state
    
def rcfg_rstatstring(strn, ifd=False):
    __exec_rcfg(strn, debug=ifd)

def rcfg_addmountable(name):
    RCFGPATH.append(name)
