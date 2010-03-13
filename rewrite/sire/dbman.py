
# Execute SQL statement.
def dbexec(template, values, volatile):
    from sire.shared import db
    from sire.helpers import pretend
    import sire.shared

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

def connect():
    from sire.printer import *
    from sire.helpers import *
    from sire.misc import *
    import sys

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
    from sire.printer import *
    from sire.helpers import *
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
    from sire.printer import *
    from sire.helpers import *
    import os
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
    from sire.helpers import *
    from sire.printer import *
    from sire.misc import *
    import sys

    type = config_value("database.type")
    if not type:
        text_error(Misc.ERROR["dbtype"])
        sys.exit(1)
    if type not in Misc.DBLOCATION.keys():
        text_error(Misc.ERROR["dbunknown"] % str(type))
        sys.exit(1)
    return type

def get_db_backup_location(type):
    from sire.helpers import *
    from sire.printer import *
    from sire.misc import *

    dbbak = config_value("database.backup")
    if not dbbak:
        text_warning(Misc.ERROR["dbbackup"])
        dbbak = Misc.DBBACKUP[type]
    return dbbak

def get_db_location(type):
    from sire.helpers import *
    from sire.printer import *
    from sire.misc import *

    dbloc = config_value("database.location")
    if not dbloc:
        text_warning(Misc.ERROR["dbloc"])
        dbloc = Misc.DBLOCATION[type]
    return dbloc
