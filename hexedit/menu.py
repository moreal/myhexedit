from hexedit.viewer import Viewer


class Menu:
    _MENU_MESSAGE = """===== 짱짱짱 에디터 =====
    0. 종료
    1. 파일 경로 설정
    2. 10육진su 보기
    3. 파티션 정보"""

    def __init__(self, viewer: Viewer):
        self._viewer = viewer

    def show(self):
        print(self._MENU_MESSAGE)

    def select(self):
        self._select: int = int(input('> '))

    def execute(self):
        selected = self._select
        if 0 == selected:
            print("Good Byte!!")
            exit(0)

        elif 1 == selected:
            self._viewer.open(input("File path > "))

        elif 2 == selected:
            sector = int(input("Sector Position > "))
            self._viewer.show(sector)
