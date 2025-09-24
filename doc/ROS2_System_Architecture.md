# ROS 2 Mimarisi: Node'lar, Topic'ler ve Abonelikler

Bu belge, Hava Savunma Sistemi projesinin ROS 2 tabanlı iletişim mimarisini özetlemektedir.

## Topic'ler ve İlgili Node'lar

### 1. `/gimbal/cmd`
*   **Açıklama:** Gimbal'a hedef açı komutlarını gönderir.
*   **Yayıncı (Publisher):**
    *   `Operasyon Yöneticisi` (AUTO_TRACK modunda)
    *   `Yer İstasyonu Arayüzü` (MANUAL_TRACK modunda, `/ui/mouse_target` verisini işleyerek)
*   **Abone (Subscriber):**
    *   `Gimbal Kontrolcüsü (ESP32)`

### 2. `/gimbal/feedback`
*   **Açıklama:** Gimbal'ın anlık pozisyonunu ve IMU verilerini yayınlar.
*   **Yayıncı (Publisher):**
    *   `Gimbal Kontrolcüsü (ESP32)`
*   **Abone (Subscriber):**
    *   `Yer İstasyonu Arayüzü` (Telemetri için)
    *   `Operasyon Yöneticisi` (Gerekirse pozisyon doğruluğu kontrolü için)

### 3. `/vision/targets`
*   **Açıklama:** Tespit edilen hedeflerin bilgilerini (ID, konum, güven skoru, renk bilgisi) ve Aşama 3 için algılanan QR kod verisini yayınlar.
*   **Yayıncı (Publisher):**
    *   `Görüntü İşleme` (Hedeflerin renk bilgisini ve QR kod verisini `/vision/targets` topic'inde yayınlar)
*   **Abone (Subscriber):**
    *   `Operasyon Yöneticisi` (AUTO_TRACK, AUTO_KILL_COLOR ve QR_ENGAGE modlarında hedefi merkeze almak ve angajman kararı vermek için)
    *   `Yer İstasyonu Arayüzü` (Hedefleri video üzerinde göstermek için)

### 4. `/op/state`
*   **Açıklama:** Sistemin mevcut operasyonel modunu (AUTO_TRACK, MANUAL_TRACK, AUTO_KILL_COLOR, QR_ENGAGE, SAFE) yayınlar.
*   **Yayıncı (Publisher):**
    *   `Operasyon Yöneticisi`
*   **Abone (Subscriber):**
    *   `Yer İstasyonu Arayüzü` (Arayüzde aktif modu göstermek için)

### 5. `/ui/mouse_target`
*   **Açıklama:** Yer istasyonu arayüzündeki fare hareketlerini gimbal kontrolü için yayınlar.
*   **Yayıncı (Publisher):**
    *   `Yer İstasyonu Arayüzü`
*   **Abone (Subscriber):**
    *   `Operasyon Yöneticisi` (MANUAL_TRACK modunda bu veriyi alıp `/gimbal/cmd`'ye yönlendirir)

### 6. `/laser/fire`
*   **Açıklama:** Lazer ateşleme komutunu tetikler.
*   **Yayıncı (Publisher):**
    *   `Operasyon Yöneticisi` (AUTO_KILL_COLOR ve QR_ENGAGE modlarında otonom olarak)
    *   `Yer İstasyonu Arayüzü` (Manuel ateşleme onayı ile, fare tıklaması veya "ATEŞ ET" butonu aracılığıyla)
*   **Abone (Subscriber):**
    *   `Gimbal Kontrolcüsü (ESP32)`

## Servisler

### 1. `/op/set_mode`
*   **Açıklama:** Operasyon modunu (AUTO_TRACK, MANUAL_TRACK, AUTO_KILL_COLOR, QR_ENGAGE, SAFE) değiştirmek için kullanılır.
*   **Servis Sunucusu (Server):**
    *   `Operasyon Yöneticisi`
*   **Servis İstemcisi (Client):**
    *   `Yer İstasyonu Arayüzü`
    *   (Fiziksel butonları dinleyen bir node da istemci olabilir)