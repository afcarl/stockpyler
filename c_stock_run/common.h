#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define container_of(ptr, type, member)                                                                                \
  ({                                                                                                                   \
    typeof(((type *)0)->member) *__mptr = (ptr);                                                                       \
    (type *)(void *)((char *)__mptr - offsetof(type, member));                                                         \
  })

typedef uint8_t u8;
typedef int8_t s8;
typedef uint16_t u16;
typedef int16_t s16;
typedef uint32_t u32;
typedef int32_t s32;
typedef uint64_t u64;
typedef int64_t s64;
typedef __uint128_t u128;
typedef __int128_t s128;
typedef float f32;
typedef double f64;

#ifdef __clang__
#define _vector(datatype, n) datatype __attribute__((ext_vector_type(n)))
#elif __GNUC__
#define _vector(datatype, n) datatype __attribute__((vector_size(n * sizeof(datatype))))
#else //msvc
#define _vector(datatype, n) datatype 
#endif

typedef _vector(u8, 16)  v16ub;
typedef _vector(s8, 16) v16sb;
typedef _vector(u16, 8) v8uh;
typedef _vector(s16, 8) v8sh;
typedef _vector(u32, 4) v4uw;
typedef _vector(s32, 4) v4sw;
typedef _vector(u64, 2) v2ud;
typedef _vector(s64, 2) v2sd;

typedef _vector(u8, 4) v4ub;
typedef _vector(s8, 4) v4sb;
typedef _vector(u16, 2) v2uh;
typedef _vector(s16, 2) v2sh;

typedef _vector(u8, 2) v2ub;
typedef _vector(s8, 2) v2sb;

typedef _vector(f32, 4) v4f;
typedef _vector(f64, 4) v4d;

#undef _vector

typedef union f32_u32_convert_t {
	f32 f;
	u32 i;
} f32_u32_convert_t;

#define warn(msg, ...)                                                                                                 \
  do {                                                                                                                 \
    printf(msg, ##__VA_ARGS__);                                                                                        \
  } while (0)

#define bail(msg, ...)                                                                                                 \
  do {                                                                                                                 \
    printf("encountered fatal error at %d in file %s\n", __LINE__, __FILE__);                                          \
    printf(msg, ##__VA_ARGS__);                                                                                        \
    exit(1);                                                                                                           \
  } while (0)

#define bail_if(condition, msg, ...)                                                                                   \
  do {                                                                                                                 \
    if (condition) {                                                                                                   \
      bail(msg, ##__VA_ARGS__);                                                                                        \
    }                                                                                                                  \
  } while (0)

#define bail_if_not(condition, msg, ...)                                                                               \
  do {                                                                                                                 \
    if (!(condition)) {                                                                                                \
      bail(msg, ##__VA_ARGS__);                                                                                        \
    }                                                                                                                  \
  } while (0)

#define ARRAY_LEN(x) ((int)(sizeof(x) / sizeof((x)[0])))

#ifdef MIN
#undef MIN
#endif

#define MIN(x, y)                                                                                                      \
  ({                                                                                                                   \
    typeof(x) _x = (x);                                                                                                \
    typeof(y) _y = (y);                                                                                                \
    (void)(&_x == &_y);                                                                                                \
    _x < _y ? _x : _y;                                                                                                 \
  })

#ifdef MAX
#undef MAX
#endif

#define MAX(x, y)                                                                                                      \
  ({                                                                                                                   \
    typeof(x) _x = (x);                                                                                                \
    typeof(y) _y = (y);                                                                                                \
    (void)(&_x == &_y);                                                                                                \
    _x > _y ? _x : _y;                                                                                                 \
  })

typedef enum error_type_e
{
	E_SUCCESS,
	E_FAILURE,
}error_type_e;

#ifdef __clang__ 
#define attr_cleanup(cleanup_func) __attribute__((cleanup(cleanup_func)))
#else
#define attr_cleanup(cleanup_func)
#endif