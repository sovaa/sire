
from sire.printer import *
from sire.dbman import *
from sire.misc import Misc as misc
from sire.shared import opt
C = misc.C

# try to see if specified category is valid
def is_valid_category(cat):
    if not cat:
        return False
    notallowed = "\\'"
    for char in cat:
        if char in notallowed:
            return False
    return True

# try to see if specified ID, range, negative etc. is a valid ID
def is_valid_id(id):
    if id[0] is '%':
        if not is_valid_id_number(id[1:]):
            text_error(misc.ERROR['bad_id'] % c(id))
            return False

    if '-' in id:
        idrange = id.split('-')
        if not is_valid_id_number(idrange[0]) or not is_valid_id_number(idrange[1]):
            text_error(misc.ERROR['bad_range'] % c(id))
            return False

    elif not is_valid_id_number(id):
        text_error(misc.ERROR['bad_id'] % c(id))
        return False
    return True

# single ID checked if it's a number (i.e. no range, negation etc.)
def is_valid_id_number(id):
    sid = None
    try:
        iid = int(id)
        sid = str(iid)
        if iid < 0:
            return False
    except:
        return False

    if sid != id:
        return False
    return True

# figure out if an item-to-be-added is allowed in that category according to the category's policy
def enforce_duplicate_policy(name, category):
    from shared import opt
    import sys

    dup = get_duplicate_policy(category)
    if dup == '0' and item_exists(name):
        existing_category = get_category_from_title(name)
        existing_duplicate = get_duplicate_policy(existing_category)
        if existing_duplicate not in ["1", "2"]:
            text_warning("Item already exists in category '%s'. Use (--force, -f) to add anyway." % c(existing_category))
            if not opt.get('force'):
                sys.exit(1)

    # need to check both
    if dup == '1' and title_exists(category, name):
        text_warning("Item already exists in category '%s'. Use (--force, -f) to add anyway." % c(category))
        if not opt.get('force'):
            sys.exit(1)
    return


# if 'ident' is specified in the config, return its value
def config_value(ident):
    from sire.shared import config
    if ident in config.keys():
        return config[ident]
    return None

# return True if the difference between specified unix time and now is 
# less than 'daysago' specified in config. False otherwise
def is_young(date):
    from sire.shared import opt
    import time
    if opt.get('daysago') is not 0:
        if int(time.time()) - int(date) > opt.get('daysago')*24*3600:
            return False
    return True

# see if we're only pretending to be mad
def pretend():
    from sire.shared import opt
    return opt.get('pretend')

# Prints version number, licence and authors with email.
def version():
    print Misc.NAME,Misc.VERSION,'\n',Misc.LICENCE,'\n\nWritten by: ',Misc.AUTHORS,Misc.EMAIL
    return

# check if item exists in a category
def title_exists(cat, item):
    cursor = dbexec("SELECT * FROM item WHERE title = '%s' AND cat = '%s'" % (item, cat), None, False)
    if len(cursor) > 0:
        return True
    return False

# Internal function to check for already existing items.
def id_exists(id):
    if not is_valid_id(id):
        text_error(misc.ERROR['bad_id'] % c(id))
        sys.exit(1);

    cursor = dbexec("SELECT * FROM item WHERE id = '%s'" % str(id), None, False)
    if len(cursor) > 0:
        return True
    return False
    
# Internal function to check for already existing items.
def get_title_from_id(id):
    if not is_valid_id(id):
        text_error(misc.ERROR['bad_id'] % c(id))
        sys.exit(1);

    cursor = dbexec("SELECT title FROM item WHERE id = '%s'" % id, None, False)
    res = cursor
    if len(res) > 0:
        return res[0][0]
    text_error(misc.ERROR["item"] % c(id)) 
    sys.exit(1)

def get_category_from_title(title):
    import sire.printer as printer
    from sire.shared import db, config
    res = dbexec("SELECT cat FROM item WHERE title = '%s'" % format_text_in(title), None, False)
    if len(res) > 0:
        return res[0][0]
    error(misc.ERROR["notitle"] % c(title))
    sys.exit(1)

# Get the category of a title with a certain ID.
def get_category_from_id(id):
    import sire.helpers as helpers
    import sire.printer as printer
    import sys
    res = dbexec("SELECT cat FROM item WHERE id = '%s'" % id, None, False)
    if len(res) > 0:
        return res[0][0]
    error(misc.ERROR["item"] % c(id))
    sys.exit(1)

# Internal function to check for already existing items.
def item_exists(item):
    cursor = dbexec("SELECT * FROM item WHERE title = '%s'" % item, None, False)
    if len(cursor) > 0:
        return True
    return False

# get the duplicate policy for a certain category
# TODO: use config_value()
def get_duplicate_policy(cat):
    from sire.shared import config
    if not cat is None and ("duplicates." + cat) in config.keys():
        return config["duplicates." + cat]

    elif ("defval.duplicates") in config.keys():
        return config["defval.duplicates"]
    return None

# replace occurances in text of dict items from dic
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

# friendly output
def format_time_passed(date):
    date = time_passed(date)
    return "%s years, %s days, %s hours, %s minutes and %s seconds." % \
       (c(date[0]), c(date[1]), c(date[2]), c(date[3]), c(date[4]))


# get all category names
def get_all_categories():
    cursor = dbexec("SELECT DISTINCT cat FROM item", None, False)
    return [x[0] for x in cursor]

# calculate how long time has passed since a certain date and return
# a tuple on the form (years, days, hours, minutes, seconds)
def time_passed(date):
    import time
    date = int(time.time()- int(date))
    return (str(date/60/60/24/365), str(date/60/60/24 % 365), \
        str(date/60/60 % 24), str(date/60 % 60), str(date % 60))

# internal function used by info() a heck of a lot to get info from -one- ID
def get_info_from_id(id, rangewarn = None):
    import time
    result = dbexec("SELECT * FROM item WHERE id = '%s'" % str(id), None, False)
    if not result:
        if rangewarn:
            text_error(misc.ERROR["item"] % c(id))
        return

    result = result[0]
    # add the columns needed for printing and rearange them a bit for fun and profit
    d = time.gmtime(int(result[2]))
    date_added = '%d-%d-%d, %d:%d:%d' % (d[0], d[1], d[2], d[3], d[4], d[5])
    result = [
        result[0], # id
        result[4], # score
        format_text_out(result[1]), # title
        result[3], # category
        date_added, # added
        time_passed(result[2]) # time in category
    ]
    return result

# parse a specified config file
def parse_config(conffile):
    import os, ConfigParser, string
    if not os.path.isfile(conffile):
        f = file(conffile, 'w')
        f.close()
        text_error(misc.ERROR["conf"])
        sys.exit(1)

    _config = {}
    cp = ConfigParser.ConfigParser()
    cp.read(conffile)

    for sec in cp.sections():
        name = string.lower(sec)
        for opt in cp.options(sec):
            _config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
    return _config


