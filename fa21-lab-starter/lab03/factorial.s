.globl factorial

.data
n: .word 8

.text
main:
    la t0, n # t0 n address
    lw a0, 0(t0) # a0 = t0[0] = 8
    jal ra, factorial 

    addi a1, a0, 0 # a1 = 8
    addi a0, x0, 1 # a0 = 1
    ecall # Print Result

    addi a1, x0, '\n'
    addi a0, x0, 11
    ecall # Print newline

    addi a0, x0, 10
    ecall # Exit

factorial:
    # YOUR CODE HERE
    addi t0, a0, -1 # t0 = a0 -1 = 7 (current number)
    addi s2, x0, 1 # s2 = 1 (use to minus 1)
loop:
    beq t0, x0, exit # while t0 != 0
    mul a0, a0, t0 # a0 = previous product * current number
    sub t0, t0, s2 # t0 -= 1
    jal x0, loop # loop
exit:
    jr ra  # return a0
