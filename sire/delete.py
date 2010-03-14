
from sire.printer import *
from sire.helpers import *
from sire.misc import *

# Delete an item from the database.
def delete(ids):
    from sire.helpers import *
    alldbs = get_all_categories()
    ids = str(ids).split(',')

    # backup db if something goes wrong
    db_backup()

    for id in ids:
        # works for non-range IDs too
        if not is_valid_id(id):
            continue

        # hack to get the for loop to go once if no range was used
        idrange = [id, id]
        if '-' in id:
            idrange = id.split('-')

        # only happens once if not a range
        for i in range(int(idrange[0]), int(idrange[1]) + 1):
            delete_id(str(i))
    return

def delete_id(id):
    import sire.dbman as dbman
    result = dbman.get_item_with_id(id)

    # doesn't exist
    if len(result) == 0:
        text_warning(Misc.ERROR["item"] % c(id))
        return

    cat = result[0][3]
    title = format_text_out(result[0][1])
    dbman.delete(id)
    print_info('delete', (id, title, cat, result[0][2]))
    return

