#include <stdio.h>
#include "vec.h"

int main(int argc, char *argv)
{
  FILE *fp = fopen("image.dat", "w+");
  
  for (int y = 0; y < ny; y++) {
    for (int x = 0; x < nx; x++) {
      vec r = {1.0, 0.9, 0.8};
      fprintf(fp, "%d %d %d\n", toInt(r.x), toInt(r.y), toInt(r.z));
    }
  }
  
  return 0;
}
