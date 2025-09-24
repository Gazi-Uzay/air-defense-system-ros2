# Yapılacaklar Listesi (TO-DO List)

Bu belge, "ROS 2 Tabanlı Hava Savunma Sistemi" PRD'sinde belirtilen gereksinimler ve kapsam doğrultusunda geliştirme sürecinde tamamlanması gereken görevleri listelemektedir.

## 2. Kapsam
- [ ] Gerçek zamanlı gimbal yönlendirme (step motor + PID) sistemini geliştir.
- [ ] Görüntü işleme tabanlı hedef tespiti ve takibi sistemini geliştir.
- [ ] Operation Manager ile mod kontrolü (AUTO_TRACK, MANUAL_TRACK, AUTO_KILL, SAFE) sistemini geliştir.
- [ ] Düşük gecikmeli RTSP video yayını sistemini entegre et.
- [ ] Wi-Fi üzerinden güvenilir ROS 2 topic paylaşımını sağla.
- [ ] Manuel kontrol ve telemetri takibi için yer istasyonu arayüzünü geliştir.

## 3. Sistem Gereksinimleri
### 3.1. Donanım
- [ ] MCU (ESP32) temin et ve konfigüre et (Step motor PID döngüsü, IMU ve buton verilerinin toplanması, lazer atış kontrolü için).
- [ ] Dahili IMU Sensörünü gimbal içerisine yerleştir ve entegre et.
- [ ] Fiziksel Butonlar ve Kill Switch'i ESP32'ye bağla ve işlevselliğini sağla.
- [ ] Raspberry Pi / Jetson temin et ve konfigüre et (Görüntü işleme, ROS 2 ana düğüm, RTSP yayını, ağ köprüsü için).
- [ ] Step Motor Sürücülerini (TMC2209/TMC5160 veya eşdeğer) temin et ve entegre et.
- [ ] Kamerayı (USB veya MIPI CSI, en az 720p@30fps) temin et ve entegre et.
- [ ] Wi-Fi Modülü (Raspberry Pi/Jetson dahili Wi-Fi veya harici dongle) konfigüre et.

### 3.2. Yazılım
- [ ] ROS 2 Humble / Foxy veya uyumlu sürümü kur ve konfigüre et.
- [ ] micro-ROS'u ESP32 üzerinde kur ve entegre et (IMU, butonlar, gimbal durumu için ROS 2 topic paylaşımı).
- [ ] OpenCV / YOLO / TensorRT'yi hedef tespiti için entegre et.
- [ ] RTSP Server'ı (GStreamer / v4l2rtspserver) video yayını için kur ve konfigüre et.
- [ ] CycloneDDS'i tercih edilen DDS middleware olarak konfigüre et.
- [ ] PyQt veya Web Tabanlı UI kullanarak yer istasyonu arayüzünü geliştir.

## 4. Fonksiyonel Gereksinimler
### 4.1. Gimbal PID Kontrolü
- [ ] Step motor PID döngüsünü MCU üzerinde ≥ 500 Hz frekansta çalışacak şekilde geliştir.
- [ ] `/gimbal/cmd` topic’inden açı komutlarını alacak mekanizmayı geliştir.
- [ ] `/gimbal/feedback` topic’inde güncel açı ve IMU verisini yayınla.
- [ ] Limit switch ile güvenli park/homing işlevselliğini sağla.

### 4.2. Görüntü İşleme
- [ ] Kameradan alınan görüntüde hedef(ler)i tespit et (≥ 15 FPS).
- [ ] Her hedef için ID, konum, güven skoru hesapla.
- [ ] `/vision/targets` topic’inde sürekli yayın yap.

### 4.3. Operation Manager
- [ ] AUTO_TRACK modunu geliştir (Görüntü işleme ile kilitlenen hedefi otonom olarak merkezde tutar).
- [ ] MANUAL_TRACK modunu geliştir (Yer istasyonundan gelen fare komutları ile hedefi merkezde tutar).
- [ ] AUTO_KILL modunu geliştir (Görüntü işleme ile kilitlenen hedefi otonom olarak merkezler ve lazer atışı yapar).
- [ ] SAFE modunu geliştir (Gimbal park pozisyonunda kalır, tüm hareketler ve lazer sistemi durur).
- [ ] Fiziksel butonlar veya `/op/set_mode` servisi ile mod değişimi işlevselliğini sağla.
- [ ] `/op/state` ile aktif modu yayınla.

### 4.4. Yer İstasyonu Arayüzü
- [ ] RTSP video akışını ana arayüzde göster.
- [ ] Video üzerinde fare hareketi ile gimbal'ı kontrol et (`/ui/mouse_target` topic'i üzerinden).
- [ ] Fare tıklaması ile lazer ateşleme komutunu (`/laser/fire`) tetikleme işlevselliğini sağla.
- [ ] Telemetri Paneli'ni geliştir (Gimbal açısı, mod, hedef durumu gibi verileri göstermeli).

### 4.5. Lazer Angajmanı
- [ ] Lazer atış mekanizmasını ESP32 tarafından kontrol edilecek şekilde geliştir.
- [ ] AUTO_KILL modunda otonom atış işlevselliğini sağla.
- [ ] AUTO_TRACK ve MANUAL_TRACK modlarında yer istasyonu arayüzünden fare tıklaması ile onay verildiğinde atış işlevselliğini sağla.
- [ ] ESP32 üzerindeki fiziksel bir buton ile atış işlevselliğini sağla.
- [ ] `/laser/fire` komutu ile tetikleme işlevselliğini sağla.

## 5. İletişim Katmanı ve Protokoller
### 5.1. Ağ Protokolü
- [ ] RTSP/UDP video yayını için konfigüre et.
- [ ] DDS BEST_EFFORT QoS profilini telemetri verileri için kullan.
- [ ] DDS RELIABLE QoS profilini komutlar (gimbal, mod) için kullan.
- [ ] Çift kanallı güvenlikli Acil Durdurma (E-Stop) mekanizmasını geliştir (ROS 2 RELIABLE + ESP32 watchdog).

### 5.2. DDS Konfigürasyonu (CycloneDDS)
- [ ] CycloneDDS'i Wi-Fi ortamında düşük gecikme, Unicast discovery ile stabil bağlantı sağlayacak şekilde konfigüre et.
- [ ] `~/.cyclonedds.xml` dosyasını örnek konfigürasyona göre ayarla (Yer İstasyonu ve Jetson/Pi IP'lerini güncelle).

### 5.3. QoS Profilleri
- [ ] `~/.ros/qos_overrides.yaml` dosyasını örnek profillere göre oluştur ve konfigüre et (gimbal_cmd_profile, telem_fast_profile).

## 6. Güvenlik ve Failsafe
- [ ] Failsafe Manager'ı geliştir (Yer istasyonundan gelen acil durdurma komutlarını yönetir, gimbal ve lazer sistemini anında durdurur).
- [ ] Komut kaybı durumunda sistemin otomatik olarak SAFE moda geçmesini sağla.
- [ ] Limit Switch Korumasını donanımsal olarak entegre et.
- [ ] "No-go Zone" yazılımsal kısıtlamalarını tanımla ve uygula.
- [ ] AUTO_KILL modu hariç, lazerle ateş etmeden önce operatör onayı gerekliliğini uygula.

## 9. Risk Analizi ve Önlemler
- [ ] Wi-Fi bağlantısının kopması riskine karşı önlem al (Sistemin otomatik olarak SAFE moda geçmesini sağla).
- [ ] Görüntü işlemenin yanlış hedefi kilitlemesi riskine karşı önlem al (AUTO_KILL modu hariç, operatör onayı olmadan angajman yapılmamasını sağla).
- [ ] Step motor veya sürücü arızası riskine karşı önlem al (Sistemin hatayı algılayıp SAFE moda geçmesini sağla).
- [ ] Yüksek ağ gecikmesi riskine karşı önlem al (Acil durdurma (E-Stop) komutunun her zaman en yüksek önceliğe sahip olmasını sağla).

## 8. Test ve Doğrulama Senaryoları
- [ ] PID Testini gerçekleştir (Sinüzoidal komut verilerek PID cevabının başarısını ölç).
- [ ] Görüntü İşleme Testini gerçekleştir (Farklı ışık ve mesafe koşullarında hedef maketi kullanarak tespit doğruluğunu ölç).
- [ ] Mod Geçiş Testini gerçekleştir (Tüm modlar arasında geçiş senaryolarını test et).
- [ ] Ağ Testini gerçekleştir (Wi-Fi sinyalinin zayıfladığı durumlarda paket kaybı ve gecikme analizi yap).
- [ ] Entegre Sistem Testini gerçekleştir (Tam bir "görev" senaryosunu uçtan uca çalıştır).

## 11. Başarı Kriterleri
- [ ] Sistem stabilitesini sağla (En az 5 dakika boyunca kesintisiz ve stabil çalışabilmeli).
- [ ] Gimbal hedef tutma hassasiyetini sağla (Hedefi ekran merkezinde ±1° açısal hata payı ile tutabilmeli).
- [ ] Hedef tespiti doğruluğunu sağla (≥ %90 olmalı).
- [ ] Uçtan uca komut gecikmesini optimize et (≤ 300 ms olmalı).