# HSS ROS 2 İletişim Mimarisi (Sürüm 2.1)

Bu doküman, **HSS Product Requirements Document (PRD)** temel alınarak güncellenmiştir. Projedeki tüm ROS 2 düğümlerini, kullandıkları **topic** ve **service** arayüzlerini ve önerilen detaylı **mesaj yapıları**nı içerir.

> Not: Bu mimari, PRD'de belirtilen tüm fonksiyonel gereksinimleri karşılayacak şekilde tasarlanmıştır.
> Her bir düğümün rolü ve sorumlulukları hakkında daha fazla bilgi için **ProjectTree.md** ve **`../nodes/`** klasöründeki dokümanlara bakınız.

## 1. Mimari Genel Bakış (Node I/O)

| Node | Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- | :--- |
| `camera_driver` | `/camera/image_raw` *(sensor_msgs/Image)*,<br>`/camera/camera_info` *(sensor_msgs/CameraInfo)* | – | – | – |
| `robot_state_publisher` | `/tf_static` *(tf2_msgs/TFMessage)* | – | – | – |
| `vision_processor_node` | `/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/vision/image_processed` *(sensor_msgs/Image)* | `/camera/image_raw` *(sensor_msgs/Image)*,<br>`/camera/camera_info` *(sensor_msgs/CameraInfo)* | – | – |
| `operation_manager_node` | `/gimbal/cmd` *(hss_interfaces/GimbalCommand)*,<br>`/op/state` *(hss_interfaces/OpState)*,<br>`/laser/armed` *(std_msgs/Bool)* | `/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/ui/mouse_target` *(hss_interfaces/UiMouseTarget)*,<br>`/gimbal/state` *(hss_interfaces/GimbalState)*,<br>`/gimbal/imu` *(sensor_msgs/Imu)*,<br>`/op/emergency_stop` *(std_msgs/Bool)* | `/op/set_mode`,<br>`/op/clear_emergency`,<br>`/op/request_fire` | `/laser/fire`,<br>`/laser/set_armed` |
| `gimbal_controller_node` | `/gimbal/cmd_rate` *(hss_interfaces/GimbalRateCmd)* | `/gimbal/cmd` *(hss_interfaces/GimbalCommand)*,<br>`/camera/camera_info` *(sensor_msgs/CameraInfo)*,<br>`/ui/mouse_target` *(hss_interfaces/UiMouseTarget)*,<br>`/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/gimbal/state` *(hss_interfaces/GimbalState)*,<br>`/gimbal/imu` *(sensor_msgs/Imu)* | – | – |
| `micro_ros_agent` | `/gimbal/state` *(hss_interfaces/GimbalState)*,<br>`/gimbal/imu` *(sensor_msgs/Imu)*,<br>`/op/emergency_stop` *(std_msgs/Bool)*,<br>`/tf` | `/gimbal/cmd_rate` *(hss_interfaces/GimbalRateCmd)*,<br>`/laser/armed` *(std_msgs/Bool)* | `/laser/fire`,<br>`/laser/set_armed` | – |
| `ground_station_gateway` | `/ui/mouse_target` *(hss_interfaces/UiMouseTarget)*,<br>`/op/emergency_stop` *(std_msgs/Bool)*,<br>`/ui/video_source_select` *(std_msgs/String)* | `/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/gimbal/state` *(hss_interfaces/GimbalState)*,<br>`/gimbal/imu` *(sensor_msgs/Imu)*,<br>`/op/state` *(hss_interfaces/OpState)*,<br>`/vision/image_processed` *(sensor_msgs/Image)*,<br>`/camera/image_raw` *(sensor_msgs/Image)*,<br>`/laser/armed` *(std_msgs/Bool)*<br>*(Not: UI, "raw" ve "processed" video akışları arasında geçiş yapabilmelidir.)* | – | `/op/set_mode`,<br>`/op/clear_emergency`,<br>`/op/request_fire` |

---

## 2. Arayüz Kontratı (YAML Formatında)

Sistemin tüm topic ve service arayüzleri, merkezi bir YAML tanımı olarak aşağıda verilmiştir. Bu, hem dokümantasyonun güncel tutulmasını kolaylaştırır hem de gelecekteki kod üretim (code-generation) araçları için bir temel oluşturur.

```yaml
# HSS Interface Contract v2.1
topics:
  /camera/image_raw:
    type: "sensor_msgs/msg/Image"
    qos: "Best Effort, Lifespan=100ms"
  /camera/camera_info:
    type: "sensor_msgs/msg/CameraInfo"
    qos: "Reliable, TransientLocal"
  /vision/image_processed:
    type: "sensor_msgs/msg/Image"
    qos: "Best Effort, Lifespan=150ms"
  /vision/targets:
    type: "hss_interfaces/msg/TargetArray"
    qos: "Reliable"
  /ui/mouse_target:
    type: "hss_interfaces/msg/UiMouseTarget"
    qos: "Reliable"
  /ui/video_source_select:
    type: "std_msgs/msg/String"  # "raw" | "processed"
    qos: "Reliable"
  /gimbal/cmd:
    type: "hss_interfaces/msg/GimbalCommand"
    qos: "Reliable"

  /gimbal/cmd_rate:
    type: "hss_interfaces/msg/GimbalRateCmd"
    qos: "Reliable"
  /gimbal/state:
    type: "hss_interfaces/msg/GimbalState"
    qos: "Best Effort, Lifespan=150ms"

  # (Opsiyonel) Düşük seviye telemetri
  /gimbal/motor_feedback:
    type: "hss_interfaces/msg/GimbalMotorFeedback"
    qos: "Best Effort, Lifespan=150ms"
  /gimbal/status:
    type: "hss_interfaces/msg/GimbalStatus"
    qos: "Reliable, TransientLocal"
  /gimbal/imu:
    type: "sensor_msgs/msg/Imu"
    qos: "Best Effort, Lifespan=150ms"

  # (Opsiyonel) PID ayarı için iç durum verileri (hata, P, I, D, çıkış)
  /gimbal/debug:
    type: "hss_interfaces/msg/GimbalDebug"
    qos: "Best Effort"
    
  /op/state:
    type: "hss_interfaces/msg/OpState"
    qos: "Reliable, TransientLocal"
  /op/emergency_stop:
    type: "std_msgs/msg/Bool"
    qos: "Reliable, TransientLocal"
  /laser/armed:
    type: "std_msgs/msg/Bool"
    qos: "Reliable, TransientLocal"

services:
  /op/set_mode:
    type: "hss_interfaces/srv/SetMode"
  /laser/fire:
    type: "hss_interfaces/srv/FireCommand"
  /laser/set_armed:
    type: "std_srvs/srv/SetBool"
    note: "Tek otorite prensibi: Sadece operation_manager, arming durumuna karar verir ve bu servisi çağırır. MCU yalnızca komutu uygular."
  /op/clear_emergency:
    type: "std_srvs/srv/Trigger"
    note: "Sadece operation_manager tarafından sunulur. E-Stop durumunu sıfırlar."
  /op/request_fire:
    type: "std_srvs/srv/Trigger"
    note: "UI isteği OM’e gelir; OM policy/arming kontrolünden sonra /laser/fire’ı kendisi çağırır."
```

---

## 3. TF2 (Transform) Ağacı

Sistemdeki farklı bileşenlerin pozisyon ve oryantasyonlarını ilişkilendirmek için standart bir TF2 ağacı kullanılır.

-   `map` -> `base_link` (Araç gövdesi, opsiyonel, SLAM/GPS ile sağlanır)
-   `base_link` -> `gimbal_link` (Gimbal'ın dönen tabanı)
-   `gimbal_link` -> `camera_optical_frame` (Kameranın optik merkezi)

Bu dönüşümler, `micro_ros_agent` (gimbal açılarına göre) ve `robot_state_publisher` (statik URDF'den) tarafından `/tf` ve `/tf_static` topic'leri üzerinden yayınlanır.

---

## 4. `hss_interfaces` Paket Taslağı

```
hss_interfaces/
├─ CMakeLists.txt
├─ package.xml
├─ msg/
│  ├─ Target.msg
│  ├─ TargetArray.msg
│  ├─ UiMouseTarget.msg
│  ├─ GimbalRateCmd.msg
│  ├─ GimbalCommand.msg
│  ├─ GimbalMotorFeedback.msg
│  ├─ GimbalStatus.msg
│  ├─ GimbalState.msg
│  ├─ GimbalDebug.msg
│  └─ OpState.msg
└─ srv/
   ├─ SetMode.srv
   └─ FireCommand.srv
```

---

## 5. Mesaj ve Servis Tanımları

### `msg/Target.msg`
*Hedefin özelliklerini tanımlar.*
```
uint32 id            # Hedefin benzersiz kimliği (ör. her karede artan ID veya takip ID'si)
float32 u_norm       # Normalleştirilmiş yatay konum [0.0 - 1.0] (görüntü koordinatı)
float32 v_norm       # Normalleştirilmiş dikey konum [0.0 - 1.0] (görüntü koordinatı)
float32 confidence   # Tespit güven skoru [0.0 - 1.0]

float32 x_m          # Kamera koordinat sisteminde hedefin X konumu (metre)
float32 y_m          # Kamera koordinat sisteminde hedefin Y konumu (metre)
float32 z_m          # Kamera koordinat sisteminde hedefin Z konumu (metre)

float32 screen_u_norm # Hedefin ekrandaki yatay konumu (UI'da işaretleme için)
float32 screen_v_norm # Hedefin ekrandaki dikey konumu (UI'da işaretleme için)

string class_label   # Hedef sınıf etiketi (örn: "balloon", "qr_code")
string color_label   # Hedefin renk etiketi (örn: "red", "blue")
string qr_code_data  # Çözülmüş QR kod verisi (varsa, yoksa boş string "")
```

### `msg/TargetArray.msg`
*Anlık olarak tespit edilen tüm hedefleri içeren dizi.*
```
std_msgs/Header header      # Zaman damgası (stamp) ve referans çerçevesi (frame_id: genelde "camera_optical_frame")
hss_interfaces/Target[] targets   # Aynı karede tespit edilen tüm hedeflerin listesi
```

### `msg/UiMouseTarget.msg`
*UI üzerinden gönderilen fare komutları.*
```
std_msgs/Header header   # Zaman damgası ve referans çerçevesi (frame_id: genelde "ui_screen")

float32 u_norm           # Normalleştirilmiş yatay konum [0.0 - 1.0] (ekran koordinatı)
float32 v_norm           # Normalleştirilmiş dikey konum [0.0 - 1.0] (ekran koordinatı)
bool    is_drag          # True: sürükleme işlemi, False: tek tıklama
string  source           # Komutu gönderen kaynak (örn: "ground_station_ui")
```

### `msg/GimbalCommand.msg`
*Gimbal'a gönderilen yönlendirme komutu.*
```
std_msgs/Header header   # Zaman damgası ve referans çerçevesi (frame_id: REF_BODY için "base_link", REF_WORLD için "map")

uint8  mode              # Komut tipi: pozisyon veya hız modu
uint8  ref_frame         # Referans çerçevesi: gövde veya dünya

float32 pan_deg          # Pozisyon modu: hedef pan açısı (derece)
float32 tilt_deg         # Pozisyon modu: hedef tilt açısı (derece)
float32 pan_rate_dps     # Hız modu: hedef pan hızı (derece/saniye)
float32 tilt_rate_dps    # Hız modu: hedef tilt hızı (derece/saniye)

uint8  priority          # Komut önceliği (yüksek öncelik düşük önceliği override edebilir)
string requester         # Komutu talep eden düğümün adı (örn: "operation_manager")

# Mode sabitleri
uint8 MODE_POS=0         # Pozisyon kontrol modu
uint8 MODE_VEL=1         # Hız kontrol modu

# Referans çerçevesi sabitleri
uint8 REF_BODY=0         # Gövdeye göre (base_link)
uint8 REF_WORLD=1        # Dünya koordinat sistemine göre (map)
```

### `msg/GimbalMotorFeedback.msg`
*Gimbal motorlarının anlık pozisyonunu içerir.*
```
std_msgs/Header header   # stamp + frame_id (genelde "gimbal_link")

float32 pan_deg          # Anlık pan açısı (derece)
float32 tilt_deg         # Anlık tilt açısı (derece)

# (Opsiyonel) Hız geri bildirimi
# float32 pan_rate_dps   # Pan açısal hız (derece/s)
# float32 tilt_rate_dps  # Tilt açısal hız (derece/s)
```

### `msg/GimbalStatus.msg`
*Gimbal'ın genel sağlık ve kalibrasyon durumunu içerir.*
```
std_msgs/Header header   # stamp + frame_id

bool    is_calibrated    # Kalibrasyon tamam mı?
uint8   status           # Genel durum (aşağıdaki sabitlere bakınız)
string  status_text      # İnsan-okur açıklama (örn. "OK", "Limit hit", "Overcurrent")

# Durum sabitleri
uint8 STATUS_UNKNOWN=0
uint8 STATUS_OK=1
uint8 STATUS_CALIBRATING=2
uint8 STATUS_LIMIT=3
uint8 STATUS_ERROR=4
```

### `msg/OpState.msg`
*Operation Manager'ın mevcut çalışma durumu.*
```
std_msgs/Header header   # Zaman damgası (stamp) ve referans çerçevesi (frame_id: genelde "map")

uint8  mode              # Mevcut mod
string mode_text         # Modun açıklayıcı adı
string detail            # Alt durum / ek bilgi (örn: "Hedef aranıyor", "Kilitlenme sağlandı")

# PRD'ye göre mod sabitleri
uint8 MODE_SAFE=0
uint8 MODE_MANUAL_TRACK=1 
uint8 MODE_AUTO_TRACK=2 
uint8 MODE_AUTO_KILL=3
uint8 MODE_QR_ENGAGE=4
uint8 MODE_EMERGENCY=5
```
> **Not:** `detail` alanı, bir modun içindeki alt durumları (sub-states) belirtmek için kullanılır. Örneğin, `AUTO_KILL` modundayken `detail` alanı şu değerleri alabilir: `"Düşman aranıyor"`, `"Hedef merkezleniyor"`, `"Kilitlenme sağlanıyor: 1.2sn"`, `"HEDEF KİLİTLENDİ - ATEŞ"`. Bu, kullanıcı arayüzüne zengin durum bilgisi sağlar.

### `srv/SetMode.srv`
*Operation Manager'ın modunu değiştirmek için kullanılır.*
```
uint8  mode        # Yeni mod (OpState.msg içindeki sabitlere uygun olmalı)
string reason      # Mod değişikliği gerekçesi (örn: "UI'dan kullanıcı talebi", "failsafe tetiklendi")
---
bool   accepted    # Mod değişikliği kabul edildi mi?
string message     # Ek bilgi veya hata mesajı (örn: "Geçersiz mod", "Mod başarıyla ayarlandı")
```

### `srv/FireCommand.srv`
*Lazer ateşleme komutunu tetikler.*
```
uint32 duration_ms     # Ateşleme süresi (milisaniye)
uint8  power_percent   # Güç seviyesi [%0 - %100]
string safety_token    # Emniyet için gerekli özel anahtar/jeton (örn: UI onayı)
---
bool   accepted        # Komut kabul edildi mi?
string message         # Ek bilgi veya hata mesajı (örn: "Emniyet kilidi açık", "Ateşleme tamamlandı")
```

---

## 5. QoS Önerileri (Tazelik Öncelikli)

| Topic | Reliability | History/Depth | Durability | Ek QoS (öneri) | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/camera/image_raw` | Best Effort | KeepLast/5 | Volatile | lifespan≈100ms | Yüksek bant; eski frame’ler değersiz |
| `/vision/image_processed` | Best Effort | KeepLast/5 | Volatile | lifespan≈150ms | GUI canlılığı; gecikmeli kareleri at |
| `/vision/targets` | Reliable | KeepLast/10 | Volatile | deadline≈50ms *(ops.)* | Hedef listesi kritik |
| `/ui/mouse_target` | Reliable | KeepLast/5 | Volatile | deadline≈100ms *(ops.)* | Operatör girdisi kaybolmasın |
| `/gimbal/cmd` | Reliable | KeepLast/10 | Volatile | deadline≈30ms *(ops.)* | Komut hattı güvenilir olmalı |
| `/gimbal/cmd_rate` | Reliable | KeepLast/10 | Volatile | deadline≈20ms *(ops.)* | Donanım arayüz komutları. İdeal hedef 20ms, watchdog sınırı 100ms. |
| `/gimbal/state` | Best Effort | KeepLast/10 | Volatile | lifespan≈150ms | En güncel durum kıymetli, eskileri at. |
| `/gimbal/imu` | Best Effort | KeepLast/50 | Volatile | lifespan≈150ms | Çok yüksek frekans; güncel veri önemli |
| `/op/state` | Reliable | KeepLast/10 | TransientLocal | — | UI geç katılımda son durumu görsün |
| `/op/emergency_stop` | Reliable | KeepLast/1 | TransientLocal | — | “Latched” benzeri davranış şart |
