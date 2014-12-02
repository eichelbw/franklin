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
            elif curr == None:
                del(curr)
        except AttributeError: # end of document
            break


def format_divs_for_EN(batch):
    """translates tags from frontend style to EN style. housekeeping."""
    update_divs = []
    batch = unpack_divs(batch)
    for div in batch:
        if div['id'] == 'tdcontent':
            # print "1"
            del(div['id'])
            for child in div.children:
                try:
                    if child["checked"] == "checked":
                        child["checked"] = "true"
                except:
                    pass
            update_divs.append(div)
        elif div['id'] == "tdheader":
            # print "2"
            del(div['id'])
            update_divs.append(div)
        elif div['id'] == 'nav' or div['id'] == 'tdholder':
            # print "3"
            pass
        else:
            print "unexpected div id encountered when reformatting for EN"
    return unicode.join(u'\n', map(unicode, update_divs))

def unpack_divs(batch):
    """adds divs contained in divs to the list of divs. ends up duplicating,
    but hey, let's be thorough here."""
    for index, div in enumerate(batch):
        try:
            if div.find("div").name == "div":
                batch.insert(index+1, div.find("div"))
        except:
            pass
    return batch
