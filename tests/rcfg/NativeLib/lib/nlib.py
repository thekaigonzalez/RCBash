# NLIB - NativeLib

NAME='recfg'
TYPE='full-lib'

def recfg_linked(args):
    try:
        import RCScript.RCReConfig
        return True
    except Exception:
        return False

def recfg_statstring(args):
    from RCScript.RCReConfig import rcfg_rstatstring
    
    rcfg_rstatstring(args[0])

rcfg_registers = {
    'linked': recfg_linked,
    'statstring': recfg_statstring
}