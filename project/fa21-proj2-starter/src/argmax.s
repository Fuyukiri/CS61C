.globl argmax

.text
# =================================================================
# FUNCTION: Given a int vector, return the index of the largest
#	element. If there are multiple, return the one
#	with the smallest index.
# Arguments:
# 	a0 (int*) is the pointer to the start of the vector
#	a1 (int)  is the # of elements in the vector
# Returns:
#	a0 (int)  is the first index of the largest element
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 57
# =================================================================
argmax:
    # Prologue
    li t0, 1
    blt a1, t0, exception    # if a1 < 1, go to exit
    addi sp, sp, -12
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)

loop_start:
    li t0, 0                 # counter
    li t1, 4                 # size of a word
    li s0, 0                 # index of max
    lw s1, 0(a0)             # max value

loop_continue:
    beq t0, a1, loop_end     # end loop when t0 == a1
    mul t2, t0, t1      
    add t3, t2, a0           # index i
    lw t4, 0(t3)             # array[i]
    addi t0, t0, 1           # i++
    blt s1, t4, update_max   # if s1 < t4, update max value
    j loop_continue

loop_end:
    # Epilogue
    mv a0, s0
    lw ra, 0(sp)
    lw s0, 4(sp)
    lw s1, 8(sp)
    addi sp, sp, 12
	ret

update_max:
    addi t2, t0, -1
    mv s0, t2                # update index
    mv s1, t4                # update max value
    j loop_continue

exception:
    li a1 57 
    call exit2