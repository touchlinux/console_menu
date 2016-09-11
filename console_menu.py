#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Topmenu and the submenus are based of the example found at this location http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/
# The rest of the work was done by Matthew Bennett and he requests you keep these two mentions when you reuse the code :-)
# Code has been improved by Andrew Scheller on https://gist.github.com/abishur/2482046
# Touchlinux refactored code to make it easy to work with other python modules

from time import sleep
import curses, os # curses is the interface for capturing key presses on the menu, os launches the files

MENU = "menu"
EXITMENU = "exitmenu"
FUNCTION = "function"

class Menu(object):
    def __init__(self):
        self.screen = curses.initscr() # initializes a new window for capturing key presses
        curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
        curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
        curses.start_color() # Lets you use colors when highlighting selected menu option
        self.screen.keypad(1) # Capture input from keypad

        # Change this to use different colors when highlighting
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW) # Sets up color pair #1, it does black text with white background

    def run(self, menu, parent):
        """
        This function displays the appropriate menu and returns the option selected
        """
        # work out what text to display as the last menu option
        if parent is None:
            lastoption = "Exit"
        else:
            lastoption = "Return to %s menu" % parent['title']

        optioncount = len(menu['options']) # how many options in this menu

        pos = 0 # Index of the hightlighted menu option.
                # When run is called, position starts from 0.
                # When run ends the position is returned and tells the program what option the user selected.
        oldpos = None # Used to prevent the screen being re-drawn every time
        x = None # Control for while loop, let you scroll through options until return key is pressed.

        # Loop until return key is pressed
        while x != ord('\n'):
            if pos != oldpos:
                oldpos = pos
                self.screen.border(0)
                self.screen.addstr(2, 2, menu['title'], curses.A_UNDERLINE) # Title for this menu
                self.screen.addstr(4, 2, menu['subtitle'], curses.A_BOLD) # Subtitle for this menu

                # Display all the menu items, showing the 'pos' item highlighted
                for index in range(optioncount):
                    textstyle = curses.A_NORMAL
                    if pos == index:
                        textstyle = curses.color_pair(1)
                    self.screen.addstr(5+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
                # Now display Exit/Return at bottom of menu
                textstyle = curses.A_NORMAL
                if pos == optioncount:
                    textstyle = curses.color_pair(1)
                self.screen.addstr(5+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
                self.screen.refresh()
                # finished updating screen

            x = self.screen.getch() # Gets user input

            # What is user input?
            if x >= ord('1') and x <= ord(str(optioncount+1)):
                pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
            elif x == 258: # down arrow
                if pos < optioncount: pos += 1
                else: pos = 0
            elif x == 259: # up arrow
                if pos > 0: pos += -1
                else: pos = optioncount

        # return index of the selected item
        return pos

    def process(self, menu, funcs, parent=None):
        '''
        This function calls showmenu and then acts on the selected item
        '''
        optioncount = len(menu['options'])
        exitmenu = False

        while not exitmenu: # Loop until the user exits the menu
            getin = self.run(menu, parent)
            if getin == optioncount:
                exitmenu = True
            elif menu['options'][getin]['type'] == FUNCTION:
                curses.def_prog_mode()    # save curent curses environment
                fname = menu['options'][getin]['fname']
                result = funcs[fname]() # Execute function HE
                self.screen.addstr(3,2, "Result of %s : %s" % (fname, result), curses.A_STANDOUT)
                self.screen.refresh()
                curses.reset_prog_mode()   # reset to 'current' curses environment
                curses.curs_set(1)         # reset doesn't do this right
                curses.curs_set(0)
            elif menu['options'][getin]['type'] == MENU:
                self.screen.clear() # clears previous screen on key press and updates display based on pos
                self.process(menu['options'][getin], funcs, menu) # display the submenu
                self.screen.clear() # clears previous screen on key press and updates display based on pos
            elif menu['options'][getin]['type'] == EXITMENU:
                exitmenu = True

    def cleanup(self):
        curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
        os.system('clear')

# Main program
if __name__ == "__main__":
    def your_code_example():
        return "Your code..."

    menu_data = {
    'title': "Console menu", 'type': MENU, 'subtitle': "Please select an option...",
    'options':[
        {'title': "Option 1", 'type': FUNCTION, 'fname': 'your_code_example'},
        {'title': "Option 2", 'type': MENU, 'subtitle': "Please select an option...",
         'options': [
             {'title': "Option 2.1", 'type': FUNCTION, 'fname': 'your_code_example'},
         ]
        },
    ]
    }

    funcs = {'your_code_example': your_code_example}

    menu = Menu()
    menu.process(menu_data, funcs)
    menu.cleanup()

