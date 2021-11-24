# Copyright (C) 2021 Kai D. Gonzalez
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import RCScript.RCLexer as lexer
import subprocess
import os

uservars = lexer.uservars

def eval_rc(code):
    ast = lexer.dictionary_ofrc(code)
    # print(ast)


    for item in ast:
        # print("iterate")
        if type(item) == str: break;
        if (ast[item] != None):
            
            

            built = False
            arg = ast[item]['args']
        
            if (arg[0] == 'exit'):
                quit(-1)
                built = True
            elif (arg[0] == 'echo'):
                if (len(arg) > 1):
                    print(str(arg[1]))
                built = True
            elif arg[0] == 'set':
                if (len(arg) > 2):
                    uservars[arg[1]] = arg[2]
                built = True
            elif arg[0] == 'cd':
                if (len(arg) > 1):
                    os.chdir(arg[1])
            elif arg[0] == 'cmpare':
                if (len(arg) >= 4):
                    print("good " + arg[1])
                    if uservars.get(arg[1]) != None:
                        print("good")
                        if uservars[arg[1]] == arg[2]:
                            # print("done")
                            eval_rc(arg[3])
            elif arg[0] == 'pwd':
                
                built = True

                return os.getcwd()
            if uservars.get(arg[0].strip()) != None:
                eval_rc(uservars[arg[0]])
                break;
            if not built:
                try:
                    return subprocess.call(arg)
                except Exception as e:
                    print("error: rcbash: command not found: " + str(e))
