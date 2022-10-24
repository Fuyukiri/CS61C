from pathlib import Path
import argparse
import csv
import hashlib
import os
import re
import subprocess
import sys
import time
import traceback


CIRC_IMPORT_REGEX = re.compile(r"desc=\"file#([^\"]+?\.circ)\"")

proj_dir_path = Path(__file__).parent
tests_dir_path = proj_dir_path / "tests"
logisim_path = proj_dir_path / "tools" / "logisim-evolution.jar"

banned_component_names = [
  "Pull Resistor",
  "Transistor",
  "Transmission Gate",
  "Power",
  "POR",
  "Ground",
  "Divider",
  "Random",
  "PLA",
  "RAM",
  "Random Generator",
]
known_imports_dict = {
  "cpu/cpu.circ": [
    "cpu/alu.circ",
    "cpu/branch-comp.circ",
    "cpu/control-logic.circ",
    "cpu/csr.circ",
    "cpu/imm-gen.circ",
    "cpu/regfile.circ",
  ],
  "harnesses/alu-harness.circ": [
    "cpu/alu.circ",
  ],
  "harnesses/csr-harness.circ": [
    "cpu/cpu.circ",
    "cpu/mem.circ",
  ],
  "harnesses/cpu-harness.circ": [
    "cpu/cpu.circ",
    "cpu/mem.circ",
  ],
  "harnesses/regfile-harness.circ": [
    "cpu/regfile.circ",
  ],
  "harnesses/run.circ": [
    "harnesses/cpu-harness.circ",
  ],
  "tests/part-a/alu/*.circ": [
    "cpu/alu.circ",
  ],
  "tests/part-a/regfile/*.circ": [
    "cpu/regfile.circ",
  ],
  "tests/part-b/unit/cpu-csr*.circ": [
    "harnesses/csr-harness.circ",
  ],
  "tests/part-b/unit/*.circ": [
    "harnesses/cpu-harness.circ",
  ],
}
known_imports_dict["tests/part-a/addi/*.circ"] = known_imports_dict["tests/part-b/unit/*.circ"]
known_imports_dict["tests/part-b/edge/*.circ"] = known_imports_dict["tests/part-b/unit/*.circ"]
known_imports_dict["tests/part-b/integration/*.circ"] = known_imports_dict["tests/part-b/unit/*.circ"]

def find_banned(circ_path):
  if circ_path.name in ["mem.circ"]: return False
  with circ_path.open("r") as f:
    contents = f.read()
  found = False
  for component_name in banned_component_names:
    if re.search(fr'<comp.*\bname="{component_name}"', contents):
      print(f"ERROR: found banned element ({component_name}) in {circ_path.as_posix()}")
      found = True
  return found

starter_file_hashes = {
  "tests/part-a/addi/cpu-addi-basic.circ": "68ce93fcd5f02892858b5346cef9912c",
  "tests/part-a/addi/cpu-addi-negative.circ": "1fd2e2a4d8de8e8e94ecfdb6ff4a7791",
  "tests/part-a/addi/cpu-addi-positive.circ": "de40498352126b3bac7adc3beaf05ef8",
  "tests/part-a/addi/reference-output/cpu-addi-basic-pipelined-ref.out": "9ed073c6b6be1aa4b5a2b139a51aaeb2",
  "tests/part-a/addi/reference-output/cpu-addi-basic-ref.out": "5210cedf06a9a3c79d8d008e8d45b780",
  "tests/part-a/addi/reference-output/cpu-addi-negative-pipelined-ref.out": "99ffcb410c8ec56f1f20fde736723c47",
  "tests/part-a/addi/reference-output/cpu-addi-negative-ref.out": "dc63e8150ff05142ea49f0e1b0b53720",
  "tests/part-a/addi/reference-output/cpu-addi-positive-pipelined-ref.out": "b4bef27bc990695af3fcdf08f14bbf05",
  "tests/part-a/addi/reference-output/cpu-addi-positive-ref.out": "d1acd4f4f93fb0fac202335856623f0a",
  "tests/part-a/alu/alu-add.circ": "020b3a12c7327966b6d60e26101f36a8",
  "tests/part-a/alu/alu-all.circ": "fb830659d6fdd9707207f97fb7859db8",
  "tests/part-a/alu/alu-logic.circ": "f91844febf85e3c36f1e160ff472a36b",
  "tests/part-a/alu/alu-mult.circ": "d452d8763733f371845afdcc7ee7b08c",
  "tests/part-a/alu/alu-shift.circ": "8d65fc446876dbadb0eeee2db273e657",
  "tests/part-a/alu/alu-slt-sub-bsel.circ": "dfd7bd6c04ba627665238d1d6ee44202",
  "tests/part-a/alu/reference-output/alu-add-ref.out": "0b354116160285fc52e5a98b5f424ca4",
  "tests/part-a/alu/reference-output/alu-all-ref.out": "431f65bb245946b1317376ea27c37281",
  "tests/part-a/alu/reference-output/alu-logic-ref.out": "d0f792f92fd98b0c6eeca62919e4cc53",
  "tests/part-a/alu/reference-output/alu-mult-ref.out": "8c21bdbab00fb44012056738939b20de",
  "tests/part-a/alu/reference-output/alu-shift-ref.out": "8a21482a9940d4364676f7567a4df3a1",
  "tests/part-a/alu/reference-output/alu-slt-sub-bsel-ref.out": "4b7a9d24113e875e90e91733f43ec063",
  "tests/part-a/regfile/reference-output/regfile-more-regs-ref.out": "dcefc797885d916c117a364e40adc3e9",
  "tests/part-a/regfile/reference-output/regfile-read-only-ref.out": "3a8874916007675ee644e10e8cb4f440",
  "tests/part-a/regfile/reference-output/regfile-read-write-ref.out": "1c2f42eb2985621b4ad013f173b8b8ab",
  "tests/part-a/regfile/reference-output/regfile-x0-ref.out": "13340ed18bd0260757e32094c07e5427",
  "tests/part-a/regfile/regfile-more-regs.circ": "fe6ce135a3274502ecd07d3dd4ed3731",
  "tests/part-a/regfile/regfile-read-only.circ": "8327e83a7908068fac8b5e3df7c93f2c",
  "tests/part-a/regfile/regfile-read-write.circ": "f51735d8244634fc2197834eb05fb6bf",
  "tests/part-a/regfile/regfile-x0.circ": "99f3af65aaf5eca9bcfbc4908df7b0b5",
  "tests/part-b/edge/cpu-edge-all-regs.circ": "2b0a65f4db54a7643c855e94270b32f9",
  "tests/part-b/edge/cpu-edge-branch.circ": "777cca361ae4aab85f67e18eceb88d60",
  "tests/part-b/edge/cpu-edge-immediates.circ": "b81ecd1a41c62153d945afe5a6f00d29",
  "tests/part-b/edge/cpu-edge-jump-around.circ": "4ceb303ff056785438cdbd3a654a91af",
  "tests/part-b/edge/cpu-edge-jump-empty.circ": "5eef52d4553f2673d35c60325a928b97",
  "tests/part-b/edge/cpu-edge-jump-far.circ": "b5c39b5ed6add99e6400572e56cf282a",
  "tests/part-b/edge/cpu-edge-lui.circ": "13c721cc813fe2564ea2f9998e3d8eea",
  "tests/part-b/edge/cpu-edge-mem-extend.circ": "60ab64ce5ab960626873bd44d4f85bf2",
  "tests/part-b/edge/cpu-edge-mem-unaligned.circ": "ed16a869310b8f9488022a47299c725d",
  "tests/part-b/edge/reference-output/cpu-edge-all-regs-pipelined-ref.out": "6d6bed4b2a71b3efc6460708eab80d31",
  "tests/part-b/edge/reference-output/cpu-edge-all-regs-ref.out": "60e963c0dbeb784b6308bb2d9fe05f7a",
  "tests/part-b/edge/reference-output/cpu-edge-branch-pipelined-ref.out": "d7c8f42f22493278823dfb9f6d248c51",
  "tests/part-b/edge/reference-output/cpu-edge-branch-ref.out": "db7b6f3ca845c436c29c424fb47938e1",
  "tests/part-b/edge/reference-output/cpu-edge-immediates-pipelined-ref.out": "54aa566b2d77a1d154b53c5de47bb37a",
  "tests/part-b/edge/reference-output/cpu-edge-immediates-ref.out": "ba3355f52f904ff841acb5beabc86bb4",
  "tests/part-b/edge/reference-output/cpu-edge-jump-around-pipelined-ref.out": "eab3ac0af1c9aee1f0ffea5a89e13a09",
  "tests/part-b/edge/reference-output/cpu-edge-jump-around-ref.out": "4c49597f8b3fff4b15f968a828a11b95",
  "tests/part-b/edge/reference-output/cpu-edge-jump-empty-pipelined-ref.out": "00d49b60cd60c8bc99a6e7911e1bb69e",
  "tests/part-b/edge/reference-output/cpu-edge-jump-empty-ref.out": "3f5bc638299a7bf13457928983d9d120",
  "tests/part-b/edge/reference-output/cpu-edge-jump-far-pipelined-ref.out": "94221f7d4afa9e181009d5956a1448c4",
  "tests/part-b/edge/reference-output/cpu-edge-jump-far-ref.out": "c1cbf7005c10b7e6bf6a58c7103183d0",
  "tests/part-b/edge/reference-output/cpu-edge-lui-pipelined-ref.out": "29d86a0fac0f1beba33bad63d984c7a1",
  "tests/part-b/edge/reference-output/cpu-edge-lui-ref.out": "f0d63dc64d2887d77736dc1ce1556e51",
  "tests/part-b/edge/reference-output/cpu-edge-mem-extend-pipelined-ref.out": "423d5cec26b6fd1552106181ecca2a6c",
  "tests/part-b/edge/reference-output/cpu-edge-mem-extend-ref.out": "cf5696a4aeceab0fcaea2f57149a5c6f",
  "tests/part-b/edge/reference-output/cpu-edge-mem-unaligned-pipelined-ref.out": "666e2dcbd9137d9d018e15adf0963927",
  "tests/part-b/edge/reference-output/cpu-edge-mem-unaligned-ref.out": "5dda404eba44f1ba4093048d2f3cc74b",
  "tests/part-b/integration/cpu-integration-fib.circ": "d6922662584e347e503682f845c830d9",
  "tests/part-b/integration/cpu-integration-power.circ": "ffd3859331f875ebaf4db87fe3806a31",
  "tests/part-b/integration/reference-output/cpu-integration-fib-pipelined-ref.out": "7f9ec37d48d4d0ef4b9098f1e42cf43d",
  "tests/part-b/integration/reference-output/cpu-integration-fib-ref.out": "527d353547095655073e25af73ce300d",
  "tests/part-b/integration/reference-output/cpu-integration-power-pipelined-ref.out": "de91d6c5b7c51f76f7c93e27292af53e",
  "tests/part-b/integration/reference-output/cpu-integration-power-ref.out": "d4e922c3511f02c889815608f7bcd72b",
  "tests/part-b/unit/cpu-csrw.circ": "c52429dcb849fb55a97aae8ef36e225b",
  "tests/part-b/unit/cpu-csrwi.circ": "e4895e6b0b0fe47c7654dc0306739efd",
  "tests/part-b/unit/reference-output/cpu-csrw-pipelined-ref.out": "e6603795a5c1560ecfa478aa850ebe40",
  "tests/part-b/unit/reference-output/cpu-csrw-ref.out": "2b25de178d49bcf528b201f162851174",
  "tests/part-b/unit/reference-output/cpu-csrwi-pipelined-ref.out": "33ce8ffe4e8b5ac0642c292bf41a2007",
  "tests/part-b/unit/reference-output/cpu-csrwi-ref.out": "34815f04f7119947f77cf6a0abcf7b8d",
}

class TestCase():
  def __init__(self, circ_path, name=None):
    self.circ_path = Path(circ_path)
    self.id = str(self.circ_path)
    self.name = name or self.circ_path.stem

  def can_pipeline(self):
    if self.circ_path.match("alu/*.circ") or self.circ_path.match("regfile/*.circ"):
      return False
    return True

  def fix_circ(self):
    fix_circ(self.circ_path)

  def check_hashes(self, pipelined=False):
    passed, reason = check_hash(self.circ_path)
    if not passed: return passed, reason

    passed, reason = check_hash(self.get_expected_table_path(pipelined=pipelined))
    if not passed: return passed, reason

    return (True, "Circuit data matches starter code")

  def get_actual_table_path(self):
    return self.circ_path.parent / "student-output" / f"{self.name}-student.out"

  def get_expected_table_path(self, pipelined=False):
    path = self.circ_path.parent / "reference-output" / f"{self.name}-ref.out"
    if pipelined:
      path = path.with_name(f"{self.name}-pipelined-ref.out")
    return path

  def run(self, pipelined=False):
    self.fix_circ()
    passed, reason = self.check_hashes(pipelined=pipelined)
    if not passed:
      return passed, reason

    if pipelined and not self.can_pipeline():
      pipelined = False
    passed = False
    proc = None
    try:
      proc = subprocess.Popen(["java", "-jar", str(logisim_path), "-tty", "table,binary,csv", str(self.circ_path)], stdout=subprocess.PIPE, encoding="utf-8", errors="ignore")

      with self.get_expected_table_path(pipelined=pipelined).open("r", encoding="utf-8", errors="ignore") as expected_file:
        passed = self.check_output(proc.stdout, expected_file)
        kill_proc(proc)
        if not passed:
          return (False, "Did not match expected output")
        return (True, "Matched expected output")
    except KeyboardInterrupt:
      kill_proc(proc)
      sys.exit(1)
    except:
      traceback.print_exc()
      kill_proc(proc)
    return (False, "Errored while running test")

  def check_output(self, actual_file, expected_file):
    passed = True
    actual_csv = csv.reader(actual_file)
    expected_csv = csv.reader(expected_file)
    actual_lines = []
    while True:
      actual_line = next(actual_csv, None)
      expected_line = next(expected_csv, None)
      if expected_line is None:
        break
      if actual_line != expected_line:
        passed = False
      if actual_line is None:
        break
      actual_lines.append(actual_line)
    output_path = self.get_actual_table_path()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as output_file:
      output_csv = csv.writer(output_file, lineterminator="\n")
      for line in actual_lines:
        output_csv.writerow(line)
    return passed

def fix_circ(circ_path):
  circ_path = circ_path.resolve()

  for glob, known_imports in known_imports_dict.items():
    if circ_path.match(glob):
      old_data = None
      data = None
      is_modified = False
      with circ_path.open("r", encoding="utf-8") as test_circ:
        old_data = test_circ.read()
        data = old_data
      for match in re.finditer(CIRC_IMPORT_REGEX, old_data):
        import_path_str = match.group(1)
        import_path = (circ_path.parent / Path(import_path_str)).resolve()
        for known_import in known_imports:
          if import_path.match(known_import):
            known_import_path = (proj_dir_path / known_import).resolve()
            expected_import_path = Path(os.path.relpath(known_import_path, circ_path.parent))
            if import_path_str != expected_import_path.as_posix():
              print(f"Fixing bad import {import_path_str} in {circ_path.as_posix()} (should be {expected_import_path.as_posix()})")
              data = data.replace(import_path_str, expected_import_path.as_posix())
              is_modified = True
            break
        else:
          expected_import_path = Path(os.path.relpath(import_path, circ_path.parent))
          if import_path_str != expected_import_path.as_posix():
            print(f"Fixing probably bad import {import_path_str} in {circ_path.as_posix()} (should be {expected_import_path.as_posix()})")
            data = data.replace(import_path_str, expected_import_path.as_posix())
            is_modified = True
      if is_modified:
        with circ_path.open("w", encoding="utf-8") as test_circ:
          test_circ.write(data)
      break

def run_tests(search_paths, pipelined=False):
  circ_paths = []
  for search_path in search_paths:
    if search_path.is_file() and search_path.suffix == ".circ":
      circ_paths.append(search_path)
      continue
    for circ_path in search_path.rglob("*.circ"):
      circ_paths.append(circ_path)
  circ_paths = sorted(circ_paths)

  has_banned_circuit = False
  for circ_path in proj_dir_path.rglob("cpu/*.circ"):
    fix_circ(circ_path)
    if find_banned(circ_path):
      has_banned_circuit = True
  for circ_path in proj_dir_path.rglob("harnesses/*.circ"):
    fix_circ(circ_path)
  if has_banned_circuit:
    return

  failed_tests = []
  passed_tests = []
  for circ_path in circ_paths:
    test = TestCase(circ_path)
    did_pass, reason = False, "Unknown test error"
    try:
      did_pass, reason = test.run(pipelined=pipelined)
    except KeyboardInterrupt:
      raise
    except SystemExit:
      raise
    except:
      traceback.print_exc()
    if did_pass:
      print(f"PASS: {test.id}", flush=True)
      passed_tests.append(test)
    else:
      print(f"FAIL: {test.id} ({reason})", flush=True)
      failed_tests.append(test)

  print(f"Passed {len(passed_tests)}/{len(failed_tests) + len(passed_tests)} tests", flush=True)

def check_hash(path):
  rel_path = path.resolve().relative_to(proj_dir_path.resolve())
  rel_path_str = rel_path.as_posix()
  if rel_path_str not in starter_file_hashes:
    return (True, f"Starter does not have hash for {path.name}")
  with path.open("rb") as f:
    contents = f.read()
  contents = contents.replace(b"\r\n", b"\n")
  hashed_val = hashlib.md5(contents).hexdigest()
  if hashed_val != starter_file_hashes[rel_path_str]:
    return (False, f"{path.name} was changed from starter")
  return (True, f"{path.name} matches starter file")

def kill_proc(proc):
  if proc.poll() is None:
    proc.terminate()
    for _ in range(10):
      if proc.poll() is not None:
        return
      time.sleep(0.1)
  if proc.poll() is None:
    proc.kill()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Run Logisim tests")
  parser.add_argument("test_path", help="Path to a test circuit, or a directory containing test circuits", type=Path, nargs="+")
  parser.add_argument("-p", "--pipelined", help="Check against reference output for 2-stage pipeline (when applicable)", action="store_true", default=False)
  args = parser.parse_args()

  run_tests(args.test_path, args.pipelined)
