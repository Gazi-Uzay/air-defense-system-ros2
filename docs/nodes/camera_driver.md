# 📸 `camera_driver`

**Rol:** Fiziksel kamera donanımından ham görüntü ve bilgi verilerini alıp ROS 2 ağına yayınlayan sürücü düğümü.

---

## 1. Fonksiyonel Gereksinimler

*   Sistem, birincil kameradan ham görüntü verisini `/camera/image_raw` topic'i üzerinden sürekli olarak yayınlamalıdır.
*   Kamera sürücüsü, aynı zamanda kameranın içsel parametrelerini (kalibrasyon matrisi, distorsiyon katsayıları) içeren `/camera/camera_info` topic'ini `sensor_msgs/CameraInfo` formatında yayınlamalıdır.

---

## 2. İletişim Arayüzü

### 2.1. Node I/O

| Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- |
| `/camera/image_raw` *(sensor_msgs/Image)*,<br>`/camera/camera_info` *(sensor_msgs/CameraInfo)* | – | – | – |

### 2.2. Topic Detayları

```yaml
/camera/image_raw:
  type: "sensor_msgs/msg/Image"
  qos: "Best Effort, Lifespan=100ms"

/camera/camera_info:
  type: "sensor_msgs/msg/CameraInfo"
  qos: "Reliable, TransientLocal"
```