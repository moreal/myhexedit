from enum import Enum


class PartitionType(Enum):
    EMPTY = 0x00
    EXTENDED_WITH_CHS = 0x05
    FAT32_WITH_LBA = 0x0C
