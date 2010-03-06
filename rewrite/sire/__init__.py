#!/usr/bin/python

import opts, misc

def init():
    import os
    # Check if config and database files exists and are read- and writeable.
    print misc.__dict__
    if not os.path.exists(misc.Misc.CONFIG):
        text_error(ERROR["dbcat"])
        sys.exit(1)

    # Read the config file.
    config = parse_config(CONFIG)

    db = MySQLdb.connect(
        config["database.host"], 
        config["database.user"], 
        config["database.pass"], 
        config["database.name"]
    )

    return (config, db)

# Handle command line arguments.
def entrypoint():
    (config, db) = init()
    do = misc.args.parseargs()

    if do.pretend is True:
        misc.set('pretend', True)

    if do.version is True:
        version()
        return

    if do.daysago is not None:
        misc.set('daysago', do.daysago)

    if do.noid is True:
        misc.set('id', False)

    if do.printcolor is False:
        misc.set('color', False)

    if do.printnewline is False:
        misc.set('newline', False)

    if do.printcat is False:
        misc.set('category', False)

    if do.hide is True:
        misc.set('id', False)
        misc.set('color', False)
        misc.set('newline', False)
        misc.set('category', False)

    if do.verbose is not None:
        misc.set('verbose', do.verbose)

    if do.force is True:
        misc.set('force', True)

    if do.sort is not None:
        misc.set('sort', do.sort)
        
    # Will always either be True, False or None, even if not specified.
    misc.set('score', do.noscore)

    if do.edits is not None:
        misc.set('edits', do.edits)

    # Options that do things comes last.
    if do.restore is not None:
        db_restore(config)
        return

    if do.find is not None:
        approxsearch(db, config, misc.get('edits'), do.find)
        return

    if do.move is not None:
        move(db, config, do.move, do.dest)
        return

    if do.change is not None:
        change(db, config, do.change, do.dest, dbfile)
        return

    if do.delete is not None:
        delete(db, config, do.delete, dbfile)
        return

    if do.info is not None:
        info(db, config, do.info, do.dest)
        return

    if do.add is not None:
        add(db, config, do.add, do.dest)
        return

    if do.score is not None:
        set_score(db, config, do.dest, do.score)
        return
        
    # Nothing else was done, so list a category.
    list(db, config, do.list, do.dest)
    return
