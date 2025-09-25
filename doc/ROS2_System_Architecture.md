### 6. `/laser/fire`
*   **Açıklama:** Lazer ateşleme komutunu tetikler.
*   **Yayıncı (Publisher):**
    *   `Operasyon Yöneticisi` (AUTO_KILL_COLOR ve QR_ENGAGE modlarında otonom olarak)
    *   `Yer İstasyonu Arayüzü` (Manuel ateşleme onayı ile, fare tıklaması veya "ATEŞ ET" butonu aracılığıyla)
*   **Abone (Subscriber):**
    *   `Gimbal Kontrolcüsü (ESP32)`

### 7. `/camera/image_raw`
*   **Açıklama:** Kamera görüntüsünü ham formatta yayınlar.
*   **Yayıncı (Publisher):**
    *   `Kamera Yayıncısı` (Gerçek veya simüle edilmiş)
*   **Abone (Subscriber):**
    *   `Görüntü İşleme`

## Servisler