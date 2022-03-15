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

import os


TYPE='full-lib'
NAME='os'

def os_system(args):
    os.system(args[0])

def os_mkdir(args):
    os.mkdir(args[0])

def os_remove(args):
    os.remove(args[0])

def os_rename(args):
    os.rename(args[0], args[1])

rcfg_registers = {
    'system': os_system,
    'remove': os_remove,
    'mkdir': os_remove,
    'rename': os_rename
}