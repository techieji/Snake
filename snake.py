import curses
from random import randint
from time import sleep
from collections import deque

SNAKE_CHAR = '█'
APPLE_CHAR = '█'
MARGIN     = 10

movement_dict = {
    curses.KEY_RIGHT: (0 , 1 ),
    curses.KEY_LEFT : (0 , -1),
    curses.KEY_UP   : (-1, 0 ),
    curses.KEY_DOWN : (1 , 0 )
}

opposite_dict = {
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_DOWN: curses.KEY_UP
}

num = 0

def text_corner(win, txt):
    ymax, xmax = win.getmaxyx()
    calc_x = xmax - 5 - len(txt)
    win.addstr(0, calc_x, '┌' + '─'*(len(txt) + 2) + '┐')
    win.addstr(1, calc_x, '│ ')
    win.addstr(1, calc_x + 2, txt, curses.color_pair(1))
    win.addstr(1, xmax - 3, ' │')
    win.addstr(2, calc_x, '└' + '─'*(len(txt) + 2) + '┘')

def main(stdscr):
    global num
    max_y, max_x = stdscr.getmaxyx()
    apple_pos = (randint(MARGIN, max_y - MARGIN), randint(MARGIN, max_x - MARGIN))
    snake = deque([(max_y//2, max_x//2)], maxlen=1)
    movement = curses.KEY_RIGHT
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.nodelay(1)
    while True:
        sleep(1/30)
        c = stdscr.getch()
        if c == 113:        # 'q'
            return
        if c != curses.ERR and c in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN] and opposite_dict[movement] != c:
            movement = c
        delta = movement_dict[movement]
        lastelem = snake[-1]
        snake.append((lastelem[0] + delta[0], lastelem[1] + delta[1]))
        if snake[-1] in list(snake)[:-1]: return
        stdscr.erase()
        text_corner(stdscr, f'Length: {num}')
        stdscr.addstr(*apple_pos, APPLE_CHAR, curses.color_pair(1))
        for x in snake:
            try:
                stdscr.addstr(*x, SNAKE_CHAR, curses.color_pair(2))
            except:
                return
        if snake[-1] == apple_pos:
            num += 1
            snake = deque(snake, maxlen=snake.maxlen + 1)
            apple_pos = (randint(MARGIN, max_y - MARGIN), randint(MARGIN, max_x - MARGIN))

while True:
    curses.wrapper(main)
    s = input(f'You ate {num} apples. Play again? [y/N] ')
    if (not s) or s[0].lower() != 'y':
        break
