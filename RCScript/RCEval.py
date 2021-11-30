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
import platform
import os

def xxd(arg):
    b = ' '.join(format(ord(x), 'b') for x in ' '.join(arg[1]))
    print(b)
def cat(args):
     if args[1] == "--file":
        if args[2] == "--read":

            name = args[3]
            ufile = open(name, 'r+')
            a= ufile.readlines()
            for line in a:
                print(line)
builta = {
    'xxd': xxd,
    'cat': cat,
    "rd": lambda x: print("System Specs:\n " + platform.uname().system + ", {}, {}".format(platform.uname().processor, platform.uname().machine, platform.uname().version) )
}

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
            try:
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
                        if arg[1].find("usr") != -1 or arg[1].find("system") != -1:
                            if uservars.get("secure_warnings") == 'yes' and uservars.get("secure_warnings") != None:
                                print("WARNING: We recommend you back down!\nWe seen that this command: `" + code + "` could\nPOTENTIALLY be running malicious actions.\nYou can turn this warning off using the 'set secure_warnings no` command.\n(secure_warnings)")
                                break
                        os.chdir(arg[1])
                    built = True
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
            except Exception:
                print("build-core: exception")
            if uservars.get(arg[0].strip()) != None:
                eval_rc(uservars[arg[0]])
                break;
            if builta.get(arg[0].strip()) != None:
                try:
                    builta[arg[0]](arg)
                except:
                    print("builtin-core: error")
                break;
            if not built:
                try:
                    return subprocess.call(arg)
                except Exception as e:
                    print("error: rcbash: command not found: " + str(e))
