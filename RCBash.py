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

from typing import List
import RCScript.RCEval as evaluate
import readline
import os
import subprocess
import sys
import time
import datetime
import pathlib
import colorama

def dyn_color(argv: List[str]):
    if len(argv) >= 1:
        try:
            print(eval("colorama.Fore." + argv[1]))
        except Exception as e:
            print("fcolor: issue with coloring fore " + e)


evaluate.add_runtime_bind('fcolor', dyn_color)

def bmain():
    if pathlib.Path("./.rcbrc").exists():
        with open("./.rcbrc") as f:
            m = f.readlines()
            for i in m:
                evaluate.eval_rc(i.strip())
    #localize: implement default rcbrc
    if pathlib.Path(os.path.expanduser("~/.rcbrc")).exists():
        with open(os.path.expanduser("~/.rcbrc")) as f:
            m = f.readlines()
            for i in m:
                evaluate.eval_rc(i.strip())

    if pathlib.Path("/etc/rcb.rc").exists():
        with open("/etc/rcb.rc") as f:
            m = f.readlines()
            for i in m:
                evaluate.eval_rc(i.strip())

    if evaluate.uservars.get('default') != None:
        evaluate.subprocess.call(evaluate.uservars['default'])
    if not pathlib.Path("./.first_time_login").exists():
        
        if (evaluate.uservars.get("show-editor-message") != None):
            if pathlib.Path("/usr/bin/editor").exists():
                if pathlib.Path("Extras/RCBash-Message.txt").exists():
                    subprocess.call(['/usr/bin/editor' , 'Extras/RCBash-Message.txt'])
            else:
                if pathlib.Path("Extras/RCBash-Message.txt").exists():
                    j = open("Extras/RCBash-Message.txt")
                    print("\n".join(j.readlines()))
                    j.close()
        open("./.first_time_login", "w").close()
    while True:
        try:
            inp = input((evaluate.uservars['agent'] if evaluate.uservars['agent'] != None else "agent") + " at " + evaluate.uservars['ps1'] if evaluate.uservars['ps1'] != None else '[ bash ] $')

            evaluate.eval_rc(inp)
        except EOFError:
            print("logout")
            quit(-1)
        except KeyboardInterrupt:
            print("exit")
            quit(-1)

bmain()