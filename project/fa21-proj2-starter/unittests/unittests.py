from unittest import TestCase
from framework import AssemblyTest

SIMPLE0_ARGS = ["../inputs/simple0/bin/m0.bin", "../inputs/simple0/bin/m1.bin", "../inputs/simple0/bin/inputs/input2.bin"]
LARGER0_ARGS = ["../inputs/larger0/bin/m0.bin", "../inputs/larger0/bin/m1.bin", "../inputs/larger0/bin/inputs/input0.bin"]
MNIST10_ARGS = ["../inputs/mnist/bin/m0.bin", "../inputs/mnist/bin/m1.bin", "../inputs/mnist/bin/inputs/mnist_input10.bin"]
MNIST127_ARGS = ["../inputs/mnist/bin/m0.bin", "../inputs/mnist/bin/m1.bin", "../inputs/mnist/bin/inputs/mnist_input127.bin"]

class TestAbs(TestCase):
    def test_zero(self):
        # load the test for abs.s
        t = AssemblyTest(self, "abs.s")
        # place the input at a0
        t.input_scalar("a0", 0)
        # call the `abs` function
        t.call("abs")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_one(self):
        # load the test for abs.s
        t = AssemblyTest(self, "abs.s")
        # place the input at a0
        t.input_scalar("a0", 1)
        # call the `abs` function
        t.call("abs")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 1)
        # generate the `assembly/TestAbs_test_one.s` file and run it through venus
        t.execute()

    def test_minus_one(self):
        # load the test for abs.s
        t = AssemblyTest(self, "abs.s")
        # place the input at a0
        t.input_scalar("a0", -1)
        # call the `abs` function
        t.call("abs")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 1)
        # generate the `assembly/TestAbs_test_minus_one.s` file and run it through venus
        t.execute()



class TestRelu(TestCase):
    def test_standard(self):
        # load the test for relu.s
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `relu` function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_length_1(self):
        # load the test for relu.s
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([-1])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `relu` function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [0])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "relu.s")
        # set a1 to an invalid length of array
        t.input_scalar("a1", -1)
        # call the `relu` function
        t.call("relu")
        # generate the `assembly/TestRelu_test_invalid_n.s` file and run it through venus
        t.execute(code=57)


class TestArgmax(TestCase):
    def test_standard(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([3, -42, 432, 7, -5, 6, 5, -114, 2])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 2)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_length_1(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([3])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "argmax.s")
        # set a1 to an invalid length of the array
        t.input_scalar("a1", 0)
        # call the `argmax` function
        t.call("argmax")
        # generate the `assembly/TestArgmax_test_invalid_n.s` file and run it through venus
        t.execute(code=57)


class TestDot(TestCase):
    def test_standard(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(v0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 285)
        t.execute()

    def test_stride(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 22)
        t.execute()

    def test_length_1(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([9])
        v1 = t.array([1])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 1)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 9)
        t.execute()

    def test_stride_error1(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 0)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
        t.execute(code=58)

    def test_stride_error2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 0)
        # call the `dot` function
        t.call("dot")
        t.execute(code=58)

    def test_length_error(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 0)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        t.execute(code=57)

    def test_length_error2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", -1)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        t.execute(code=57)


class TestMatmul(TestCase):

    def doMatmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code = 0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # load address of input matrices and set their dimensions
        t.input_array("a0", t.array(m0))
        t.input_scalar("a1", m0_rows)
        t.input_scalar("a2", m0_cols)
        t.input_array("a3", t.array(m1))
        t.input_scalar("a4", m1_rows)
        t.input_scalar("a5", m1_cols)
        # load address of output array
        output_array = t.array([0] * len(result))
        t.input_array("a6", output_array)

        # call the matmul function
        t.call("matmul")
        t.check_array(output_array, result)
        t.execute(code = code)

    def test_standard(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )

    def test_length_1(self):
        self.doMatmul(
            [4], 1, 1,
            [5], 1, 1,
            [20]
        )

    def test_zero_dim_m0(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0], # result does not matter
            code=59
        )

    def test_negative_dim_m0_y(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, -1,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=59
        )

    def test_negative_dim_m0_x(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], -1, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=59
        )

    def test_zero_dim_m1(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0], # result does not matter
            code=59
        )

    def test_negative_dim_m1_y(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, -1,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=59
        )

    def test_negative_dim_m1_x(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], -1, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=59
        )

    def test_unmatched_dims(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 2,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=59
        )


class TestReadMatrix(TestCase):

    def doReadMatrix(self, input_file = "inputs/test_read_matrix/test_input.bin",
     result_row = 3, result_col = 3, result_array = [1, 2, 3, 4, 5, 6, 7, 8, 9], fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", input_file)

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)

        # call the main function within test_read_matrix_no_cc, which randomizes registers and calls read_matrix
        t.call("read_matrix")

        # check the output from the function
        t.check_array(rows, [result_row])
        t.check_array(cols, [result_col])
        t.check_array_pointer("a0", result_array)

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple_read(self):
        self.doReadMatrix()

    def test_simple0(self):
        self.doReadMatrix(input_file = "inputs/simple0/bin/inputs/input2.bin", result_row = 3,
         result_col = 1, result_array= [2, 1, 6])

    def test_larger0(self):
        self.doReadMatrix(input_file = "inputs/larger0/bin/inputs/input0.bin", result_row = 15,
         result_col = 15,
         result_array= [-5, 2, 1, 8, 12, 12, -1, 13, 2, 15, 15, 0, -5, 5, 10,
                        -5, 15, 1, 15, -3, 1, 3, 9, 8, 14, 0, 15, -2, 8, 12,
                        15, 10, 5, 5, 11, 14, 2, -4, 0, -1, 10, 5, 10, 15, 1,
                        5, 6, -5, 6, 12, 13, 6, 13, 8, 8, -3, 8, -4, -1, 12,
                        0, 13, 15, 7, -2, 5, -5, 3, -3, 12, 1, -5, -2, 10, -4,
                        9, -3, 9, 3, -4, 10, 3, 9, 2, -1, 6, 11, 15, 7, 7,
                        -3, 7, 11, 6, 2, 11, -4, 0, -1, 3, 14, 15, 10, 13, -1,
                        9, -5, 7, 10, -1, -5, 12, 8, 7, 12, 3, -5, 4, 2, -3,
                        10, 12, 15, -2, 2, 1, -5, 7, 0, 2, 11, 2, 8, 14, 15,
                        13, -2, 7, 13, 7, 8, 13, 0, 5, 8, 6, 7, 0, -3, 2,
                        15, 12, -1, 12, 10, 15, -3, 12, -1, -4, 0, 6, 3, 7, 2,
                        -4, 7, -2, 9, 12, 5, -1, 12, -4, 10, -3, -4, -4, 10, 2,
                        15, 3, 10, 0, 7, -1, -4, 7, 9, 8, -3, -5, 6, 9, 11,
                        5, 13, 14, 7, 0, 9, 9, -1, 0, 5, 5, 15, -5, -5, 12,
                        0, 2, -5, 0, 9, -1, 14, 3, 3, -1, 0, 7, 5, 14, 13])

    def test_fail_fopen(self):
        self.doReadMatrix(fail='fopen', code=89)

    def test_fail_fread(self):
        self.doReadMatrix(fail='fread', code=91)

    def test_fail_fclose(self):
        self.doReadMatrix(fail='fclose', code=90)

    def test_fail_malloc(self):
        self.doReadMatrix(fail='malloc', code=88)


class TestWriteMatrix(TestCase):

    def doWriteMatrix(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        outfile = "outputs/test_write_matrix/student.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", t.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        t.input_scalar("a2", 3)  # rows
        t.input_scalar("a3", 3)  # columns
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if code == 0:
            t.check_file_output(outfile, "outputs/test_write_matrix/reference.bin")

    def test_simple(self):
        self.doWriteMatrix()

    def test_fail_fopen(self):
        self.doWriteMatrix(fail='fopen', code=89)

    def test_fail_fwrite(self):
        self.doWriteMatrix(fail='fwrite', code=92)

    def test_fail_fclose(self):
        self.doWriteMatrix(fail='fclose', code=90)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def run_classify(self, input_dir, input, output_id, msg: str = "", fail='', code=0):
        t = self.make_test()
        output_dir = "outputs/test_basic_main"
        outfile = f"{output_dir}/student{output_id}.bin"
        args = [f"{input_dir}/m0.bin", f"{input_dir}/m1.bin", f"{input_dir}/inputs/{input}", outfile]
        silent = len(msg) == 0
        t.input_scalar("a2", 1 if silent else 0)
        t.call("classify")
        t.execute(fail=fail, code=code, args=args)
        if code == 0:
            t.check_file_output(outfile, f"{output_dir}/reference{output_id}.bin")
            t.check_stdout(msg)

    def test_simple0_input0(self):
        self.run_classify(input_dir="inputs/simple0/bin", input="input0.bin", output_id=0)

    def test_simple0_input0_print_out(self):
        self.run_classify(input_dir="inputs/simple0/bin", input="input0.bin", output_id=0, msg="2")

    def test_fail_malloc(self):
        # unfortunately this test actually does not fail inside classify, but inside read_matrix
        self.run_classify(input_dir="inputs/simple0/bin", input="input0.bin", output_id=0, fail="malloc", code=88)

    def test_wrong_number_of_args(self):
        t = self.make_test()
        t.call("classify")
        t.execute(code=72, args=[""])

# The following are some simple sanity checks:
import subprocess, pathlib, os
script_dir = pathlib.Path(os.path.dirname(__file__)).resolve()

def compare_files(test, actual, expected):
    assert os.path.isfile(expected), f"Reference file {expected} does not exist!"
    test.assertTrue(os.path.isfile(actual), f"It seems like the program never created the output file {actual}")
    # open and compare the files
    with open(actual, 'rb') as a:
        actual_bin = a.read()
    with open(expected, 'rb') as e:
        expected_bin = e.read()
    test.assertEqual(actual_bin, expected_bin, f"Bytes of {actual} and {expected} did not match!")


class TestMain(TestCase):
    """ This sanity check executes src/main.s using venus and verifies the stdout and the file that is generated.
    """

    def run_venus(self, args):
        venus_jar = pathlib.Path('tools') / 'venus.jar'
        cmd = ['java', '-jar', venus_jar, '--immutableText', '--maxsteps', '-1', '--callingConvention'] + args
        # run venus from the project root directory
        r = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=script_dir / '..')
        return r.returncode, r.stdout.decode('utf-8').strip()

    def run_main(self, inputs, output_id, lbl):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin", f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"

        code, stdout = self.run_venus(["src/main.s"] + args)
        self.assertEqual(code, 0, stdout)
        self.assertEqual(stdout, lbl)

        compare_files(self, actual=script_dir / '..' / args[-1], expected=script_dir / '..' / reference)

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")

    def test_chain_main(self):
        code, stdout = self.run_venus(["src/tests/main_chain.s"])

        outfile_simple = f"reference_outputs/files/generic/std_cm_simple0.bin"
        reffile_simple = f"reference_outputs/files/generic/ref_simple0.bin"
        outfile_larger = f"reference_outputs/files/generic/std_cm_larger0.bin"
        reffile_larger = f"reference_outputs/files/generic/ref_larger0.bin"

        compare_files(self, actual = script_dir / '..' / outfile_simple, expected = script_dir / '..' / reffile_simple)
        compare_files(self, actual = script_dir / '..' / outfile_larger, expected = script_dir / '..' / reffile_larger)
        self.assertEqual(stdout, "Two classifications:\n2\n2\nTwo classifications:\n2\n48\nTwo classifications:\n48\n48")
