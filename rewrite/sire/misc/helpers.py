# Prints version number, licence and authors with email.
def version():
    print NAME,VERSION,'\n',LICENCE,'\n\nWritten by: ',AUTHORS,EMAIL
    return

# check if item exists in a category
def title_exists(db, cat, item):
    cursor = dbexec(db, "SELECT * FROM item WHERE title = '%s' AND cat = '%s'" % (item, cat), None, False)
    if len(cursor.fetchall()) > 0:
        return True
    return False

# Internal function to check for already existing items.
def id_exists(db, id):
    if not is_valid_id(id):
        text_error(ERROR['bad_id'] % c(id))
        sys.exit(1);

    cursor = dbexec(db, "SELECT * FROM item WHERE id = '%s'" % str(id), None, False)
    if len(cursor.fetchall()) > 0:
        return True
    return False
    
# Internal function to check for already existing items.
def get_title_from_id(db, id):
    if not is_valid_id(id):
        text_error(ERROR['bad_id'] % c(id))
        sys.exit(1);

    cursor = dbexec(db, "SELECT title FROM item WHERE id = '%s'" % id, None, False)
    res = cursor.fetchall()
    if len(res) > 0:
        return res[0][0]
    text_error(ERROR["item"] % c(id)) 
    sys.exit(1)

def get_category_from_title(db, config, title):
    cursor = dbexec(db, "SELECT cat FROM item WHERE title = '%s'" % format_text_in(title), None, False)
    res = cursor.fetchall()
    if len(res) > 0:
        return res[0][0]
    text_error(ERROR["notitle"] % c(title))
    sys.exit(1)

'''
# same thing, though if multiple items with the same title exists, from category may be
# selected when using this function
def get_category_from_id(db, config, id):
    return get_category_from_title(db, config, get_title_from_id(db, config, id))
'''
    
# Get the category of a title with a certain ID.
def get_category_from_id(db, config, id):
    cursor = dbexec(db, "SELECT cat FROM item WHERE id = '%s'" % id, None, False)
    res = cursor.fetchall()
    if len(res) > 0:
        return res[0][0]
    text_error(ERROR["item"] % c(id))
    sys.exit(1)

# Internal function to check for already existing items.
def item_exists(db, item):
    cursor = dbexec(db, "SELECT * FROM item WHERE title = '%s'" % item, None, False)
    if len(cursor.fetchall()) > 0:
        return True
    return False

# get the duplicate policy for a certain category
def get_duplicate_policy(config, cat):
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
def get_all_categories(db):
    cursor = dbexec(db, "SELECT DISTINCT cat FROM item", None, False)
    return [x[0] for x in cursor.fetchall()]

# calculate how long time has passed since a certain date and return
# a tuple on the form (years, days, hours, minutes, seconds)
def time_passed(date):
    date = int(time.time()- int(date))
    return (str(date/60/60/24/365), str(date/60/60/24 % 365), \
        str(date/60/60 % 24), str(date/60 % 60), str(date % 60))

# internal function used by info() a heck of a lot to get info from -one- ID
def get_info_from_id(db, id, rangewarn = None):
    result = dbexec(db, "SELECT * FROM item WHERE id = '%s'" % str(id), None, False).fetchall()
    if not result:
        if rangewarn:
            text_error(ERROR["item"] % c(id))
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
    if not os.path.isfile(conffile):
        f = file(conffile, 'w')
        f.close()
        text_error(ERROR["conf"])
        sys.exit(1)

    _config = {}
    cp = ConfigParser.ConfigParser()
    cp.read(conffile)

    for sec in cp.sections():
        name = string.lower(sec)
        for opt in cp.options(sec):
            _config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
    return _config

# Print a category description using bold and colors.
def format_category_out(category, config):
    if ("categories." + category) not in config.keys():
        text_error(ERROR["catdesc"] % c(category))
        sys.exit(1)

    color = ''
    if ("colors." + category) in config.keys():
        color = C[config["colors." + category]]

    elif "colors.defcol" in config.keys():
        color = C[config["colors.defcol"]]

    if misc.get('color'):
        return "  %s%s%s ('%s')%s\n" %(C["bold"], color, config["categories." + category], category, C["default"])
    return "  %s ('%s')\n" % (config["categories." + category],  category)

# sql friendly format
def format_text_in(title):
    import re
    title = re.sub('"', "&#34;", title)
    title = re.sub("'", "&#39;", title)
    return title

# sql unfriendly format
def format_text_out(title):
    import re
    title = re.sub("&#34;", '"', title)
    title = re.sub("&#39;", "'", title)
    return title

