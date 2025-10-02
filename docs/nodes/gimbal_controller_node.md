# 🔄 `gimbal_controller_node`

**Rol:** Sistemin **dış kontrol döngüsünü (outer loop)** çalıştırır. Yüksek seviyeli hedefleme verilerini (görüntü koordinatları, UI tıklamaları vb.) işleyerek, donanımın takip edeceği düşük seviyeli hedef açısal hız komutlarını üretir.

---

## 1. Fonksiyonel Gereksinimler

*   `/vision/targets` veya `/ui/mouse_target`'tan gelen görüntü tabanlı açısal hatayı (`u,v` koordinatları), `/camera/camera_info` verisini kullanarak gerçek açısal hataya (`e_yaw`, `e_pitch`) dönüştürür.
*   PI tabanlı bir kontrolcü ile bu açısal hatadan bir hedef açısal hız komutu (`ω_cmd`) üretir.
*   Üretilen hız komutunu `/gimbal/cmd_rate` topic'i üzerinden yayınlar.
*   Kontrol döngüsü için geri besleme olarak `/gimbal/state` (anlık açı/hız) ve `/gimbal/imu` (anlık açı/hız) topic'lerini dinler.
*   `SAFE` veya `EMERGENCY` modlarında hız komutlarını sıfırlayarak sistemi güvenli duruşa alır.

---

## 2. İletişim Arayüzü

### 2.1. Node I/O

| Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- |
| `/gimbal/cmd_rate` *(hss_interfaces/GimbalRateCmd)* | `/gimbal/cmd`,<br>`/camera/camera_info`,<br>`/ui/mouse_target`,<br>`/vision/targets`,<br>`/gimbal/state`,<br>`/gimbal/imu` | – | – |

### 2.2. Arayüz Detayları

```yaml
# Yayınlanan Topic'ler
/gimbal/cmd_rate:
  type: "hss_interfaces/msg/GimbalRateCmd"
  qos: "Reliable"
/gimbal/debug: # Opsiyonel
  type: "hss_interfaces/msg/GimbalDebug"
  qos: "Best Effort"

# Abone Olunan Topic'ler
/gimbal/cmd: { type: "hss_interfaces/msg/GimbalCommand" }
/camera/camera_info: { type: "sensor_msgs/CameraInfo" }
/ui/mouse_target: { type: "hss_interfaces/msg/UiMouseTarget" }
/vision/targets: { type: "hss_interfaces/msg/TargetArray" }
/gimbal/state: { type: "hss_interfaces/msg/GimbalState" }
/gimbal/imu: { type: "sensor_msgs/msg/Imu" }
```

---

## 3. Parametreler

*   `HFOV_deg`, `VFOV_deg`: Kameranın görüş açıları.
*   `Kp_ang`, `Ki_ang`: Dış açı döngüsü için PI katsayıları.
*   `deadband_deg`: Kontrolcünün tepki vermeyeceği minimum hata eşiği.
*   `rate_limit_dps`: Maksimum hedef açısal hız.
*   `jerk_limit_dps2`: Maksimum açısal ivmelenme (yumuşak hareket için).
*   `control_loop_frequency_hz`: Kontrol döngüsünün çalışma frekansı (örn: 50 Hz).