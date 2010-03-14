
from sire.helpers import *
from sire.printer import *
from sire.misc import *

'''
List either all categories or only the default category.
'''
def list(category, dests = None, colw_score = 7, colw_id = 5):
    from sire.shared import opt
    import sire.dbman as dbman

    pnewline = opt.get('newline')
    pcolor = opt.get('color')
    pscore = opt.get('score')
    pcat = opt.get('category')
    pid = opt.get('id')

    if dests:
        dests = dests.split(',')

    alldbs = get_all_categories()

    # Only print the category titles.
    if category == 'titles':
        for title in alldbs:
            print format_category_out(title)
        return

    # might print on only one line if so choose
    newline = ', '
    if pnewline:
        newline = '\n'

    # List duplicates.
    # TODO: separate argument, e.g. --list-duplicates
    if category == 'dupe':
        list_duplicates(dests)
        return

    dbs = [category]
    if category == '%':  dbs = alldbs
    elif category and ',' in category: dbs = category.split(',')
    elif category == None: dbs = [config_value("defval.list")]

    if not dbs[0]:
        text_error(misc.ERROR['deflist'])
        return

    # only care if it's set and not 0, and if newline is not... newline, dont show the table
    if config_value("general.showtable") and newline is '\n':
        colw_title = 0
        for category in dbs:
            dbsel = dbman.get_items_with_category(category)
            #dbexec("SELECT * FROM item WHERE cat = '%s'" % category, None, False)
            for id, title, date, cat, score in dbsel:
                if len(title) > colw_title:
                    colw_title = len(title)
        table_head(pid, pscore, [colw_title, colw_id, colw_score])

    output = ''
    for category in dbs:
        if category not in alldbs:
            text_error(misc.ERROR["emptycat"] % c(category))
            return

        dbsel = dbman.get_items_with_category(category)
        #dbexec("SELECT * FROM item WHERE cat = '"+category+"'", None, False)

        # Sorting is optional.
        sortmethod = opt.get('sort')
        if not sortmethod: sortmethod = config_value("sort." + category)
        if not sortmethod: sortmethod = config_value("defval.sort")

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
            output += format_category_out(category)
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
            gscore = config_value("general.showscore")
            if config_value("general.showid") is '1' and pid:
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
def list_duplicates(cats):
    from sire.shared import opt, db, config
    from sire.helpers import *
    from sire.printer import *
    from sire.misc import Misc as misc
    import sire.dbman

    results = dbman.get_duplicates_in_categories(cats)
    if not results:
        text_note("No duplicates found in category '%s'." % c(cat))
        return
    
    # each item returned by that last query up there only returns one of the duplicate items,
    # so get all matching titles and print their IDs and categories
    for item in results:
        print
        text_note("%s entries found for '%s':" % (c(str(item[2])), c(item[1])))
        dupeids = dbexec(db, "SELECT id, cat FROM item WHERE title = '%s'" % item[1], None, False)
        for id in dupeids:
            print "  ID '%s' in category '%s'" % (c(str(id[0])), c(id[1]))
    return

