#include "balados.h"

#include "bala.h"

Balados::Balados() : current_speed(0) {}

void Balados::rotate(int16_t wheel_speed, short direction /* =1 */) {
    SetSpeed(wheel_speed * direction, -wheel_speed * direction);
}

void Balados::accelerate(int16_t wheel_speed, unsigned int interval /* = 4 */) {
    int direction = wheel_speed > 0 ? 1 : -1;

    for (int i = abs(wheel_speed) / 4; i < abs(wheel_speed); ++i) {
        // unsigned int left_speed = (i < abs(wheel_speed) * 0.75) ? (i * 1.1) :
        // i;
        unsigned int left_speed = i;
        unsigned int right_speed = i;
        SetSpeed(left_speed * direction * 1.05, right_speed * direction);
        delay(interval);
    }
}

void Balados::brake(unsigned int interval /* = 4 */) {
    int direction = current_speed > 0 ? 1 : -1;
    for (int i = abs(current_speed); i >= 0; --i) {
        SetSpeed(i * direction, i * direction);
        delay(interval);
    }
}
