# print and error (like 'No item with ID blalba')
def text_error(text):
    text = format_text_out(text)
    if misc.get('verbose') is not 0:
        if misc.get('color'):
            print "%s%sError: %s%s" % (C["bold"], C["red"], C["default"], text)
        else:
            print "Error: " + text
    return

# print a warning. Sort of the same as error, duh, should remove one of them
def text_warning(text):
    text = format_text_out(text)
    if misc.get('verbose') is not 0:
        if misc.get('color'):
            print "%s%sWarning: %s%s" % (C["bold"], C["yellow"], C["default"], text)
        else:
            print "Warning: " + text
    return

def text_color(text, color, bold = False):
    if not bold:
        return C[color] + text + C["default"]
    return C[color] + C["bold"] + text + C["default"]

# colorize some random text if told to in the config
def c(text):
    if misc.get('color'):
        return C['g'] + text + C['d']
    return text

# return bold version of the text if not color is false
def bold(string, color = true):
    if color:
        return c['bold'] + string + c['default']
    return string

