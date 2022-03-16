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
import sys
import types
from typing import List

true = True
false = False

""" STD LIBRARY """
def std_println(args):
    """
    std:println(...) - ReConfiguration Standard Library

    Appends every argument to stdout with a space.
    """
    for i in args:
        sys.stdout.write(str(i) + " ")
    print()

def std_assert(args):
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

def std_assertcmp(args):
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

def std_chunkit(args):
    """
    std:chunkit(func, ...) - ReConfiguration Standard Library

    Chunk and run a function programmatically with positional args (...)
    
    """
    if len(args) != 1: pass
    args[0](args[1:])

def std_add(args):
    # if len(args) != 2: pass
    return args[0] + args[1]

def std_string_sub(args: List[str]):
    """ 
    std:string:sub(str, one, two) - ReConfiguration Standard Library
    
    Get text within two characters (or indices) of a string.
    
    """
    if len(args) != 3: pass # undefined behavior
    return args[0][args[1]:args[2]]



def std_string_strip(args):
    """
    std:string:strip(string) - ReConfiguration Standard Library
    
    """
    return args[0].strip()

def std_input(args):
    """
    std:input(prompt) - ReConfiguration Standard Library

    Returns input with given prompt.
    """
    return input(args[0])

def std_loadlib(args):
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

    try:

        mod = importlib.import_module(args[0])

        if type(mod.rcfg_registers) == dict:
            if mod.TYPE == 'full-lib':
                builtins[mod.NAME] = mod.rcfg_registers
    except Exception as e:
        print("std:lib - Failed to import library `" + args[0] + "'\nError Message: " + str(e))

def std_cmp(args):
    """
    std:cmp(one, two, func, ...) - ReConfiguration Standard Library

    Combines std:chunkit with std:asert

    if one and two are the same, then it will run "func" with any positional arguments (...)
    
    """
    if len(args) != 3: pass

    if args[0] == args[1]:
        args[2](args[3:])

def std_bool(args):
    if args[0] == args[1]: return True
    else: return False

def std_length(args):
    return len(args[0])

def std_multiply(args):
    return args[0] * args[1]

def std_macro(args):
    strs= args[1]
    def exec(args):
        __exec_rcfg(strs)
    builtins[args[0]] = exec

def std_fwrite(args, fsile):
    fsile.write(args[0])

def std_fread(args, fsile):
    return fsile.read()

def std_fclose(args, file):
    file.close()

def std_file(args):
    fsile = open(args[0], args[1])
    def loadwrite(args):
        std_fwrite(args, fsile)
    
    def loadread(args):
        return std_fread(args, fsile);

    def loadclose(args):
        std_fclose(args, fsile);
        
    return {
        'write': loadwrite,
        'read': loadread,
        'close': loadclose
    }


builtins = {
    "std": {
        "println": std_println,
        "VERSION": '0.1',
        "assert": std_assert,
        "assertcmp": std_assertcmp,
        "chunkit": std_chunkit,
        "add": std_add,
        "string": {
            "sub": std_string_sub,
            "strip": std_string_strip
        },
        "cmp": std_cmp,
        "lib": std_loadlib,
        "input": std_input,
        "bool": std_bool,
        "length": std_length,
        "multiply": std_multiply,
        "macro": std_macro,
        "file": std_file
    }

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

def __exec_rcfg(chu, rfv=False):
    """
    ## Execute RConfig Code

    * Does Lexing, Parsing, and Executing.

    """
    if type(chu) == str:
        """DECL"""
        vb = ""
        state = 0
        cfunc = ""
        flag = None
        args = [] #tmp arg holder (deleted after)
        name = ""
        value = ""
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

            elif char == '(' and state == 1:
                state += 10
                vb += "("

            elif char == '(' and state != 1 and state != 5 and state != 69 and state != 81:
                state += 10
                vb += "("
            
            elif char == "," and state == 1:
                args.append(vb)
                vb = ""

            elif char == ")" and state != 1 and state != 5 and state != 69 and state != 81:
                state -= 10
                vb += ")"
            
            elif char == ')' and state == 1:
                state = 5

                
                
                if (len(vb) != 0 and vb.strip() != ''): args.append(vb)
                
                idx = 0
                for i in args:
                        args[idx] = __exec_rcfg(i.strip(), True)
                        idx += 1
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

            elif char == ';' or char == '\n' and state == 5 and state != 81:
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

            elif char == '\n' or char == ';' and state == 81:
                
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
                state = 0
                
                vb=""
            else:
                if state == 69: vb = ""
                elif state == 81: value += char
                else:
                    vb += char
    
def rcfg_rstatstring(strn):
    __exec_rcfg(strn)