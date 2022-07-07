#include <M5Stack.h>

#include "bala.h"
#include "balados.h"

Balados balados;
String DATA_PREFIX = String("--");

unsigned long curtime = 0, prevtime = 0, rottime = 0;

void rot(unsigned int dly = 200, bool direction = true) {
    if (curtime - rottime > 1250) {
        balados.rotate(direction ? 200 : -200);
        delay(dly);
        balados.SetSpeed(0, 0);
        rottime = curtime;
    }
}

void setup() {
    M5.begin(true, false, true, true);
    // M5.Power.begin();

    M5.Lcd.setTextDatum(MC_DATUM);
    M5.Lcd.setTextSize(3);
    M5.Lcd.drawString("Capt. Balados", 160, 120, 2);
    delay(2000);

    M5.Lcd.setTextDatum(TL_DATUM);
    M5.Lcd.setTextSize(2);

    // UnitVとの通信ではPort Cにつなぐ
    Serial2.begin(9600, SERIAL_8N1, 16, 17);
}

int i = 0;

void loop() {
    if (i % 5 == 0) {
        // Fireの画面が埋まるのでリセットする
        M5.Lcd.fillScreen(CYAN);
        M5.Lcd.setCursor(0, 10);
        i = 0;
    }

    // UnitVからの結果を格納する
    String str = "";

    // UnitVからの通信を受け取る
    for (int j = 0; j < 25; j++) {
        if (Serial2.available() > 0) {
            str = Serial2.readStringUntil('\n');
            break;
        }
        delay(10);
    }

    curtime = millis();
    Serial.println("[log]" + str);

    if (str != "" && str.startsWith(DATA_PREFIX)) {
        if (str.startsWith(DATA_PREFIX + " found")) {
            if (str.endsWith("center")) {
                M5.Lcd.fillScreen(RED);
                if (curtime - prevtime > 6000) {
                    balados.accelerate(400);
                    // balados.SetSpeed(400, 400);
                    delay(1000);
                    balados.brake();
                    prevtime = curtime;
                }
            } else if (str.endsWith("left")) {
                M5.Lcd.fillScreen(PURPLE);
                rot(100, false);
            } else if (str.endsWith("right")) {
                M5.Lcd.fillScreen(ORANGE);
                rot(100);
            }
        } else {
            rot();
        }
        M5.Lcd.println(str);
        M5.Lcd.println(curtime / 100);
    } else {
        M5.Lcd.println("[UNITV] no signal");
    }

    M5.update();
    delay(100);
    i++;
}
