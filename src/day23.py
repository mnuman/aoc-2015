from utils.file_utils import read_file


class TuringLock:
    def __init__(self, pgm, a=0, b=0):
        self.pgm = pgm
        self.pc = 0
        self.registers = {"a": a, "b": b}

    def step(self):
        if self.pc < 0 or self.pc >= len(self.pgm):
            return False
        cmd, *args = self.pgm[self.pc]
        match cmd:
            case "hlf":
                self.registers[args[0]] //= 2
                self.pc += 1
            case "tpl":
                self.registers[args[0]] *= 3
                self.pc += 1
            case "inc":
                self.registers[args[0]] += 1
                self.pc += 1
            case "jmp":
                self.pc += int(args[0])
            case "jie":
                if self.registers[args[0]] % 2 == 0:
                    self.pc += args[1]
                else:
                    self.pc += 1
            case "jio":
                if self.registers[args[0]] == 1:
                    self.pc += args[1]
                else:
                    self.pc += 1

        return True

    def __repr__(self) -> str:
        return f"TuringLock(pc={self.pc}, registers={self.registers})"


def parse_input(filename):
    instructions = []
    data = read_file(filename)
    for line in data:
        cmd_reg, *qty = line.split(", ")
        cmd, reg = cmd_reg.split()
        instructions.append((cmd, reg, int(qty[0]) if len(qty) > 0 else None))
    return instructions


if __name__ == "__main__":
    instructions = parse_input("day23.txt")
    print(instructions)
    lock = TuringLock(instructions)
    while lock.step():
        print(lock)
    print(lock.registers)
    new_lock = TuringLock(instructions, a=1, b=0)
    while new_lock.step():
        print(new_lock)
    print(new_lock.registers)
