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

# A programming language for macros and information.

import os


class ErrorTypes:
    RMAC_NO_DEF = 0

def variablize(string: str, vars: dict):
    """
    Takes a string and checks if it's formatted like: "$[NAME]" and uses @vars to replace it.
    """
    s = 0
    i2 = ""
    for i in string:
        if i == "$" and s == 0:
            s = 1;
        else:
            i2 += i
    if (vars.get(i2) != None):
        return vars[i2];
    else:
        return i2

def rmacro(parf: str, variables: dict) -> dict:
    """
    RMacro - New way to write macros.

    Supports:
    
    * Variables
    * Basic GNU-like macro syntax
    * Comments

    Basic code:

    ```
    mac(arg)

    mac(arg, arg2)
    
    mac($VARIABLE)
    
    \# comment
    ```
    """
    parse = ""
    _def = None
    knowledge = 0

    macros = {}

    current_macro_name = None

    for i in parf:
        if i == "(" and knowledge == 0:
            current_macro_name = parse.strip()
            parse = ""
            # clear it
            knowledge = 1
        elif i == "," and knowledge == 1:
            _def = []
            variablize(parse, variables)
            _def.append(parse)

            parse = ""
            knowledge = 2
        elif i == ")" and knowledge == 1 and type(_def) != list:
            _def = parse
            knowledge = 2
        elif i == ")" and type(_def) == list:
            _def.append(parse.strip())
        elif i == "\n" and knowledge == 2:
            if (_def is not None):
                macros[current_macro_name] = _def
                _def = None
                current_macro_name = None
                parse = ""
                knowledge = 0
            else:
                print("rmacro: no definitions for function `{}'".format(
                    current_macro_name))
        elif i == "\n" and knowledge == -100:
            knowledge = 0;
            parse = ""
            current_macro_name = None
            _def = None

        elif i == "#":
            knowledge = -100
        else:
            parse += i
            parse = variablize(parse, variables)
    return macros




