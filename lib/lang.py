from lib import runtime_values

def text(text: str):
    text_split = text.split(".")
    if len(text_split) == 2:
        return runtime_values.lang[text_split[0]][text_split[1]]
    elif len(text_split) == 3:
        return runtime_values.lang[text_split[0]][text_split[1]][text_split[2]]
    else:
        return runtime_values.lang[text]