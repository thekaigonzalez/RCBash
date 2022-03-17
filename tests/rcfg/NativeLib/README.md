# NativeLib

Implements ReConfig into itself.

```
std:lib("nlib")

@if recfg:linked() {
    recfg:statstring("std:println('hello');");
}
```