import getopt
from optparse import OptionParser
from optparse import OptionGroup

def parseargs():
    parser = OptionParser()
    htxt = {
        "--list":         "List the specified category. Comma-separated values and negations can be used here.",
        "--add":          "Add an item to a category. If no destination (category in this case) is specified (using --destination, -D) the default add " + \
                          "category will be used (specified in config file).",
        "--destination":  "Specify to which category an item is to be added/moved/etc., or a new value to be used when using --change, -c.",
        "--delete":       "Delete items with certain IDs. Comma-separated values, negations and ranges can be used here.",
        "--info":         "Show formated table with information about items with the specified comma separated IDs. Can be used together with -d, --destination to " + \
                          "specify which categories to look in, or not look in. Comma-separated values, negations and ranges can be used here.",
        "--find":         "Find titles matching specified value. Using fuzzy string searching, can be customized in the config file.",

        "--move":         
"""
Move title with specified ID to another category. Comma-separated values, negations and ranges can be used here. If no destination
(category in this case) is specified (using --destination, -D) the default move category will be used (specified in config file).
""",

        "--change":       
"""
Change the title of one or more items with the specified IDs to a new value, specified using --destination, -D. Here the destination 
can contain %(#) for self referencing, or %(123) for referencing title with ID 123. See the examples for more information. The IDs can
be specified using comma-separated values, negations and ranges.
""",

        "--no-id":        "Hide ID when listing, even if specified in config file to show them.",
        "--no-category":  "Hide category title when listing a category.",
        "--no-color":     "Don't use any color/bold when printing.",
        "--no-newline":   "Don't print newlines. Use ', ' instead of '\\n' (newline) when listing one or more categories.",
        "--no-score":     "Don't print score when listing. Overrides setting in configuration.",
        "--show-score":   "Show score when printing. Overrides setting in configuration.",
        "--force":        "Ignore warnings and continue execution anyway.",
        "--version":      "Show the current version.",
        "--profile":      "Use an alternative profile. A different profile defines a whole different set of items.",
        "--edits":        "Specify the number of allowed edits to the search value when using --find, -f.",
        "--quiet":        "Be quiet. Don't print notices or warnings. Errors will still be printed.",
        "--verbose":      "Be verbose. Print notices, warnings and errors.",
        "--hide-all":     "Same as -LINC (--no-color --no-id --no-newline --no-category).",
        "--pretend":      "Only pretend to do the speicified things.",
        "--days-ago":     "Only list items added no longer ago than this.",
        "--sort":         "Specify what to sort by. Overrides setting in configuration.",
        "--score":        "Assign a score to an item.",
        "--restore":      "Restore the DB from the backup."
    }
    
    group = OptionGroup(parser, "Hide and/or change output options", "These options will hide or change different types of output.")
    group.add_option("-I", "--no-id", action = "store_true", default = False, dest = "noid", help = htxt["--no-id"])
    group.add_option("-C", "--no-category", action = "store_false", default = True, dest = "printcat", help = htxt["--no-category"])
    group.add_option("-L", "--no-color", action = "store_false", default = True, dest = "printcolor", help = htxt["--no-color"])
    group.add_option("-N", "--no-newline", action = "store_false", default = True, dest = "printnewline", help = htxt["--no-newline"])
    group.add_option("-S", "--no-score", action = "store_true", dest = "noscore", default = None, help = htxt["--no-score"])
    group.add_option("-W", "--show-score", action = "store_false", dest = "noscore", default = None, help = htxt["--show-score"])
    group.add_option("-H", "--hide-all", action = "store_true", default = False, dest = "hide", help = htxt["--hide-all"])
    group.add_option("-q", "--quiet", action = "store_const", const = 0, dest = "verbose", default = 1, help = htxt["--quiet"])
    group.add_option("-v", "--verbose", action = "store_const", const = 2, dest = "verbose", default = 1, help = htxt["--verbose"])
    parser.add_option_group(group)
    
    group = OptionGroup(parser, "Modify options", "These options will modify items in categories in some way.")
    group.add_option("-a", "--add", dest = "add", help = htxt["--add"], metavar = "TITLE")
    group.add_option("-d", "--delete", dest = "delete", help = htxt["--delete"], metavar = "ID1[,ID2[...]]")
    group.add_option("-m", "--move", type="int", dest = "move", help = htxt["--move"], metavar = "ID")
    group.add_option("-c", "--change", dest = "change", help = htxt["--change"], metavar = "ID1[,ID2[...]]")
    group.add_option("-b", "--restore", action = "store_true", dest = "restore", help = htxt["--restore"])
    parser.add_option_group(group)
    
    group = OptionGroup(parser, "Printing options", "These options only prints information and does not modify anything.")
    group.add_option("-f", "--find", dest = "find", help = htxt["--find"], metavar = "VALUE")
    group.add_option("-e", "--edits", type="int", dest = "edits", help = htxt["--edits"], metavar = "VALUE")
    group.add_option("-i", "--info", dest = "info", help = htxt["--info"], metavar = "ID1[,ID2[...]]")
    group.add_option("-l", "--list", dest = "list", help = htxt["--list"], metavar = "CATEGORY")
    group.add_option("-s", "--sort", action = "store", dest = "sort", help = htxt["--sort"])
    group.add_option("-V", "--version", action = "store_true", dest = "version", help = htxt["--version"])
    parser.add_option_group(group)
    
    group = OptionGroup(parser, "Other options", "Options that does not fit in any other option group and is usually used together with other options.")
    group.add_option("-D", "--destination", dest = "dest", help = htxt["--destination"], metavar = "VALUE")
    group.add_option("-O", "--score", dest = "score", help = htxt["--score"], metavar = "VALUE")
    group.add_option("-P", "--profile", dest = "profile", help = htxt["--profile"], metavar = "NAME")
    group.add_option("-F", "--force", action = "store_true", dest = "force", help = htxt["--force"])
    group.add_option("-p", "--pretend", action = "store_true", dest = "pretend", help = htxt["--pretend"])
    group.add_option("-y", "--days-ago", type = "int", dest = "daysago", help = htxt["--days-ago"], metavar = "DAYS")
    parser.add_option_group(group)
    
    return parser.parse_args()[0]

