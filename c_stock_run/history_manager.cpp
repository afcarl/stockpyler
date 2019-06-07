#include <stdbool.h>
#include <time.h>

#include "common.h"
#include "rff_tools.h"

class HistoryManager {
    bool done;
    time_t today, earliest_date, latest_date;
    rff_t rff;
} ;