.import lotsofaccumulators.s

.data
inputarray: .word 1,2,3,4,5,6,7,0
inputarray_zero: .word 0,2,3,4,5,6,7,0

TestPassed: .asciiz "Test Passed!"
TestFailed: .asciiz "Test Failed!"

.text
# Tests if the given implementation of accumulate is correct.
# Input: a0 contains a pointer to the version of accumulate in question. See lotsofaccumulators.s for more details
#
#
#
#The main function currently runs a simple test that checks if accumulator works on the given input array. All versions of accumulate should pass this.
#Modify the test so that you can catch the bugs in four of the five solutions!
main:
    # test 1
    # la a0 inputarray
    # jal accumulatorone
    # li t0 28
    # beq a0 t0 Pass

    # test 2
    # la a0 inputarray
    # addi sp, sp, -4
    # sw t0, 4(sp)
    # jal accumulatortwo
    # li t0 28
    # lw t0, 4(sp)
    # addi sp, sp, 4
    # beq a0 t0 Pass

    # test 3
    # la a0 inputarray
    # li t2 1
    # jal accumulatorfour
    # li t0 28
    # beq a0 t0 Pass

    # test 4
    la a0 inputarray_zero
    jal accumulatorfive
    li t0 0
    beq a0 t0 Pass
Fail:
    la a0 TestFailed
    jal print_string
    j End
Pass:
    la a0 TestPassed
    jal print_string
End:
    jal exit

print_int:
	mv a1 a0
    li a0 1
    ecall
    jr ra
    
print_string:
	mv a1 a0
    li a0 4
    ecall
    jr ra
    
exit:
    li a0 10
    ecall