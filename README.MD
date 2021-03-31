# PHP SHELL HANDLER by Watchdog

## WHAT IS IT?
PHP Shell Handler is a Python based, pseudo terminal, C2 like framework to interact with php web shells that you have managed to place onto a server. 

It offers encoded shell communication, so you needn't worry about special characters messing up your commands, as well as non encoded to interact with shells you may already have.

This package comes with pre-coded php shells that are offered to you on runtime of the tool. These shells will work right out of the box with this tool and it's C2 like built in commands. However, there is no reason why you couldnt have your own shells, or expand the ones provided.

It is designed to be flexible, and will continually update.

## python3 php_handler.py --help
```bash
usage: php_handler.py [-h] -u URL [-p PARAM]
                      [--encoded [ENCODED [ENCODED ...]]]

Python based tool to interact with php web shells!

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The URL location that your web shell will be uploaded
                        to
  -p PARAM, --param PARAM
                        The name of the php get parameter used in the php file
                        uploaded (default of 'phpshellcmd' is used with the
                        built in php shells that are suggested to be used
  --encoded
                        Decide whether communication with the shell will be
                        encoded or not (default is not encoded, but add --encoded to allow encoded shells)
```
