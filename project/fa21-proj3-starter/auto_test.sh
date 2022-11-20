#!/bin/sh

python3 tests/part-b/custom/unittest-generator.py

python3 tools/create-test.py tests/part-b/custom/inputs/*.s

# for windows
# python3 .\tools\create-test.py .\tests\part-b\custom\inputs\loadsave.s
# python3 .\tools\create-test.py (get-item .\tests\part-b\custom\inputs\*.s)

python3 test.py tests/part-b/custom/
# python3 test.py .\tests\part-b\custom\

# python3 tools/format-output.py tests/part-b/custom/reference-output/<TEST_NAME>-ref.out > reference.out
# python3 tools/format-output.py tests/part-b/custom/student-output/<TEST_NAME>-student.out > student.out
# diff reference.out student.out

# windows
# python3 .\tools\format-output.py .\tests\part-b\custom\reference-output\cpu-loadsave-ref.out > reference.out
# python3 .\tools\format-output.py .\tests\part-b\custom\student-output\cpu-loadsave-student.out > student.out