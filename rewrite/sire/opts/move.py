# Move an item with ID 'id' to a new category.
def move(db, conf, id, newcat):
    # newcat = dest
    # User didn't specify what category to move to, try to use the default value.
    if newcat is None:
        # Try default for current category.
        newcat = config_value('move.' + get_category_from_id(db, config, id))
        if not defdest:
            text_error(ERROR["destdefcat"])
            sys.exit(1)

    if not config_value('categories.' + newcat):
        text_error(ERROR["nocat"] % c(newcat))
        sys.exit(1)

    newdate = str(int(time.time()))
    enforce_duplicate_policy(db, conf, get_title_from_id(db, id), newcat)

    result = dbexec(db, "SELECT * FROM item WHERE id = '%s'" % id, None, False).fetchall()
    if len(result) == 0:
        text_error(ERROR['item'] % c(id))
        sys.exit(1)

    dbexec(db, "UPDATE item SET cat = '%s' WHERE id = '%s'" % (newcat, str(id)), None, True)
    dbexec(db, "UPDATE item SET date = '%s' WHERE id = '%s'" % (newdate, str(id)), None, True)
    title = result[0][1]
    times = result[0][3]

    print_info(conf, 'move', (id, format_text_out(title), newcat, result[0][2], times))
    return

