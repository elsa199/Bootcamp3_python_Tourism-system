import sys

from packages.common.clear import clear_console

def __inputDeco(inpFunc):
    def newFunc(prompt:str = "Please enter your input: ", reprompr:str = "Please enter a valid input: ", **kwarg: dict):
        '''key = a list of appling keys to output : list
        convert = a data type to convert output into it.'''
        try:
            out = inpFunc(prompt)  # First time taking input
        except KeyboardInterrupt:
            clear_console(0)
            sys.exit(0)
        check = False # Assume additional keys are false (pass the while) and check them later

        # Converting output if said so:
        if kwarg.get('convert'):
            try:
                out = kwarg.get('convert')(out)
            except:
                check = True
                

        while not bool(out) or check:
            try:
                out = inpFunc(reprompr)  # First time taking input
                check = False
            except KeyboardInterrupt:
                clear_console(0)
                sys.exit(0)
            if kwarg.get('convert'):
                try:
                    out = kwarg.get('convert')(out)
                    check = False
                except:
                    check = True

        # Checking addition keys if said so:
        # If there is additional keys check that input passes them (return true turn to false)
        if kwarg.get('key'):
            if callable(kwarg.get('key')): kwarg['key'] = [kwarg.get('key')]
            for key in kwarg.get('key'):
                try:
                    check |= not key(out)
                    if check:
                        break
                except:
                    print("Please use inp function correctly (use convert for numeric data).")
                    raise Exception("Error in using inp function.")
        while not bool(out) or check:
            try:
                out = inpFunc(reprompr)  # First time taking input
            except KeyboardInterrupt:
                clear_console(0)
                sys.exit(0)
            if kwarg.get('convert'):
                try:
                    out = kwarg.get('convert')(out)
                    check = False
                except:
                    check = True

            check = False
            if kwarg.get('key'):
                if callable(kwarg.get('key')): kwarg['key'] = [kwarg.get('key')]
                for key in kwarg.get('key'):
                    try: 
                        check |= not key(out)
                        if check:
                            break
                    except IndexError or TypeError:
                        check = True
                        break
                    except:
                        print("Please use inp function correctly (use convert for numeric data).")
                        raise Exception("Error in using inp function.")

        return out

    return newFunc

inp = __inputDeco(input)

def key_try_except(el, cb):
    try:
        cb(el)
        return True
    except:
        return False
