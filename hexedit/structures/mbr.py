from hexedit.structures.partition_table_entry import PartitionTableEntry
from hexedit.reader import Reader

from typing import List


class MBR:
    def __init__(
        self,
        BOOT_CODE: bytes,
        PARTITION_TABLE_ENTRIES: List[PartitionTableEntry],
        SIGNATURE: bytes,
    ):
        self.BOOT_CODE = BOOT_CODE
        self.PARTITION_TABLE_ENTRIES = PARTITION_TABLE_ENTRIES
        self.SIGNATURE = SIGNATURE

    @staticmethod
    def from_reader(reader: Reader):
        raw = reader._read(0)

        boot_code = raw[0:446]
        signature = raw[-2:]

        partition_table_entries: List[PartitionTableEntry] = list()

        base_sectors = [0]

        die_flag = True

        while die_flag:
            raw_partitions = raw[446 : 446 + 64]

            for i in range(0, 64, 16):
                partition_table_entry = PartitionTableEntry.from_bytes(
                    raw_partitions[i : i + 16]
                )

                if partition_table_entry.START_LBA_ADDRESS == 0x00000000:
                    die_flag = False
                    break
                elif partition_table_entry.PARTITION_TYPE == 0x05:
                    base_sectors.append(
                        base_sectors[-1] + partition_table_entry.START_LBA_ADDRESS
                    )
                    raw = reader._read(
                        base_sectors[0 if len(base_sectors) == 2 else 1]
                        + partition_table_entry.START_LBA_ADDRESS
                    )
                    break
                else:
                    partition_table_entry.START_LBA_ADDRESS += base_sectors[-1]
                    partition_table_entries.append(partition_table_entry)

        return MBR(boot_code, partition_table_entries, signature)
