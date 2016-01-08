#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline

def input_prefill(prompt, text):
  """Prefills user input with text"""
  def hook():
    readline.insert_text(text)
    readline.redisplay()
  readline.set_pre_input_hook(hook)
  result = input(prompt)
  readline.set_pre_input_hook()
  return result
