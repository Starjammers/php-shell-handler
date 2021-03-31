import argparse
from php_shell_interactor.php_shell_handler import PHP_Web_Shell_Handler


def main():
    arg_parser = argparse.ArgumentParser(description="Python based tool to interact with php web shells!")
    arg_parser.add_argument("-u", "--url", help=f"The URL location that your web shell will be uploaded to", required=True)
    arg_parser.add_argument("-p", "--param", help=f"The name of the php get parameter used in the php file uploaded (default of '{PHP_Web_Shell_Handler.DEFAULT_WEBSHELL_PARAM}' is used with the built in php shells that are suggested to be used")
    arg_parser.add_argument("--encoded", help=f"Decide whether communication with the shell will be encoded or not (default is not encoded, but add --encoded to allow encoded shells)", nargs='*')
    arg_parser.add_argument("-o", "--os", help=f"Set the operating system to either WINDOWS or UNIX for C2 functionality to work correctly")

    args = arg_parser.parse_args()

    url = args.url

    php_param_name = None
    if args.param:
        php_param_name = args.param

    encoded = False
    if args.encoded != None:
        encoded = True

    if args.os:
        os = args.os
    else:
        os = PHP_Web_Shell_Handler.DEFAULT_OS

    handler = PHP_Web_Shell_Handler(url, encoded=encoded, webshell_param=php_param_name, os=os)    
    handler.shell()


if __name__ == '__main__':
    main()
