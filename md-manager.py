#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import os
import shelve
from lib import input_prefill

class MDManager(cmd.Cmd, object):

  # Colorize
  purple='\033[95m'
  gray='\033[1;30m'
  nc='\033[0m'

  dbCache = []
  dbPath = './db/'
  database = None
  dbData = None
  prompt = '''{gray}Moondocks Manager: {dbp}{purple}{db}{nc}
❯❯ '''.format(
    purple = purple,
    gray = gray,
    nc = nc,
    db = database,
    dbp = dbPath
  )

  def __init__(self):
    mdm = MDManager
    cmd.Cmd.__init__(self)
    self.ruler = '-'
    self.intro = '''

    Welcome to the MoonDocks Database Manager (MDdb)

    MDdb Commands:
    - {purple}open{nc}:   Opens a database
    - {purple}close{nc}:  Closes the current database
    - {purple}list{nc}:   Lists available databases
    - {purple}create{nc}: Creates a new database
    - {purple}find{nc}:   Display all documents
    - {purple}insert{nc}: Inserts «key» «value» into database
    - {purple}help{nc}:   Display help

    *Note: Use tab to autocomplete commands.

    '''.format(purple=mdm.purple, nc=mdm.nc)

  ## Database commands

  def do_open(self, args):
    '''Open an existing database'''
    # TODO: add db autocompletion
    if args and '.db' not in args: args = args + '.db'
    MDManager.opendb(args)

  def do_close(self, args):
    '''Close an open database'''
    md = MDManager
    if args:
      print('Too many arguments.')
      return
    md.closedb()

  def do_list(self, args):
    '''List databases'''
    MDManager.listdb()

  def do_find(self, args):
    '''Display all documents'''
    md = MDManager
    if md.dbSimpleStatus(): return
    elif not args:
      db_data_key = list(md.dbData.keys())
      db_data_val = list(md.dbData.values())
      for i in range(len(db_data_key)):
        print('')
        print(db_data_key[i], '=', db_data_val[i])
    else:
      print('Unknown command: %s' % (args))

  def do_insert(self, args):
    '''Insert data into the database'''
    md = MDManager
    insert_usage = 'Usage: insert «key» [«key», «value»]'
    args = args.split(' ')

    if md.dbSimpleStatus(): return
    elif not args or len(args) <= 2:
      print(insert_usage)
      return
    else:
      insert_key = args[0]
      del args[0]
      i = iter(args)
      new_dict = dict(zip(i, i))
      print(insert_key, ':', new_dict)
      askInsert = input('\nInsert? [y/n/edit]: ').lower()
      if askInsert == 'y':
        pass
      elif askInsert in ['e', 'edit']:
        edit_string = insert_key + ' ' + ' '.join(args)
        input_prefill('edit: ', edit_string)
        pass
      else:
        print('Aborting insert...')
        return

      # shelve insert data
      md.dbData[insert_key] = new_dict

  ## Core commands

  def dbSimpleStatus():
    '''Simplified dbStatus()'''
    self = MDManager
    if self.database is None and self.dbData is None:
      print('No database open.')
      self.opendb('')
      return True
    else:
      return False

  def dbStatus(db):
    '''Check if there is an open database'''
    self = MDManager
    if self.database is not None:
      print('The database {purple}{db}{nc} is open.'.format(
        purple = self.purple,
        db = self.database,
        nc = self.nc
      ))
      return True
    else:
      return False

  def updatedbCache():
    '''Update the list of available db'''
    self = MDManager
    self.dbCache = []
    for dirname, dirnames, filenames in os.walk(MDManager.dbPath):
      for filename in filenames:
        MDManager.dbCache.append(filename)

  def closedb():
    '''Close an open database'''
    self = MDManager

    if self.database is None:
      return
    else:
      askClose = input('\nWould you like to close it now? [y/n]: ').lower()
      if askClose == 'y':
        print('closing db...')
      else:
        return False

      self.database = None
      self.dbData = None
      # shelve close db
      if self.dbData is not None: self.dbData.close()
      return True

  def opendb(db):
    '''Open a database'''
    self = MDManager

    # Check if there is an open db
    if db == self.database: return
    if self.dbStatus(db):
      if self.closedb(): pass
      else: return
    # Scrub data
    if not db:
      db = input('\nWhich database would you like to open?: ')
      if db == 'list':
        self.listdb()
        self.opendb('')
        return
      elif not db: return
    # Check for prexisting db
    if '.db' not in db: db = db + '.db'
    if db not in self.dbCache:
      print('The database {purple}{db}{nc} doesn\'t exist.'.format(
        purple = self.purple,
        db = db,
        nc = self.nc
      ))
      askCreate = input('\nWould you like to create it now? [y/n]: ').lower()
      if askCreate == 'y':
        print('creating db...')
      else:
        return

    # Set current db
    self.database = db
    print('Opening database {purple}{db}{nc}'.format(
      purple = self.purple,
      db = self.dbPath + db,
      nc = self.nc
    ))

    # shelve open db
    self.dbData = shelve.open(self.dbPath + db, writeback=True)
    print(self.dbData)

  def listdb():
    '''List db'''
    self = MDManager
    db_index = 0
    for dirname, dirnames, filenames in os.walk(self.dbPath):
      print('└── ' + self.dbPath)
      for filename in filenames:
        if '.db' not in filename:
          print('   └── ' + os.path.join(filename))
        else:
          print('   └── '
                + '\033[95m'
                + os.path.join(filename)
                + '\033[0m'
                )
          db_index += 1
      print('''
Available database(s): {0}{1}{2} '''.format('\033[95m', db_index, '\033[0m'))

  def do_exit(self, args):
    '''Exit MoonDocks db Manager'''
    md = MDManager
    if args:
      print('Too many arguments.')
      return
    md.closedb()
    return -1

  def do_EOF(self, args):
    '''Exit on system EOF character'''
    return self.do_exit(args)

  def do_shell(self, args):
    '''Pass command to the system shell when the line begins with `!`'''
    os.system(args)

  def do_help(self, args):
    '''Get help for commands
        `help` or `?` with no arguments prints a list of commands
        `help «command»` or `? «command»` gives help on «command»
    '''
    cmd.Cmd.do_help(self, args)

  #################################################
  # Override Cmd object methods
  #################################################

  def precmd(self, line):
    """Pre command processing"""
    MDManager.updatedbCache()
    return line

  def postcmd(self, stop, line):
    '''Post command processing'''
    md = MDManager
    print('') # adds an empty space
    md.prompt = '''{gray}Moondocks Manager: {dbp}{purple}{db}{nc}
❯❯ '''.format(
      purple = md.purple,
      gray = md.gray,
      nc = md.nc,
      db = md.database,
      dbp = md.dbPath
    )

    return stop

  def preloop(self):
    '''Initialization before prompting user for commands.'''
    cmd.Cmd.preloop(self)
    self._hist    = []
    self._locals  = {}
    self._globals = {}

  def postloop(self):
    '''Do any necessary cleanup.'''
    cmd.Cmd.postloop(self)
    os.system('clear')
    print('Closing MoonDocks db Manager...')


if __name__ == '__main__':
  os.system('clear')
  mdmanager = MDManager()
  mdmanager.cmdloop()
