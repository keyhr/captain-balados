#include <M5Stack.h>

#include "bala.h"
#include "balados.h"

Balados balados;
String DATA_PREFIX = String("--");

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
    Serial.begin(115200);
}

int i = 0;

void loop() {
    if (i % 5 == 0) {
        // Fireの画面が埋まるのでリセットする
        M5.Lcd.fillScreen(BLACK);
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

    unsigned long time = millis();
    Serial.println(str);

    if (str != "" && str.startsWith(DATA_PREFIX)) {
        if (str.startsWith(DATA_PREFIX + " found")) {
            M5.Lcd.fillScreen(RED);
            balados.accelerate(250);
            delay(1000);
            balados.brake();
        }
        M5.Lcd.println(str);
        M5.Lcd.println(time / 100);
    }

    M5.update();
    delay(500);
    i++;
}
