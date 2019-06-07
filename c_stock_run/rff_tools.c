#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <sys/mman.h>

#include "rff_tools.h"


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
  rff->len = size / RFF_LINE_SIZE;
  rff->pos = 0;
  rff->done = false;

  return 0;
}

int rff_close(rff_t* rff) {
  int ret;
  if (ret = munmap(rff->mmap_handle, rff->len)) {
    printf("failed to munmap!\n");
    return 1;
  }
  if (ret = fclose(rff->file_handle)){
    printf("failed to fclose!\n");
    return 1;
  }
  rff->file_handle = NULL;
  rff->mmap_handle = NULL;
  rff->lines = NULL;
  rff->len = 0;
  return ret;
}

rff_line_t* next_rff_line(rff_t* rff)
{
  if (rff->pos > rff->len){
    return NULL;
  }
  rff_line_t* line = &rff->lines[rff->pos];
  rff->pos++;
  return line;
}

rff_line_t* rff_line_at(rff_t* rff, int64_t index)
{
  if (index > rff->len){
    return NULL;
  }
  rff_line_t* line = &rff->lines[index];
  return line;
}

#ifdef STANDALONE
int main()
{
  char* path = "/home/forrest/NDExport/ALL_DATA.rff";
  rff_t rff;
  int ret = rff_init(path, &rff);
  printf("rff_init: %d\n",ret);
  rff_line_t* line = next_rff_line(&rff);
  printf("%f\n",line->close);  
  while(line=next_rff_line(&rff)) {
    //printf("%s: %f\n",line->symbol, line->close);
    
  }
  rff_close(&rff);
}
#endif

