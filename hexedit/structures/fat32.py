from typing import Any

from pystructs import fields


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
