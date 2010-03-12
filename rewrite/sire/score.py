'''
Assign a score to and item.
'''
def set_score(db, config, id, score):
    if id is None:
        text_error(ERROR['destscore'])
        sys.exit(1)

    if not id_exists(db, id):
        text_error(ERROR['item'] % c(id))
        sys.exit(1)

    title = format_text_out(get_title_from_id(db, id))
    dbexec(db, "UPDATE item SET score = '%s' WHERE id = '%s'" % (score, id), None, True)
    text_note("Assigned score '%s' to item with ID '%s' and value '%s'." % (c(score), c(id), c(title)))
    return

