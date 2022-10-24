from pathlib import Path
import argparse
import csv
import math

known_formats = {
  "alu/*/*.out": [
    ["Test",    "Time"],
    ["ALU_Sel", "ALUSel"],
    ["Input_A", "A"],
    ["Input_B", "B"],
    ["Result",  "Result"],
  ],
  "regfile/*/*.out": [
    ["Test",        "Time"],
    ["rd",          "rd"],
    ["rs1",         "rs1"],
    ["rs2",         "rs2"],
    ["RegWEn",      "RegWEn"],
    ["WriteData",   "WriteData"],
    ["ra",          "ra (x1)"],
    ["sp",          "sp (x2)"],
    ["t0",          "t0 (x5)"],
    ["t1",          "t1 (x6)"],
    ["t2",          "t2 (x7)"],
    ["s0",          "s0 (x8)"],
    ["s1",          "s1 (x9)"],
    ["a0",          "a0 (x10)"],
    ["Read_Data_1", "ReadData1"],
    ["Read_Data_2", "ReadData2"],
  ],
  "part-b/unit/*/cpu-csr*.out": [
    ["Time_Step",             "Time"],
    ["Requested_Address",     "PC"],
    ["Requested_Instruction", "Instruc."],
    ["ra",                    "ra (x1)"],
    ["sp",                    "sp (x2)"],
    ["t0",                    "t0 (x5)"],
    ["t1",                    "t1 (x6)"],
    ["t2",                    "t2 (x7)"],
    ["s0",                    "s0 (x8)"],
    ["s1",                    "s1 (x9)"],
    ["a0",                    "a0 (x10)"],
    ["tohost",                "tohost"],
  ],
  "part-b/unit/*/*.out": [
    ["Time_Step",             "Time"],
    ["Requested_Address",     "PC"],
    ["Requested_Instruction", "Instruc."],
    ["ra",                    "ra (x1)"],
    ["sp",                    "sp (x2)"],
    ["t0",                    "t0 (x5)"],
    ["t1",                    "t1 (x6)"],
    ["t2",                    "t2 (x7)"],
    ["s0",                    "s0 (x8)"],
    ["s1",                    "s1 (x9)"],
    ["a0",                    "a0 (x10)"],
  ],
}
known_formats["part-a/addi/*/*.out"] = known_formats["part-b/unit/*/*.out"]
known_formats["part-b/edge/*/*.out"] = known_formats["part-b/unit/*/*.out"]
known_formats["part-b/integration/*/*.out"] = known_formats["part-b/unit/*/*.out"]


def bin2hex(bin_str):
  hex_str = ""
  num_groups = math.ceil(len(bin_str) / 4)
  bin_str = ("0" * (num_groups * 4 - len(bin_str))) + bin_str
  for i in range(num_groups):
    group = bin_str[i * 4:(i + 1) * 4]
    if "E" in group:
      hex_str += "X"
    elif "U" in group:
      hex_str += "U"
    else:
      hex_str += format(int(group, 2), "x")
  return hex_str

def print_line(arr, lengths, remap=None):
  arr_len = len(arr)
  if remap is not None and len(remap) < arr_len:
    arr_len = len(remap)
  for i in range(arr_len):
    suffix = "\n" if i == arr_len - 1 else " "
    if remap:
      i = remap[i]
    cell = arr[i].ljust(lengths[i])
    print(f"{cell}", end=suffix)

def format_line(arr):
  return [bin2hex(bin_str).rjust(math.ceil(len(bin_str) / 4), "0") for bin_str in arr]

def format_output(output_path):
  with output_path.open("r", encoding="utf-8", errors="ignore") as output_file:
    output_csv = csv.reader(output_file)
    header_line = next(output_csv, None)
    if header_line is None:
      print(f"{str(output_path)} is empty")
      return
    output_line = next(output_csv, None)
    if output_line is None:
      print(f"{str(output_path)} has no rows")
      return
    column_remap = list(range(len(header_line)))
    for glob, column_order in known_formats.items():
      if output_path.match(glob):
        column_remap = [header_line.index(cur_name) for cur_name, _ in column_order]
        for (_, new_name), i in zip(column_order, column_remap):
          header_line[i] = new_name
        break
    column_lengths = [max(len(h), math.ceil(len(o) / 4)) for h, o in zip(header_line, output_line)]
    print_line(header_line, lengths=column_lengths, remap=column_remap)
    print_line(format_line(output_line), lengths=column_lengths, remap=column_remap)
    for output_line in output_csv:
      print_line(format_line(output_line), lengths=column_lengths, remap=column_remap)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Format Logisim test output")
  parser.add_argument("output_path", help="Path to a test output file", type=Path)
  args = parser.parse_args()

  format_output(args.output_path)
