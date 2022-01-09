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

# This plugin adds support for QBasic-based RC files.
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

import pathlib

def pluginInit(env):
    if (env.get("use-qbasic-support") == "true"):
        # print("QBasic: loading file")
        if pathlib.Path("rc.qbas").exists():
            with open("rc.qbas", "r") as f:
                for line in f.readlines():
                    QB_Vrun(line)
        else:
            print("QBasic: rc.qbas not found.")