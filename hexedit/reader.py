from io import FileIO
from hexedit.decorators import check_opened

class Reader:
    SECTOR_SIZE = 512

    def __init__(self):
        self._file: FileIO = None

    def open(self, filename: str):
        try:
            self._file = open(filename, "rb")
            return True
        except FileNotFoundError:
            return False

    @check_opened
    def close(self):
        self._file.close()

    @check_opened
    def _read(self, sector: int, with_pad: bool=True):
        file = self._file
        file.seek(sector * self.SECTOR_SIZE)
        data = file.read(self.SECTOR_SIZE)
        if with_pad:
            data += b'\x00' * (self.SECTOR_SIZE - len(data))
        return data
