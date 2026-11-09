# Recursos

## Conocimiento

- [cppreference.com](https://en.cppreference.com/)
  Referencia del lenguaje y la biblioteca estándar. Usar para: tipos, `static`, `extern`, sufijos de literales, orden de inicialización, `constexpr`.
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
  Reglas de Stroustrup y Sutter. Usar para: propiedad de objetos, punteros vs referencias, `enum class`, const.
- [Documentación de Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/)
  API del core 3.x. Usar para: LEDC, BLE, WiFi, Preferences (NVS), deep sleep, pines.
- [ESP-IDF Programming Guide (ESP32-S3)](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)
  Lo que hay debajo del core. Usar para: FreeRTOS, memoria, strapping pins, ADC, sleep modes.
- [Hojas de datos de Espressif](https://www.espressif.com/en/support/documents/technical-documents)
  Fuente final para pines, ADC y consumos de cada chip.
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/current/)
  Usar para: claves primarias compuestas, `ON CONFLICT`, row level security.
- [Documentación de Express](https://expressjs.com/)
  Usar para: middlewares, routing, manejo de errores.

## Sabiduría (comunidades)

- [Foro de ESP32 (esp32.com)](https://esp32.com/)
  Foro oficial de Espressif, con ingenieros de la empresa respondiendo. Usar para: comportamientos raros del chip, BLE, sleep.
- [Foro de Arduino](https://forum.arduino.cc/)
  Grande y moderado. Usar para: librerías, cableado, dudas de principiante.
- [r/esp32](https://www.reddit.com/r/esp32/)
  Usar para: revisión de proyectos y diseños.

## Huecos

- Falta una fuente confiable y corta sobre idempotencia en APIs de ingesta de IoT.
- Falta una fuente sobre fragmentación del heap en ESP32 a largo plazo.
- Todo lo de arriba hay que verificarlo al citarlo en una lección: link exacto a la sección, no a la portada.
