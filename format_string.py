def format_string(string, length=5):
    if(type(string) != str):
        string = str(string)
    if(type(length) != int):
        length = int(length)
    string_len = len(string)
    if string_len < length:
        string += " " * (length - string_len)
    return string
