
import sire.dbman as dbman
from sire.misc import Misc
from sire.shared import opt
from sire.printer import c

'''
List either the default category or specified ones.
'''
def list(cats, colw_score = 7, colw_id = 5):
    from sire.helpers import cnr_parser, config_value, sort, is_young
    from sire.printer import text_warning, text_note, table_head, format_category_out, format_text_out, bold
    alldbs = dbman.get_all_categories()
    cats = cnr_parser(cats)
    if not cats:
        cats = [config_value("defval.list")]

    if not cats:
        text_error(Misc.ERROR['deflist'])
        return

    # only care if it's set and not 0, and if newline is not... newline, dont show the table
    if config_value("general.showtable") and opt.get('newline') is '\n':
        colw_title = 0
        for cat in cats:
            dbsel = dbman.get_items_with_category(cat)
            for id, title, date, cat, score in dbsel:
                if len(title) > colw_title:
                    colw_title = len(title)
        table_head(opt.get('id'), opt.get('score'), [colw_title, colw_id, colw_score])

    output = ''
    for cat in cats:
        if cat not in alldbs:
            if config_value('warn.emptycat') in [None, 1]:
                text_warning(Misc.ERROR["emptycat"] % c(cat))
            continue

        # get all items in category 'cat' and sort them if sorting is specified
        dbsel = sort(dbman.get_items_with_category(cat))

        # (--no-category, -C) was used
        if opt.get('category'): 
            formcat = format_category_out(cat)
            if formcat:
                output += formcat + opt.get('newline')

        for id, title, date, cat, score in dbsel:
            # (--days-ago, -y) was used
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
            if config_value("general.showid") is '1' and opt.get('id'):
                output += bold(id, opt.get('color')) + sid + ': '

            # break it down: gscore is the CONFIG value that tells us to PRINT scores or not,
            # opt.get('score') is the COMMAND LINE value that tells us to NOT PRINT (double negative)
            #
            # the command line have higher priority than the config
            # remember: 'command' here is double negative, so NO is YES, ignorance is bliss, war is..., sorry
            # config + command = 
            #   NO   +    NO   = YES
            #   NO   +    YES  = NO
            #   YES  +    NO   = YES (not necessary, since config already sais 'print ahead, dude'
            #   YES  +    YES  = NO
            if gscore in l1 and opt.get('score') in l1 or gscore in l2 and opt.get('score') in l2:
                output += bold(str(score), opt.get('color')) + sscore + ': '
            output += format_text_out(title) + opt.get('newline')

    output = output.strip()
    if len(output) is 0:
        return text_note(Misc.ERROR["itemnotfound"])
    if output[-1] == ',':
        output = output[:-1]

    print output
    return

'''
List duplicates; all or in a specific categories.
'''
def list_duplicates(cats):
    from sire.printer import text_note
    from sire.helpers import cnr_parser

    cats = cnr_parser(cats)
    results = dbman.get_duplicates_in_categories(cats)
    if not results:
        return text_note(Misc.ERROR["nodupe"] % c(str(cats)))
    
    # each item returned by that last query up there only returns one of the duplicate items,
    # so get all matching titles and print their IDs and categories
    for item in results:
        print
        text_note("%s entries found for '%s':" % (c(str(item[2])), c(item[1])))
        dupeids = dbexec(db, "SELECT id, cat FROM item WHERE title = '%s'" % item[1], None, False)
        for id in dupeids:
            print "  ID '%s' in category '%s'" % (c(str(id[0])), c(id[1]))
    return

def list_categories(cats):
    from sire.printer import format_category_out
    from sire.helpers import cnr_parser

    cats = cnr_parser(cats)
    if not cats:
        cats = dbman.get_all_categories()
    for cat in cats:
        formated_cat = format_category_out(cat[0])
        if formated_cat:
            print formated_cat
    return

