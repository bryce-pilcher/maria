import re

file_name_regex = "\w+\.(?:py|java|h|cc|proto)"


def sanitize(string):
    if string is not None:
        string = string.strip(" ")\
            .replace("\'", "")\
            .replace("\\", "")\
            .replace("\"", "")\
            .replace("\n", " ")\
            .replace("\r", " ")
    else:
        string = ""
    return string


def list_to_string(list_of_things):
    if list_of_things is not None:
        return ", ".join(list_of_things)
    else:
        return ""


def regex_match(reg, string):
    regex = re.compile(reg)
    results = regex.findall(string)
    return results


def dec_to_percent(d):
    return '{0:3.2f}'.format(d*100) + "%"
