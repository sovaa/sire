# Do an approximate string search using the Apse package.
def approxsearch(db, conf, edits, sstr):
    import Apse # for approximate searching
    reslist = []
    reps = {'.':' ', '_':' ', '-':' '}

    if edits is 0 and "find.edits" in conf.keys():
        edits = int(conf["find.edits"])
    
    if edits > 10:
        edits = 10
    elif edits < 0:
        edits = 0

    db = dbman.get_items()
    print db
    for search in [sstr]:
        # allow at most 'edits' edits 
        ap = Apse.Approx(search.lower(), edit=edits)

        # messy, I know
        for key in db: 
            val = key[1]
            id = key[0]
            cat = key[3]
            val_orig = val.lower()
            fnd = bool(ap.match(val_orig))
            dst = ap.dist(val_orig)
            res = (id, val, dst, cat)

            if fnd and val not in reslist:
                reslist.append(res)

            # Try to match if we replace some characters.
            val_rep = replace_all(val.lower(), reps)
            fnd_rep = bool(ap.match(val_rep))
            dst_rep = ap.dist(val)
            res_rep = (id, val, dst_rep, cat)

            if not fnd and fnd_rep and val not in reslist:
                reslist.append(res_rep)

    if reslist != []:
        showcats = False
        if "find.showcats" in conf.keys() and conf["find.showcats"] == '1':
            showcats = True

        text_note("Match found. Best match at the top.\n")
        old_cat = None

        if showcats:
            reslist.sort(lambda x,y:cmp(x[3],y[3]))
            reslist.reverse()
        
        else:
            reslist.sort(lambda x,y:cmp(x[2],y[2]))
            reslist.reverse()

        for res in reslist:
            if showcats:
                if old_cat is None or res[3] != old_cat:
                    print
                    if misc.get('category'):
                        print format_category_out(res[3], conf)
                    old_cat = res[3]

            # Make titles aligned.
            spacer = ' '*(5 - len(str(res[0])))

            # Showing ID when listing is optional.
            if "general.showid" not in conf.keys() or not misc.get('id'):
                print res[1]
            
            elif conf["general.showid"] == '1':
                print "%s%s%s %s: %s" % (C['bold'], res[0], C['default'], spacer, format_text_out(res[1]))
    else:
        text_warning("No matches found!")
    return

