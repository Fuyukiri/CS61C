# Tools for generate unittest file
import random
registers = ['x0', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 't3', 't4', 't5', 't6']

I_type_instructions = ['addi', 'slli', 'slti', 'xori', 'srli', 'srai', 'ori', 'andi']

for ins in I_type_instructions:
    file_name ='inputs/' + ins + '.s'
    f = open(file_name, 'a')
    for i in range(100):
        rand_value = random.randint(-1000, 1000)
        
        if (ins == 'slli' or ins == 'srai' or ins == 'srli'):
            rand_value = random.randint(0, 5)
        
        f.write(ins + ' ' + random.choice(registers) + ', ' + random.choice(registers) + ', ' + str(rand_value) + '\n')
    f.close()