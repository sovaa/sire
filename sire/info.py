
# Prints formated table with info about items with specified IDs.
def info(ids, dests = None):
    from sire.helpers import config_value, is_valid_id, get_info_from_id, cnr_parser, sort, add_formated_date
    import sys

    ids = cnr_parser(ids)
    dests = cnr_parser(dests)

    # [id, score, title, category, date_added, time_in_category]
    strlens = [1,1,1,1,1,1]
    items = []

    # go through all specified IDs
    for id in ids:
        result = get_info_from_id(id)
        if result:
            items.append(result[0])

    # found nothin', error/warning/whatever already shown if so
    if not items:
        return

    # calculate each columns max width
    for item in items:
        item = add_formated_date(item)
        # if destination cateogries are specified, and this item's not in it, continue
        if dests and item[3] not in dests:
            continue
        for i in range(len(strlens)):
            if len(str(item[i])) > strlens[i]:
                strlens[i] = len(str(item[i]))

    # calculate spaces between column headers and print them
    width = 0
    labels = ['ID  ', 'SCORE  ', 'TITLE  ', 'CATEGORY  ', 'DATE ADDED  ', 'TIME IN CATEGORY  ']
    for i in range(len(labels)):
        spaces = max(strlens[i], len(labels[i])) - len(labels[i]) + 1
        width += spaces + len(labels[i])
        sys.stdout.write(labels[i] + ' '*spaces + '| ')
    width = width + 2*len(labels) - 1
    print '\n' + '-'*width

    items = sort(items)

    # calculate spaces between column items and print them
    for item in items:
        item = add_formated_date(item)
        # if destination cateogries are specified, and this item's not in it, continue
        if dests and item[3] not in dests:
            continue
        for i in range(len(strlens) - 1):
            spaces = max(strlens[i] - len(str(item[i])), len(labels[i]) - len(str(item[i]))) + 1
            sys.stdout.write('%s%s| ' % (item[i], ' '*spaces))
        # this is the time it's been in this category
        print '%sy %sd %sh %sm %ss' % (item[5][0], item[5][1], item[5][2], item[5][3], item[5][4])
    print '-'*width
    return

