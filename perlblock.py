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

# modified version of perlblock written for Rc

STRING_QUOTE = 1999

STRING_INTERP = 1111

STRING_VAL = 1232

COLLECTING =7777

def interp_string(stri):
    string_state = 0
    get = ""
    buffer = ""
    for i in range(len(stri)):
        if stri[i] == '"' and string_state == 0:
            string_state = STRING_QUOTE
        elif stri[i] == "'" and string_state == 0:
            string_state = STRING_INTERP
        elif stri[i] == '`' and string_state == 0 and string_state != COLLECTING:
            string_state = STRING_VAL
        elif stri[i] == '"' and string_state == STRING_QUOTE:
            break
        elif stri[i] == '`' and string_state == STRING_VAL:
            break
        elif stri[i] == '\'' and string_state == STRING_INTERP:
            break
        elif stri[i] == '$' and string_state == STRING_VAL:
            string_state = COLLECTING
        elif string_state == COLLECTING and stri[i] == ' ':
            # print(get)
            get = str(eval(get))
            # print(get)
            buffer += str(get)
            get = ""
            string_state = STRING_VAL
            buffer += stri[i]
        elif string_state == COLLECTING and stri[i] == '`':
            # space = ""

            # for _ in range(i):
            #     space += " "
            # print("error: unexpected token '`' at position " + str(i) + "\n1 | " + stri + "\n" + space + "^")
            continue
        elif string_state == COLLECTING and stri[i] != '`':
            get += stri[i]

        else:
            buffer += stri[i]
    if len(get) > 0:
        # print(get)
        # print(buffer)
        get = str(eval(get))
        # print(get)
        buffer += str(get)
    print(buffer)    
    

# awesome = "Very Cool!"

# interp_string("`String interpolation is $awesome`")
# interp_string("'String interpolation is $awesome'")