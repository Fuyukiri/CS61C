.globl main

.data
source:
    .word   3
    .word   1
    .word   4
    .word   1
    .word   5
    .word   9
    .word   0
dest:
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0

.text
fun:
    addi t0, a0, 1  # t0 = a0(x) + 1 = 0x00000003 + 1 = 4
    sub t1, x0, a0  # t1 = -x = -3
    mul a0, t0, t1  # a0 = 4 * -3 = -12 (0xFFFFFFF4)
    jr ra # return

main:
    # BEGIN PROLOGUE
    addi sp, sp, -20
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw ra, 16(sp)
    # END PROLOGUE
    addi t0, x0, 0 # t0(k) = 0
    addi s0, x0, 0 # s0(sum) = 0
    la s1, source  # s1 -> source[0] address 0x10000000
    la s2, dest    # s2 -> dest[0] address 0x1000001C
loop:
    slli s3, t0, 2  # s3 = t0(k) << 2 = 0x00000000 || s3 = 1 << 2 = 0x100 = 4 || 2 << 2 = 8
    add t1, s1, s3  # t1 = s1 + s3 = 0x10000000 -> source[0] address || source[1] (4 bytes for a word)
    lw t2, 0(t1)    # t2 = 0x00000003 = source[0]
    beq t2, x0, exit # t2 != 0
    add a0, x0, t2  # a0 = t2 = 0x00000003 = source[0]
    addi sp, sp, -8 # sp = 0x7FFFFFC4 (+8)
    sw t0, 0(sp)  # save t0(k) (0)
    sw t2, 4(sp)  # save t2 (0x00000003)
    jal fun       # --> fun() | a0 = 0xFFFFFFF4(-12)
    lw t0, 0(sp)  # load t0(k) = 0
    lw t2, 4(sp)  # load t2 = 3
    addi sp, sp, 8 # sp = 0x7FFFFFCC (+8)
    add t2, x0, a0 # t2 = a0 = -12
    add t3, s2, s3 # t3 = 0x1000001C + 0 (dest[0] address)
    sw t2, 0(t3)  # dest[0] = t2 = -12
    add s0, s0, t2 # s0 = s0 + t2 = -12
    addi t0, t0, 1 # t0 + 1 k++
    jal x0, loop # return to loop start location
exit:
    add a0, x0, s0
    # BEGIN EPILOGUE
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw ra, 16(sp)
    addi sp, sp, 20
    # END EPILOGUE
    jr ra
