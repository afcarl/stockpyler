#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <sys/mman.h>

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
  bool done;
} rff_t;

int rff_init(char* path, rff_t* rff)
{
  FILE* fp = fopen(path, "rb");
  if(!fp) {
    printf("Could not open %s\n",path);
    return 1;
  }

  fseek(fp, 0, SEEK_END);
  int64_t size = ftell(fp);

  void* mmap_handle = mmap(NULL, size, PROT_READ, MAP_SHARED, fileno(fp), 0);
  if (mmap_handle == MAP_FAILED) {
    return 1;
  }

  rff->file_handle = fp;
  rff->mmap_handle = mmap_handle;
  rff->lines = mmap_handle;
  rff->len = size;
  rff->done = false;

  return 0;
}

rff_line_t* next_rff_line(rff_t* rff)
{
  if ((intptr_t)rff->lines > (intptr_t)rff->mmap_handle + (intptr_t)rff->len){
    return NULL;
  }
  rff_line_t* line = rff->lines;
  rff->lines++;
  return line;
}


int main()
{
  char* path = "/home/forrest/NDExport/ALL_DATA.rff";
  rff_t rff;
  int ret = rff_init(path, &rff);
  printf("rff_init: %d\n",ret);
  rff_line_t* line = next_rff_line(&rff);
  printf("%f\n",line->close);  
  while(line=next_rff_line(&rff)) {
    printf("%s: %f\n",line->symbol, line->close);
    
  }
}


