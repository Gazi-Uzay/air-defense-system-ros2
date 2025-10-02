# 👁️ `vision_processor_node`

**Rol:** Ham kamera görüntüsünü işleyerek hedef tespiti yapan ve sonuçları ROS 2 ağına yayınlayan düğüm.

---

## 1. Fonksiyonel Gereksinimler

*   Görüntüleri işlemek için `/camera/image_raw` ve `/camera/camera_info` topic'lerine abone olmalıdır.
*   İşleme sonucunda tespit edilen hedeflerin bilgilerini (`id`, 3D pozisyon, güven skoru, renk, QR kod verisi) `/vision/targets` topic'inde `hss_interfaces/TargetArray` formatında yayınlamalıdır.
*   Hata ayıklama ve görsel doğrulama için, hedeflerin üzerine çizildiği işlenmiş görüntü `/vision/image_processed` topic'inde yayınlanmalıdır.

---

## 2. İletişim Arayüzü

### 2.1. Node I/O

| Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- |
| `/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/vision/image_processed` *(sensor_msgs/Image)* | `/camera/image_raw` *(sensor_msgs/Image)*,<br>`/camera/camera_info` *(sensor_msgs/CameraInfo)* | – | – |

### 2.2. Topic Detayları

```yaml
# Yayınlanan Topic'ler
/vision/image_processed:
  type: "sensor_msgs/msg/Image"
  qos: "Best Effort, Lifespan=150ms"
/vision/targets:
  type: "hss_interfaces/msg/TargetArray"
  qos: "Reliable"

# Abone Olunan Topic'ler
/camera/image_raw:
  type: "sensor_msgs/msg/Image"
/camera/camera_info:
  type: "sensor_msgs/msg/CameraInfo"
```