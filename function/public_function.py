import os
import platform

def emty_list(n):
    return [None for x in range(n)]

def clear_terminal():
    if "Windows"==platform.system():
        os.system('cls')
    else:
        os.system('clear')
