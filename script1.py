# режем дамп на блоки по 4 КБ и выкидываем пустые (забитые 0xFF).
# так отделяем живые области (код программы, данные сейфа)
# от стёртой неиспользуемой памяти.

with open("dump.bin", "rb") as f:
    data = f.read()

block_size = 4096
active_blocks = []
for i in range(0, len(data), block_size):
    chunk = data[i:i + block_size]
    if chunk != b"\xff" * block_size:
        active_blocks.append(i)

print(f"Общий размер: {len(data)} байт")
print("Занятые блоки:")

start = None
prev = None
for b in active_blocks:
    if start is None:
        start = b
        prev = b
    elif b == prev + block_size:
        prev = b
    else:
        print(f"  0x{start:06X} - 0x{prev + block_size:06X}")
        start = b
        prev = b
if start is not None:
    print(f"  0x{start:06X} - 0x{prev + block_size:06X}")
