# Move an item with ID 'id' to a new category.
def move(id, newcat):
    from sire.shared import db
    from sire.shared import config
    import sire.helpers as helpers
    import sire.printer as printer
    import time
    id = str(id)

    # User didn't specify what category to move to, try to use the default value.
    if newcat is None:
        # Try default for current category.
        newcat = helpers.config_value('move.' + helpers.get_category_from_id(id))
        if not newcat:
            printer.text_error(ERROR["destdefcat"])
            sys.exit(1)

    if not helpers.config_value('categories.' + newcat):
        printer.text_error(ERROR["nocat"] % c(newcat))
        sys.exit(1)

    newdate = str(int(time.time()))
    helpers.enforce_duplicate_policy(helpers.get_title_from_id(id), newcat)

    result = helpers.dbexec("SELECT * FROM item WHERE id = '%s'" % id, None, False).fetchall()
    if len(result) == 0:
        printer.text_error(ERROR['item'] % c(id))
        sys.exit(1)

    helpers.dbexec("UPDATE item SET cat = '%s' WHERE id = '%s'" % (newcat, str(id)), None, True)
    helpers.dbexec("UPDATE item SET date = '%s' WHERE id = '%s'" % (newdate, str(id)), None, True)
    title = result[0][1]
    times = result[0][3]

    printer.info('move', (id, printer.format_text_out(title), newcat, result[0][2], times))
    return

