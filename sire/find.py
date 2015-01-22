from sire.helpers import config_value


# Do an approximate string search using the Apse package.
def approxsearch(edits, search_strings, destinations):
    from sire.helpers import text_warning, format_text_out
    from sire.printer import format_category_out
    from sire.shared import opt
    from sire.misc import Misc

    show_categories = config_value('find.showcats') == '1' and opt.get('category') is not False
    edits = determine_edits(edits)
    results = search(edits, search_strings, destinations)
    sort_results(results, show_categories)

    if not results:
        text_warning("No matches found!")
        return

    previous_category = None
    for result in results:
        item_id, ratio, title, category = result[0], str(result[2]) + '%', result[1], result[3]
        spacer_id = ' '*(5 - len(str(item_id)))
        spacer_ratio = ' '*(6 - len(ratio))

        if show_categories:
            if should_show_category_header(previous_category, category):
                if previous_category is not None:
                    print("")
                previous_category = category
                print(format_category_out(category))
                print_columns()

        # Showing ID when listing is optional.
        if config_value("general.showid") == '0' or opt.get('id') is False:
            print(format_text_out(title))
        else:
            print("%s%s%s %s | %s%s | %s" %
                  (Misc.C['bold'], item_id, Misc.C['default'],
                  spacer_id, ratio, spacer_ratio, format_text_out(title)))


def should_show_category_header(previous_category, category):
    if previous_category is None:
        return True
    if category is not previous_category:
        return True
    return False


def sort_results(results, show_categories):
    if not results:
        return
    if show_categories:
        results.sort(lambda x, y: cmp(x[2], y[2]))
        results.sort(lambda x, y: cmp(x[3], y[3]))
        results.reverse()
    else:
        results.sort(lambda x, y: cmp(x[2], y[2]))
        results.reverse()


def determine_edits(edits):
    if edits is 0:
        if config_value("find.edits"):
            edits = int(config_value("find.edits"))
        else:
            edits = 18  # default
    if edits < 0:
        edits = 0
    elif edits > 100:
        edits = 100
    return edits


def search(edits, search_strings, destinations):
    from sire.helpers import replace_all
    from fuzzywuzzy import fuzz  # fuzzy string matching
    import sire.dbman as dbman

    db = dbman.get_items()
    results = []
    reps = {
        '.': ' ',
        '_': ' ',
        '-': ' '
    }
    for search_string in [search_strings]:
        # allow at most 'edits' edits
        min_ratio = 100 - edits
        for key in db:
            item_id, value, category = key[0], key[1], key[2]
            if should_skip_category(category, destinations):
                continue

            ratio = fuzz.partial_ratio(search_string.lower(), replace_all(value.lower(), reps))
            found = ratio >= min_ratio
            res = (item_id, value, ratio, category)
            if found and value not in results:
                results.append(res)
    return results


def should_skip_category(category, destinations):
    if not destinations:
        return False
    if category not in destinations:
        return True
    return False


def print_columns():
    print("ID     | MATCH  | TITLE")
    print("-------+--------+----------------------------------------------------")