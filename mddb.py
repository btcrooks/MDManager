#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import os
import shelve
from lib import input_prefill, Colorize

class DbUtil(object):

  def __init__(self):
    self.dbCache = []
    self.dbPath = './db/'
    self.database = None
    self.dbData = None

  # GENERAL

  def add_db_ext(self, data):
    '''Append .db in extension'''
    if '.db' not in data:
      data = data + '.db'
    return data

  def database_is_open(self):
    '''Check if there if there is an open database'''
    if self.database is None and self.dbData is None:
      return True
    else:
      return False

  def update_db_cache(self):
    '''Update list of available databases'''
    self.dbCache = [] # Clear cache
    for dirname, dirnames, filenames in os.walk(self.dbPath):
      for filename in filenames:
        DbUtil.dbCache.append(filename)

  # DATABASE

  def open_database(self, db):
    '''Open a database'''

    if not db:
      db = input('\nWhich database would you like to open?: ')
      if db == 'list':
        self.list_databases()
        self.open_database(None)
        return
      elif not db:
        return

    db = DbUtil.add_db_ext(db)
    if self.database_is_open():
      if not self.close_database():
        print('Did not close database sucessfully.')
        return
    if db not in DbUtil.dbCache:
      print('The database {purple}{db}{nc} doesn\'t exist.'.format(
              purple = Colorize.purple, db = db, nc = Colorize.nc))
      askCreate = input('\nWould you like to create it now? [y/n]: ').lower()
      if askCreate == 'y':
        print('creating db...')
      else:
        return
    self.database = db
    print('Opening database {purple}{db}{nc}'.format(
          purple = Colorize.purple, db = self.dbPath + db, nc = Colorize.nc))
    try:
      self.dbData = shelve.open(self.dbPath + db, writeback=True)
    finally:
      print(self.dbData)

  def close_database(self):
    '''Close an open database'''
    if DbUtil.database is None:
      return True
    else:
      askClose = input('\nWould you like to close %s now? [y/n]: '
                       % (DbUtil.database)).lower()
      if askClose == 'y':
        print('closing db...')
        self.database = self.dbData = None
        # shelve close db
        if self.dbData is not None: self.dbData.close()
        return True
      else:
        return False

  def drop_database(self, db):
    '''Delete a databse'''
    if not db:
      self.list_databases()
      ask_drop = input('\nWhich database would you like to drop?: ')
      if not ask_drop: return
      else: db = ask_drop

    self.update_db_cache()
    db = self.add_db_ext(db)
    if db == self.database:
      self.close_database(None)
    if db not in self.dbCache:
      print('%s doesn\'t exist.' % (db))
    else:
      ask_delete = input('Are you sure you want to delete %s?: [y/n] '
                         % (db)).lower()
      if ask_delete == 'y':
        try:
          os.remove(self.dbPath + db)
        finally:
          print('Deleted %s' % (db))
      else:
        print('Aborting...')
        return

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
    - {purple}drop{nc}:   Deletes a database
    - {purple}find{nc}:   Display all documents
    - {purple}insert{nc}: Inserts «key» «value» into database
    - {purple}help{nc}:   Display help

    *Note: Use tab to autocomplete commands.

    '''.format(purple=Colorize.purple, nc=Colorize.nc)

  ## Database commands

  def do_create(self, args):
    """Create a new database"""
    if not args:
      ask_create = input('\nNew database name?: ')
      if not ask_create:
        print('Aborting...')
        return
      else:
        args = ask_create
    DbUtil.open_database(args)

  def do_open(self, args):
    '''Open an existing database'''
    # TODO: add db autocompletion
    if DbUtil.add_db_ext(args) == DbUtil.database:
      print('%s is already open' % (self.database))
    else:
      DbUtil.close_database()
      DbUtil.open_database(args)

  def do_close(self, args):
    '''Close an open database'''
    DbUtil.close_database()

  def do_drop(self, args):
    """Delete a database"""
    DbUtil.drop_database(args)


  def do_list(self, args):
    '''List databases'''
    DbUtil.list_databases()

  def do_find(self, args):
    '''Display all documents'''
    if DbUtil.database_is_open(): return
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
    usage = 'Usage: insert «dict» «key» «value»'
    args = args.split(' ')

    if DbUtil.database_is_open():
      print('You need an open database first. Run \'open\'')
      return
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
      DbUtil.dbData[insert_key] = new_dict

  def do_exit(self, args):
    '''Exit interface'''
    if DbUtil.database_is_open():
      if not DbUtil.close_database():
        print('Did not close the database sucessfully')
        return
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
    DbInterface.prompt = '{gray}Moondocks Manager: {dbp}{purple}{db}{nc}\n❯❯ '.format(
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
