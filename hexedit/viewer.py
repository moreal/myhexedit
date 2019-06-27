from hexedit.reader import Reader
from hexedit.decorators import check_opened


class Viewer(Reader):
    @check_opened
    def show(self, sector: int):
        import string

        available_characters = string.printable[:-5]

        SECTOR_SIZE = self.SECTOR_SIZE

        data = self._read(sector)

        print("# HEXAEDIT # " + " ".join([format(x, "02X") for x in range(16)]))

        for i in range(0, SECTOR_SIZE, 16):
            line_data = data[i : i + 16]
            print(
                "  {address}   {hex_values} {asciis}".format(
                    address=format(SECTOR_SIZE * sector + i * 16, "08X"),
                    hex_values=" ".join([format(x, "02X") for x in line_data]),
                    asciis="".join(
                        [
                            chr(x) if chr(x) in available_characters else "."
                            for x in line_data
                        ]
                    ),
                )
            )

        print()  # next line
