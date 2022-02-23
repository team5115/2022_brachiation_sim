import re


# def escape_lots_of_stuff(a_string):
#      escaped = a_string.translate(str.maketrans({"-":  r"\-",
#                                                  "]":  r"\]",
#                                                  "\\": r"\\",
#                                                 "^":  r"\^",
#                                                  "$":  r"\$",
#                                                  "*":  r"\*",
#                                                  ".":  r"\."}))
     
#      escaped = re.escape(a_string)
#      return escaped

# def escape_underscores(a_string):
#      escaped = a_string.translate(str.maketrans({"_":  r"\\_"}))
     
#      escaped = re.escape(a_string)
#      return escaped

def replace_underscores(a_string):     
     return a_string.replace("_", " ")

def escape_underscores(a_string):     
     return a_string.replace("_", "\\_")


 
# formatting_url = re.sub(
#     'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'[\g<0>]', original_text)
# escaping_char = formatting_url.replace('*', '\*').replace('_', '\_')
