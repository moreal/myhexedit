class PartitionTableEntry:
    def __init__(
        self,
        boot_indicator: int,
        start_chs_address: int,
        partition_type: int,
        end_chs_address: int,
        start_lba_address: int,
        total_sectors: int,
    ):
        self.BOOT_INDICATOR = boot_indicator
        self.START_CHS_ADDRESS = start_chs_address
        self.PARTITION_TYPE = partition_type
        self.END_CHS_ADDRESS = end_chs_address
        self.START_LBA_ADDRESS = start_lba_address
        self.TOTAL_SECTORS = total_sectors

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
