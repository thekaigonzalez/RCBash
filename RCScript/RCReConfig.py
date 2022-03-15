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

true = True
false = False

def std_println(args):
    for i in args:
        sys.stdout.write(str(i) + " ")
    print()

def std_assert(args):
    if len(args) == 0: pass # undefined behaviour
    if (args[0] == True): 
        pass
    else:
        print("error: Assert failed!\nwhat(): " + str(args[0]) + " != 1")
        exit(-1)

def std_assertcmp(args):
    if len(args) != 2: pass # undefined behaviour
    if (args[0] == args[1]):
        pass
    else:
        print("error: Assert failed!\nwhat(): " + str(args[0]) + " != " + str(args[1]))
        exit(-1)

def std_chunkit(args):
    if len(args) != 1: pass
    args[0](args[1:])

def std_add(args):
    # if len(args) != 2: pass
    return args[0] + args[1]
builtins = {
    "std": {
        "println": std_println,
        "VERSION": '0.1',
        "assert": std_assert,
        "assertcmp": std_assertcmp,
        "chunkit": std_chunkit,
        "add": std_add
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

def __exec_rcfg(chu):
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
            if char == "(" and state == 0:
                if vb.strip() == "return":
                    flag = "RETURN"

                    # cfunc = "return"
                else:
                    cfunc = __rcfg_absd(vb.strip())

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
                        args[idx] = __exec_rcfg(i.strip())
                        idx += 1
                
                if flag == "RETURN":
                    return args[0]
                else:
                    
                    cfunc(args)
                
                
                vb = ""

            elif char == ';' or char == '\n' and state == 5 and state != 81:
                if state == 81:
                    builtins[name] = __exec_rcfg(value.strip());
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
                    builtins[name] = __exec_rcfg(value.strip());
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