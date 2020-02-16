import logging

class Menu(object):

    global_commands_list = [
            {
                   "key" : 'B',
                  "label": "Back",
               "command" : "back",
                  "test" : None,
              "category" : 'System',
            },
            {
                   "key" : '?',
                  "label": "Help",
               "command" : 'help',
                  "test" : None,
              "category" : 'System',
            },
            {
                   "key" : 'S',
                  "label": "Settings",
               "command" : None, #RetroBridgeBBS.rooms.settings.Settings,
                  "test" : None,
              "category" : 'System',
            },
    ]

    def __init__(self,user_session, commands_list, 
                      title=None, add_global_commands=True, menu_type=None,
                      menu_text=None, menu_intro=None, menu_outro=None):
        self.user_session        = user_session
        self.commands_list       = commands_list
        self.terminal            = self.user_session.terminal
        self.add_global_commands = add_global_commands
        self.menu_text           = menu_text
        self.title               = title
        self.menu_type           = menu_type
        self.menu_intro          = menu_intro
        self.menu_outro          = menu_outro
        return

    def make_command_entry_string(self, key, label):
        if label[0] == key:
            command_entry_string = f"[{key}]-"+label[1:]
        else:
            command_entry_string = f"[{key}] {label}"
        return command_entry_string


    def generate_menu_text(self):
        if self.menu_type == 'Download':
            return self.generate_download_menu_text()
        else:
            return self.generate_basic_menu_text()

    def generate_basic_menu_text(self):

        self.validate_menu_keys()   # doesn't just validate, but fixes them too.
        menu_text = self.terminal.make_box_hr()

        if self.title is not None:
            menu_text += self.terminal.make_box_title(self.title)
            menu_text += self.terminal.make_box_hr()

        _entries = []
        for _idx, command_entry in enumerate(self.commands_list):
            if command_entry['key'] is None:
                command_entry['key'] = str(_idx)

            _entries.append(self.make_command_entry_string(command_entry['key'], command_entry['label']))
        for _e in _entries:
            menu_text += self.terminal.make_box_string(_e)

        menu_text += self.terminal.make_box_hr()
        global_command_strings = []
        for global_entry in Menu.global_commands_list:
            global_command_strings.append(self.make_command_entry_string(global_entry['key'], global_entry['label']))

        menu_text += self.terminal.make_box_string(", ".join(global_command_strings))
        menu_text += self.terminal.make_box_hr()
        return menu_text

    def generate_download_menu_text(self):

        self.validate_menu_keys()   # doesn't just validate, but fixes them too.
        menu_text = self.terminal.make_box_hr()

        if self.title is not None:
            menu_text += self.terminal.make_box_title(self.title)
            menu_text += self.terminal.make_box_hr()

        if self.menu_intro is not None:
            import textwrap
            from textwrap import wrap, dedent
            intro_text = self.menu_intro
            intro_as_list = wrap(raw_desc, WIDTH-4)
            for line in desc_list:
                menu_text += self.terminal.make_box_string(line)
            menu_text += self.terminal.make_box_hr()

        for _idx, command_entry in enumerate(self.commands_list):
            if command_entry['key'] is None:
                command_entry['key'] = str(_idx)

            if self.command_entry_is_link(command_entry):
                link = command_entry['args']['link']

                first_line = self.make_command_entry_string(command_entry['key'], command_entry['label'])
                command_length = len(first_line)
                first_line += f" : {link.label:.20}"
                menu_text  += self.terminal.make_box_string(first_line)

                extra_info_list = [link.filesize] + link.notes
                extra_string = "/".join(extra_info_list)
                menu_text  += self.terminal.make_box_string(" " * command_length + " : " + extra_string)
            else:
                _string = self.make_command_entry_string(command_entry['key'], command_entry['label'])
                menu_text += self.terminal.make_box_string(_string)

        if self.menu_outro is not None:
            import textwrap
            from textwrap import wrap, dedent
            outro_text = self.menu_outro
            outro_as_list = wrap(raw_desc, WIDTH-4)
            for line in desc_list:
                menu_text += self.terminal.make_box_string(line)
            menu_text += self.terminal.make_box_hr()

        menu_text += self.terminal.make_box_hr()
        global_command_strings = []
        for global_entry in Menu.global_commands_list:
            global_command_strings.append(self.make_command_entry_string(global_entry['key'], global_entry['label']))

        menu_text += self.terminal.make_box_string(", ".join(global_command_strings))
        menu_text += self.terminal.make_box_hr()
        return menu_text

    def command_entry_is_link(self, command_entry):
        """
        entry = {
               "key" : None,
              "label": link.filename,
           "command" : self.get_file_from_archive,
              "args" : { 'link':link },
              "test" : None
        }
        """
        if 'args' in command_entry.keys():
            if 'link' in command_entry['args']:
                return True
            else:
                return False
        else:
            return False

    def validate_menu_keys(self):

        global_keys     = [x['key'] for x in Menu.global_commands_list]
        local_menu_keys = [x['key'] for x in self.commands_list]

        keys_in_both_lists = list(set(global_keys) & set(local_menu_keys))

        if len(keys_in_both_lists) > 0:
            logging.warning(f"There is a collision between the global and local commands {keys_in_both_lists} requested by this menu: {self}")
            for key in keys_in_both_lists:
                logging.info(f"Changing menu key: {key}")
                local_idx = local_menu_keys.index(key)
                self.commands_list[local_idx]['key'] = str(local_idx)

    def handle_menu(self):

        if self.menu_text is None:
            self.menu_text = self.generate_menu_text()

        #self.terminal.color_test()
        self.terminal.writeln(self.menu_text)
        c = self.terminal.character_prompt("RetroBridgeBBS")
        c = c.upper()

        logging.debug(f"Keypress: {c}")
        logging.debug(f"  length: {len(c)}")
        logging.debug(f"    type: {type(c)}")

        global_keys     = [x['key'] for x in Menu.global_commands_list]
        local_menu_keys = [x['key'] for x in self.commands_list]
        if c in global_keys:
            logging.debug(f"{c} found in global_keys: {global_keys}")
            global_command_idx = global_keys.index(c)
            command_entry = Menu.global_commands_list[global_command_idx]
            valid_selection = True
        elif c in local_menu_keys:
            logging.debug(f"{c} found in local_keys: {local_menu_keys}")
            local_command_idx = local_menu_keys.index(c)
            command_entry = self.commands_list[local_command_idx]
            valid_selection = True
        else:
            logging.debug(f"No valid command found for the key: [{c}] of type {type(c)}")
            valid_selection = False

        if valid_selection:
            logging.debug(f"User entered: {command_entry['label']}")
            self.terminal.writeln()
            self.terminal.writeln(f"{command_entry['label']}")
            command_entry['valid'] = True
        else:
            logging.debug(f"User entered: [{c}] is Invalid!")
            self.terminal.writeln(f"[{c}] is Invalid!")
            command_entry = dict()
            command_entry['valid'] = False

        return command_entry

                
#        # Send input feedback to terminal
#
#        return {'valid':valid_selection, 'fn':fn, 'name':name, 'c':c}
