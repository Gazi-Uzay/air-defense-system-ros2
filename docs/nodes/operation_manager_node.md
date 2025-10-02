# 🧠 `operation_manager_node`

**Rol:** Sistemin merkezi karar alma ve mantık birimi. Farklı sensör verilerini ve kullanıcı komutlarını birleştirerek sistemin genel çalışma modunu yönetir ve diğer düğümlere komutlar gönderir.

---

## 1. Fonksiyonel Gereksinimler

*   **Mod Yönetimi:** `SAFE`, `MANUAL_TRACK`, `AUTO_TRACK`, `AUTO_KILL`, `QR_ENGAGE` ve `EMERGENCY` operasyonel modlarını desteklemelidir.
*   **Durum Yayını:** Mevcut mod ve alt durum bilgisini (`detail`) `/op/state` topic'i üzerinden yayınlamalıdır.
*   **Mod Değişikliği:** `/op/set_mode` servisi aracılığıyla gelen mod değiştirme taleplerini yönetmelidir.
*   **Otonom Takip (`AUTO_TRACK`):** `/vision/targets` verisini kullanarak kilitlenen hedefi merkezde tutacak şekilde `/gimbal/cmd` komutları üretmelidir.
*   **Manuel Takip (`MANUAL_TRACK`):** `/ui/mouse_target` verisini kullanarak hedefi merkezde tutacak şekilde `/gimbal/cmd` komutları üretmelidir.
*   **Otonom Angajman (`AUTO_KILL`):** 
    *   Düşman hedefi merkezde belirli bir süre (`lock_on_duration_s` parametresi) stabil tuttuğunda "kilitlendi" kabul etmelidir.
    *   Kilitlenme sağlandığında `/laser/fire` servisi aracılığıyla ateşleme komutunu tetiklemelidir.
*   **Güvenlik ve Arming:**
    *   Lazerin ateşlenmesini kontrol eden bir "arming" mekanizmasını yönetmelidir.
    *   Arming durumu `/laser/armed` topic'i ile bildirilmeli ve `/laser/set_armed` servisi ile donanıma iletilmelidir.
    *   Arming durumu yalnızca `SAFE` modda etkinleştirilebilir ve `EMERGENCY` moduna geçildiğinde otomatik olarak devre dışı bırakılmalıdır.
    *   **Tasarım Notu:** Bu arming mekanizması, test edilebilirliği artırmak için `ARMED -> READY_TO_FIRE -> FIRED -> SAFE` gibi adımları içeren bir durum makinesi olarak tasarlanabilir.
*   **Acil Durum (E-Stop):**
    *   `/op/emergency_stop` mesajı aldığında `EMERGENCY` moduna geçmelidir.
    *   `/op/clear_emergency` servisi ile acil durumdan çıkış taleplerini yönetmelidir.
*   **Ateşleme Yetkisi:** UI'dan gelen `/op/request_fire` talebini almalı, gerekli güvenlik (mod, arming durumu vb.) kontrollerini yaptıktan sonra `/laser/fire` servisini kendisi çağırmalıdır.
*   **Sistem Sağlığı:** `/gimbal/state` ve `/gimbal/imu` telemetrisini dinleyerek genel sistem sağlığını izlemelidir.

---

## 2. İletişim Arayüzü

### 2.1. Node I/O

| Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- |
| `/gimbal/cmd`,<br>`/op/state`,<br>`/laser/armed` | `/vision/targets`,<br>`/ui/mouse_target`,<br>`/gimbal/state`,<br>`/gimbal/imu`,<br>`/op/emergency_stop` | `/op/set_mode`,<br>`/op/clear_emergency`,<br>`/op/request_fire` | `/laser/fire`,<br>`/laser/set_armed` |

### 2.2. Arayüz Detayları

```yaml
# Yayınlanan Topic'ler
/gimbal/cmd: { type: "hss_interfaces/msg/GimbalCommand", qos: "Reliable" }
/op/state: { type: "hss_interfaces/msg/OpState", qos: "Reliable, TransientLocal" }
/laser/armed: { type: "std_msgs/msg/Bool", qos: "Reliable, TransientLocal" }

# Abone Olunan Topic'ler
/vision/targets: { type: "hss_interfaces/msg/TargetArray" }
/ui/mouse_target: { type: "hss_interfaces/msg/UiMouseTarget" }
/gimbal/state: { type: "hss_interfaces/msg/GimbalState" }
/gimbal/imu: { type: "sensor_msgs/msg/Imu" }
/op/emergency_stop: { type: "std_msgs/msg/Bool" }

# Sunulan Servisler
/op/set_mode: { type: "hss_interfaces/srv/SetMode" }
/op/clear_emergency: { type: "std_srvs/srv/Trigger" }
/op/request_fire: { type: "std_srvs/srv/Trigger" }

# Kullanılan Servisler
/laser/fire: { type: "hss_interfaces/srv/FireCommand" }
/laser/set_armed: { type: "std_srvs/srv/SetBool" }
```

---

## 3. Parametreler

*   `lock_on_duration_s`: `AUTO_KILL` modunda, bir hedefin kilitli kabul edilmesi için merkezde stabil kalması gereken süre (saniye).
```