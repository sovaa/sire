'''
List either all categories or only the default category.
'''
def list(db, config, category, dests = None, colw_score = 7, colw_id = 5):
    pnewline = misc.get('newline')
    pcolor = misc.get('color')
    pscore = misc.get('score')
    pcat = misc.get('category')
    pid = misc.get('id')

    if dests:
        dests = dests.split(',')

    alldbs = get_all_categories(db)

    # Only print the category titles.
    if category == 'titles':
        for title in alldbs:
            print format_category_out(title, config)
        return

    # might print on only one line if so choose
    newline = ', '
    if pnewline:
        newline = '\n'

    # List duplicates.
    # TODO: separate argument, e.g. --list-duplicates
    if category == 'dupe':
        list_duplicates(db, config, dests)
        return

    dbs = [category]
    if category == '%':  dbs = alldbs
    elif category and ',' in category: dbs = category.split(',')
    elif category == None: dbs = [config_value(config, "defval.list")]

    if not dbs[0]:
        text_error(ERROR['deflist'])
        return

    # only care if it's set and not 0, and if newline is not... newline, dont show the table
    if config_value(config, "general.showtable") and newline is '\n':
        colw_title = 0
        for category in dbs:
            dbsel = dbexec(db, "SELECT * FROM item WHERE cat = '%s'" % category, None, False).fetchall()
            for id, title, date, cat, score in dbsel:
                if len(title) > colw_title:
                    colw_title = len(title)
        print_table_head(pid, pscore, [colw_title, colw_id, colw_score])

    output = ''
    for category in dbs:
        if category not in alldbs:
            text_error(ERROR["emptycat"] % c(category))
            return

        dbsel = dbexec(db, "SELECT * FROM item WHERE cat = '"+category+"'", None, False).fetchall()

        # Sorting is optional.
        sortmethod = misc.get('sort')
        if not sortmethod: sortmethod = config_value(config, "sort." + category)
        if not sortmethod: sortmethod = config_value(config, "defval.sort")

        if sortmethod is not None:
            # Sort by specified method.
            if sortmethod == "title":
                dbsel = sorted(dbsel, key=lambda (k,v,a,b,c): (v.lower(),int(k),a,b,c))
            elif sortmethod == "id":
                dbsel = sorted(dbsel, key=lambda (k,v,a,b,c): (int(k),v,a,b,c))
            elif sortmethod == "time":
                dbsel = sorted(dbsel, key=lambda (k,v,a,b,c): (a,int(k),v,b,c))
            elif sortmethod == "score":
                dbsel = sorted(dbsel, key=lambda (k,v,a,b,c): (int(c),int(k),v,a,b))

        if pcat: 
            output += format_category_out(category, config)
        for id, title, date, cat, score in dbsel:
            if not is_young(date):
                continue

            # Make titles aligned.
            id = str(id)
            sid = ' '*(colw_id - len(id))
            sscore = ' '*(colw_score - len(str(score)))

            # uuh, you probably don't want to touch the next few lines; it -works-, okay?
            l1 = ['1', None, False]
            l2 = ['0', False]
            gscore = config_value(config, "general.showscore")
            if config_value(config, "general.showid") is '1' and pid:
                output += bold(id, pcolor) + sid + ': '

            # break it down: gscore is the CONFIG value that tells us to PRINT scores or not,
            # pscore is the COMMAND LINE value that tells us to NOT PRINT (double negative)
            #
            # the command line have higher priority than the config
            # remember: 'command' here is double negative, so NO is YES, ignorance is bliss, war is..., sorry
            # config + command = 
            #   NO   +    NO   = YES
            #   NO   +    YES  = NO
            #   YES  +    NO   = YES (not necessary, since config already sais 'print ahead, dude'
            #   YES  +    YES  = NO
            if gscore in l1 and pscore in l1 or gscore in l2 and pscore in l2:
                output += bold(str(score), pcolor) + sscore + ': '
            output += format_text_out(title) + newline

    output = output.strip()
    if len(output) is 0:
        text_note("Could not find any items matching your criterion.")
        return

    if output[-1] == ',':
        output = output[:-1]

    print output
    return

'''
List duplicates, all or in a specific categories.
'''
def list_duplicates(db, conf, cats):
    # if comma separated, split and prepare the extra sql values
    sqlcat = ''
    if cats is not None:
        sqlcat = 'WHERE '
        # set up the WHERE sql thingie
        for cat in cats:
            # no dropping tables here kiddo
            if not is_valid_category(cat):
                text_error(ERROR['bad_cat'] % cat)
                continue
            sqlcat += "cat = '%s' OR " % cat
        # probably don't want the last ' OR ' anyway
        sqlcat = sqlcat[:-4]

    # fire up the main laseeer
    results = dbexec(db, "SELECT id, title, COUNT(title) FROM item %s GROUP BY title HAVING (COUNT(title) > 1)" % sqlcat, None, False).fetchall()
    if not results:
        text_note("No duplicates found in category '%s'." % c(cat))
        return
    
    # each item returned by that last query up there only returns one of the duplicate items,
    # so get all matching titles and print their IDs and categories
    for item in results:
        print
        text_note("%s entries found for '%s':" % (c(str(item[2])), c(item[1])))
        dupeids = dbexec(db, "SELECT id, cat FROM item WHERE title = '%s'" % item[1], None, False).fetchall()
        for id in dupeids:
            print "  ID '%s' in category '%s'" % (c(str(id[0])), c(id[1]))
    return
