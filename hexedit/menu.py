from hexedit.structures.fat32 import Fat32
from hexedit.structures.ntfs import NTFS
from hexedit.viewer import Viewer
from hexedit.structures.mbr import MBR


class Menu:
    _MENU_MESSAGE = """
===== 짱짱짱 에디터 =====
0. 종료
1. 파일 경로 설정 [{file_status}]
2. 10육진su 보기
3. 파티션 정보
4. FAT32 파티션 보기
5. NTFS 파티션 보기"""

    def __init__(self, viewer: Viewer):
        self.__viewer = viewer

    def show(self):
        print(self._MENU_MESSAGE.format(file_status=self.__viewer.get_filename()))

    def select(self):
        self._select: int = int(input("> "))

    def execute(self):
        selected = self._select
        if 0 == selected:
            print("Good Byte!!")
            exit(0)

        elif 1 == selected:
            self.__viewer.open(input("File path > "))

        elif 2 == selected:
            sector = int(input("Sector Position > "))
            self.__viewer.show(sector)

        elif 3 == selected:
            partition_entries = MBR.from_reader(self.__viewer).PARTITION_TABLE_ENTRIES
            for index, partition_entry in enumerate(partition_entries):
                print("Partition", index + 1, ":")
                print(partition_entry)

        elif 4 == selected:
            mbr = MBR.from_reader(self.__viewer)
            fat32s = Fat32.from_reader_with_mbr(self.__viewer, mbr)
            for fat32 in fat32s:
                print(fat32)

        elif 5 == selected:
            mbr = MBR.from_reader(self.__viewer)
            ntfss = NTFS.from_reader_with_mbr(self.__viewer, mbr)
            for ntfs in ntfss:
                print(ntfs)
