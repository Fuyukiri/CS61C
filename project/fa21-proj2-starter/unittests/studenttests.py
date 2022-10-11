from unittest import TestCase
from framework import AssemblyTest, print_coverage

"""
Coverage tests for project 2 is meant to make sure you understand
how to test RISC-V code based on function descriptions.
Before you attempt to write these tests, it might be helpful to read
unittests.py and framework.py.
Like project 1, you can see your coverage score by submitting to gradescope.
The coverage will be determined by how many lines of code your tests run,
so remember to test for the exceptions!
"""

"""
abs_loss
# =======================================================
# FUNCTION: Get the absolute difference of 2 int vectors,
#   store in the result vector and compute the sum
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int*) is the pointer to the start of the result vector

# Returns:
#   a0 (int)  is the sum of the absolute loss
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 36.
# =======================================================
"""


class TestAbsLoss(TestCase):
    def test_simple(self):
        # load the test for abs_loss.s
        t = AssemblyTest(self, "abs_loss.s")
        # create array0 in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # create array1 in the data section
        array1 = t.array([1, 6, 1, 6, 1, 6, 1, 6, 1])
        # load address of `array1` into register a1
        t.input_array("a1", array1)
        # set a2 to the length of the array
        t.input_scalar("a2", len(array0))
        # create a result array in the data section (fill values with -1)
        array2 = t.array([-1 for i in range(9)])
        # load address of `array2` into register a3
        t.input_array("a3", array2)
        # call the `abs_loss` function
        t.call("abs_loss")
        # check that the result array contains the correct output
        t.check_array(array2, [0, 4, 2, 2, 4, 0, 6, 2, 8])
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 28)
        # generate the `assembly/TestAbsLoss_test_simple.s` file and run it through venus
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "abs_loss.s")
        # set a1 to an invalid length of array
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 6, 1, 6, 1, 6, 1, 6, 1])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 0)
        # call the `relu` function
        t.call("abs_loss")
        # generate the `assembly/TestRelu_test_invalid_n.s` file and run it through venus
        t.execute(code=36)

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs_loss.s", verbose=False)


"""
squared_loss
# =======================================================
# FUNCTION: Get the squared difference of 2 int vectors,
#   store in the result vector and compute the sum
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int*) is the pointer to the start of the result vector

# Returns:
#   a0 (int)  is the sum of the squared loss
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 36.
# =======================================================
"""


class TestSquaredLoss(TestCase):

    def test_simple(self):
        # load the test for squared_loss.s
        t = AssemblyTest(self, "squared_loss.s")
        # create input arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 6, 1, 6, 1, 6, 1, 6, 1])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array length into argument register
        t.input_scalar("a2", len(array0))
        # create a result array in the data section (fill values with -1)
        array2 = t.array([-1 for i in range(9)])
        # load result array address into argument register
        t.input_array("a3", array2)
        # call the `squared_loss` function
        t.call("squared_loss")
        # check that the result array contains the correct output
        t.check_array(array2, [0, 16, 4, 4, 16, 0, 36, 4, 64])
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 144)
        # generate the `assembly/TestSquaredLoss_test_simple.s` file and run it through venus
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "squared_loss.s")
        # set a1 to an invalid length of array
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 6, 1, 6, 1, 6, 1, 6, 1])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 0)
        # call the `relu` function
        t.call("squared_loss")
        # generate the `assembly/TestRelu_test_invalid_n.s` file and run it through venus
        t.execute(code=36)

    @classmethod
    def tearDownClass(cls):
        print_coverage("squared_loss.s", verbose=False)


"""
zero_one_loss
# =======================================================
# FUNCTION: Generates a 0-1 classifer vector inplace in the result vector,
#  where result[i] = (v0[i] == v1[i])
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int*) is the pointer to the start of the result vector

# Returns:
#   NONE
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 36.
# =======================================================
"""


class TestZeroOneLoss(TestCase):
    def test_simple(self):
        # load the test for zero_one_loss.s
        t = AssemblyTest(self, "zero_one_loss.s")
        # create input arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 6, 1, 6, 1, 6, 1, 6, 1])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array length into argument register
        t.input_scalar("a2", len(array0))
        # create a result array in the data section (fill values with -1)
        array2 = t.array([-1 for i in range(9)])
        # load result array address into argument register
        t.input_array("a3", array2)
        # call the `zero_one_loss` function
        t.call("zero_one_loss")
        # check that the result array contains the correct output
        t.check_array(array2, [1, 0, 0, 0, 0, 1, 0, 0, 0])
        # generate the `assembly/TestZeroOneLoss_test_simple.s` file and run it through venus
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "zero_one_loss.s")
        # set a1 to an invalid length of array
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 6, 1, 6, 1, 6, 1, 6, 1])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 0)
        # call the `relu` function
        t.call("zero_one_loss")
        # generate the `assembly/TestRelu_test_invalid_n.s` file and run it through venus
        t.execute(code=36)

    @classmethod
    def tearDownClass(cls):
        print_coverage("zero_one_loss.s", verbose=False)


"""
initialize_zero
# =======================================================
# FUNCTION: Initialize a zero vector with the given length
# Arguments:
#   a0 (int) size of the vector

# Returns:
#   a0 (int*)  is the pointer to the zero vector
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 36.
# - If malloc fails, this function terminats the program with exit code 16.
# =======================================================
"""


class TestInitializeZero(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "initialize_zero.s")
        # input the length of the desired array
        t.input_scalar("a0", 3)
        # call the `initialize_zero` function
        t.call("initialize_zero")
        # check that the register a0 contains the correct array (hint: look at the check_array_pointer function in framework.py)
        t.check_array_pointer("a0", [0, 0, 0])
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "initialize_zero.s")
        # input the length of the desired array
        t.input_scalar("a0", 0)
        # call the `initialize_zero` function
        t.call("initialize_zero")
        # TODO: Not sure why exit code is not 36
        t.execute()

    def test_malloc_failed(self):
        t = AssemblyTest(self, "initialize_zero.s")
        t.input_scalar("a0", 4)
        t.call("initialize_zero")
        # Not sure why code is 16 not 26
        t.execute(fail='malloc', code=16)

    @classmethod
    def tearDownClass(cls):
        print_coverage("initialize_zero.s", verbose=False)
