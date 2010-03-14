'''
Add an item to the database.
'''
def add(title, category):
    from sire.printer import *
    from sire.helpers import *
    from sire.misc import *
    import sire.dbman, sys

    if not category:
        category = config_value('defval.add')
        if not category:
            text_error(Misc.ERROR['defadd'])
            sys.exit(1)

    if not config_value('categories.' + category):
        text_error(Misc.ERROR['nocat'] % c(category))
        sys.exit(1)

    # check if item is allowed to be added to this category according to its policy
    enforce_duplicate_policy(title, category)

    # add the item to the db
    dbman.add(title, category)
    #dbexec("INSERT INTO item (title, cat) VALUES ('%s', '%s')" % (format_text_in(title), category), None, True)
    id = dbman.get_last_id()
    #id = dbexec("SELECT last_insert_rowid()", None, False)[0][0]

    print_info('add', (str(id), title, category, None))
    return

