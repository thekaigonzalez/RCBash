# RCLexer

uservars = {}

def dictionary_ofrc(stri):
    state = 0

    stat_dict = {}

    args = []
    
    buffer = ""

    i = 0
    get = ""
    stat_level = 0
    for char in stri:
        
        if (char == '"' and state == 10 and stri[i-1] != '\\'):
            state = 100
        elif char == '"' and state == 100 and stri[i-1] != '\\':
            state = 10
        elif (char == '`' and state == 10 and stri[i-1] != '\\'):
            state = 1010
        elif stri[i] == '$' and state == 1010:
            state = 999
        elif state == 999 and stri[i] == ' ':
            # print(get)
            if uservars.get(get) != None:
                get = uservars[get]
            get = str(get)
            # print(get)
            buffer += str(get)
            get = ""
            state = 1010
            buffer += stri[i]
        elif state == 999 and stri[i] == '`':
            # space = ""

            # for _ in range(i):
            #     space += " "
            # print("error: unexpected token '`' at position " + str(i) + "\n1 | " + stri + "\n" + space + "^")
            continue
        elif state == 999 and stri[i] != '`':
            get += stri[i]
        elif char == '`' and state == 1010 and stri[i-1] != '\\':
            state = 10
        elif char == '{' and state == 10:
            state = 777
        elif char == '\n' and state == 777:
            print(buffer)
        elif char == ' ' and state == 0:
            if len(buffer) > 0:
                
                args.append(buffer.strip())
                buffer = "";
            state = 10
        elif char == ' ' and state == 10:
            args.append(buffer)
            buffer = ""
        elif char == "#" and state == 0: return "comment"
        elif char == '&' and state == 10:
            if (stri[i+1] == '&'):
                return print("error: lexer: 'bash-like features' are not supported (key '&&')")
            stat_dict[stat_level] = {}
            stat_dict[stat_level]['args'] = args

            # print(stat_dict)
            
            state = 0
            buffer = '';
            args = [];

            # print("finishing")
            stat_level += 1



        else:
            buffer += char
        i += 1
    if len(get) > 0:
        # print("left var")
        # print(get)
        # print(": " + buffer)
        # print(get)
        # print(buffer)
        get = str(eval(get))
        # print(get)
        buffer += str(get)

        args.append(buffer)
    if len(buffer) > 0 and state == 10:
        args.append(buffer)
    if len(args) > 0 and state != 0:
        stat_dict[stat_level] = {}
        stat_dict[stat_level]['args'] = args
    if len(buffer) > 0 and state == 0:
        stat_dict[stat_level] = {}
        stat_dict[stat_level]['args'] = [buffer.strip()]
    # print(stat_dict)
    # print(args[1])
    # print(stat_dict)

    return stat_dict

