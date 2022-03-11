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

# Customized Plugin Commit

In your PluginManage, there's a feature that new-plugins branch adds called the "Advanced Commit" feature.
Essentially it allows you to single install addons.

Example: say you wanted to install a custom addon from another user. You'd download the repository and CD into it.

After, you'd use PluginManage from the local plugin directory using "sudo PluginManage commit -d -s myplugin -l"

sudo: Superuser do
PluginManage: The pluginmanage Software.
commit -d: Commit an advanced operation. '-d' checks and confirms it's what you want to do.
-s myplugin: -s selects a plugin.
-l: use a local directory.

English:
    Run PluginManage as superuser and commit an advanced operation selecting 
    and installing "myplugin" using the local install directory.


[ /home/kaigonzalez/RCBash/TestPlug ] $ sudo PluginManage commit -d -s myplugin -l 
                                                              
Using advanced commit
installing from directory plugins/
Checking for directory plugins and loading plugin myplugin.
Found plugins, single-load myplugin
Found myplugin, adding to Plugins!

This would then load the plugin.

You can see the test Plugin at /TestPlug in GitHub.

