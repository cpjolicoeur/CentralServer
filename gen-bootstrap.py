#!/usr/bin/env python
#
# Set up a virtualenv environment with the prerequisites for csrv.
# To use this, install virtualenv, run this script, and then run the generated
# csrv-bootstrap.py to create an environment with the needed dependencies.
#
import virtualenv

script = virtualenv.create_bootstrap_script('''

import os
import subprocess

requires = ['tornado', 'redis']

def after_install(options, home_dir):
  etc = os.path.join(home_dir, 'etc')
  if not os.path.exists(etc):
    os.makedirs(etc)

  for r in requires:
    subprocess.call([os.path.join(home_dir, 'bin', 'pip'), 'install', r])

''')
with open('csrv-bootstrap.py', 'w') as script_file:
  script_file.write(script)
