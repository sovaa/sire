
import sys
from sire.misc import Misc
C = Misc.C
ERROR = Misc.ERROR

# print and error (like 'No item with ID blalba')
def text_error(text):
    from sire.shared import opt
    if opt.get('verbose') is 0:
        return
    text = format_text_out(text)
    if opt.get('color'):
        print "%s%sError: %s%s" % (C["bold"], C["red"], C["default"], text)
    else:
        print "Error: " + text
    return

# print a warning. Sort of the same as error, duh, should remove one of them
def text_warning(text):
    from sire.shared import opt
    if opt.get('verbose') is 0:
        return
    text = format_text_out(text)
    if opt.get('color'):
        print "%s%sWarning: %s%s" % (C["bold"], C["yellow"], C["default"], text)
    else:
        print "Warning: " + text
    return

# print a notice (like 'Deleted item blabla' or 'Added item blabla')
def text_note(text):
    from sire.shared import opt
    text = format_text_out(text)
    if opt.get('color'):
        print "%s%sNote: %s%s" % (C["bold"], C["green"], C["default"], text)
    else:
        print "Note: " + text
    return

def text_info(text):
    text = format_text_out(text)
    print text
    return

# Print a category description using bold and colors.
def format_category_out(category):
    from sire.helpers import config_value
    from sire.shared import opt

    cattitle = config_value("categories." + category)
    if not cattitle:
        text_error(ERROR["catdesc"] % c(category))
        return

    if not opt.get('color'):
        return "  %s ('%s')\n" % (cattitle,  category)

    color = config_value("colors." + category)
    if not color:
        color = config_value("defval.color")
    if color in C:
        color = C[color]

    return "  %s%s%s ('%s')%s" %(C["bold"], color, cattitle, category, C["default"])

def color(text, color, bold = False):
    if not bold:
        return C[color] + text + C["default"]
    return C[color] + C["bold"] + text + C["default"]

# colorize some random text if told to in the config
def c(text):
    from sire.shared import opt
    if opt.get('color'):
        return C['g'] + str(text) + C['d']
    return text

# prints names of the shown columns when listing if chosen to in config
# TODO: do not need to send pid and pscore, use opt
def table_head(pid, pscore, cw):
    LABEL = ['TITLE', 'ID', 'SCORE']
    output = ''

    for i in range(3):
        cw[i] -= len(LABEL[i])
        if cw[i] % 2 != 0:
            cw[i] += 1

    for i in range(3):
        LABEL[i] = ' '*(cw[i]/2) + LABEL[i] + ' '*(cw[i]/2)

    if pid:
        output += LABEL[1][:-1] + '|'
    if pscore in [0, False]:
        output += LABEL[2] + ' |'
    output += LABEL[0]

    print output
    # sum of all label lengths
    print '-'*(sum([len(x) for x in LABEL]) + 2)
    return



# return bold version of the text if not color is false
def bold(string, color = True):
    if color:
        return C['bold'] + string + C['default']
    return string

# sql friendly format
def format_text_in(title):
    import re
    title = re.sub('"', "&#34;", title)
    title = re.sub("'", "&#39;", title)
    return title

# sql unfriendly format
def format_text_out(title):
    import re
    title = re.sub("&#34;", '"', title)
    title = re.sub("&#39;", "'", title)
    return title

def text_color(text, color, bold = False):
    if not bold:
        return C[color] + text + C["default"]
    return C[color] + C["bold"] + text + C["default"]

def print_info(type, values):
    from sire.helpers import format_time_passed, config_value
    from sire.printer import text_info, c

    style = config_value("general.printstyle")
    if type is 'delete':
        words = ('Deleted', 'from', 'red', True)
    elif type is 'add':
        words = ('Added', 'to', 'green', True)
    elif type is 'move':
        words = ('Moved', "from '%s' to" % c(values[4]), 'green', True)

    # default value
    if not style or style == '0':
        text_info(text_color(words[0], words[2], words[3]))
        text_info("ID       : %s" % c(values[0]))
        text_info("Title    : %s" % c(values[1]))
        text_info("Category : %s" % c(values[2]))
        if values[3]:
            text_info("Age      : %s" % format_time_passed(values[3]))
        print

    elif style == '1':
        text_info("%s item with ID '%s' and title '%s' %s category '%s'" % \
            (words[0], c(values[0]), c(str(values[1])), words[1], c(values[2])))
        if values[3]:
            text_info("It was in that category for %s" % format_time_passed(values[3]))

    elif style == '2':
        text_info("%s '%s' '%s' %s '%s'" % (words[0], c(values[0]), c(str(values[1])), words[1], c(values[2])))
        if values[3]:
            text_info("Age was %s" % format_time_passed(values[3]))

    elif style == '3':
        text_info("%s '%s' '%s' %s '%s'" % (words[0], c(values[0]), c(str(values[1])), words[1], c(values[2])))

    else:
        text_info("%s '%s'" % (words[0], c(str(values[1]))))
        
    return

