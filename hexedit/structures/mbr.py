from hexedit.enums.partition_type import PartitionType
from hexedit.structures.partition_table_entry import PartitionTableEntry
from hexedit.reader import Reader

from typing import List


class MBR:
    def __init__(
        self,
        boot_code: bytes,
        partition_table_entries: List[PartitionTableEntry],
        signature: bytes,
    ):
        self.BOOT_CODE = boot_code
        self.PARTITION_TABLE_ENTRIES = partition_table_entries
        self.SIGNATURE = signature

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

                if partition_table_entry.START_LBA_ADDRESS == PartitionType.EMPTY:
                    die_flag = False
                    break

                elif (
                    partition_table_entry.PARTITION_TYPE
                    == PartitionType.EXTENDED_WITH_CHS
                ):
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
