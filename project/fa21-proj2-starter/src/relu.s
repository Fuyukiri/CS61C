.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
# 	a0 (int*) is the pointer to the array
#	a1 (int)  is the # of elements in the array
# Returns:
#	None
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 57
# ==============================================================================
relu:
    # Prologue
    li t0, 1
    blt a1, t0, exception    # if a1 < 1, go to exit
    addi sp, sp, -4
    sw ra, 0(sp)

loop_start:
    li t0, 0                 # counter
    li t1, 4                 # size of a word

loop_continue:
    beq t0, a1, loop_end
    mul t2, t0, t1      
    add t3, t2, a0           # index i
    lw t4, 0(t3)             # array[i]
    addi t0, t0, 1
    blt t4, x0, change_sign
    j loop_continue

loop_end:
    # Epilogue
    lw ra, 0(sp)
    addi sp, sp, 4
	ret

change_sign:
    sw x0, 0(t3)
    j loop_continue

exception:
    li a1 36 
    call exit2
