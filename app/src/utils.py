import time
import sys

def print_with_time(msg):
  print('{}: {}'.format(time.ctime(), msg))
  sys.stdout.flush()
