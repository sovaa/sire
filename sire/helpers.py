
from sire.printer import *
import sire.dbman as dbman
from sire.misc import Misc
from sire.shared import opt
import time, sys
C = Misc.C

# parse input which may contain Comma-separated values, Negations and Ranges (CNR)
def cnr_parser(cnrs):
    allcnrs = []
    skips = []
    if cnrs is None:
        return allcnrs
    cnrs = cnrs.split(',')

    # get all skips
    for cnr in cnrs:
        if cnr[0] is not '%':
            continue
        cnr = cnr[1:]
        if '-' in cnr:
            cnr_range = get_range(cnr)
            if cnr_range:
                skips.extend(cnr_range)
            continue
        skips.append(cnr)

    # get all not skips
    for cnr in cnrs:
        if cnr[0] is '%':
            continue
        if '-' in cnr:
            cnr = get_range(cnr)
            if not cnr:
                continue
            for c in cnr:
                if c in skips:
                    continue
                allcnrs.append(c)
            continue
        allcnrs.append(cnr)
    return allcnrs

def get_range(cnrs):
    rangeids = []
    if not is_valid_id(cnrs):
        return None

    cnrs = cnrs.split('-')
    for i in range(int(cnrs[0]), int(cnrs[1]) + 1):
        rangeids.append(str(i))
    return rangeids

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
    from sire.printer import text_error
    id = str(id)
    if id[0] == '%':
        if not is_valid_id_number(id[1:]):
            if config_value('warn.id') in [None, 1]:
                text_warning(Misc.ERROR['bad_id'] % c(id))
            return False

    if '-' in id:
        idrange = id.split('-')
        if not is_valid_id_number(idrange[0]) or not is_valid_id_number(idrange[1]) or (int(idrange[0]) > int(idrange[1])):
            if config_value('warn.range') in [None, 1]:
                text_warning(Misc.ERROR['bad_range'] % c(id))
            return False

    elif not is_valid_id_number(id):
        if config_value('warn.id') in [None, 1]:
            text_warning(Misc.ERROR['bad_id'] % c(id))
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
        text_warning(Misc.ERROR["itemexists"] % c(category))
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
    if opt.get('daysago') is 0:
        return True
    if int(time.time()) - int(date) > opt.get('daysago')*24*3600:
        return False
    return True

# see if we're only pretending to be mad
def pretend():
    return opt.get('pretend')

# Prints version number, licence and authors with email.
def version():
    print Misc.NAME,Misc.VERSION,'\n',Misc.LICENCE,'\n\nWritten by: ',Misc.AUTHORS,Misc.EMAIL
    return

# check if item exists in a category
# TODO: call dbman
def title_exists(cat, item):
    return dbman.title_exists(cat, item)

# Internal function to check for already existing items.
# TODO: call dbman
def id_exists(id):
    if not is_valid_id(id):
        text_error(Misc.ERROR['bad_id'] % c(id))
        sys.exit(1);

    cursor = dbexec("SELECT * FROM item WHERE id = '%s'" % str(id), None, False)
    if len(cursor) > 0:
        return True
    return False
    
# Internal function to check for already existing items.
# TODO: call dbman
def get_title_from_id(id):
    if not is_valid_id(id):
        text_error(Misc.ERROR['bad_id'] % c(id))
        sys.exit(1);

    cursor = dbman.dbexec("SELECT title FROM item WHERE id = '%s'" % id, None, False)
    res = cursor
    if len(res) > 0:
        return res[0][0]
    text_error(Misc.ERROR["item"] % c(id)) 
    sys.exit(1)

# TODO: call dbman
def get_category_from_title(title):
    import sire.printer as printer
    import sire.dbman as dbman
    from sire.shared import db, config
    res = dbman.dbexec("SELECT cat FROM item WHERE title = '%s'" % format_text_in(title), None, False)
    if len(res) > 0:
        return res[0][0]
    error(Misc.ERROR["notitle"] % c(title))
    sys.exit(1)

# Get the category of a title with a certain ID.
# TODO: call dbman
def get_category_from_id(id):
    import sire.helpers as helpers
    import sire.printer as printer
    import sire.dbman as dbman
    import sys
    res = dbman.dbexec("SELECT cat FROM item WHERE id = '%s'" % id, None, False)
    if len(res) > 0:
        return res[0][0]
    error(Misc.ERROR["item"] % c(id))
    sys.exit(1)

# Internal function to check for already existing items.
# TODO: call dbman
def item_exists(item):
    import sire.dbman as dbman
    cursor = dbman.dbexec("SELECT * FROM item WHERE title = '%s'" % item, None, False)
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
    cursor = dbman.get_all_categories()
    return [x[0] for x in cursor]

# calculate how long time has passed since a certain date and return
# a tuple on the form (years, days, hours, minutes, seconds)
def time_passed(date):
    import time
    date = int(time.time()- int(date))
    return (str(date/60/60/24/365), str(date/60/60/24 % 365), \
        str(date/60/60 % 24), str(date/60 % 60), str(date % 60))

def sort(items):
    # Sorting is optional.
    sortmethod = opt.get('sort')
    if not sortmethod: 
        sortmethod = config_value("defval.sort")
    
    if sortmethod is None:
        return items
    
    if sortmethod == "title":
        items = sorted(items, key=lambda (k,v,a,b,c): (v.lower(),int(k),a,b,c))
    elif sortmethod == "id":
        items = sorted(items, key=lambda (k,v,a,b,c): (int(k),v,a,b,c))
    elif sortmethod == "time":
        items = sorted(items, key=lambda (k,v,a,b,c): (a,int(k),v,b,c))
    elif sortmethod == "score":
        items = sorted(items, key=lambda (k,v,a,b,c): (int(c),int(k),v,a,b))

    return items


# internal function used by info() a heck of a lot to get info from -one- ID
def get_info_from_id(id):
    from printer import text_warning
    result = dbman.get_item_with_id(str(id))
    if not result and config_value('warn.range') in [None, 1]:
        text_warning(Misc.ERROR["item"] % c(id))
    return result

def add_formated_date(item):
    from printer import format_text_out
    # add the columns needed for printing and rearange them a bit for fun and profit
    d = time.gmtime(int(item[2]))
    date_added = '%d-%d-%d, %d:%d:%d' % (d[0], d[1], d[2], d[3], d[4], d[5])
    item = [
        item[0], # id
        item[4], # score
        format_text_out(item[1]), # title
        item[3], # category
        date_added, # added
        time_passed(item[2]) # time in category
    ]
    return item

# parse a specified config file
def parse_config(conffile):
    import os, ConfigParser, string
    if not os.path.isfile(conffile):
        f = file(conffile, 'w')
        f.close()
        text_error(Misc.ERROR["conf"])
        sys.exit(1)

    _config = {}
    cp = ConfigParser.ConfigParser()
    cp.read(conffile)

    for sec in cp.sections():
        name = string.lower(sec)
        for opt in cp.options(sec):
            _config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
    return _config


