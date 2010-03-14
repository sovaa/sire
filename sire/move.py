# Move an item with ID 'id' to a new category.
def move(id, newcat):
    from sire.misc import Misc
    from sire.printer import c
    import sire.dbman as dbman
    import sire.helpers as helpers
    import sire.printer as printer
    import time, sys

    # User didn't specify what category to move to, try to use the default value.
    if newcat is None:
        # Try default for current category.
        newcat = helpers.config_value('move.' + helpers.get_category_from_id(id))
        if not newcat:
            printer.text_error(Misc.ERROR["destdefcat"])
            sys.exit(1)

    if not helpers.config_value('categories.' + newcat):
        printer.text_error(Misc.ERROR["nocat"] % c(newcat))
        sys.exit(1)

    newdate = str(int(time.time()))
    helpers.enforce_duplicate_policy(helpers.get_title_from_id(id), newcat)

    result = dbman.get_item_with_id(id)
    if len(result) == 0:
        printer.text_error(Misc.ERROR['item'] % c(id))
        sys.exit(1)

    dbman.update_category(str(id), newcat)
    dbman.update_date(str(id), newdate)
    title = result[0][1]
    times = result[0][3]

    printer.print_info('move', (id, printer.format_text_out(title), newcat, result[0][2], times))
    return

