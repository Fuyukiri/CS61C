addi t0 zero 5
addi t1 zero 20
add t2 zero zero
add a1 zero zero
add a2 zero zero

sw t0 256(a1)
lw a0 256(a1)

sh t1 260(a1)
lh a0 260(a1)

sb t1 264(a1)
lb a0 264(a1)

sw t0 512(a1)
lw a0 512(a1)

sh t1 128(a1)
lh a0 128(a1)

sb t1 768(a0)
lb a2 768(a0)

sh t0 130(a1)
lh t0 130(a1)

sb t1 265(a1)
sb t1 266(a1)
sb t1 267(a1)

lb a0 265(a1)
lb a0 266(a1)
lb a0 267(a1)


