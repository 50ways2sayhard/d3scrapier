import re


def extract_url(raw):
    return re.search('\((.+)\)', raw).group(1)