#include <cstdint>
#include <cstdio>
#include <sys/mman.h>

#include <string>

#include "rff_tools.hpp"


RFF::RFF(std::string path)
{
  FILE* fp = fopen(path, "rb");
  if(!fp) {
    printf("Could not open %s\n",path);
    return;
  }

  fseek(fp, 0, SEEK_END);
  int64_t size = ftell(fp);

  void* mmap_handle = mmap(NULL, size, PROT_READ, MAP_SHARED, fileno(fp), 0);
  if (mmap_handle == MAP_FAILED) {
    return;
  }

  this.file_handle = fp;
  this.mmap_handle = mmap_handle;
  this.lines = mmap_handle;
  this.len = size / RFF_LINE_SIZE;
  this.pos = 0;
  this.done = false;
}

RFF::~RFF() {
  int ret;
  if (ret = munmap(this.mmap_handle, this.len)) {
    printf("failed to munmap!\n");
	return;
  }
  if (ret = fclose(this.file_handle)){
    printf("failed to fclose!\n");
    return;
  }
  this.file_handle = NULL;
  this.mmap_handle = NULL;
  this.lines = NULL;
  this.len = 0;
}

RFFLine*  RFF::next()
{
  if (this.pos > this.len){
    return nullptr;
  }
  rff_line_t* line = &this.lines[this.pos];
  this.pos++;
  return line;
}

RFFLine* RFF::at(int64_t index)
{
  if (index > this.len){
    return nullptr;
  }
  rff_line_t* line = &this.lines[index];
  return line;
}
