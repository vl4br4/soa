#include <iostream>

class Tick {
public:
    Tick();
    uint64_t Measure();

private:
    uint64_t StartTime;

    static inline uint64_t tick() {
        uint64_t d;
         __asm__ __volatile__ ("rdtsc" : "=A" (d) );
        return d;
    }
};