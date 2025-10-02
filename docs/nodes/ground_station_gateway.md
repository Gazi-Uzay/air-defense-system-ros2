# 🖥️ `ground_station_gateway`

**Rol:** Operatör için birincil kontrol ve izleme arayüzünü sağlayan düğüm. Genellikle bir GUI (Grafiksel Kullanıcı Arayüzü) ile entegre çalışır ve ROS 2 ağı ile kullanıcı etkileşimleri arasında köprü kurar.

---

## 1. Fonksiyonel Gereksinimler

*   **Video Gösterimi:** Ham (`/camera/image_raw`) ve işlenmiş (`/vision/image_processed`) video akışlarını gösterebilmeli ve `/ui/video_source_select` topic'i ile aralarında geçiş yapabilmelidir.
*   **Telemetri Gösterimi:** `/vision/targets`, `/gimbal/state`, `/op/state`, `/gimbal/imu` gibi tüm önemli telemetri verilerini anlık olarak göstermelidir.
*   **Manuel Kontrol:** Video akışı üzerinde fare ile hedef belirlemeye olanak tanımalı ve bu komutları `/ui/mouse_target` topic'inde yayınlamalıdır.
*   **Mod Kontrolü:** Arayüzdeki butonlar aracılığıyla `/op/set_mode` servisini çağırarak sistemin operasyonel modunu değiştirmelidir.
*   **Ateşleme Talebi:** "ATEŞ ET" butonuna basıldığında, doğrudan donanıma değil, `operation_manager`'a `/op/request_fire` servisi ile ateşleme talebi göndermelidir.
*   **Acil Durum:**
    *   Arayüzdeki bir acil durum butonu ile `/op/emergency_stop` topic'ine yayın yapabilmelidir.
    *   `EMERGENCY` durumundan çıkmak için `/op/clear_emergency` servisini çağıran bir "Reset" butonu sunmalıdır.
*   **Geri Bildirim:** `/op/state` ve `/laser/armed` gibi durum topic'lerini dinleyerek operatöre anlık ve anlaşılır (renk kodlu, vurgulu vb.) geri bildirim sağlamalıdır.

---

## 2. İletişim Arayüzü

### 2.1. Node I/O

| Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- |
| `/ui/mouse_target`,<br>`/op/emergency_stop`,<br>`/ui/video_source_select` | `/vision/targets`,<br>`/gimbal/state`,<br>`/gimbal/imu`,<br>`/op/state`,<br>`/vision/image_processed`,<br>`/camera/image_raw`,<br>`/laser/armed` | – | `/op/set_mode`,<br>`/op/clear_emergency`,<br>`/op/request_fire` |

### 2.2. Arayüz Detayları

```yaml
# Yayınlanan Topic'ler
/ui/mouse_target: { type: "hss_interfaces/msg/UiMouseTarget", qos: "Reliable" }
/op/emergency_stop: { type: "std_msgs/msg/Bool", qos: "Reliable, TransientLocal" }
/ui/video_source_select: { type: "std_msgs/msg/String", qos: "Reliable" }

# Kullanılan Servisler
/op/set_mode: { type: "hss_interfaces/srv/SetMode" }
/op/clear_emergency: { type: "std_srvs/srv/Trigger" }
/op/request_fire: { type: "std_srvs/srv/Trigger" }
```