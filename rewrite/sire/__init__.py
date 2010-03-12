#!/usr/bin/python

import sire.shared
import sire.helpers
import sire.args

import sire.misc as misc
from sire.list import list
from sire.move import move
from sire.change import change

shared.opt = misc.Misc.miscfunctions()

def init():
    import MySQLdb
    import os
    # Check if config and database files exists and are read- and writeable.
    if not os.path.exists(misc.Misc.CONFIG):
        text_error(ERROR["dbcat"])
        sys.exit(1)

    # Read the config file.
    config = helpers.parse_config(misc.Misc.CONFIG)

    db = MySQLdb.connect(
        config["database.host"], 
        config["database.user"], 
        config["database.pass"], 
        config["database.name"]
    )
    shared.db = db
    shared.config = config
    return

# Handle command line arguments.
def entrypoint():
    init()
    do = args.parseargs()
    opt = shared.opt

    if do.pretend is True:
        opt.set('pretend', True)

    if do.version is True:
        version()
        return

    if do.daysago is not None:
        opt.set('daysago', do.daysago)

    if do.noid is True:
        opt.set('id', False)

    if do.printcolor is False:
        opt.set('color', False)

    if do.printnewline is False:
        opt.set('newline', False)

    if do.printcat is False:
        opt.set('category', False)

    if do.hide is True:
        opt.set('id', False)
        opt.set('color', False)
        opt.set('newline', False)
        opt.set('category', False)

    if do.verbose is not None:
        opt.set('verbose', do.verbose)

    if do.force is True:
        opt.set('force', True)

    if do.sort is not None:
        opt.set('sort', do.sort)
        
    # Will always either be True, False or None, even if not specified.
    opt.set('score', do.noscore)

    if do.edits is not None:
        opt.set('edits', do.edits)

    # Options that do things comes last.
    if do.restore is not None:
        db_restore()
        return

    if do.find is not None:
        approxsearch(opt.get('edits'), do.find)
        return

    if do.move is not None:
        move(do.move, do.dest)
        return

    if do.change is not None:
        change(do.change, do.dest, dbfile)
        return

    if do.delete is not None:
        delete(do.delete, dbfile)
        return

    if do.info is not None:
        info(do.info, do.dest)
        return

    if do.add is not None:
        add(do.add, do.dest)
        return

    if do.score is not None:
        set_score(do.dest, do.score)
        return
        
    # Nothing else was done, so list a category.
    list(do.list, do.dest)
    return
