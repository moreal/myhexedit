from typing import Any, List

from pystructs import fields

from hexedit.enums.partition_type import PartitionType
from hexedit.reader import Reader
from hexedit.structures.mbr import MBR


class Fat32(fields.Struct):
    JUMP_BOOT_CODE: int = fields.IntField(size=3)
    OEM_ID: str = fields.StringField(size=8, encoding="ascii")
    BYTES_PER_SECTOR: int = fields.IntField(size=2)
    SEC_PER_CLUS: int = fields.IntField(size=1)
    RESERVED_SEC_COUNT: int = fields.IntField(size=2)

    NUM_FATS: int = fields.IntField(size=1)
    ROOT_ENTRY_COUNT: int = fields.IntField(size=2)
    TOTAL_SECTOR_16: int = fields.IntField(size=2)
    MEDIA: Any = fields.BytesField(size=1)
    FAT_SIZE_16: int = fields.IntField(size=2)
    SECTOR_PER_TRACK: int = fields.IntField(size=2)
    NUM_OF_HEADS: int = fields.IntField(size=2)
    HIDDEN_SECTOR: int = fields.Int32Field()

    TOTAL_SECTOR_32: int = fields.Int32Field()
    FAT_SIZE_32: int = fields.Int32Field()
    EXT_FLAGS: int = fields.IntField(size=2)
    FILE_SYS_VERSION: int = fields.IntField(size=2)
    ROOT_DIRECTORY_CLUSTER: int = fields.Int32Field()

    FILE_SYS_INFO: int = fields.IntField(size=2)
    BACKUP_BOOT_SEC: int = fields.IntField(size=2)
    RESERVED: bytes = fields.BytesField(size=12)

    DRV_NUM: int = fields.IntField(size=1)
    RESERV1: bytes = fields.BytesField(size=1)
    BOOT_SIG: int = fields.IntField(size=1)
    VOLUME_ID: int = fields.Int32Field()
    VOLUME_LABEL: str = fields.StringField(size=11)
    FILE_SYSTEM_TYPE: int = fields.StringField(8, encoding="ascii")

    PARTITION_INDEX: int  # index of related partition
    VBR_START: int
    FAT1_START: int
    FAT2_START: int
    ROOT_DIRECTORY_START: int

    @staticmethod
    def from_reader_with_mbr(reader: Reader, mbr: MBR) -> "List[Fat32]":
        partition_table_entries = mbr.PARTITION_TABLE_ENTRIES
        fat32s = list()

        for index, partition_table_entry in enumerate(partition_table_entries):
            if partition_table_entry.PARTITION_TYPE == PartitionType.FAT32_WITH_LBA:
                lba_start = partition_table_entry.START_LBA_ADDRESS
                raw = reader._read(lba_start)

                fat32 = Fat32(raw)
                fat32.initialize()

                fat32.PARTITION_INDEX = index

                fat32.VBR_START = lba_start
                fat32.FAT1_START = lba_start + fat32.RESERVED_SEC_COUNT
                fat32.FAT2_START = fat32.FAT1_START + fat32.FAT_SIZE_32
                fat32.ROOT_DIRECTORY_START = fat32.FAT2_START + fat32.FAT_SIZE_32

                fat32s.append(fat32)

        return fat32s

    def __str__(self):
        return f"""
        ------------- PARTITION [{self.PARTITION_INDEX+1}] -------------
        Byte Per Sector         {self.BYTES_PER_SECTOR}
        Sector Per Cluster      {self.SEC_PER_CLUS}
        Reserved Sector Count   {self.RESERVED_SEC_COUNT}
        Total Sector FAT32      {self.TOTAL_SECTOR_32}
        FAT Size 32             {self.FAT_SIZE_32}
        
        VBR start               {self.VBR_START}
        FAT1 start              {self.FAT1_START}
        FAT2 start              {self.FAT2_START}
        Root Directory start    {self.ROOT_DIRECTORY_START}
        """
