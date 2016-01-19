#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Colorize(object):
  def __init__(self):
    super(Colorize, self).__init__()
    self.red = '\033[31m'
    self.green = '\033[32m'
    self.purple='\033[95m'
    self.gray='\033[1;30m'
    self.nc = '\033[0m'
