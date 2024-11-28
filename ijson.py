import os
import json
import sys
import curses

class MatchingBraceNotFoundError(Exception):
    """
    Custom error indicating that a search for a matching brace
    returned no results.
    """

    def __init__(self, message, additional_info=None):
        super().__init__(message)
        self.additional_info = additional_info


def load(file_path="./sample.json"):
    contents = {}
    with open(file_path, 'r') as file:
        contents = json.load(file)
    return contents

def init():
    data = load()
    # curses.wrapper(explore)
    d_str = json.dumps(data, indent=4)
    sample_arr = (d_str).split("\n")
    cache = cacheDepthChars(sample_arr)
    print(f"sample data:\n{d_str}\n")
    print("brace cache for sample data:")
    print(json.dumps(cache, indent=4))

# TODO: refac to use 'in' for simplicity
def hasOpenBrace(line):
    open_square = -1
    try:
        open_square = line.index("[")
    except:
        pass
    
    open_curly = -1
    try:
        open_curly = line.index("{")
    except:
        pass
    
    return (open_curly + open_square) > -2


# TODO: refac to use 'in' for simplicity
def hasCloseBrace(line):
    close_square = -1
    try:
        close_square = line.index("]")
    except:
        pass

    close_curly = -1
    try:
        close_curly = line.index("}")
    except:
        pass

    return (close_curly + close_square) > -2

def get_matching_brace_row(lines, b_type, start_row):
    match_map = {
        "{": "}",
        "}": "{",
        "[": "]",
        "]": "["
    }
    for i, line in enumerate(lines):
        target_type = match_map[b_type]
        if b_type in ["[", "{"] and i < start_row:
            continue
        elif b_type in ["]", "}"] and i >= start_row:
            raise MatchingBraceNotFoundError(f"No matching brace was found to close the {b_type} on line {start_row}")
        if target_type in line:
            return i
    raise MatchingBraceNotFoundError(f"No matching brace was found to close the {b_type} on line {start_row}")

def cacheDepthChars(stringified_json_arr=[]):
    """
    Cache the (row, col) location of '{}' and '[]' chars for easier
    depth-based brace highlighting
    """
    arr = stringified_json_arr
    cache = {}
    keys = cache.keys()
    for i, line in enumerate(arr):
        if i not in keys:
            cache[i] = {}
            keys = cache.keys()
            
        if hasOpenBrace(line):
            b_type = "["
            col = 0
            if "[" in line:
                col = line.index("[")
            elif "{" in line:
                b_type = "{"
                col = line.index("{")
            matching_row = get_matching_brace_row(arr, b_type, i)
            cache[i]['type'] = b_type
            cache[i]['col'] = col
            cache[i]['matching_row'] = matching_row

        if hasCloseBrace(line):
            b_type = "]"
            col = 0
            if "]" in line:
                col = line.index("]")
            elif "}" in line:
                b_type = "}"
                col = line.index("}")
            matching_row = get_matching_brace_row(arr, b_type, i)
            cache[i]['type'] = b_type
            cache[i]['col'] = col
            cache[i]['matching_row'] = matching_row
    return cache

def explore(stdscr):
    cursor_location = 0
    invis = 0
    depth = 0
    curses.curs_set(invis)
    data = load()
    stringified_data = json.dumps(data, indent=4)
    arr_data = stringified_data.split("\n")
    row_count = len(arr_data)
    brace_cache = cacheDepthChars(arr_data)

    while True:
        stdscr.clear()
        stdscr.addstr(f"Press 'q' to quit... (depth: {depth} - braces on )\n\n")


        
        for i, line in enumerate(arr_data):
            # Take the 'quit' reminder message into account
            if (i) == cursor_location:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(line)
                stdscr.attroff(curses.A_REVERSE)
            else:
                try:
                    stdscr.addstr(line)
                except:
                    msg = "Error adding line to screen - " + line
                    raise RuntimeError(msg)
            stdscr.addstr('\n')
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('q'):
            break

        elif key == 27: #ESC
            break 

        elif key == curses.KEY_UP:
            if cursor_location > 0:
                if hasCloseBrace(arr_data[cursor_location]):
                    depth += 1

                cursor_location -= 1

                if hasOpenBrace(arr_data[cursor_location]):
                    depth -= 1

        elif key == curses.KEY_DOWN:
            if cursor_location < (row_count - 1):
               if hasOpenBrace(arr_data[cursor_location]):
                   depth += 1

               cursor_location += 1

               if hasCloseBrace(arr_data[cursor_location]):
                   depth -= 1



init()
