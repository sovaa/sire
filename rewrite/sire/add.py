'''
Add an item to the database.
'''
def add(db, config, name, category):
    if not category:
        category = config_value('defval.add')
        if not category:
            text_error(ERROR['defadd'])
            sys.exit(1)

    if not config_value('categories.' + category):
        text_error(ERROR['nocat'] % c(category))
        sys.exit(1)

    # sql friendly
    name = format_text_in(name)

    # check if item is allowed to be added to this category according to its policy
    enforce_duplicate_policy(db, config, name, category)

    # time.time() returns float, so throw away the ms, then convert to string for writing
    date = str(int(time.time()))

    # FIXME: AUTO_INCREMENT
    dbexec(db, 'UPDATE curid SET id = id + 1', None, True)
    id = dbexec(db, 'SELECT * FROM curid', None, False).fetchall()[0][0]

    # add the item to the db
    dbexec(db, "INSERT INTO item (id, title, date, cat) VALUES ('%s', '%s', '%s', '%s')" % (id, name, date, category), True)

    print_info(config, 'add', (str(id), name, category, None))
    return

