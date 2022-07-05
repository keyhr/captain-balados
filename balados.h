#ifndef ___BALADOS_H___
#define ___BALADOS_H___

#include "Arduino.h"
#include "bala.h"

class Balados : public Bala {
    int16_t current_speed;

  public:
    Balados();

    void rotate(int16_t wheel_speed, short direction = 1);

    void accelerate(int16_t wheel_speed, unsigned int interval = 4);

    void brake(unsigned int interval = 4);
};

#endif  // ___BALADOS_H___
