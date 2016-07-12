#!/usr/bin/python
import os
import shlex
import sys
from constants import *
from builtins.cd import *
from builtins.exit import *

built_in_cmds = {}

def register_command(name, func):
  built_in_cmds[name] = func

def loop():
  status = STATUS_RUN

  while status == STATUS_RUN:
    # Display command prompt
    sys.stdout.write('> ')
    sys.stdout.flush()

    # Read in command line
    cmd = sys.stdin.readline()

    # Tokenize the command line input
    cmd_tokens = tokenize(cmd)

    # Execute commands and retrieve the new status
    status = execute(cmd_tokens)

def tokenize(cmd):
  # Splits text using shell-like syntax
  return shlex.split(cmd)

def execute(tokens):
  cmd_name = tokens[0]
  cmd_args = tokens[1:]

  if cmd_name in built_in_cmds:
    return built_in_cmds[cmd_name](cmd_args)

  # Fork a child shell process
  # If current process is a child, 'pid' is 0
  # else current process is a parent, 'pid' is process id of its child process
  pid = os.fork()

  if pid == 0:
    # Child process
    os.execvp(tokens[0], tokens)
  elif pid > 0:
    # Parent process
    while True:
      wpid, status = os.waitpid(pid, 0)
      if os.WIFEXITED(status) or os.WIFSIGNALED(status):
        break
  #
  return STATUS_RUN

def init():
  register_command('cd', cd)
  register_command('exit', exit)

def main():
  loop()

if __name__ == '__main__':
  init()
  main()
