#include "tick.h"

Tick::Tick() {
    StartTime = tick();
}

uint64_t Tick::Measure() {
    return tick() - StartTime;
}
