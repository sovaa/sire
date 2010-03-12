
'''
Change the value of an item with ID 'id'.
'''
def change(db, conf, id, val_orig):
    # internal, updates the db and prints the result
    def db_and_print(val, i):
        # sql friendly
        val = format_text_in(val)
        dbexec(db, "UPDATE item SET title = '%s' WHERE id = '%s'" % (val, i), None, True)
        old = format_text_out(dbexec(db, "SELECT * FROM item WHERE id = '%s'" % i, None, False).fetchall()[0][1])
        text_note("Changed item with ID '%s' from '%s' to '%s'." % (c(i), c(old), c(format_text_out(val))))
        return

    if opts.dest is None:
        text_error(ERROR['destchg'])
        sys.exit(1)

    import re

    # Find all '%([0-9]+)' in 'val'.
    id = id.split(',')
    res = re.findall(r'\%\(([0-9]+|#)\)', format_text_out(val_orig))

    # removes all specified IDs from the job list that doesn't exists and warns about them
    rids = []
    for k, i in enumerate(id):
        if not id_exists(db, i):
            text_warning(ERROR['item'] % i)
            rids = [k] + rids
    for j in rids:
        del id[j]

    # fuck yeah, no search and replace needed, just do it
    if not res:
        for i in id:
            db_and_print(val, i)
        return

    # so the user had some %(blabal) in their query; do some search and replace
    for i in id:
        val = val_orig
        # may be multiple %()
        for v in res:
            # this means "if %(#), do this"
            if not cmp(v, '#'):
                rval = dbexec(db, "SELECT * FROM item WHERE id = '%s'" % i, None, False).fetchall()[0][1]
            # otherwise it's a %(<some ID>)
            else:
                rval = dbexec(db, "SELECT * FROM item WHERE id = '%s'" % v, None, False).fetchall()[0][1]
            val = re.compile('\%\(%s\)' % v).sub(rval, val)
        db_and_print(val, i)

    return

