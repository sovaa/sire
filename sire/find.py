


# Do an approximate string search using the Apse package.
def approxsearch(edits, sstr):
    from sire.helpers import config_value, replace_all, text_warning, text_note, format_text_out
    from sire.printer import format_category_out
    from fuzzywuzzy import fuzz # fuzzy string matching
    import sire.dbman as dbman
    from sire.shared import opt
    from sire.misc import Misc

    results = []
    reps = {
        '.': ' ',
        '_': ' ',
        '-': ' '
    }

    if edits is 0 and config_value("find.edits"):
        edits = int(config_value("find.edits"))
    if edits < 0:
        edits = 0
    elif edits > 100:
        edits = 100

    db = dbman.get_items()
    for search in [sstr]:
        # allow at most 'edits' edits
        min_ratio = 100 - edits

        for key in db: 
            value = key[1]
            item_id = key[0]
            category = key[2]
            ratio = fuzz.ratio(search.lower(), replace_all(value.lower(), reps))
            found = ratio >= min_ratio
            res = (item_id, value, ratio, category)
            if found and value not in results:
                results.append(res)

    if not results:
        text_warning("No matches found!")
        return

    showcats = config_value('find.showcats') == '1' and opt.get('category') is not False
    text_note("Match found. Best match at the top.")

    if showcats:
        results.sort(lambda x, y: cmp(x[2], y[2]))
        results.sort(lambda x, y: cmp(x[3], y[3]))
        results.reverse()
    else:
        results.sort(lambda x, y: cmp(x[2], y[2]))
        results.reverse()

    previous_category = None
    for result in results:
        if showcats:
            if previous_category is None or result[3] != previous_category:
                previous_category = result[3]
                print '\n' + format_category_out(result[3])

        # Make titles aligned.
        spacer = ' '*(5 - len(str(res[0])) + 3 - len(str(result[2])))

        # Showing ID when listing is optional.
        if config_value("general.showid") == '0' or opt.get('id') is False:
            print result[1]
        else:
            print "%s%s%s %s (ratio %s): %s" % (Misc.C['bold'], result[0], Misc.C['default'], spacer, result[2], format_text_out(result[1]))
