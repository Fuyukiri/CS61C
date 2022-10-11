PYTHON = python3

.PHONY = help setup test test-partA test-partB test-abs test-relu test-argMax test-dot test-matMul test-readMat test-writeMat test-classify

.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To test this project type: make test"
	@echo "To test partA type: make test-partA"
	@echo "To test partB type: make test-partB"
	@echo "To test a function type: make test-[INSERT FUNCTION NAME]"
	@echo "------------------------------------"

test:
	${PYTHON} -m unittest unittests.py -v

test-partA:
	${PYTHON} -m unittest unittests.TestAbs -v
	${PYTHON} -m unittest unittests.TestRelu -v
	${PYTHON} -m unittest unittests.TestArgmax -v
	${PYTHON} -m unittest unittests.TestDot -v
	${PYTHON} -m unittest unittests.TestMatmul -v

test-partB:
	${PYTHON} -m unittest unittests.TestReadMatrix -v
	${PYTHON} -m unittest unittests.TestWriteMatrix -v
	${PYTHON} -m unittest unittests.TestClassify -v
	${PYTHON} -m unittest unittests.TestMain -v

test-abs:
	${PYTHON} -m unittest unittests.TestAbs -v

test-relu:
	${PYTHON} -m unittest unittests.TestRelu -v

test-argmax:
	${PYTHON} -m unittest unittests.TestArgmax -v

test-dot:
	${PYTHON} -m unittest unittests.TestDot -v

test-matmul:
	${PYTHON} -m unittest unittests.TestMatmul -v

test-read_matrix:
	${PYTHON} -m unittest unittests.TestReadMatrix -v

test-write_matrix:
	${PYTHON} -m unittest unittests.TestWriteMatrix -v

test-classify:
	${PYTHON} -m unittest unittests.TestClassify -v

test-main:
	${PYTHON} -m unittest unittests.TestMain -v
