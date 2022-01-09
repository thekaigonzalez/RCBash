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

# QBasic Support for RCBash

QBasic is a very minimal BASIC implementation, it's under 100 lines of code, so it was fairly easy to embed.

To use QBasic support, you need to set the "use-qbasic-support" variable to "true".

```bash

# in your .rcbrc !!!
set use-qbasic-support "true"

```

After, restart and it should load a rc.qbas file and load it.

Check https://github.com/thekaigonzalez/QBasic for the language spec.