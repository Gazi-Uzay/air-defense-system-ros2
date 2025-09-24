# 📄 Product Requirements Document (PRD)
**Proje:** ROS 2 Tabanlı Hava Savunma Sistemi  
**Hazırlayan:** Tayfur Çınar  
**Tarih:** [24/09/2025]  
**Sürüm:** 1.0

---

## 1. Amaç
Bu proje, Teknofest Hava Savunma Sistemleri yarışmasının üç aşamasına yönelik olarak **hedef tespiti, takip ve angajman** yeteneklerine sahip, ROS 2 tabanlı bir platform sunmayı amaçlar. Sistem; step motor tabanlı PID kontrollü gimbal, gelişmiş görüntü işleme (renk ayrımı ve QR kod algılama dahil), operasyon yönetimi, RTSP video yayını, Wi-Fi haberleşmesi, lazer angajmanı ve yer istasyonu arayüzünden oluşur.

---

## 2. Kapsam
- Gerçek zamanlı gimbal yönlendirme (step motor + PID)  
- Görüntü işleme tabanlı hedef tespiti ve takibi.
- Operation Manager ile mod kontrolü (AUTO_TRACK, MANUAL_TRACK, AUTO_KILL, SAFE).
- Düşük gecikmeli RTSP video yayını.
- Wi-Fi üzerinden güvenilir ROS 2 topic paylaşımı.
- Manuel kontrol ve telemetri takibi için yer istasyonu arayüzü.
- Hareketli hedeflerin renk ayrımı yaparak (kırmızı düşman, mavi dost) otonom takibi ve imhası.
- Silahın sıfır noktasındaki ekranda çıkan QR kod ile hedefe angajman.

---

## 3. Sistem Gereksinimleri

### 3.1. Donanım
- **MCU (ESP32):** Step motor PID döngüsü, IMU ve buton verilerinin toplanması, lazer atış kontrolü.
- **Dahili IMU Sensörü:** Gimbal içerisine yerleştirilmiş, hassas konum verisi sağlar.
- **Fiziksel Butonlar & Kill Switch:** Mod değişimi ve acil durdurma için ESP32'ye bağlı.
- **Raspberry Pi / Jetson:** Görüntü işleme, ROS 2 ana düğüm, RTSP yayını, ağ köprüsü.
- **Step Motor Sürücüleri:** TMC2209/TMC5160 veya eşdeğer.
- **Kamera:** USB veya MIPI CSI, en az 720p@30fps.
- **Wi-Fi Modül:** Raspberry Pi/Jetson dahili Wi-Fi veya harici dongle.

### 3.2. Yazılım
- **ROS 2 Humble / Foxy** veya uyumlu sürüm.
- **micro-ROS:** ESP32 üzerindeki verilerin (IMU, butonlar, gimbal durumu) ROS 2 topic'leri üzerinden paylaşılması için.
- **OpenCV / YOLO / TensorRT:** Hedef tespiti için.
- **RTSP Server (GStreamer / v4l2rtspserver):** Video yayını için.
- **CycloneDDS:** Tercih edilen DDS middleware.
- **PyQt veya Web Tabanlı UI:** Yer istasyonu arayüzü için.
- **ZBar / Quagga (veya benzeri kütüphane):** QR kod algılama ve çözme için.

---

## 4. Fonksiyonel Gereksinimler

### 4.1. Gimbal PID Kontrolü
- Step motor PID döngüsü MCU üzerinde ≥ 500 Hz frekansta çalışmalı.
- `/gimbal/cmd` topic’inden açı komutu almalı.
- `/gimbal/feedback` topic’inde güncel açı ve IMU verisi yayınlanmalı.
- Limit switch ile güvenli park/homing yapılabilmeli.

### 4.2. Görüntü İşleme
- Kameradan alınan görüntüde hedef(ler) tespit edilmeli (≥ 15 FPS).
- **Aşama 1 için:** Renk ayrımı yapmadan hareketli hedefler tespit edilmeli.
- **Aşama 2 için:** Hareketli hedefler kırmızı (düşman) ve mavi (dost) olarak ayırt edilmeli.
- **Aşama 3 için:** Silahın sıfır noktasındaki ekranda çıkan QR kodlar algılanmalı ve çözülmeli.
- Her hedef için **ID, konum, güven skoru ve renk bilgisi (varsa)** hesaplanmalı.
- `/vision/targets` topic’inde sürekli yayın yapılmalı (hedef bilgileri ve QR kod verisi dahil).

### 4.3. Operation Manager
- 5 mod desteklemeli:
  - **AUTO_TRACK (Aşama 1):** Görüntü işleme ile renk ayrımı yapmadan kilitlenen hedefi otonom olarak merkezde tutar. Angajman manueldir (Yer istasyonundan onay beklenir).
  - **MANUAL_TRACK:** Yer istasyonundan gelen fare komutları ile hedefi merkezde tutar. Angajman manueldir (Yer istasyonundan onay beklenir).
  - **AUTO_KILL_COLOR (Aşama 2):** Görüntü işleme ile tespit edilen kırmızı (düşman) hedefleri otonom olarak merkezler ve lazer atışı yapar. Mavi (dost) hedefleri görmezden gelir.
  - **QR_ENGAGE (Aşama 3):** Silahın sıfır noktasındaki ekranda algılanan QR kod verisine göre belirlenen hedefi otonom olarak takip eder ve imha eder.
  - **SAFE:** Gimbal park pozisyonunda kalır, tüm hareketler ve lazer sistemi durur.
- Fiziksel butonlar veya `/op/set_mode` servisi ile mod değişimi yapılabilmeli.
- `/op/state` ile aktif modu yayınlamalı.

### 4.4. Yer İstasyonu Arayüzü
- **Ana Arayüz (PyQt/Web):**
  - RTSP video akışını göstermeli.
  - Video üzerinde fare hareketi ile gimbal'ı kontrol etmeli (`/ui/mouse_target` topic'i üzerinden).
  - Manuel angajman için ayrı bir "ATEŞ ET" butonu içermeli (AUTO_TRACK ve MANUAL_TRACK modları için).
  - Fare tıklaması veya "ATEŞ ET" butonu ile lazer ateşleme komutunu (`/laser/fire`) tetiklemeli.
  - Aşama 2 için hedeflerin renk bilgilerini (kırmızı/mavi) video üzerinde göstermeli.
  - Aşama 3 için algılanan QR kod verisini ve hedeflenen hedefi göstermeli.
- **Telemetri Paneli:** Gimbal açısı, aktif mod, hedef durumu (ID, konum, güven skoru, renk), QR kod verisi gibi verileri göstermeli.

### 4.5. Lazer Angajmanı
- Lazer atış mekanizması ESP32 tarafından kontrol edilmeli.
- **AUTO_KILL_COLOR** ve **QR_ENGAGE** modlarında otonom olarak, **AUTO_TRACK** ve **MANUAL_TRACK** modlarında ise yer istasyonu arayüzünden "ATEŞ ET" butonu veya fare tıklaması ile onay verildiğinde veya ESP32 üzerindeki fiziksel bir buton ile atış yapılabilmeli.
- `/laser/fire` komutu ile tetiklenmeli.

---

## 5. İletişim Katmanı ve Protokoller

### 5.1. Ağ Protokolü
- **Video Yayını:** RTSP/UDP (düşük gecikme için).
- **Telemetri Verileri:** DDS BEST_EFFORT (hızlı ama kayıplı olabilecek veriler için).
- **Komutlar (gimbal, mod):** DDS RELIABLE (güvenilir teslimat için).
- **Acil Durdurma (E-Stop):** Çift kanallı güvenlik (ROS 2 RELIABLE + ESP32 watchdog).

### 5.2. DDS Konfigürasyonu (CycloneDDS)
- **Tercih Sebebi:** Wi-Fi ortamında düşük gecikme, Unicast discovery ile stabil bağlantı, hafif ve gömülü sistem dostu olması.
- **Örnek Konfigürasyon (`~/.cyclonedds.xml`):**
  ```xml
  <CycloneDDS xmlns="https://cdds.eclipseprojects.io/config">
    <Domain id="any">
      <General>
        <NetworkInterfaceAddress>wlan0</NetworkInterfaceAddress>
        <AllowMulticast>false</AllowMulticast>
      </General>
      <Discovery>
        <Peers>
          <Peer address="192.168.1.10"/> <!-- Yer İstasyonu IP -->
          <Peer address="192.168.1.11"/> <!-- Jetson/Pi IP -->
        </Peers>
      </Discovery>
    </Domain>
  </CycloneDDS>
  ```

### 5.3. QoS Profilleri
- Kritik komutlar için **RELIABLE**, hızlı akan telemetri için **BEST_EFFORT** profilleri kullanılacaktır.
- **Örnek Profil (`~/.ros/qos_overrides.yaml`):**
  ```yaml
  profiles:
    gimbal_cmd_profile:
      reliability: reliable
      history: keep_last
      depth: 10
      deadline: { sec: 0, nsec: 50000000 } # 50ms
    telem_fast_profile:
      reliability: best_effort
      history: keep_last
      depth: 20
  ```

---

## 6. Güvenlik ve Failsafe
- **Failsafe Manager:** Yer istasyonundan gelen acil durdurma (kill switch) komutlarını yönetir. Bu komutlar gimbal ve lazer sistemini anında durdurur.
- **Komut Kaybı:** Belirli bir süre komut alınmazsa sistem otomatik olarak **SAFE** moda geçmeli.
- **Limit Switch Koruması:** Donanımsal olarak gimbal'ın kendi sınırlarının dışına çıkması engellenmeli.
- **"No-go Zone":** Yazılımla tanımlanmış, gimbal'ın girmemesi gereken yasak bölgeler.
- **Angajman Onayı:** AUTO_KILL_COLOR ve QR_ENGAGE modları hariç, lazerle ateş etmeden önce operatör onayı gerekliliği.

---

## 7. Performans Gereksinimleri
- **PID Döngüsü:** ≥ 500 Hz (MCU üzerinde)
- **Görüntü İşleme:** ≥ 15 FPS (Pi/Jetson üzerinde)
- **Uçtan Uca Gecikme:** ≤ 300 ms (komut gönderimi ile hareket başlangıcı arası)
- **Mod Geçiş Süresi:** ≤ 200 ms
- **Paket Kaybı (Komutlar):** < %1

---

## 8. Test ve Doğrulama Senaryoları
1. **PID Testi:** Sinüzoidal komut verilerek PID cevabının ne kadar başarılı olduğu ölçülür.
2. **Görüntü İşleme Testi:** Farklı ışık ve mesafe koşullarında hedef maketi kullanılarak tespit doğruluğu (%90+) ölçülür.
3. **Mod Geçiş Testi:** Tüm modlar arasında geçiş senaryoları (AUTO_TRACK → MANUAL_TRACK, MANUAL_TRACK → AUTO_KILL_COLOR, AUTO_KILL_COLOR → QR_ENGAGE, QR_ENGAGE → SAFE, vb.) test edilir.
3.1. **Renk Ayrımı Testi:** Farklı renklerdeki (kırmızı, mavi) hareketli hedefler kullanılarak `AUTO_KILL_COLOR` modunda doğru hedeflerin takip ve imha edildiği, dost hedeflerin ise görmezden gelindiği doğrulanır.
3.2. **QR Kod Angajman Testi:** Silahın sıfır noktasındaki ekranda farklı QR kodlar gösterilerek `QR_ENGAGE` modunda sistemin QR kodu doğru algıladığı, çözdüğü ve belirtilen hedefi imha ettiği doğrulanır.
4. **Ağ Testi:** Wi-Fi sinyalinin zayıfladığı durumlarda paket kaybı ve gecikme analizi yapılır.
5. **Entegre Sistem Testi:** Tam bir "görev" senaryosu uçtan uca çalıştırılır.

---

## 9. Risk Analizi ve Önlemler
- **Risk:** Wi-Fi bağlantısının kopması. **Önlem:** Sistem otomatik olarak **SAFE** moda geçer.
- **Risk:** Görüntü işlemenin yanlış hedefi kilitlemesi. **Önlem:** AUTO_KILL modu hariç, operatör onayı olmadan angajman yapılmaz.
- **Risk:** Step motor veya sürücü arızası. **Önlem:** Sistem hatayı algılayıp SAFE moda geçer.
- **Risk:** Yüksek ağ gecikmesi. **Önlem:** Acil durdurma (E-Stop) komutu her zaman en yüksek önceliğe sahiptir.

---

## 10. Proje Zaman Çizelgesi (Sprint Planı)
- **Sprint 1 (2 Hafta):** Donanım montajı, temel gimbal mekaniği ve PID kontrol yazılımı.
- **Sprint 2 (2 Hafta):** Görüntü işleme pipeline'ının oluşturulması (hedef tespiti).
- **Sprint 3 (2 Hafta)::** RTSP yayını, micro-ROS entegrasyonu ve yer istasyonu arayüzünün ilk versiyonu.
- **Sprint 4 (3 Hafta):** Tüm modların entegrasyonu, Failsafe mekanizmalarının tamamlanması ve saha testleri.

---

## 11. Başarı Kriterleri
- Sistem en az **5 dakika** boyunca kesintisiz ve stabil çalışabilmeli.
- Gimbal, hedefi ekran merkezinde **±1°** açısal hata payı ile tutabilmeli.
- Hedef tespiti doğruluğu **≥ %90** olmalı.
- Uçtan uca komut gecikmesi (operatör komutundan gimbal hareketine kadar) **≤ 300 ms** olmalı.

---
