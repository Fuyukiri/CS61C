#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lfsr.h"

uint16_t get_bit(uint16_t x, uint16_t n);
void lfsr_calculate(uint16_t *reg)
{
    /* YOUR CODE HERE */
    uint16_t new_bit = get_bit(*reg, 0) ^ get_bit(*reg, 2) ^ get_bit(*reg, 3) ^ get_bit(*reg, 5);
    *reg >>= 1;
    *reg |= (new_bit << 15);
}

uint16_t get_bit(uint16_t x, uint16_t n)
{
    return (x >> n) & 1;
}