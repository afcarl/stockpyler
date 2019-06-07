#include <stdbool.h>
#include <time.h>

#include "common.h"
#include "rff_tools.h"

typedef struct history_manager_t {
    bool done;
    time_t today, earliest_date, latest_date;
    rff_t rff;
} history_manager_t;