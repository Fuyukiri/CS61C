.globl abs_loss

.text
# =======================================================
# FUNCTION: Get the absolute difference of 2 int arrays,
#   store in a third array and compute the sum
# Arguments:
#   a0 (int*) is the pointer to the start of arr0
#   a1 (int*) is the pointer to the start of arr1
#   a2 (int)  is the length of the arrays
#   a3 (int*) is the pointer to the start of the loss array

# Returns:
#   a0 (int)  is the sum of the absolute loss
# Exceptions:
# - If the length of the array is less than 1,
#   this function terminates the program with error code 57.
# =======================================================
abs_loss:
    # Checking to see if the stride and length is greater than 0.
    li t0 1
    blt a2 t0 exit_bad_len

    li t0 0 # t0 is the loop index "i"
    li t1 0 # t1 is the running total loss

loop_start:
    # Check loop end condition
    beq t0 a2 loop_end

    # Get addresses of "i"th element of both arrays
    slli t2 t0 2 # t2 = index * sizeof(int)
    add t3 t2 a0
    add t4 t2 a1

    # Load "i"th element of both arrays
    lw t5 0(t3)
    lw t6 0(t4)

    bge t6 t5 sub2

sub1:
    sub t2 t5 t6
    j loop_cont

sub2:
    sub t2 t6 t5

loop_cont:
    # Adding the loss to the running total
    add t1 t1 t2

    # Storing the absolute difference into a3
    slli t3 t0 2 # t2 = index * sizeof(int)
    add t3 t3 a3
    sw t2 0(t3)

    # Increment loop index and array pointers
    addi t0 t0 1
    j loop_start

loop_end:
    # Move result into a0 and return
    mv a0 t1
    ret

exit_bad_len:
    li a0 36
    call exit2
