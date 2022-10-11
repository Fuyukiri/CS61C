.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 57
# - If the stride of either vector is less than 1,
#   this function terminates the program with error code 58
# =======================================================
dot:
    li t0, 1
    blt a2, t0, exception1   # if length < 1, go to exit
    blt a3, t0, exception2  
    blt a4, t0, exception2
    # Prologue
    addi sp, sp, -8
    sw ra, 0(sp)
    sw s0, 4(sp)            # save the result
    li s0, 0

loop_start:
    li t0, 0                 # counter
    li t1, 4                 # size of a word
    li t5, 0                 # index of i + 1
    li t6, 0                 # index of j + 1

loop_continue:
    beq t0, a2, loop_end     # reach the end of array, go to end

    mul t2, t5, t1           # i * 4
    mul t3, t6, t1           # j * 4
    add t2, t2, a0           # index i
    add t3, t3, a1           # index j
    
    lw t2, 0(t2)             # array1[i]
    lw t3, 0(t3)             # array1[j]
    mul t4, t3, t2           # t4 = array1[i] * array1[j]
    add s0, s0, t4           # s0 += t4

    add t5, t5, a3           # i++
    add t6, t6, a4           # j++
    addi t0, t0, 1           # index ++
    j loop_continue

loop_end:
    # Epilogue
    mv a0, s0
    lw ra, 0(sp)
    lw s0, 4(sp)
    addi sp, sp, 8
	ret

exception1:
    li a1 57
    call exit2

exception2:
    li a1 58
    call exit2