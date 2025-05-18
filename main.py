#!/usr/bin/env python3

from struct import pack

def generate_valid_elf64():
    # Message to print
    message = b"Merhaba Dunya\n"
    message_len = len(message)

    # ELF Header (64-byte)
    elf_header = bytearray()
    elf_header += b'\x7fELF'             # Magic
    elf_header += b'\x02'                # 64-bit
    elf_header += b'\x01'                # Little endian
    elf_header += b'\x01'                # ELF version
    elf_header += b'\x00' * 9            # Padding
    elf_header += pack('<H', 2)          # Type: Executable
    elf_header += pack('<H', 0x3e)       # Machine: x86-64
    elf_header += pack('<I', 1)          # Version
    elf_header += pack('<Q', 0x400078)   # Entry point (where _start is)
    elf_header += pack('<Q', 64)         # Program header table offset
    elf_header += pack('<Q', 0)          # Section header offset
    elf_header += pack('<I', 0)          # Flags
    elf_header += pack('<H', 64)         # ELF header size
    elf_header += pack('<H', 56)         # Program header entry size
    elf_header += pack('<H', 1)          # Program header number
    elf_header += pack('<H', 0)          # Section header size
    elf_header += pack('<H', 0)          # Section header number
    elf_header += pack('<H', 0)          # Section header string table index

    # Program Header (56-byte)
    program_header = bytearray()
    program_header += pack('<I', 1)      # Type: PT_LOAD
    program_header += pack('<I', 5)      # Flags: RX
    program_header += pack('<Q', 0)      # Offset in file
    program_header += pack('<Q', 0x400000) # Virtual address
    program_header += pack('<Q', 0x400000) # Physical address
    code_size = 0x78 + 29 + message_len  # .text + message
    program_header += pack('<Q', code_size)  # File size
    program_header += pack('<Q', code_size)  # Mem size
    program_header += pack('<Q', 0x1000)     # Alignment

    # Assembly instructions (x86-64) for:
    # write(1, "msg", len); exit(0)
    code = bytearray([
        0x48, 0xc7, 0xc0, 0x01, 0x00, 0x00, 0x00,       # mov rax, 1 (write)
        0x48, 0xc7, 0xc7, 0x01, 0x00, 0x00, 0x00,       # mov rdi, 1 (stdout)
        0x48, 0x8d, 0x35, 0x0f, 0x00, 0x00, 0x00,       # lea rsi, [rip+15] (msg)
        0x48, 0xc7, 0xc2, message_len, 0x00, 0x00, 0x00,  # mov rdx, len
        0x0f, 0x05,                                     # syscall
        0x48, 0xc7, 0xc0, 0x3c, 0x00, 0x00, 0x00,       # mov rax, 60 (exit)
        0x48, 0x31, 0xff,                               # xor rdi, rdi
        0x0f, 0x05                                      # syscall
    ])

    # Combine everything
    elf_binary = elf_header + program_header + b'\x00' * (0x78 - len(elf_header + program_header))
    elf_binary += code + message

    # Write to file
    with open("print_hello", "wb") as f:
        f.write(elf_binary)

    print("✅ ELF dosyası yazıldı: ./print_hello")
    print("📦 Çalıştırmak için: chmod +x ./print_hello && ./print_hello")


if __name__ == "__main__":
    generate_valid_elf64()
