
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
    return cursor.fetchall()

def connect():
    from sire.printer import *
    from sire.helpers import *
    from sire.misc import *
    import sys

    db = None
    type = config_value("database.type")
    if not type:
        text_error(Misc.ERROR["dbtype"])
        sys.exit(1)

    if type not in Misc.DBS:
        text_error(Misc.ERROR["dbunknown"])
        sys.exit(1)

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

    if type == "mysql":
        import MySQLdb
        host = config_value("database.host")

        if not host:
            text_warning(Misc.ERROR["db"])
            host = "localhost"
            sys.exit(1)

        if not config_value("database.user"):
            text_error(Misc.ERROR["db"])
            sys.exit(1)

        if not config_value("database.pass"):
            text_error(Misc.ERROR["db"])
            sys.exit(1)

        if not config_value("database.name"):
            text_error(Misc.ERROR["db"])
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

