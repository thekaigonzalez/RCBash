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

# RCBash's attempt at a markdown parser (For documenting purposes)

import os
import pathlib


def RCMD_FROMMD(markdown):
    """ 
    
    MARKDOWN TO HTML 
    
    After hours, it's finally done

    # Lexer spec:

    `# <text>`
    `## <text>`
    `### <text>` **HEADERS**

    `%<text>%` **EVAL-TEXT**
    
    `- <text> -` **COMMENT**

    `\\n<participants>` **NEWLINE**

    This system is very fragile, it's recommended to not mess with this, as it can
    break very easily!
    """

    """ DECL """

    buffer = ""
    state = 0
    htm=""
    ind = 0

    """LEX"""

    for ch in markdown:
        # print(state)
        if (ch == "#" and state == 0 and markdown[ind+1] != "#"):
            state = 1 # collecting
            buffer = ""
        elif (ch == "#" and state == 0 and markdown[ind+1] == '#' and markdown[ind+2]!="#"):
            state = 2
            buffer = ""
        elif (ch == "#" and state == 0 and markdown[ind+1] == '#' and markdown[ind+2] == '#'):
            state = 3
            buffer = ""

        elif ch == "-" and state == 0:
            state = 12938213
            buffer = ""
        elif ch == "-" and state == 12938213:
            state = 0
            buffer = ""
            
        
        elif (ch == "\n"):
            if (state == 1):
                
                htm+='<h1>' + buffer.strip() + "</h1>\n"
                buffer = ""
                state = 0
            elif (state == 2):
                htm+='<h2>' + buffer.strip() + "</h2>\n"
                buffer = ""
                state = 0
            elif (state == 3):
                htm+='<h3>' + buffer.strip() + "</h3>\n"
                buffer = ""
                state = 0
            elif(state==0):
                if buffer.strip() != '':
                    htm+="<p>" + buffer + "</p>\n"
                buffer = ""
            
            
        elif (ch == "*" and state == 0):
            buffer += "<b>"
            state = 200
        elif ch == "*" and state == 200:
            buffer += "</b>"
            state = 0
        elif ch == "%" and state == 0:
            if (state == 1):
                
                htm+='<h1>' + buffer.strip() + "</h1>"
                buffer = ""
                state = 0
            elif (state == 2):
                htm+='<h2>' + buffer.strip() + "</h2>"
                buffer = ""
                state = 0
            elif (state == 3):
                htm+='<h3>' + buffer.strip() + "</h3>"
                buffer = ""
                state = 0
            elif(state==0):
                if buffer.strip() != '':
                    htm+="<p>" + buffer + "</p>"
                buffer = ""
            htm += "<p>"
            state = 69
            buffer = ""
        elif ch == "%" and state == 69:
            htm += str(eval(buffer)) + "</p>\n"
            state = 0
            buffer = ""
        else: 
            
            if ch == "#":
                continue
            elif state == 12938213:
                if ch == '-' and state == 12938213:
                    state = 0
            else:
                
                buffer += ch
            
        ind += 1
    if len(buffer) != 0 and state == 0:
        if buffer.strip() != '':
                    if ch!='':
                        htm+="<p>" + buffer + "</p>\n"
                        buffer = ""
    if len(buffer) != 0:
        if (state == 1):
                htm+='<h1>' + buffer.strip() + "</h1>\n"
                buffer = ""
                state = 0
        elif (state == 2):
                htm+='<h2>' + buffer.strip() + "</h2>\n"
                buffer = ""
                state = 0
        elif (state == 3):
                htm+='<h3>' + buffer.strip() + "</h3>\n"
                buffer = ""
                state = 0
        elif (state == 12938213): raise Exception("Unfinished comment\nWhere: " + buffer + "\n      ^^")
    return htm

def compileRCDocFile(filename, sheet=None):
    file = open(filename, "r")
    if sheet != None:
        out = open(filename + ".html", "w")
        out.write("<link rel=\"stylesheet\" href=\"" + sheet + "\">\n")
        out.close()
    if (pathlib.Path(filename + ".html").exists()):
        os.remove(filename + ".html")
    out = open(filename + ".html", "a")
    out.write(RCMD_FROMMD(file.read()))
    out.close()
   
#compileRCDocFile("test.rcdoc")