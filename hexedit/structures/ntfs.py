from typing import List

from pystructs import fields

from hexedit.enums.partition_type import PartitionType
from hexedit.reader import Reader
from hexedit.structures.mbr import MBR


class NTFS(fields.Struct):
    JUMP_BOOT_CODE: int = fields.IntField(size=3)
    OEM_ID: str = fields.StringField(size=8, encoding="ascii")
    BYTES_PER_SECTOR: int = fields.IntField(size=2)
    SEC_PER_CLUS: int = fields.IntField(size=1)
    RESERVED_SEC_COUNT: int = fields.IntField(size=2)

    UNUSED_1 = fields.BytesField(size=5)
    MEDIA = fields.BytesField(1)
    UNUSED_2 = fields.BytesField(size=18)

    TOTAL_SECTORS: int = fields.Int64Field()
    START_CLUSTER_FOR_MFT: int = fields.Int64Field()
    START_CLUSTER_FOR_MFT_MIRR: int = fields.Int64Field()

    CLUSTER_PER_ENTRY: int = fields.IntField(size=1)
    UNUSED_3 = fields.BytesField(size=3)
    CLUSTER_PER_INDEX: int = fields.IntField(size=1)
    UNUSED_4 = fields.BytesField(size=3)

    VOLUME_SERIAL_NUMBER: int = fields.Int64Field()

    PARTITION_INDEX: int

    @staticmethod
    def from_reader_with_mbr(reader: Reader, mbr: MBR) -> "List[NTFS]":
        partition_table_entries = mbr.PARTITION_TABLE_ENTRIES
        ntfss = list()

        for index, partition_table_entry in enumerate(partition_table_entries):
            if partition_table_entry.PARTITION_TYPE == PartitionType.NTFS_WITH_LBA_CHS:
                lba_start = partition_table_entry.START_LBA_ADDRESS
                raw = reader._read(lba_start)

                ntfs = NTFS(raw)
                ntfs.initialize()

                ntfs.PARTITION_INDEX = index

                ntfss.append(ntfs)

        return ntfss

    def __str__(self):
        return f"""
        ------------- PARTITION [{self.PARTITION_INDEX + 1}] -------------
        OEM                     {self.OEM_ID}
        Byte Per Sector         {self.BYTES_PER_SECTOR}
        Sector Per Cluster      {self.SEC_PER_CLUS}
        Reserved Sector Count   {self.RESERVED_SEC_COUNT}
        Total Sectors           {self.TOTAL_SECTORS}
        
        MFT start               {self.START_CLUSTER_FOR_MFT}
        MFT Mirr start          {self.START_CLUSTER_FOR_MFT_MIRR}
        """
