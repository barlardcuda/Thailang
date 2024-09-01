import os

output_dir = 'lang/cut'
os.makedirs(output_dir, exist_ok=True)

with open('lang/cleaned_en_GB.lang', 'r') as file:
    lines = file.readlines()

additional_output_dir = 'lang/output'
os.makedirs(additional_output_dir, exist_ok=True)

total_lines = len(lines)

lines_per_part = total_lines // 3

part1_lines = lines[:lines_per_part]
part2_lines = lines[lines_per_part:2*lines_per_part]
part3_lines = lines[2*lines_per_part:]

with open(os.path.join(output_dir, '1.lang'), 'w') as file:
    file.writelines(part1_lines)

with open(os.path.join(output_dir, '2.lang'), 'w') as file:
    file.writelines(part2_lines)

with open(os.path.join(output_dir, '3.lang'), 'w') as file:
    file.writelines(part3_lines)
