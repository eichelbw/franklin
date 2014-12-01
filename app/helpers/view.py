###############################################################################
##
## helper functions for the flask views.
##
###############################################################################

def split_request(curr):
    """called on a tag (hopefully a h1) in the update request. returns siblings
    of the tag in sequence until it hits another h1, at which point it breaks
    out of the loop."""
    while True:
        curr = curr.next_sibling
        try:
            if curr.name == "h1": # reached the end of the current group o divs
                return
            elif curr.name == "div": # gets rid of br and None tag names
                yield curr
        except AttributeError: # end of document
            break


def format_divs_for_EN(batch):
    """translates tags from frontend style to EN style. housekeeping."""
    update_divs = []
    for div in batch:
        if div['id'] == 'tdcontent':
            print "1"
            del(div['id'])
            for child in div.children:
                try:
                    if child["checked"] == "checked":
                        child["checked"] = "true"
                except:
                    pass
            update_divs.append(div)
        elif div['id'] == "tdheader":
            print "2"
            del(div['id'])
            update_divs.append(div)
        elif div['id'] == 'nav' or div['id'] == 'tdholder':
            print "3"
            pass
        else:
            print "something's gone wrong in the sync route"
    # print unicode.join(u'\n', map(unicode, update_divs))
