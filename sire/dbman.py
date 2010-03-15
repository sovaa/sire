
from sire.misc import Misc
from sire.shared import opt
import sys

# Execute SQL statement.
def dbexec(template, values, volatile):
    from sire.shared import db
    from sire.helpers import pretend

    # volatile is all UPDATE, INSERT etc., so if pretending, 
    # don't actually do anything, just look busy so the boss
    # won't thing something's up
    if volatile and pretend():
        return

    cursor = db.cursor()
    if values is None:
        cursor.execute(template)
    else:
        cursor.execute(template, values)
    db.commit()
    return cursor.fetchall()

def get_items_with_category(cat):
    db_valid_category(cat)
    return dbexec("SELECT id, title, date, cat, score FROM item WHERE cat = '%s' AND profile = '%s'" % (cat, opt.get('profile')), None, False)

def get_item_with_id(id):
    db_valid_id(id)
    return dbexec("SELECT id, title, date, cat, score FROM item WHERE id = '%s' AND profile = '%s'" % (id, opt.get('profile')), None, False)

def add(title, category):
    from sire.helpers import format_text_in
    dbexec("INSERT INTO item (title, cat, profile) VALUES ('%s', '%s', '%s')" % (format_text_in(title), category, opt.get('profile')), None, True)

def get_items():
    return dbexec("SELECT id, title, cat, date, score FROM item", None, False)

def get_title_with_id(id):
    from sire.helpers import format_text_out
    db_valid_id(id)
    return format_text_out(dbexec("SELECT title FROM item WHERE id = '%s' AND profile = '%s'" % (id, opt.get('profile')), None, False)[0][0])

def update_category(id, cat):
    db_valid_id(id)
    db_valid_category(cat)
    dbexec("UPDATE item SET cat = '%s' WHERE id = '%s' AND profile = '%s'" % (cat, id, opt.get('profile')), None, True)

def update_date(id, date):
    db_valid_id(id)
    dbexec("UPDATE item SET date = '%s' WHERE id = '%s' AND profile = '%s'" % (date, id, opt.get('profile')), None, True)

def delete(id):
    db_valid_id(id)
    dbexec("DELETE FROM item WHERE id = '%s' AND profile = '%s'" % (id, opt.get('profile')), None, True)

def set_title_with_id(title, id):
    from sire.helpers import format_text_in
    db_valid_id(id)
    dbexec("UPDATE item SET title = '%s' WHERE id = '%s' AND profile = '%s'" % (format_text_in(title), id, opt.get('profile')), None, True)

def get_last_id():
    return dbexec("SELECT last_insert_rowid()", None, False)[0][0]

def title_exists(cat, title):
    from sire.helpers import format_text_in
    db_valid_category(cat)
    cursor = dbexec("SELECT title FROM item WHERE title = '%s' AND cat = '%s' AND profile = '%s'" % 
        (format_text_in(title), format_text_in(cat), opt.get('profile')), None, False)
    if len(cursor) > 0:
        return True
    return False

def get_all_categories():
    return dbexec("SELECT DISTINCT cat FROM item", None, False)

def db_valid_category(cat):
    from sire.helpers import is_valid_category
    from sire.printer import text_error
    if not is_valid_category(cat):
        text_error(Misc.ERROR["bad_id"])
        sys.exit(1)

def db_valid_id(id):
    from sire.helpers import is_valid_id, format_text_out
    from sire.printer import text_error
    if not is_valid_id(id):
        text_error(Misc.ERROR["bad_id"])
        sys.exit(1)

def get_duplicates_from_categories(cats):
    from sire.helpers import is_valid_category
    from sire.printer import text_error
    from sire.misc import Misc
    # if comma separated, split and prepare the extra sql values
    sqlcat = ''
    if cats is None:
        return None

    sqlcat = "WHERE profile = '%s' AND (" % opt.get('profile')
    # set up the WHERE sql thingie
    for cat in cats:
        # no dropping tables here kiddo
        if not is_valid_category(cat):
            text_error(Misc.ERROR['bad_cat'] % cat)
            continue
        sqlcat += "cat = '%s' OR " % cat
    # probably don't want the last ' OR ' anyway
    sqlcat = sqlcat[:-4] + ')'

    # fire up the main laseeer
    return dbexec("SELECT id, title, COUNT(title) FROM item %s GROUP BY title HAVING (COUNT(title) > 1)" % sqlcat, None, False)

def update_title_with_id(title, id):
    from sire.helpers import is_valid_id
    from sire.printers import text_error
    if not is_valid_id(id):
        text_error(Misc.ERROR["bad_id"])
        sys.exit(1)
    dbexec("UPDATE item SET title = '%s' WHERE id = '%s' AND profile = '%s'" % (title, id, opt.get('profile')), None, True)

def connect():
    from sire.helpers import config_value
    from sire.printer import text_warning, text_error
    from sire.misc import Misc
    db = None
    type = get_db_type()
    if type == "sqlite":
        from pysqlite2 import dbapi2 as sqlite3

        location = config_value("database.location")
        if not location:
            text_warning(Misc.ERROR["dbloc"])
            location = "/etc/sire/db.sqlite"

        try:
            db = sqlite3.connect(location)
        except:
            text_error(Misc.ERROR["dbcon"])
            sys.exit(1)

    elif type == "mysql":
        import MySQLdb
        host = config_value("database.host")
        username = config_value("database.user")
        password = config_value("database.pass")
        dbname = config_value("database.name")

        if not host:
            text_warning(Misc.ERROR["dbinfohost"])
            host = "localhost"
        if not username:
            text_error(Misc.ERROR["dbinfouser"])
        if not password:
            text_error(Misc.ERROR["dbinfopass"])
        if not dbname:
            text_error(Misc.ERROR["dbinfoname"])
        if None in [username, password, dbname]:
            sys.exit(1)

        try:
            db = MySQLdb.connect(
                host,
                config_value("database.user"), 
                config_value("database.pass"), 
                config_value("database.name")
            )
        except:
            text_error(Misc.ERROR["dbcon"])
            sys.exit(1)

    if not db:
        text_error(Misc.ERROR["dbcon"])
        sys.exit(1)

    return db

# TODO: check for mysqldump
def db_backup():
    import commands, sys, os
    from sire.printer import text_note, text_warning, text_error
    from sire.helpers import config_value

    text_note("Backing up database...")

    type = get_db_type()
    dbbak = get_db_backup_location(type)

    if type == "sqlite":
        dbloc = get_db_location(type)
        if os.path.exists(dbbak + '.gz'):
            os.remove(dbbak + '.gz')

        os.popen('cp %s %s' % (dbloc, dbbak))
        os.popen('gzip -9 %s' % dbbak)

    elif type == "mysql":
        import MySQLdb
        host = config_value("database.host")
        username = config_value("database.user")
        password = config_value("database.pass")
        dbname = config_value("database.name")

        if not host:
            text_warning(Misc.ERROR["dbinfohost"])
            host = "localhost"
        if not username:
            text_error(Misc.ERROR["dbinfouser"])
        if not password:
            text_error(Misc.ERROR["dbinfopass"])
        if not dbname:
            text_error(Misc.ERROR["dbinfoname"])
        if None in [username, password, dbname]:
            sys.exit(1)

        os.popen('mysqldump -u %s -p%s %s | gzip -9 > %s.gz' % (username, password, dbname, dbbak))

    text_note("Backup complete!")
    return

# TODO: check for gunzip
def db_restore():
    import os
    from sire.helpers import pretend, config_value
    from sire.printer import text_note

    text_note("Restoring database from backup...")
    if pretend():
        return text_note("Backup restored!")

    type = get_db_type()
    dbbak = get_db_backup_location(type)
    if type == "sqlite":
        dbloc = get_db_location(type)
        os.popen("gunzip -c %s > %s" % (dbbak, dbloc))

    elif type == "mysql":
        username = config_value('database.user')
        password = config_value('database.pass')
        dbname = config_value('database.name')
        os.open("gunzip -c %s.gz | mysql -u %s -p%s %s" % (dbbak, username, password, dbname))
    text_note("Backup restored!")
    return

def get_db_type():
    from sire.helpers import config_value
    from sire.printer import text_error
    type = config_value("database.type")
    if not type:
        text_error(Misc.ERROR["dbtype"])
        sys.exit(1)
    if type not in Misc.DBLOCATION.keys():
        text_error(Misc.ERROR["dbunknown"] % str(type))
        sys.exit(1)
    return type

def get_db_backup_location(type):
    from sire.helpers import config_value
    from sire.printer import text_warning
    dbbak = config_value("database.backup")
    if not dbbak:
        text_warning(Misc.ERROR["dbbackup"])
        dbbak = Misc.DBBACKUP[type]
    return dbbak

def get_db_location(type):
    from sire.helpers import config_value
    from sire.printer import text_warning
    dbloc = config_value("database.location")
    if not dbloc:
        text_warning(Misc.ERROR["dbloc"])
        dbloc = Misc.DBLOCATION[type]
    return dbloc
