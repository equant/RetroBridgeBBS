
class Menu2(object):

    global_commands_list = [
            {
                   "key" : 'Q',
                  "label": "Quit",
                    "do" : "quit",
                  "test" : None,
              "category" : 'System',
            },
            {
                   "key" : '?',
                  "label": "Help",
                    "do" : 'help',
                  "test" : None,
              "category" : 'System',
            },
            {
                   "key" : 'S',
                  "label": "Settings",
                    "do" : RetroBridgeBBS.rooms.settings.Settings,
                  "test" : None,
              "category" : 'System',
            },
    ]

    def __init__(self,user_session, menu_list, add_global_commands=True):
        self.user_session = user_session
        self.menu_list    = menu_list
        self.terminal     = self.user_session.terminal
        self.add_global_commands = add_global_commands
        return

    def handle_menu(self):

        # Create/Display Menu
        menu_list = self.menu_list
        for _idx, item in enumerate(menu_list):
            menu_line = "[" + str(_idx+1) + "] " + item[0]
            self.terminal.writeln(menu_line)
        self.terminal.write(">")

        # Wait for user input
        c = self.terminal.read()
        if c.isnumeric():
            selected_index = int(c) - 1

        # Validate User input
        try:
            menu_list[selected_index]
            valid_selection = True
            fn   = menu_list[selected_index][1]
            name = menu_list[selected_index][0]
        except IndexError:
            valid_selection = False
            fn   = None
            name = None
        except TypeError:
            valid_selection = False
            fn   = None
            name = None
        except UnboundLocalError:
            valid_selection = False
            fn   = None
            name = None

        # Send input feedback to terminal
        if valid_selection:
            self.terminal.writeln(f"[{c}] - {name}")
            #self.terminal.newline()
        else:
            self.terminal.writeln(f"[{c}] - Invalid!")
            #self.terminal.newline()

        return {'valid':valid_selection, 'fn':fn, 'name':name, 'c':c}
