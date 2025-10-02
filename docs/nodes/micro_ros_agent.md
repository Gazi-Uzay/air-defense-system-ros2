# 🤖 `micro_ros_agent` (ESP32 Firmware)

**Rol:** Düşük seviyeli donanım (motorlar, IMU, lazer) ile ROS 2 dünyası arasında köprü kuran mikrodenetleyici yazılımı ve onun ROS 2 tarafındaki arayüzü. Gimbal'ın **iç kontrol döngüsünü (inner loop)** gerçek zamanlı olarak yürütür.

---

## 1. Fonksiyonel Gereksinimler

*   **İç Kontrol Döngüsü:**
    *   `/gimbal/cmd_rate` topic'inden gelen hedef açısal hızı (`ω_cmd`) dinler.
    *   Yüksek frekansta (örn. 1 kHz) IMU (gyro) verisini okuyarak anlık hızı (`ω_meas`) ölçer.
    *   Hedef hız ile ölçülen hız arasındaki hatayı minimize etmek için bir **Rate PID kontrolcüsü** çalıştırır.
    *   PID çıktısını, motor sürücüler için PWM/akım komutlarına dönüştürür.
*   **Telemetri Yayını:**
    *   Periyodik olarak detaylı telemetri verisini (`açı`, `hız`, `limit durumu` vb.) `/gimbal/state` topic'inde yayınlar.
    *   IMU verilerini `/gimbal/imu` topic'inde yayınlar.
*   **TF Yayını:** Anlık gimbal açılarına göre dinamik `gimbal_link` -> `camera_optical_frame` transformunu `/tf` topic'inde yayınlar.
*   **Donanım Kontrolü:**
    *   `/laser/fire` servisi için sunucu (server) rolünü üstlenir ve lazeri tetikler.
    *   Fiziksel acil durum butonunu izler ve tetiklendiğinde `/op/emergency_stop` topic'ine yayın yapar.
*   **Başlangıç ve Güvenlik:**
    *   Sistem başlangıcında (power-up) IMU sensörü için ofset kalibrasyonu ve bir "homing" (başlangıç pozisyonuna dönme) işlemi yapar. Bu süreçte sistem `SAFE` modda kalmalıdır.
    *   Komut zaman aşımı (watchdog > 100ms), açı limitleri, anti-windup gibi düşük seviyeli güvenlik mekanizmalarını içerir.

> **Tasarım Notu:** Bu firmware, istenirse doğrudan açı komutu (`/gimbal/cmd`) alacak şekilde de programlanabilir. Bu durumda, kendi içinde "açı PI → hız PID" şeklinde bir kademeli kontrol yapısı çalıştırır. Varsayılan çalışma modu, ROS 2'den gelen hız komutlarını (`/gimbal/cmd_rate`) takip etmektir.


---

## 2. İletişim Arayüzü

### 2.1. Node I/O

| Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- |
| `/gimbal/state`,<br>`/gimbal/imu`,<br>`/op/emergency_stop`,<br>`/tf` | `/gimbal/cmd_rate`,<br>`/laser/armed` | `/laser/fire`,<br>`/laser/set_armed` | – |

### 2.2. Arayüz Detayları

```yaml
# Yayınlanan Topic'ler
/gimbal/state: { type: "hss_interfaces/msg/GimbalState", qos: "Best Effort, Lifespan=150ms" }
/gimbal/imu: { type: "sensor_msgs/msg/Imu", qos: "Best Effort, Lifespan=150ms" }
/op/emergency_stop: { type: "std_msgs/msg/Bool", qos: "Reliable, TransientLocal" }
/tf: { type: "tf2_msgs/msg/TFMessage" }

# Abone Olunan Topic'ler
/gimbal/cmd_rate: { type: "hss_interfaces/msg/GimbalRateCmd" }
/laser/armed: { type: "std_msgs/msg/Bool" }
```