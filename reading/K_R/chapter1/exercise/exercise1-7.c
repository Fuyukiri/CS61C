#include <stdio.h>

void print_EOF();
int main() { print_EOF(); }

// exercise 1.7
void print_EOF() { printf("%d\n", EOF); }