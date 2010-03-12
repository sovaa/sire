
class Misc:
    import string, sys, os, ConfigParser, time, shutil
    import MySQLdb # database

    HOME = os.path.expanduser("~")
    PATH = HOME + "/.sire/"
    CONFIG = PATH + "/sirerc"
    DB = PATH + "/siredb"
    ALTDB = PATH + "/altdb/"
    ALTRC = PATH + "/altrc/"
    DBBAK = PATH + "dbbak"
    
    NAME = "sire"
    VERSION = "0.2.3"
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
    
    ERROR = {
        'item':        "Item with ID '%s' does not exist.",
        'dest':        "Need destination. Use --destination, -d.",
        'destcat':     "Need to specify a category ID. Specify it with --destination, -D.",
        'destchg':     "No change-to value specified. Specify it using --destination, -D.",
        'destscore':   "Need an item to assign the score to. Use --destination, -D.",
        'destdefcat':  "Need to specify category, default category not found. Use --destination, -D or edit your config file.", 
        'conf':        "Config file didn't exist. I created it for you. Populate it before continuing.",
        'catdesc':     "There is no category description for category '%s'.",
        'nocat':       "Category '%s' does not exist.",
        'notitle':     "There is no item with title '%s'.",
        'nodb':        "Database didn't exist. I created it for you.",
        'emptydb':     "Your database is empty.",
        'emptycat':    "Empty category '%s'.",
        'dbcat':       "Database and/or config file not found. Should be in '~/.sire/'.",
        'defadd':      "defval.add not specified in config file, and no category specified on command line when adding.",
        'deflist':     "defval.list is not specified in config file, and no category specified on command line when listing.",
        'bad_id':      "'%s' is not a valid ID.",
        'bad_cat':     "Bad chars in destination ('%s'). ' and \ are not allowed.",
        'bad_range':   "'%s' is not a valid range.",
        'dupe_cat':    "Category with ID '%s' already exists with the title '%s'.",
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
                'score': True
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
                    
