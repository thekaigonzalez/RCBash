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

# Localize is a preload addon.

# version is not required, but recommended.
from os import chroot


VERSION='0.0.1'


# this is the first addon which utilizes the Plugin system
# these are sort of sub-threads for RCBash.
# Not RCBScripting, Python scripting.
# You use these like they're a branch for RCBash.
# Contributions safely.
# The 'env' variable is for the user environment. You can check certain settings.
def pluginInit(env):
    print("localize-chroot: version {}".format(VERSION))
    dir = env.get("chroot-dir")
    if (env.get("use-chroot") != None):
        if dir != None:
            chroot(dir)
        else:
            print("chroot-plugin: there's no chroot directory to change?")
        
# called when the plugin exits. Required.
def exitPlugin():
    pass