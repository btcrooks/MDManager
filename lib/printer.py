#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Printer(object):
  '''Print stuff'''
  def __init__(self):
    super(Printer, self).__init__()
    self.red = '\033[31m'
    self.green = '\033[32m'
    self.purple='\033[95m'
    self.gray='\033[1;30m'
    self.nc = '\033[0m'

  def err(self, msg):
    '''Print an error message'''
    print('{c}Error: {nc}{msg}'.format(
      c = self.red, msg = msg, nc = self.nc))

  def ok(self, msg):
    '''Print an ok pessage'''
    print('{c}{msg}{nc}'.format(
      c = self.green, msg = msg, nc = self.nc))

  def hi(self, *args):
    '''Highlight part of a message'''
    if len(args) == 1:
      print('{c}{msg0}{nc}'.format(
        c = self.purple, msg0 = args[0], nc = self.nc))
    elif len(args) == 2:
      print('{msg0} {c}{msg1}{nc}'.format(
        c = self.purple, msg0 = args[0], nc = self.nc, msg1 = args[1]))
    elif len(args) == 3:
      print('{msg0} {c}{msg1}{nc} {msg2}'.format(
        c = self.purple, msg0 = args[0], nc = self.nc,
        msg1 = args[1], msg2 = args[2]))

printer = Printer()
printer.hi('Woah!', 'more', 'stuff')
printer.err('Woah!!! stop')
