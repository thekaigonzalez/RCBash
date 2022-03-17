# ReConfig Objects

ReConfiguration is not an object oriented language, but can be as such:

take this code for example...

```

f = std:file("test.txt", "w");
f:write("hello!");
f:close();

```

How is this able to be an object? without an object oriented programming feature?

std:file documentation is such:

> std:file(name, mode) - ReConfiguration Standard Library:
> The file object,
> A wrapper around the open() function in Python.

The file **object**

In this tutorial, I will teach you how to create a class in ReConfig.

First, initialize a `remake` project.

After, create a directory in the project folder called "lib" and put "mylib.py" inside of it.

Your directory tree should look like this:

```
project/
    lib/    
        mylib.py
    source/
        main.recfg
    README.md
    remake.toml
```

After, open "mylib.py".

When you write a lib, ReConfig looks for a variable called `rcfg_registers`, so if you want any kind of library, you need to use `rcfg_registers` name.

Write this in mylib.py:

```py

# mylib

# NAME and TYPE are required for classes.
NAME='mylib'
TYPE='full-lib'

# create a way to return the functions into a variable
def myobject_new(args):
    """ Initialize object """

    # method
    def myobject_print(args):
        print(args[0]) # first argument
    # return the class
    return {
        'print': myobject_print
    }

# register lib
rcfg_registers = {
    'object': myobject_new
}

```

Then, in source/main.recfg, write

```recfg
std:lib("mylib")

obj = mylib:object();

obj:print("Hello!");
```

If everything worked right, your output should be:

```
Hello!
```

If so, you just learned about ReConfig inheritence!