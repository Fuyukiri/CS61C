.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
# - If malloc returns an error,
#   this function terminates the program with error code 88
# - If you receive an fopen error or eof,
#   this function terminates the program with error code 89
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 90
# - If you receive an fread error or eof,
#   this function terminates the program with error code 91
# ==============================================================================
read_matrix:

    # Prologue
    addi sp, sp, -28
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw ra, 24(sp)

    # Prologue
    mv s1, a1                   # row
    mv s2, a2                   # col

    # open file
    mv a1, a0                   # filepath
    li a2, 0                    # read permission 0
    jal fopen
    li t0, -1
    beq a0, t0, fopen_exception # exception 89
    mv s0, a0                   # file descriptor

    # malloc 8 bytes for row, col
    li a0, 8                    # The size of the memory that we want to allocate (in bytes).
    jal malloc
    beqz a0, malloc_exception
    mv s4, a0                   # save pointer location    

    # read file for row, col
    mv a1, s0                   # file descriptor
    mv a2, s4                   # A pointer to the allocated memory. If the allocation failed, this value is 0.
    li a3, 8                    # read 8 bytes (row, col)
    jal fread
    li t0, 8
    bne a0, t0, fread_exception # exception 91
    
    # Allocate space on the heap to store the matrix
    lw t0, 0(s4)
    sw t0, 0(s1)
    lw t1, 4(s4)
    sw t1, 0(s2)

    mul a0, t0, t1              # row * col
    li t0, 4
    mul a0, t0, a0
    mv s5, a0                   # save malloc space for error check
    jal malloc
    beqz a0, malloc_exception
    mv s3, a0                   # save pointer

    # read file
    mv a1, s0                   # file descriptor
    mv a2, s3                   # A pointer to the allocated memory
    mv a3, s5                   # size of read file

    jal fread
    bne a0, s5, fread_exception

    # Close file
    mv a1, s0                   # fd
    jal fclose
    bne a0, x0, fclose_exception

    # Epilogue
    mv a0, s3                   # return pointer

    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28

    ret

malloc_exception:
    li a1, 88
    call exit2

fopen_exception:
    li a1, 89
    call exit2

fclose_exception:
    li a1, 90
    call exit2

fread_exception:
    li a1, 91
    call exit2
