"""CPU functionality."""

import sys

HLT = 0b00000001 #0x01 # halt and exit
LDI = 0b10000010 #0x82 # set val to int
PRN = 0b01000111 #0x47 # print numeric value
MUL = 0b10100010 #0xA2
ADD = 0b10100000 #0xA0
POP = 0b01000110 #0x46
PUSH = 0b01000101 #0x45
CALL = 0b01010000 #0x50 # call subroutine at address stored
RET = 0b00010001 #0x11 # return from a subroutine
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        # self.register[7] = 255
        # self.sp = self.register[7]
        self.sp = 244
        self.register[7] = self.sp
        self.flag = 0b00000000
        # self.running = True
        # self.register[7] = 244
        # self.sp = self.register[7]
        # self.sp = 244
        # self.flag = self.register[4] #0b00000000
        # Branchtable not currently working for some reason
        # self.branchtable = {
        #     HLT: self.hlt,
        #     LDI: self.ldi,
        #     PRN: self.prn,
        #     POP: self.pop,
        #     PUSH: self.push,
        #     CALL: self.call,
        #     RET: self.ret
        # }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, path):
        """Load a program into memory."""
        try:
            address = 0

            with open(path) as f:
                for line in f:
                    comment_split = line.split('#')

                    value = comment_split[0].strip()

                    if value == '':
                        continue

                    num = int(value, 2)
                    # self.ram[address] = num
                    self.ram_write(num, address)
                    address += 1

        except FileNotFoundError:
            print(f"FileNotFound: {sys.argv}")
            sys.exit(2)


            # with open(sys.argv[1], 'r')as f:
            #     line = f.readlines()
            # for line in f:
            #     stripped = line.strip()
        # if len(sys.argv) != 2:
        #     print("Error")
        #     sys.exit(1)
        # try:
        #     address = 0
        #     with open(sys.argv[1]) as f:
        #         for instruction in f:
        #             split_excess = instruction.split('#')
        #             split = split_excess[0].strip()
        #             if split == '':
        #                 continue
        #             val = int(split, 2)
        #             self.ram_write(address, val)
        #             address += 1
        # except FileNotFoundError:
        #     print(f"FileNotFound: {sys.argv}")
        #     sys.exit(2)


        # except FileNotFoundError:
        #     print('file not found')
        #     sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == 'SUB':
            self.register[reg_a] -= self.register[reg_b]
        elif op == 'CMP':
            # If they are equal, set the Equal E flag to 1,
            # otherwise set it to 0.
            # If registerA is less than registerB, set the Less-than
            # L flag to 1, otherwise set it to 0.
            # If registerA is greater than registerB, set the Greater-than
            # G flag to 1, otherwise set it to 0.

            if self.register[reg_a] == self.register[reg_b]:
                self.flag = 0b00000001
            elif self.register[reg_a] < self.register[reg_b]:
                self.flag = 0b00000100
            elif self.register[reg_a] > self.register[reg_b]:
                self.flag = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running is True:
            # IR = self.ram_read(self.pc)
            IR = self.ram[self.pc]
            oper_a = self.ram_read(self.pc + 1)
            oper_b = self.ram_read(self.pc + 2)
            # oper_a = self.ram_read(self.pc)
            # oper_b = self.ram_read(self.pc + 1)

            if IR == 'HLT':
                # self.pc += 1
                # self.running = False
                running = False
                # return False
                # self.pc += 1

            elif IR == 'LDI':
                # self.branchtable[IR](oper_a, oper_b)
                self.register[oper_a] = oper_b
                self.pc += 3
                # self.pc += (IR >> 6) + 1

            elif IR == 'PRN':
                print(self.register[oper_a])
                self.pc += 2

            elif IR == 'ADD':
                self.alu('ADD', oper_a, oper_b)
                self.pc += 3

            elif IR == 'MUL':
                self.alu('MUL', oper_a, oper_b)
                self.pc += 3

            elif IR == 'POP':
                # value = self.ram[self.sp]
                value = self.ram_read(self.sp)
                self.register[oper_a] = value
                self.sp += 1
                self.pc += 2

            elif IR == 'PUSH':
                self.sp -= 1
                # value = self.register[oper_a]
                value = self.ram[oper_a]
                self.ram[self.sp] = value
                self.pc += 2

            elif IR == 'SUB':
                self.alu('SUB', oper_a, oper_b)
                self.pc += 3

            elif IR == 'CALL':
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                # update = self.ram[self.pc + 1]
                # self.pc = self.register[update]
                self.sp = self.ram[oper_a]

            elif IR == 'RET':
                self.pc = self.ram[self.sp]
                self.sp += 1

            elif IR == 'CMP':
                self.alu('CMP', oper_a, oper_b)
                self.pc += 3

            elif IR == 'JMP':
                # Jump to the address stored in the given register.
                # Set the PC to the address stored in the given register.
                self.pc = self.register[oper_a]

            elif IR == 'JEQ':
                # If equal flag is set (true), jump to the address
                # stored in the given register.
                if self.flag == 0b00000001:
                    self.pc = self.register[oper_a]
                else:
                    self.pc += 2

            elif IR == 'JNE':
                # If E flag is clear (false, 0), jump to the address
                # stored in the given register.
                if self.flag != 0b00000001:
                    self.pc = self.register[oper_a]
                else:
                    self.pc += 2

            else:
                print('function not supported')
                self.pc += 1

# cpu = CPU()

# cpu.load(sys.argv[1])
# cpu.run()