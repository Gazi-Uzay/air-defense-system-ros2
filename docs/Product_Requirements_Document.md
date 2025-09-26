# 📄 Product Requirements Document (PRD) - HSS Projesi

**Proje:** ROS 2 Tabanlı Yönlendirilmiş Savunma Sistemi
**Kaynak Doküman:** `HSS ROS 2 İletişim Mimarisi.md`
**Sürüm:** 2.1
**Tarih:** 26/09/2025

---

## 1. Amaç

Bu doküman, ROS 2 mimarisi üzerine kurulu, hedef tespiti, takibi ve angajman yeteneklerine sahip bir savunma sisteminin gereksinimlerini tanımlar. Sistemin temel amacı, bir kamera aracılığıyla hedefleri tespit etmek, bir operatör arayüzü üzerinden sistemi yönetmek ve bir gimbal üzerine monte edilmiş bir lazer ile hedeflere angajman sağlamaktır.

---

## 2. Kapsam

-   **Gerçek Zamanlı Görüntü Aktarımı:** Ham ve işlenmiş video akışlarının yer istasyonuna iletilmesi.
-   **Görüntü İşleme:** Görüntü üzerinden hedef tespiti, renk ve QR kod bilgilerinin çıkarılması.
-   **Operasyon Yönetimi:** Sistemin farklı çalışma modları arasında (Güvenli, Manuel Takip, Otomatik Takip, Otomatik İmha) geçiş yapmasını sağlayan merkezi bir mantık birimi.
-   **Gimbal Kontrolü:** Merkezi yönetim biriminden gelen komutlarla gimbal'ın hedefe yönlendirilmesi.
-   **Donanım Arayüzü:** Düşük seviyeli donanım (motorlar, IMU, lazer) ile ROS 2 dünyası arasında köprü kuran bir mikrodenetleyici.
-   **Yer İstasyonu Arayüzü:** Operatörün sistemi izlemesine, manuel olarak kontrol etmesine ve komutlar göndermesine olanak tanıyan bir kullanıcı arayüzü.
-   **Güvenlik Mekanizmaları:** Sistem genelinde geçerli bir acil durum durdurma (E-Stop) mekanizması.

---

## 3. Fonksiyonel Gereksinimler

### 3.1. Görüntüleme Sistemi (`camera_publisher_node`, `vision_node`)

-   Sistem, birincil kameradan ham görüntü verisini `/camera/image_raw` topic'i üzerinden sürekli olarak yayınlamalıdır.
-   `vision_node`, `/camera/image_raw` topic'ine abone olarak görüntüleri işlemelidir.
-   İşleme sonucunda tespit edilen hedeflerin bilgileri (`id`, 3D pozisyon, güven skoru, renk, QR kod verisi) `/vision/targets` topic'inde `hss_interfaces/TargetArray` formatında yayınlanmalıdır.
-   Hata ayıklama ve görsel doğrulama için, hedeflerin üzerine çizildiği işlenmiş görüntü `/vision/image_processed` topic'inde yayınlanmalıdır.

### 3.2. Operasyon Yönetimi (`operation_manager_node`)

-   Sistem, `Communication_Architecture.md` dosyasında tanımlanan operasyonel modları desteklemelidir. Bunlar en az şunları içerir: `SAFE`, `MANUAL_TRACK`, `AUTO_TRACK`, `AUTO_KILL_COLOR`, `QR_ENGAGE` ve `EMERGENCY`.
-   Mevcut mod durumu, `/op/state` topic'i üzerinden `hss_interfaces/OpState` formatında yayınlanmalıdır.
-   Mod değişiklikleri, `/op/set_mode` servisi aracılığıyla talep edilmelidir.
-   `AUTO_TRACK` modunda, `/vision/targets` verisini kullanarak kilitlenen hedefi merkezde tutacak şekilde `/gimbal/cmd` topic'i üzerinden `hss_interfaces/GimbalCommand` komutları üretilmelidir.
-   `AUTO_KILL` (veya `AUTO_KILL_COLOR`) modunda aşağıdaki adımlar izlenmelidir:
    1.  Geçerli bir düşman hedef tespit edildiğinde, gimbal hedefi merkezlemek için yönlendirilir.
    2.  Hedef merkezde stabil tutulduğunda bir "kilitlenme sayacı" başlatılır.
    3.  Bu sayacın süresi bir **parametre** ile ayarlanabilmelidir (örn: `lock_on_duration_s = 1.5`).
    4.  Hedef bu süre boyunca merkezde kalırsa "kilitlendi" kabul edilir ve `/laser/fire` servisi aracılığıyla ateşleme komutu gönderilir.
    5.  Hedef süre dolmadan kaybolursa sayaç sıfırlanır ve süreç yeniden başlar.
-   `MANUAL_TRACK` modunda, `/ui/mouse_target` verisini kullanarak gimbal komutları üretilmelidir.
-   Sistem, `/op/emergency_stop` topic'ine abone olmalı ve `true` mesajı aldığında `EMERGENCY` moduna geçmelidir.
-   Lazer ateşlemesi için `/laser/fire` servisine istemci (client) olmalıdır.
-   Gimbal ve IMU telemetrisini dinleyerek genel sistem sağlığı izlenmelidir: `/gimbal/motor_feedback` (`hss_interfaces/GimbalMotorFeedback`) ve `/gimbal/imu` (`sensor_msgs/Imu`).

### 3.3. Gimbal Kontrolü (`gimbal_control_node`)

-   Bu düğüm, `/gimbal/cmd` topic'inden gelen `hss_interfaces/GimbalCommand` komutlarını dinlemelidir.
-   Gelen komutları yorumlayarak gimbal motorları için düşük seviyeli kontrol sinyallerini üretmelidir.

### 3.4. Donanım Ajanı (`micro_ros_agent`)

-   Gimbal'ı oluşturan step motorların **gerçek zamanlı PID kontrol döngüsünü** çalıştırmalıdır. Bu döngü, `/gimbal/cmd` topic'inden gelen hedef açı (setpoint) ile sensörlerden okunan mevcut açı arasındaki hatayı minimize etmelidir.
-   Bu birim (ESP32), düşük seviyeli donanım görevlerinden sorumlu olmalıdır.
-   Gimbal'ın mevcut açısal konumunu ve durumunu `/gimbal/motor_feedback` topic'inde yayınlamalıdır.
-   Gimbal üzerine monte edilmiş IMU sensöründen okuduğu veriyi `/gimbal/imu` topic'inde `sensor_msgs/Imu` formatında yayınlamalıdır.
-   Fiziksel bir acil durum butonu bağlandığında, bu butona basılmasını `/op/emergency_stop` topic'i üzerinden bildirmelidir.
-   Lazer ateşleme mekanizmasını kontrol etmeli ve bu işlevselliği `/laser/fire` servisi olarak sunmalıdır.

### 3.5. Yer İstasyonu (`ground_station_node`)

-   Operatör için birincil kontrol ve izleme arayüzü sağlamalıdır.
-   Ham (`/camera/image_raw`) ve işlenmiş (`/vision/image_processed`) video akışlarını gösterebilmeli, aralarında geçiş yapma imkanı sunmalıdır.
-   Tüm önemli telemetri verilerini (`/vision/targets`, `/gimbal/motor_feedback`, `/op/state`, `/gimbal/imu`) anlık olarak göstermelidir.
-   Operatörün video akışı üzerinde fare ile hedef belirlemesine olanak tanımalı ve bu komutları `/ui/mouse_target` topic'inde yayınlamalıdır.
-   Arayüzde, `SAFE`, `MANUAL_TRACK`, `AUTO_TRACK` gibi operasyonel modlar arasında geçişi sağlayan **özel butonlar** bulunmalıdır. Bu butonlar `/op/set_mode` servisini kullanmalıdır.
-   Manuel lazer ateşlemesini, arayüzdeki özel bir "ATEŞ ET" butonu veya doğrudan video akışı üzerine fare ile tıklama yoluyla tetikleyebilmeli ve bu komutu `/laser/fire` servisi üzerinden göndermelidir.
-   Arayüzde bulunan bir acil durum butonu ile `/op/emergency_stop` topic'ine yayın yapabilmelidir.

---

## 4. İletişim Mimarisi Özeti

Bu gereksinimler, `HSS ROS 2 İletişim Mimarisi.md` dokümanında detaylandırılan ROS 2 topic ve service yapısı ile karşılanacaktır. Kritik veriler (komutlar, hedef listesi) **Reliable**, yüksek frekanslı telemetri verileri (görüntü, IMU) ise **Best Effort** QoS profilleri ile iletilecektir. Acil durum sinyalleri, kayıpsız teslimat garantisi için **Reliable** olacaktır.
