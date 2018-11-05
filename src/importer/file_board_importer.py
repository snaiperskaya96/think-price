from abstract.abstract_board_importer import AbstractBoardImporter
from board.board import Board
from board.board_component import BoardComponent, ComponentType, MountingSide
import os
import struct

def to_uint(string):
    return struct.unpack('<L', string)[0]

ENCODED_HEADER = b'\x23\xe2\x63\x28'

class FileBoardImporter(AbstractBoardImporter):
    def __init__(self):
        self.buffer = None
        self.board = Board()

    def get_components_list(self):
        components = []

        for comp in self.board.components:
            if comp.name.strip() != '':
                components.append(comp)
        return components

    def import_board(self, file_name):
        with open(file_name, 'rb') as board:
            self.buffer = bytearray(os.fstat(board.fileno()).st_size)
            board.readinto(self.buffer)

        if len(self.buffer) == 0:
            raise RuntimeError(file_name + ' isn\'t a valid board file')

        if self.buffer[0:4] == ENCODED_HEADER:
            self.decrypt_buffer()
        
        lines = self.split_lines()
        self.parse_data_from_string(lines)

    def decrypt_buffer(self):
        new_buffer = bytearray()
        for byte in self.buffer:
            # \n \d
            if chr(byte) != '\n' and chr(byte) != '\r' and byte:# and byte != b'\x00':
                ibyte = int(byte)
                byte = (~(((ibyte >> 6) & 3) | (ibyte << 2))).to_bytes(4, 'big', signed=True)[-1]
            new_buffer.append(byte)
        self.buffer = bytearray(new_buffer)

    def split_lines(self):
        lines = []
        current_str = ''
        for byte in self.buffer:
            if chr(byte) == '\n' or chr(byte) == '\r':
                if current_str != '':
                    lines.append(current_str)
                    current_str = ''
                continue
            current_str += chr(byte)
        if current_str != '':
            lines.append(current_str)
        return lines


    def export_to(self, to):
        with open(to, 'wb') as board:
            board.write(self.buffer)

    def parse_data_from_string(self, lines):
        block = 0
        for line in lines:
            if line.startswith('str_length:'):
                block = 1
                continue
            if line.startswith('var_data:'):
                block = 2
                continue
            if line.startswith('Format:'):
                block = 3
                continue
            if line.startswith('Parts:'):
                block = 4
                continue
            if line.startswith('Pins:') or line.startswith('Pins2:'):
                block = 5
                continue

            if block == 2:
                parts = line.split()
                self.board.num_formats = int(parts[0])
                self.board.num_parts = int(parts[1])
                self.board.num_pins = int(parts[2])
                self.board.num_nails = int(parts[3])
            
            if block == 3:
                parts = line.split()
                self.board.formats.append(
                    {'x': int(parts[0]), 'y': int(parts[1])}
                )
            
            if block == 4:
                parts = line.split()
                tmp = int(parts[1])
                component = BoardComponent(
                    parts[0],
                    ComponentType.SMD if tmp & 12 else ComponentType.THROUGH_HOLE,
                    MountingSide.TOP if (tmp == 1 or (4 <= tmp and tmp < 8)) else MountingSide.BOTTOM,
                    int(parts[2])                    
                )
                self.board.components.append(component)

            
