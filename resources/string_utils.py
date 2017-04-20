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
