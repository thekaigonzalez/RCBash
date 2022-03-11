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

# Addon Creation

This episode we'll create an addon called "initialfetch" which will send system specs

like the RD Command.

Initialfetch will call neofetch, similar to how it would be done in the RC file.

Example:

import subprocess

VERSION='0.0.1'

def pluginInit(env):
    subprocess.run(['neofetch'])
    

def exitPlugin():
    pass

This is equivalent to adding

'neofetch'

to your RC File.

This was mainly to show how easy it is in python VS RC. And the flexibility Python gives you.

