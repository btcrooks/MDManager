#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import os
import shelve
from lib import input_prefill

class Colorize(object):
  def __init__(self):
    self.purple='\033[95m'
    self.gray='\033[1;30m'
    self.nc='\033[0m'

class DbUtil(object):

  def __init__(self):
    self.dbCache = []
    self.dbPath = './db/'
    self.database = None
    self.dbData = None

  def sayHello(self):
    print('Hello')
    print(self.dbPath)

  # General
  def add_db_ext(self, data):
    '''Append .db in extension'''
    if '.db' not in data:
      data = data + '.db'
    return data

  # Database
  def open_database(self, db):
    '''Open a database'''

    if not db:
      db = input('\nWhich database would you like to open?: ')
      if db == 'list':
        self.list_databases()
        self.open_database(None)
        return
      elif not db: return

    if db == self.database:
      print('%s is already open' % (self.database))
      return
    if self.databse_is_open():
      if not self.close_database(): return

    db = DbUtil.add_db_ext(db)
    if db not in DbUtil.dbCache:
      print('The database {purple}{db}{nc} doesn\'t exist.'.format(
              purple = self.purple,
              db = db,
              nc = self.nc))
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
           nc = self.nc))

    # shelve open db
    self.dbData = shelve.open(self.dbPath + db, writeback=True)
    print(self.dbData)
  def databse_is_open(self):
    '''Check if there if there is an open database'''
    if self.database is None and self.dbData is None:
      print('No database open.')
      # self.opendb('')
      return True
    else:
      return False

  def close_database(self):
    '''Close an open database'''

    if self.database is None:
      return
    else:
      askClose = input('\nWould you like to close it now? [y/n]: ').lower()
      if askClose == 'y':
        print('closing db...')
        self.database = self.dbData = None
        # shelve close db
        if self.dbData is not None: self.dbData.close()
        return True
      else:
        return False

  def update_db_cache(self):
    '''Update list of available databases'''

    self.dbCache = [] # Clear cache

    for dirname, dirnames, filenames in os.walk(self.dbPath):
      for filename in filenames:
        DbUtil.dbCache.append(filename)

  def list_databases(self):
    '''List databases'''
    db_index = 0
    directory = '└── '
    sub_directory = '   └── '

    for dirname, dirnames, filenames in os.walk(self.dbPath):
      print(directory + self.dbPath)
      for filename in filenames:
        if '.db' in filename:
          print(sub_directory + Colorize.purple
                + os.path.join(filename) + Colorize.nc)
          db_index += 1
        else:
          print(sub_directory + os.path.join(filename))
    print('Available database(s): {0}{1}{2}'.format(
          Colorize.purple, db_index, Colorize.nc))



Colorize = Colorize()
DbUtil = DbUtil()

class DbInterface(cmd.Cmd):

  def do_hello(self, args):
    DbUtil.sayHello()

  prompt = '{gray}Moondocks Manager: {dbp}{purple}{db}{nc}\n❯❯ '.format(
    purple = Colorize.purple,
    gray = Colorize.gray,
    nc = Colorize.nc,
    db = DbUtil.database,
    dbp = DbUtil.dbPath
  )

  def __init__(self):
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

    '''.format(purple=Colorize.purple, nc=Colorize.nc)

  ## Database commands

  def do_open(self, args):
    '''Open an existing database'''
    # TODO: add db autocompletion
    if args and '.db' not in args: args = args + '.db'
    DbInterface.opendb(args)

  def do_close(self, args):
    '''Close an open database'''
    DbUtil.close_database()

  def do_list(self, args):
    '''List databases'''
    DbUtil.list_databases()

  def do_find(self, args):
    '''Display all documents'''
    if DbUtil.databse_is_open(): return
    elif not args:
      db_data_key = list(DbUtil.dbData.keys())
      db_data_val = list(DbUtil.dbData.values())
      for i in range(len(db_data_key)):
        print('')
        print(db_data_key[i], '=', db_data_val[i])
    elif len(args.split(' ')) == 1:
      if args in DbUtil.dbData.keys():
        print(DbUtil.dbData.keys(), '=', DbUtil.dbData[args])
    else:
      print('Unknown command: %s' % (args))

  def do_insert(self, args):
    '''Insert data into the database'''
    md = DbInterface
    usage = 'Usage: insert «key» [«key», «value»]'
    args = args.split(' ')

    if md.dbSimpleStatus(): return
    elif not args or len(args) <= 2:
      print(usage)
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


  def dbStatus(db):
    '''Check if there is an open database'''
    self = DbInterface
    if self.database is not None:
      print('The database {purple}{db}{nc} is open.'.format(
        purple = self.purple,
        db = self.database,
        nc = self.nc
      ))
      return True
    else:
      return False





  def do_exit(self, args):
    '''Exit interface'''
    if DbUtil.databse_is_open(): DbUtil.close_database()
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
    DbUtil.update_db_cache()
    return line

  def postcmd(self, stop, line):
    '''Post command processing'''
    print('') # adds an empty space
    DbInterface.prompt = '{gray}Moondocks Manager: {dbp}{purple}{db}{nc}\n❯❯'.format(
      purple = Colorize.purple,
      gray = Colorize.gray,
      nc = Colorize.nc,
      db = DbUtil.database,
      dbp = DbUtil.dbPath
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
  interface = DbInterface()
  interface.cmdloop()
