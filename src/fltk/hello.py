"""Main code file"""
from os import getlogin
from datetime import datetime
from rich import print


def hello(name: str = getlogin()) -> str:
    """Example function to say hello. To be deleted.
    
    This function can be run from the cmd prompt with 'py -m fltk'.

    Args:
        name (str, optional): Name to use to say hello. Default is current user.

    Returns:
        str: Hello message.
    """
    time_stamp: str = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    msg: str = " ".join(["\u2139", " Hello", name, time_stamp])
    msg = "[cyan]" + msg + "[/cyan]"
    print(msg)
    return msg


# if __name__ == "__main__":
#     hello()
