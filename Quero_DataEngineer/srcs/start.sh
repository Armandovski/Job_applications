# ************************************ #
# Created on Sun Dec 20 09:05:53 2020
#
# @author: Armando Alvarez Rolins
#
# @title: start.sh
# ************************************ #

#!/bin/bash

service postgresql start

echo "
                    ##        .
              ## ## ##       ==
           ## ## ## ##      ===
       /""""""""""""""""\___/ ===
  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
       \______ o          __/
         \    \        __/
          \____\______/
          |          |
       __ |  __   __ | _  __   _
      /  \| /  \ /   |/  / _\ |
      \__/| \__/ \__ |\_ \__  |
"

# Start container's shell
bash

# Run container for undetermined time
tail -f /dev/null