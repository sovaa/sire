
'''
Change the value of an item with ID 'id'.
'''
def change(id, val_orig):
    from sire.printer import format_text_in, format_text_out, c, text_note, text_error, text_warning
    from sire.helpers import id_exists
    from sire.misc import Misc
    import sire.dbman as dbman
    import re, sys

    # internal, updates the db and prints the result
    def db_and_print(val, i):
        # sql friendly
        val = format_text_in(val)
        old = dbman.get_title_with_id(i)
        dbman.set_title_with_id(val, i)
        text_note("Changed item with ID '%s' from '%s' to '%s'." % (c(i), c(old), c(format_text_out(val))))
        return

    if val_orig is None:
        text_error(Misc.ERROR['destchg'])
        sys.exit(1)

    # user might have written something awefully wrong, so just in case
    dbman.db_backup()

    # Find all '%([0-9]+)' in 'val'.
    id = id.split(',')
    res = re.findall(r'\%\(([0-9]+|#)\)', format_text_out(val_orig))

    # removes all specified IDs from the job list that doesn't exists and warns about them
    rids = []
    for k, i in enumerate(id):
        if not id_exists(i):
            text_warning(Misc.ERROR['item'] % i)
            rids = [k] + rids
    for j in rids:
        del id[j]

    # fuck yeah, no search and replace needed, just do it
    if not res:
        for i in id:
            db_and_print(val_orig, i)
        return

    # so the user had some %(blabal) in their query; do some search and replace
    for i in id:
        val = val_orig
        # may be multiple %()
        for v in res:
            # this means "if %(#), do this"
            if not cmp(v, '#'):
                rval = dbman.get_title_with_id(i)
            # otherwise it's a %(<some ID>)
            else:
                rval = dbman.get_title_with_id(v)
            val = re.compile('\%\(' + v + '\)').sub(rval, val)
        db_and_print(val, i)

    return

