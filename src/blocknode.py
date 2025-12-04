
from enum import Enum

class BlockType(Enum):
    PAR = 1
    HEAD = 2
    CODE = 3
    QUOTE = 4
    ENUM_LIST = 5
    ITEM_LIST = 6

    def __repr__(self):
        return f"BlockType.{self.name}"

class BlockNode:
    def __init__(self, md_block, block_type = BlockType):
        self.text = md_block
        self.block_type = block_type

    def __repr__(self):
        return f"{self.text}\n{self.block_type}"
