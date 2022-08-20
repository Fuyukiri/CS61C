#include <stdio.h>
void verify_getchar_EOF();
int main() { verify_getchar_EOF(); }
// exercise 1.6
void verify_getchar_EOF() {
  // quit this funcion by typing "Ctrl+D".
  int c;
  do {
    c = getchar();
    printf("%d\n", c != EOF);
  } while (c != EOF);
}