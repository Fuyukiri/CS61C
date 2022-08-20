#include <stdio.h>

void celsius_to_fahrenheit();
int main() { celsius_to_fahrenheit(); }

// exercise 1.4
void celsius_to_fahrenheit() {
  float fahr, celsius;
  float lower, upper, step;
  lower = -17.8;   /* lower limit of temperatuire scale */
  upper = 300; /* upper limit */
  step = 10;   /* step size */
  celsius = lower;
  fahr = 0;
  while (fahr <= upper) {
    fahr = (9.0 / 5.0) * celsius + 32.0;
    printf("%6.1f %3.0f\n", celsius, fahr);
    celsius = celsius + step;
  }
}