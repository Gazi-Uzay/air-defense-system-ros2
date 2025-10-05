# 🚀 HSS Projesi Geliştirme Yol Haritası (Roadmap)

Bu doküman, `docs/architecture/` klasöründeki mimari belgelerine dayanarak projenin geliştirme adımlarını ve hedeflerini tanımlar. Geliştirme süreci, her biri belirli hedeflere sahip 4 ana sprint'e bölünmüştür.

---
## Sprint 1: Temel Altyapı ve Simülasyon (2 Hafta)

Bu sprint'in ana hedefi, projenin temel iskeletini oluşturmak ve donanım katmanının ROS 2 ile haberleşmesini sağlamaktır.

**Görevler:**
1.  **`hss_interfaces` Paketini Tamamla:**
    -   `docs/architecture/Communication_Architecture.md` dosyasının "Mesaj ve Servis Tanımları" bölümünde listelenen tüm özel arayüzleri (`Target.msg`, `GimbalCommand.msg`, `SetMode.srv` vb.) oluştur.
    -   `colcon build` ile arayüzlerin tüm sistem tarafından tanınmasını sağla.
    **Durum:** Tamamlandı ✅

2.  **`hss_firmware` Geliştirmesi (`micro_ros_agent`):**
    -   **`hss_simulation` Paketini Geliştir:** Fiziksel donanım (`hss_firmware`) olmadan geliştirme yapabilmek için gimbal davranışını taklit eden bir simülatör düğümü oluştur.
    -   **Simülatör Entegrasyonu:**
        -   `/gimbal/cmd` topic'ine abone olarak hem pozisyon hem de hız modundaki komutları alacak altyapıyı kur.
        -   Bu komutlara göre basit bir fizik modeli (örn: P kontrolcü ile pozisyon takibi, hız entegrasyonu) çalıştır.
        -   Simüle edilmiş gimbal durumunu (`pan_deg`, `tilt_deg` vb.) `/gimbal/state` topic'inde yayınla.
    **Durum:** Tamamlandı ✅

**Sprint Hedefi:** Simüle edilmiş gimbal'ın, `ros2 topic pub` komutuyla gönderilen manuel pozisyon ve hız komutlarına tepki verebilir hale gelmesi.

**Durum:** Tamamlandı ✅
**Yorum:** Gerçek donanım ile test yapabilmek adına temel mimari testleri gerçekleştirildi.

---
## Sprint 2: Donanım Entegrasyonu (Firmware Temelleri) (2 Hafta)

Bu sprint, Sprint 1'de ertelenen donanım geliştirme görevini ele alır. Amaç, `hss_simulation` düğümünün yerini alabilecek temel bir firmware oluşturmaktır.

**Görevler:**
1.  **`hss_firmware` Geliştirmesi (`micro_ros_agent`):**
    -   **1.1. Donanım Soyutlama Katmanı (HAL):**
        -   **Motor Sürücüleri:** Motorları sürmek için gerekli PWM sinyallerini üreten fonksiyonları (`set_pan_pwm`, `set_tilt_pwm`) yaz.
        -   **IMU Sensörü:** IMU (örn: MPU-6050) ile I2C/SPI üzerinden haberleşerek ham jiroskop ve ivmeölçer verilerini okuyan bir sınıf/modül oluştur.
        -   **Limit Switch'ler:** Pan ve tilt eksenlerinin limit switch'lerinin durumunu okuyan GPIO pinlerini yapılandır.
    -   **1.2. İç Kontrol Döngüsü (Rate PID):**
        -   **micro-ROS Aboneliği:** `/gimbal/cmd_rate` topic'ine abone olarak hedef açısal hızları (`pan_rate_dps`, `tilt_rate_dps`) al.
        -   **PID Algoritması:** Pan ve tilt eksenleri için ayrı ayrı çalışacak, anti-windup korumalı bir PID kontrolcüsü implemente et.
        -   **Gerçek Zamanlı Döngü:** Yüksek frekanslı (örn. 1kHz) bir timer kesmesi (interrupt) içinde aşağıdaki adımları gerçekleştir:
            1.  IMU'dan anlık açısal hızı (`ω_meas`) oku.
            2.  Hedef hız (`ω_cmd`) ile ölçülen hız arasındaki hatayı (`error = ω_cmd - ω_meas`) hesapla.
            3.  PID kontrolcüsünü bu hata ile besleyerek yeni motor PWM değerini hesapla.
            4.  Hesaplanan PWM değerini motor sürücülerine gönder.
    -   **1.3. Güvenlik ve Sınır Kontrolü:**
        -   **Limit Switch Mantığı:** Kontrol döngüsü içinde, limit switch'lerin tetiklenip tetiklenmediğini kontrol et.
        -   **Güvenli Durdurma:** Bir limit tetiklendiğinde, ilgili motorun PWM'ini sıfırla ve PID'nin integral terimini sıfırlayarak (anti-windup) birikmiş hatayı temizle.
    -   **1.4. Telemetri ve Durum Yayını:**
        -   **Açı Hesaplama:** Zaman adımı (`dt`) üzerinden jiroskop verilerini entegre ederek anlık pan ve tilt açılarını (`pan_deg`, `tilt_deg`) tahmin et. (Not: Bu, zamanla kayma (drift) yapacaktır; daha sonra ivmeölçer verisiyle birleştirilerek düzeltilebilir).
        -   **micro-ROS Yayınları:** Daha düşük bir frekansta (örn. 50Hz) aşağıdaki topic'leri yayınla:
            -   `/gimbal/state`: Hesaplanan açıları, anlık hızları ve limit switch durumunu içeren `GimbalState` mesajını yayınla.
            -   `/gimbal/imu`: Ham IMU verilerini içeren `sensor_msgs/Imu` mesajını yayınla.

**Sprint Hedefi:** Fiziksel gimbal'ın, `ros2 topic pub` ile gönderilen hız komutlarına (`/gimbal/cmd_rate`) tepki vermesi ve sonuçta oluşan durumunu (`/gimbal/state` üzerinden açı/hız) ROS 2 ağına geri yayınlayarak kapalı döngü bir testin tamamlanabilmesi.

**Durum:** Başlanmadı
**Yorum:** -

---

## Sprint 3: Görüntüleme ve Kontrol Döngüsü (2 Hafta)

---

Bu sprint, sistemin "gözlerini" oluşturmaya ve bu gözlerden gelen veriyi temel bir kontrol mantığı ile birleştirmeye odaklanır.

**Görevler:**
1.  **`hss_vision` Paketini Geliştir:**
    -   **`camera_driver`:** Kameradan görüntüleri alıp `/camera/image_raw` ve `/camera/camera_info` topic'lerinde yayınlayan düğümü oluştur.
    **Durum:** Tamamlandı ✅
    **Yorum:** [camera_driver-1] [ERROR] [1759625502.369175028] [camera_driver]: Kalibrasyon yüklenirken hata: [Errno 2] No such file or directory: '/home/kairos/.ros/calib/internal.yaml'
    Kamera kalibrasyonu yapıldıktan sonra camera_profil.yaml içerisindeki isimlerle /calib/isim içerisine
    kalibrasyon verileri girilecek. Bununla birlikte camera_info yayınlanmış olacak.
    
    -   **`vision_processor_node` (Temel):** `/camera/image_raw` topic'ine abone olan ve basit bir hedef tespit algoritması (örn: renk tabanlı) çalıştıran düğümü oluştur. Tespit edilen hedefleri `/vision/targets` topic'inde yayınla.
2.  **`hss_control` Paketini Geliştir (`gimbal_controller_node`):**
    -   **Dış Kontrol Döngüsü:** `/vision/targets` topic'ine abone ol. Gelen hedef koordinatlarını (`u,v`) kullanarak bir PI kontrolcü ile `/gimbal/cmd` (veya `/gimbal/cmd_rate`) komutları üret.
3.  **`hss_bringup` Paketini Oluştur:**
    -   Bu sprint'te geliştirilen düğümleri (`camera_driver`, `vision_processor_node`, `gimbal_controller_node`) birlikte başlatan bir `launch.py` dosyası oluştur.

**Sprint Hedefi:** Kameradan alınan canlı video akışında tespit edilen bir hedefin, sistem tarafından otonom olarak merkezde tutulmaya çalışılması (temel görsel servoing).

**Durum:** Başlanmadı
**Yorum:** -

---

## Sprint 4: Merkezi Mantık ve Manuel Operatör Kontrolü (2 Hafta)

Bu sprint, operatörün sistemi manuel olarak kontrol edebilmesini sağlayan merkezi mantık ve kullanıcı arayüzü temellerini atmayı hedefler.

**Görevler:**
1.  **`hss_op_manager` Paketini Geliştir (`operation_manager_node`):**
    -   **Durum Makinesi:** `SAFE`, `MANUAL_TRACK` ve `AUTO_TRACK` modlarını içeren bir durum makinesi (state machine) yapısı kur.
    -   **Manuel Kontrol Mantığı:** `/ui/mouse_target` topic'ine abone ol. `MANUAL_TRACK` modundayken, bu veriyi işleyerek `gimbal_controller_node`'a yönlendirme komutları gönder.
    -   `/op/state` topic'inde mevcut sistem modunu yayınla.
2.  **`hss_gui` Paketini Geliştir (`ground_station_gateway`):**
    -   **Temel Arayüz:** `/vision/image_processed` video akışını gösterecek basit bir UI penceresi oluştur.
    -   **Fare Etkileşimi:** UI üzerindeki fare tıklamalarını yakalayarak `/ui/mouse_target` topic'inde yayınla.
3.  **`hss_bringup` Güncellemesi:**
    -   `operation_manager_node` ve `ground_station_gateway` düğümlerini launch dosyasına ekle.

**Sprint Hedefi:** Operatörün, kullanıcı arayüzündeki video ekranına tıklayarak gimbal'ı manuel olarak hedefe yönlendirebilmesi.

**Durum:** Başlanmadı
**Yorum:** -

---

## Sprint 5: Otonom Angajman ve Tam Entegrasyon (3 Hafta)

Bu son sprint, projenin tam otonom modlarını, güvenlik mekanizmalarını ve kalan tüm özellikleri entegre ederek sistemi tamamlamayı hedefler.

**Görevler:**
1.  **`hss_op_manager` Yeteneklerini Genişlet:**
    -   `AUTO_KILL` modunu implemente et. Bu mod, `/vision/targets` verisini dinleyerek ve `lock_on_duration_s` parametresini kullanarak otonom angajman kararları vermelidir.
    -   **Servis Entegrasyonu:** `/op/set_mode`, `/op/request_fire` ve `/op/clear_emergency` servislerini sunucu olarak implemente et. `/laser/fire` ve `/laser/set_armed` servislerini istemci olarak kullan.
2.  **`hss_gui` Arayüzünü Tamamla:**
    -   Tüm telemetri verilerini (`/op/state`, `/gimbal/state` vb.) gösterecek panelleri ekle.
    -   Mod değiştirme, lazer ateşleme ve acil durum butonlarını arayüze ekle ve ilgili ROS 2 arayüzlerine bağla.
3.  **`hss_firmware` Fonksiyonlarını Tamamla:**
    -   `/laser/fire` ve `/laser/set_armed` servis sunucularını tam olarak implemente ederek lazer donanımını kontrol et.
    -   Fiziksel E-Stop butonunu dinleyerek `/op/emergency_stop` topic'ini yayınla.
4.  **Güvenlik ve Test:**
    -   Tüm sistem genelinde `EMERGENCY` modunun doğru çalıştığını doğrula.
    -   `docs/architecture/Product_Requirements_Document.md`'de listelenen tüm fonksiyonel test senaryolarını uçtan uca çalıştır.

**Sprint Hedefi:** PRD'de tanımlanan tüm gereksinimleri karşılayan, stabil, test edilmiş ve tam fonksiyonel bir sistemin ortaya çıkması.

**Durum:** Başlanmadı
**Yorum:** -