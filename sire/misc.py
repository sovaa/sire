
class Misc:
    import string, sys, os, ConfigParser, time, shutil
    import MySQLdb # database

    CONFIG = "/etc/sire/sire.conf"
    
    NAME = "sire"
    VERSION = "0.3.0"
    AUTHORS = "Oscar Eriksson"
    EMAIL = "(oscar.eriks@gmail.com)"
    LICENCE = '''License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to move and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.'''
    
    C = { 
        'default' : "\033[0m",
        'd'       : "\033[0m",
        'bold'    : "\033[1m",
        'b'       : "\033[1m",
        'red'     : "\033[31m",
        'green'   : "\033[32m",
        'g'       : "\033[32m",
        'yellow'  : "\033[33m",
        'blue'    : "\033[34m",
        'magenta' : "\033[35m",
        'm'       : "\033[35m",
        'cyan'    : "\033[36m",
    }

    DBLOCATION = {
        'mysql':  "localhost",
        'sqlite': "/etc/sire/db.sqlite",
    }

    DBBACKUP = {
        'mysql':  "/etc/sire/db.mysql.backup",
        'sqlite': "/etc/sire/db.sqlite.backup",
    }
    
    ERROR = {
        'dbcon':       "It looks like you don't have a database (or wrongly configured). Please create/configure one first.",
        'dbtype':      "No database type specified in the config file. Please specify and try again.",
        'dbunknown':   "The database type specified in the config file ('%s') is not a supported type. Please specify and try again.",
        'dbloc':       ("The location/host of the database is not specified in the config file, using the default ('%s' for mysql, '%s' " + \
                       "for sqlite) and hoping for the best.") % (DBLOCATION['mysql'], DBLOCATION['sqlite']),
        'dbrestore':   "Could not restore database! Do you have the right permissions where the database and it's backup is located?",
        'dbbackup':    ("The location to store the database backup is not defined in the config file, using the default ('%s' for mysql " + \
                       "and '%s' for sqlite) and hoping for the best.") % (DBBACKUP['mysql'], DBBACKUP['sqlite']),
        'dbinfouser':  "You need to specify the username for the database in the config file.",
        'dbinfopass':  "You need to specify the password for the database in the config file.",
        'dbinfoname':  "You need to specify the name of the database in the config file.",
        'item':        "Item with ID '%s' does not exist.",
        'itemnotfound':"Could not find any items matching your criterion.",
        'itemexists':  "Item already exists in category '%s'. Use (--force, -f) to add anyway.",
        'dest':        "Need destination. Use --destination, -d.",
        'destcat':     "Need to specify a category ID. Specify it with --destination, -D.",
        'destchg':     "No change-to value specified. Specify it using --destination, -D.",
        'destscore':   "Need an item to assign the score to. Use --destination, -D.",
        'destdefcat':  "Need to specify category, default category not found. Use --destination, -D or edit your config file.", 
        'dupe_cat':    "Category with ID '%s' already exists with the title '%s'.",
        'conf':        "Config file didn't exist. I created it for you. Populate it before continuing.",
        'catdesc':     "There is no category description for category '%s'.",
        'nocat':       "Category '%s' does not exist.",
        'notitle':     "There is no item with title '%s'.",
        'nodb':        "Database didn't exist. I created it for you.",
        'nodupe':      "No duplicates found in categories '%s'.",
        'emptydb':     "Your database is empty.",
        'emptycat':    "Empty category '%s'.",
        'config':      "Config file not found. Should be in '~/.sire/'.",
        'defadd':      "defval.add not specified in config file, and no category specified on command line when adding.",
        'deflist':     "defval.list is not specified in config file, and no category specified on command line when listing.",
        'bad_id':      "'%s' is not a valid ID.",
        'bad_cat':     "Bad chars in destination ('%s'). ' and \ are not allowed.",
        'bad_range':   "'%s' is not a valid range.",
    }    
    
    class miscfunctions:
        def __init__(self):
            self.info = {
                'force': False, 
                'verbose': 1, 
                'color': True, 
                'id': True, 
                'newline': True,
                'category': True, 
                'edits': 0, 
                'pretend': False, 
                'daysago': 0, 
                'sort': None,
                'score': True,
                'profile': 'default',
            }
            return
    
        def set(self, what, value):
            self.info[what] = value
            return
    
        def get(self, what):
            return self.info[what]
    
    # only really used when creating a new category as of writing. Saves the config, duh
    def save_config(config, configfile):
        if pretend():
            return
    
        cf = open(configfile, 'wb')
        for sec in config.sections():
            name = string.lower(sec)
            cf.write("\n[" + name + "]\n")
            for opt in config.options(sec):
                cf.write(string.lower(opt) + ": " + string.strip(config.get(sec, opt)) + "\n")
    
        cf.close()
        return
                    
