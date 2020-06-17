def find_self_link(links_list: list):
    return_link = ""
    # Look for an explicit "self" link
    for link in links_list:
        if link.get("rel") == "self":
            return link.get("href")
    # Failing that, look for a link with no rel
    for link in links_list:
        if link.get("rel") is None:
            return link.get("href")
    # Failing that, return the first link
    if len(links_list) > 0:
        return links_list[0].get("href")
    # Failing even that, return empty string
    return ""