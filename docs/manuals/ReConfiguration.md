<!--
 Copyright 2022 kaigonzalez
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# Reconfiguration Scripting Language: Everything you need to know

## Essentials

### Styling

When writing code, to access a function variable you need to use the builtin keyword, `return`.

```recfg

println = std:println; # WRONG

println = return(std:println); # Right!

```

Essentially you're returning the value of the function, rather than accessing the raw data itself.

This is also used for helper functions such as `std:add` where raw value linking is not promised.

### Semicolons: When to use them and when not

Semicolons (when the state machine is 0) are used as an indicator that the current statement is done,
If you want to end a statement, at the end line, put a semicolon.

```recfg

std:println("Reconfig is so cool!");

```

### End of file

With the end of the file, you NEED to either use:

A newline

A semicolon

This design is ON PURPOSE. These are style rules.

## Libraries

### std

STD is the default library that ReConfig ships with.

## Function Differences

### std:assert(pstat) VS std:assertcmp(s1, s2)

std:assert asserts a single statement. Example:

```

std:assert(1 + 1 == 2)

```
This does not support ReConfig however, therefore; the std:assertcmp was created,
It supports two values, s1: The initial value, s2: The expected value

```

std:assert(return(std:println), return(std:println))

```

## Useful Utility Functions

### std:chunkit(func: Function, args...)

std:chunkit was written to test typing in ReCfg, it executes the `func` object with "args" as the initial args.

```

std:chunkit(std:println, "hello")

```