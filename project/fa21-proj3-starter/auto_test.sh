#!/bin/sh

python3 tests/part-b/custom/unittest-generator.py

python3 tools/create-test.py tests/part-b/custom/inputs/*.s

# for windows
# python3 .\tools\create-test.py (get-item .\tests\part-b\custom\inputs\*.s)

python3 test.py tests/part-b/custom/
# python3 test.py .\tests\part-b\custom\