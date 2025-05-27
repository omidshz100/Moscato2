import time
start = 2978
end = 12653
pieces = 50

step = (end - start) / pieces

ranges = []
for i in range(pieces):
    range_start = int(start + i * step)
    range_end = int(start + (i + 1) * step) if i < pieces - 1 else end
    ranges.append((range_start, range_end))

for idx, (r_start, r_end) in enumerate(ranges, 1):
    print(f"#{idx} - [{r_start}:{r_end}]\n")
    time.sleep(0.1)  # Optional: sleep to avoid overwhelming the output