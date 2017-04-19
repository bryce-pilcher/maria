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
