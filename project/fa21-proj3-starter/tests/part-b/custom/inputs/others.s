addi a0 zero 5
addi a1 zero 10

jal ra Test
jal zero End


Test:
    addi t0 zero 1
    addi t1 zero 10
    jalr zero ra 0

End:
    addi s0 zero 100

jal ra End3

End2:
    addi s0 zero 200
    jalr zero ra 0

End3:
    addi s0 zero 300

jal ra End2

Final:
    addi s0 zero 400