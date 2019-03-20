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

    @check_opened
    def show(self, sector: int):
        import string
        available_characters = string.printable[:-5]

        SECTOR_SIZE = self.SECTOR_SIZE

        data = self._read(sector)

        print("# HEXAEDIT # " + " ".join([format(x,'02X') for x in range(16)]))

        for i in range(0, SECTOR_SIZE, 16):
            line_data = data[i:i+16]
            print("  {address}   {hex_values} {asciis}".format(
                address = format(SECTOR_SIZE * sector + i * 16, '08X'),
                hex_values = " ".join([format(x, '02X') for x in line_data]),
                asciis = "".join([chr(x) if chr(x) in available_characters else '.' for x in line_data])
            ))

        print()  # next line
