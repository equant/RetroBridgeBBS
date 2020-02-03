import os
import subprocess
import logging 

# Probably will implement/utilize the following info someday...
# https://stackoverflow.com/questions/984941/python-subprocess-popen-from-a-thread

def send_file(user_session, file_path, protocol=None):

    if protocol is None:
        protocol = user_session.bbs.default_transfer_protocol

    if protocol not in ['xmodem', 'ymodem', 'zmodem']:
        error_message = f"Error with test_modem_transfer(), unknown protocol: '{protocol}'"
        self.terminal.writeln(error_message)
        return False


    terminal = user_session.terminal
    terminal.writeln(f'Preparing to send {file_path} using {protocol}...')
    BAUD = str(terminal.device_io.comm.baudrate)
    DEV  = terminal.device_io.comm.name
    subprocess.call(["bash", "shell_scripts/send.sh", f"-{protocol}", DEV, BAUD, file_path])


def receive_file(user_session, file_name=None, protocol=None):

    if protocol is None:
        protocol = user_session.bbs.default_transfer_protocol

    if protocol not in ['xmodem', 'ymodem', 'zmodem']:
        error_message = f"Error with test_modem_transfer(), unknown protocol: '{protocol}'"
        self.terminal.writeln(error_message)
        return False

    upload_dir = user_session.bbs.archive_uploads_path

    terminal = user_session.terminal
    #terminal.writeln(f'Preparing to send {file_path} using {protocol}...')
    BAUD = str(terminal.device_io.comm.baudrate)
    DEV  = terminal.device_io.comm.name

    cwd = os.getcwd()

    #command_list = ["bash", f"cd {upload_dir} &&", "shell_scripts/receive.sh", f"-{protocol}", DEV, BAUD]
    command_list = ["bash", f"{cwd}/shell_scripts/receive.sh", f"-{protocol}", DEV, BAUD]
    logging.debug(" ".join(command_list))
    #subprocess.call(["bash", "shell_scripts/receive.sh", f"-{protocol}", DEV, BAUD, file_path])
    subprocess.call(command_list, cwd=upload_dir)
