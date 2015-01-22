#!/usr/bin/python

from sire.misc import *
import sire.shared
shared.opt = misc.Misc.miscfunctions()

from sire.helpers import *
import sys

from sire.list import list as do_list, list_duplicates, list_categories
from sire.move import move
from sire.change import change
from sire.add import add
from sire.delete import delete
from sire.info import info
from sire.find import approxsearch
from sire.score import set_score
from sire.dbman import db_restore


def init():
    import sire.dbman as dbman
    import os
    # Check if config and database files exists and are read- and writeable.
    if not os.path.exists(Misc.CONFIG):
        text_error(Misc.ERROR["config"])
        sys.exit(1)

    # Read the config file.
    shared.config = parse_config(Misc.CONFIG)
    shared.db = dbman.connect()
    return


# Handle command line arguments.
def entrypoint():
    from sire.args import parseargs
    init()
    do = parseargs()
    opt = shared.opt

    if do.version is True:
        version()
        return

    # TODO: fix this, not needed
    opt.set('daysago', do.daysago)
    opt.set('id', not do.noid)
    opt.set('color', do.printcolor)
    opt.set('category', do.printcat)
    opt.set('score', do.noscore)
    opt.set('newline', do.nonewline)
    opt.set('verbose', do.verbose)
    opt.set('profile', do.profile)
    opt.set('pretend', do.pretend)
    opt.set('edits', 50)

    # will negate any extra specified of these
    if do.hide:
        opt.set('id', do.noid)
        opt.set('color', not do.printcolor)
        opt.set('newline', ', ')
        opt.set('category', not do.printcat)

    if do.force:
        opt.set('force', True)

    if do.sort:
        opt.set('sort', do.sort)

    if do.edits:
        opt.set('edits', do.edits)

    # Options that do things comes last.
    if do.restore:
        return db_restore()

    if do.find:
        return approxsearch(opt.get('edits'), do.find)

    if do.move:
        return move(do.move, do.dest)

    if do.change:
        return change(do.change, do.dest)

    if do.delete:
        return delete(do.delete)

    if do.info:
        return info(do.info, do.dest)

    if do.add:
        return add(do.add, do.dest)

    if do.score:
        return set_score(do.dest, do.score)

    if do.listdupe:
        return list_duplicates(do.dest)

    if do.listcats:
        return list_categories(do.dest)
        
    # Nothing else was done, so list a category.
    return do_list(do.list)

