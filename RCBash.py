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

import RCScript.RCEval as evaluate
import readline
import os
import sys
import time
import datetime
import pathlib

def bmain():
    if pathlib.Path("./.rcbrc").exists():
        with open("./.rcbrc") as f:
            m = f.readlines()
            for i in m:
                evaluate.eval_rc(i.strip())
    if evaluate.uservars.get('default') != None:
        evaluate.subprocess.call(evaluate.uservars['default'])
    if not pathlib.Path("./.first_time_login").exists():
        animation = ['/', '-', '\\']

        for i in range(10):
            
            time.sleep(0.1)
            sys.stdout.write("loading .... ")
            sys.stdout.flush()
            sys.stdout.write(animation[i % len(animation)] + "\r")
            sys.stdout.flush()
        print("Welcome to RCBash!\nTo get started, you can use bash instead of the default terminal by\ntyping 'bash' if you have bash installed.")
        print("""
The next step is to Learn Your OS.

This uses all of your tools on your OS and doesn't contain any custom utilities.

It's just a BASH for simplistic users.

You can choose different default shells and more in the .rcbrc file. RCBash Is yours!
""")
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