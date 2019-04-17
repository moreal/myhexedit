#!/usr/bin/env python3

from hexedit.menu import Menu
from hexedit.viewer import Viewer


def main():
    viewer = Viewer()
    menu = Menu(viewer)
    while True:
        menu.show()
        menu.select()
        menu.execute()


if __name__ == "__main__":
    main()
