class PartitionTableEntry:
    def __init__(
        self,
        BOOT_INDICATOR: int,
        START_CHS_ADDRESS: int,
        PARTITION_TYPE: int,
        END_CHS_ADDRESS: int,
        START_LBA_ADDRESS: int,
        TOTAL_SECTORS: int,
    ):
        self.BOOT_INDICATOR = BOOT_INDICATOR
        self.START_CHS_ADDRESS = START_CHS_ADDRESS
        self.PARTITION_TYPE = PARTITION_TYPE
        self.END_CHS_ADDRESS = END_CHS_ADDRESS
        self.START_LBA_ADDRESS = START_LBA_ADDRESS
        self.TOTAL_SECTORS = TOTAL_SECTORS

    @staticmethod
    def from_bytes(raw: bytes):
        def to_int(raw: bytes) -> int:
            return int.from_bytes(raw, byteorder="little")

        return PartitionTableEntry(
            raw[0],
            to_int(raw[1:4]),
            raw[4],
            to_int(raw[5:8]),
            to_int(raw[8:12]),
            to_int(raw[12:]),
        )

    def __str__(self):
        return """
        Boot Flag:  {}
        CHS Start:  {:06X}
        Type:       {:02X}
        CHS End:    {:06X}
        LBA Start:  {}
        Size:       {}MB
        """.format(
            self.BOOT_INDICATOR,
            self.START_CHS_ADDRESS,
            self.PARTITION_TYPE,
            self.END_CHS_ADDRESS,
            self.START_LBA_ADDRESS,
            self.TOTAL_SECTORS * 512 // 1024 // 1024,
        )
