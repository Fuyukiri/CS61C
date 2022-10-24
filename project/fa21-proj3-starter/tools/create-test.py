from pathlib import Path
import argparse
import csv
import os
import subprocess
import sys
import tempfile


HARNESS_IMPORT_REF = "file#cpu-harness.circ"
ROM_CONTENTS_REF = "addr/data: 14 32\n0\n"
HALT_CONSTANT_VAL_REF = "0x4258"
TRACE_PATTERN = "%1%,%2%,%5%,%6%,%7%,%8%,%9%,%10%,%pc%,%inst%,%line%\n"
TRACE_HEADER = [ "ra", "sp", "t0", "t1", "t2", "s0", "s1", "a0", "Requested_Address", "Requested_Instruction", "Time_Step" ]

proj_dir_path = Path(__file__).parent.parent
cpu_harness_circ_path = proj_dir_path / "harnesses" / "cpu-harness.circ"
run_circ_path = proj_dir_path / "harnesses" / "run.circ"
logisim_path = proj_dir_path / "tools" / "logisim.jar"
venus_path = proj_dir_path / "tools" / "venus.jar"


class TestCreateException(Exception):
  pass

def generate_test_circ(asm_path, test_circ_path, slug, num_cycles):
  venus_cmd = ["java", "-jar", str(venus_path), str(asm_path), "--dump"]
  tmp_inst_hex_file = tempfile.NamedTemporaryFile(delete=False)
  tmp_inst_hex_path = Path(tmp_inst_hex_file.name)
  with tmp_inst_hex_file:
    proc = subprocess.Popen(venus_cmd, stdout=tmp_inst_hex_file, encoding="utf-8", errors="ignore")
    proc.wait()
  insts = []
  with tmp_inst_hex_path.open("r") as inst_hex_file:
    for line in inst_hex_file:
      line = line.strip()
      if not line:
        continue
      inst = line.replace("0x", "", 1).lstrip("0")
      if inst == "":
        inst = "0"
      insts.append(inst)
  try:
    tmp_inst_hex_path.unlink()
  except FileNotFoundError:
    pass

  rom_contents = f"addr/data: 14 32\n{' '.join(insts)}\n"
  halt_constant_val = hex(num_cycles)

  # Python `xml` is insecure, magic values to the rescue!
  with run_circ_path.open("r") as run_circ_file:
    test_circ_data = run_circ_file.read()
  if HARNESS_IMPORT_REF not in test_circ_data:
    raise TestCreateException(f"Could not write CPU harness import for {str(test_circ_path)}")
  if ROM_CONTENTS_REF not in test_circ_data:
    raise TestCreateException(f"Could not write ROM contents for {str(test_circ_path)}")
  if HALT_CONSTANT_VAL_REF not in test_circ_data:
    raise TestCreateException(f"Could not write halt value for {str(test_circ_path)}")
  # Path.relative_to() only works with direct children
  test_circ_data = test_circ_data.replace(HARNESS_IMPORT_REF, f"file#{os.path.relpath(cpu_harness_circ_path, test_circ_path.parent)}")
  test_circ_data = test_circ_data.replace(ROM_CONTENTS_REF, rom_contents)
  test_circ_data = test_circ_data.replace(HALT_CONSTANT_VAL_REF, halt_constant_val)
  with test_circ_path.open("w") as test_circ_file:
    test_circ_file.write(test_circ_data)
  print(f"[{slug}] generated test circuit")

def generate_output(asm_path, reference_output_path, slug, num_cycles=-1, is_pipelined=False):
  venus_cmd = ["java", "-jar", str(venus_path), str(asm_path), "--immutableText", "--trace", "--traceInstFirst", "--tracepattern", TRACE_PATTERN, "--unsetRegisters"]
  if num_cycles > -1:
    venus_cmd += ["--traceTotalNumCommands", str(num_cycles + 1)]
  if is_pipelined:
    venus_cmd += ["--traceTwoStage"]
  tmp_trace_file = tempfile.NamedTemporaryFile(delete=False)
  tmp_trace_path = Path(tmp_trace_file.name)
  with tmp_trace_file:
    proc = subprocess.Popen(venus_cmd, stdout=tmp_trace_file, encoding="utf-8", errors="ignore")
    proc.wait()
  did_error = proc.returncode != 0
  # Venus runtime errors have exit code 0
  if not did_error and tmp_trace_path.exists():
    with tmp_trace_path.open("r") as trace_file:
      for trace_line in trace_file:
        if "[ERROR]" in trace_line:
          did_error = True
          break
  if did_error:
    if tmp_trace_path.exists():
      print(f"Venus errored (exit code {proc.returncode}), dumping stdout...")
      print("--- BEGIN stdout ---")
      with tmp_trace_path.open("r") as trace_file:
        print(trace_file.read())
      print("---- END stdout ----")
    try:
      tmp_trace_path.unlink()
    except FileNotFoundError:
      pass
    raise TestCreateException(f"Venus errored while generating reference output for {str(asm_path)}")
  with tmp_trace_path.open("r") as trace_file:
    with reference_output_path.open("w", newline="") as reference_output_file:
      reference_output = csv.writer(reference_output_file, lineterminator="\n")
      reference_output.writerow(TRACE_HEADER)
      detected_num_cycles = 0
      for trace_line in trace_file:
        trace_line = trace_line.strip().replace(" ", "")
        row = trace_line.split(",")
        reference_output.writerow(row)
        detected_num_cycles += 1
  try:
    tmp_trace_path.unlink()
  except FileNotFoundError:
    pass

  output_type = "pipelined" if is_pipelined else "single-cycle"
  print(f"[{slug}] generated {output_type} reference output (cycles: {detected_num_cycles})")
  return detected_num_cycles

def create_test(asm_path, num_cycles=-1):
  if not asm_path.is_file() or asm_path.suffix != ".s":
    print(f"Error: {str(asm_path)} is not a RISC-V assembly file, skipping")
    return
  if not asm_path.resolve().match("inputs/*.s"):
    print(f"Error: {str(asm_path)} is not in an inputs/ dir, skipping")
    return
  if not asm_path.resolve().match("custom/inputs/*.s"):
    print(f"Warning: {str(asm_path)} is not in custom/inputs/")

  slug = asm_path.stem
  test_slug = f"cpu-{slug}"
  test_dir_path = asm_path.parent.parent
  reference_output_dir_path = test_dir_path / "reference-output"

  test_circ_path = test_dir_path / f"{test_slug}.circ"
  reference_output_1stage_path = reference_output_dir_path / f"{test_slug}-ref.out"
  reference_output_2stage_path = reference_output_dir_path / f"{test_slug}-pipelined-ref.out"

  print(f"[{slug}] creating {test_circ_path.name}...")
  try:
    generate_output(asm_path, reference_output_1stage_path, slug, num_cycles=num_cycles, is_pipelined=False)
    detected_num_cycles = generate_output(asm_path, reference_output_2stage_path, slug, num_cycles=num_cycles, is_pipelined=True)
    generate_test_circ(asm_path, test_circ_path, slug, num_cycles=detected_num_cycles)
  except TestCreateException as ex:
    print(f"[{slug}] error: {str(ex)}")
    return

def create_tests(asm_paths, num_cycles=-1):
  asm_paths = sorted(asm_paths)

  for asm_path in asm_paths:
    create_test(asm_path, num_cycles)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Create custom CPU tests")
  parser.add_argument("input_path", help="Path to a RISC-V assembly file containing instructions for a test", type=Path, nargs="+")
  parser.add_argument("-c", "--cycles", help="Number of simulation cycles to run (-1 for automatic)", type=int, default=-1)
  args = parser.parse_args()

  create_tests(args.input_path, args.cycles)
