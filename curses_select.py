import time
import math
import string
from curses import wrapper
import curses


def select_option(options_list):
    wrapper(_select_option, options_list)


def _select_option(stdscr, options_list):
    stdscr.clear()

    select_size = 50
    size_of_room_above_search = 2
    selected_x = 0
    selected_y = 0

    old_scr_height = None
    old_scr_width = None

    search_string = ''
    filtered_options_list = list(_filter_list(options_list, search_string))
    old_filtered_options_list = filtered_options_list.copy()

    options_grid = None
    row_height = None
    last_col_row_height = None
    col_width = None

    while True:
        scr_height, scr_width = stdscr.getmaxyx()
        reset_necessary = False

        if scr_height != old_scr_height or scr_width != old_scr_width:
            old_scr_width = scr_width
            old_scr_height = scr_height
            reset_necessary = True

        if filtered_options_list != old_filtered_options_list:
            old_filtered_options_list = filtered_options_list.copy()
            reset_necessary = True

        if reset_necessary:
            options_grid = list(_split_list(filtered_options_list, max(1, math.floor(scr_width / select_size))))

            row_height = len(options_grid[0])
            last_col_row_height = len(options_grid[len(options_grid)-1])
            col_width = len(options_grid)

            selected_x = 0
            selected_y = 0

        y_offset = min(max((row_height+size_of_room_above_search)-scr_height, 0), selected_y)

        stdscr.erase()
        for x in range(0, col_width):
            for y in range(0, len(options_grid[x])):  # ostatnia ma inny rozmiar więc zawsze sprawdzamy długość kolumny
                draw_y = y - y_offset + size_of_room_above_search

                if draw_y >= scr_height or draw_y < size_of_room_above_search:
                    continue
                elif selected_x == x and selected_y == y:
                    stdscr.addnstr(draw_y, x*select_size, options_grid[x][y], select_size-2, curses.A_REVERSE)
                else:
                    stdscr.addnstr(draw_y, x*select_size, options_grid[x][y], select_size-2)

        stdscr.addnstr(0, 0, search_string, scr_width-2)
        stdscr.refresh()

        char = _get_char(stdscr)

        if char == curses.KEY_RIGHT:
            selected_x = (selected_x+1) % col_width
        if char == curses.KEY_LEFT:
            selected_x = (selected_x-1) % col_width
        if char == curses.KEY_DOWN:
            if selected_x == col_width-1:
                selected_y = (selected_y+1) % last_col_row_height
            else:
                selected_y = (selected_y+1) % row_height
        if char == curses.KEY_UP:
            if selected_x == col_width-1:
                selected_y = (selected_y-1) % last_col_row_height
            else:
                selected_y = (selected_y-1) % row_height

        if selected_x == col_width-1 and selected_y >= last_col_row_height:
            selected_y = last_col_row_height-1

        if char == ord('\n'):
            return options_grid[selected_x][selected_y]

        elif chr(char) in string.printable:
            search_string += chr(char)
            filtered_options_list = list(_filter_list(options_list, search_string))
        elif char == curses.KEY_BACKSPACE:
            search_string = search_string[:-1]
            filtered_options_list = list(_filter_list(options_list, search_string))


def _filter_list(l, search):
    for s in l:
        if not search or search.lower() in s.lower():
            yield s


def _get_char(stdscr):
    stdscr.nodelay(1)
    while True:
        char = stdscr.getch()

        if char != -1:
            return char

        time.sleep(0.01)


def _split_list(l, n):
    col_size = math.ceil(len(l) / n)
    return _chunks(l, col_size)


def _chunks(l, n):
    if len(l) > 1:
        for i in range(0, len(l), n):
            yield l[i:i + n]
    else:
        yield l
