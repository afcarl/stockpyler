#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <sys/mman.h>

//#include "rff_tools.h"

#define RFF_LINE_SIZE 128

typedef struct _rff_line_t
{
  long long int timestamp;
  char symbol[24];
  double open, high, low, close, volume, turnover, unadj_close, close_ma200, averagefloat, _pad0, _pad1, _pad2;
} rff_line_t;

typedef struct _rff_t{
  FILE* file_handle;
  void* mmap_handle;
  rff_line_t* lines;
  int64_t len;
  int64_t pos;
  bool done;
} rff_t;


int rff_init(char* path, rff_t* rff);
int rff_close(rff_t* rff);
rff_line_t* next_rff_line(rff_t* rff);
