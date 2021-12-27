import os


def clear():
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")
