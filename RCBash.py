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

from math import e
import shutil
from typing import List
import RCScript.RCEval as evaluate
import readline
import os
import importlib
import RCScript.RCDoc as doc
import subprocess
import argparse
import sys
import time
import datetime
# 
import pathlib
import colorama

HM=str(pathlib.Path().home())

def dyn_color(argv: List[str]):
    if len(argv) >= 1:
        try:
            print(eval("colorama.Fore." + argv[1]))
        except Exception as e:
            print("fcolor: issue with coloring fore " + e)

def dyn_style(argv: List[str]):
    if len(argv) >= 1:
        try:
            print(eval("colorama.Style." + argv[1]))
        except Exception as e:
            print("fcolor: issue with coloring fore " + e)


def time(argv: List[str]):
    print(str(datetime.datetime.now()))

def clean(argv: List[str]):
    print("WARNING: Cleaning the cache may lead to certain issues out of my control. Use wisely!")
    shutil.rmtree("cache")
    #shutil.rmtree("/etc/rcbash/Plugins")
    os.mkdir("cache")

evaluate.add_runtime_bind("time", time)
evaluate.add_runtime_bind("clean", clean)
evaluate.add_runtime_bind('fcolor', dyn_color)
evaluate.add_runtime_bind('style', dyn_style)


evaluate.uservars['HOME'] = HM

def Interpreter():
    
    #readline-additions
    if pathlib.Path(HM + "/.rcbhistory").exists():
        with open(HM + "/.rcbhistory") as f:
            for i in f.readlines():
                readline.add_history(i.strip())
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
    def check(name, v):
        return evaluate.uservars.get(name) == v

    if check("source-current", "true"):
        print("sourcing current directory")
        import sys
        sys.path.append(os.getcwd())

    if check("g_efficiency", "true"):
        print("benutzend Deutsch tüchtigkeit")
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
    
    if pathlib.Path("/etc/rcbash/Plugins").exists():
        spp = evaluate.uservars.get("show-plugin-preload") 
        cpl = evaluate.uservars.get("confirm-plugin-load")
        b = True
        isdb = evaluate.uservars.get("DEBUG") == "true"
        if spp != None:
            print("Plugins found! Viewing and loading.")

        p = os.listdir("/etc/rcbash/Plugins/")

        if spp != None:
            print("Plugins to load: " + " ".join(p))
        
        if cpl != None:
            print("Would you like to load the plugins now?")

            yn = input("[y/N] > ").strip()

            if yn == "y":
                print("Ok! Running local extensions...")
            else:
                print("Ok! Not running extensions.")
                b = False

        if b == True:
            if spp != None:
                print("Reading extensions...")
            for entry in p:
                if pathlib.Path("/etc/rcbash/Plugins/" + entry + "/" + entry + ".py").exists():
                    if spp != None:
                        print("Loading plugin file {}".format(entry + ".py"))
                    if pathlib.Path("cache").exists():
                        if isdb:
                            print("debug: FOUND CACHE DIR")
                        
                        shutil.copyfile("/etc/rcbash/Plugins/" + entry + "/" + entry + ".py", "cache/" + entry + ".py")
                        try:
                            mod = importlib.import_module("cache." + entry)
                        except Exception as e:
                            print("Error occurred.\n" + str(e))
                        # print(str(mod))
                        try:
                            if mod.VERSION != None:
                                if spp != None:
                                    print("{}, version {}".format(entry, mod.VERSION))
                            try:
                                mod.pluginInit(evaluate.uservars)
                                mod.exitPlugin()
                                
                            except Exception as e:
                                print("Error while loading plugin: " + entry + "\nException: " + str(e))
                        except Exception as e:
                            print("Make sure you have a VERSION variable!")
                            continue
                    else:
                        os.mkdir("cache")
                        print("Error while loading plugins, couldn't find a cache. Reload RCBash and try again.")
        
        

    while True:
        try:
            inp = ""
            if evaluate.uservars.get("use-system-ps1") == "true":
                inp = input("[ " + os.getcwd() + " ] $ ")
            else:
                inp = input((evaluate.uservars.get("agent") if evaluate.uservars.get("agent") != None else "agent") + " at " + evaluate.uservars.get("ps1") if evaluate.uservars.get("ps1") != None else 'fallback $ ')

            evaluate.eval_rc(inp)
            if pathlib.Path(HM + "/.rcbhistory").exists():
                hist = open(HM + "/.rcbhistory", "a")
                hist.write("\n" + inp)
                hist.close()
            else:
                hist = open(HM + "/.rcbhistory", "w")
                hist.write(inp)
                hist.close()
        except EOFError:
            print("logout")
            quit(-1) 
        except KeyboardInterrupt:
            print()
            continue

par = argparse.ArgumentParser("rcbash")

par.add_argument("-doc", default="NONNEEE")
par.add_argument('-style', default="None")
par.add_argument("--FILE", default=None, required=False)
args = par.parse_args()
if (args.FILE != None):
    print("File exec")
    if pathlib.Path(args.FILE).exists():
        with open(os.path.expanduser(args.FILE)) as f:
            m = f.readlines()
            for i in m:
                evaluate.eval_rc(i.strip())
    exit(0)
elif args.doc != "NONNEEE":

    print("Building document")
    if pathlib.Path(args.doc).exists():
        if (args.style != "None"):
            doc.compileRCDocFile(args.doc, args.style)
        else:
            doc.compileRCDocFile(args.doc)

else:
    if __name__ == "__main__":
        Interpreter()