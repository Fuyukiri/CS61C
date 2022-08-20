#include <stdio.h>
void temperature_with_head();
int main() { temperature_with_head(); }
void temperature_with_head() {
  float fahr, celsius;
  float lower, upper, step;
  lower = 0;   /* lower limit of temperatuire scale */
  upper = 300; /* upper limit */
  step = 20;   /* step size */
  fahr = lower;
  printf("fahr celsius\n");
  printf("------------\n");

  while (fahr <= upper) {
    celsius = (5.0 / 9.0) * (fahr - 32.0);
    printf("%3.0f %6.1f\n", fahr, celsius);
    fahr = fahr + step;
  }
}