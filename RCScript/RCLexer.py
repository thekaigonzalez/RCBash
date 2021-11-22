# RCLexer

def dictionary_ofrc(stri):
    state = 0

    stat_dict = {}

    args = []
    
    buffer = ""

    i = 0

    stat_level = 0
    for char in stri:
        
        if (char == '"' and state == 10 and stri[i-1] != '\\'):
            state = 100
        elif char == '"' and state == 100 and stri[i-1] != '\\':
            state = 10
        elif (char == '`' and state == 10 and stri[i-1] != '\\'):
            state = 1010
        elif char == '`' and state == 1010 and stri[i-1] != '\\':
            state = 10
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
    if len(buffer) > 0 and state == 10:
        args.append(buffer)
    if len(args) > 0 and state != 0:
        stat_dict[stat_level] = {}
        stat_dict[stat_level]['args'] = args
    if len(buffer) > 0 and state == 0:
        stat_dict[stat_level] = {}
        stat_dict[stat_level]['args'] = [buffer.strip()]
    # print(args[1])
    # print(stat_dict)

    return stat_dict

