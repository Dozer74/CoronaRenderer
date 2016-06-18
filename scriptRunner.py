import os
import maxconnect

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'main.py')
cmd = r'python.ExecuteFile @"%s";' % filename
maxconnect.pycharm.run(cmd)