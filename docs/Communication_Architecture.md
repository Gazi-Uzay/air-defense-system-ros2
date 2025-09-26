# HSS ROS 2 İletişim Mimarisi (Sürüm 2.1)

Bu doküman, **HSS Product Requirements Document (PRD)** temel alınarak güncellenmiştir. Projedeki tüm ROS 2 düğümlerini, kullandıkları **topic** ve **service** arayüzlerini ve önerilen detaylı **mesaj yapıları**nı içerir.

> Not: Bu mimari, PRD'de belirtilen tüm fonksiyonel gereksinimleri karşılayacak şekilde tasarlanmıştır.

---

## 1. Mimari Genel Bakış (Node I/O)

| Node | Publishes | Subscribes | Service Servers | Service Clients |
| :--- | :--- | :--- | :--- | :--- |
| `camera_driver` | `/camera/image_raw` *(sensor_msgs/Image)* | – | – | – |
| `vision_processor_node` | `/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/vision/image_processed` *(sensor_msgs/Image)* | `/camera/image_raw` *(sensor_msgs/Image)* | – | – |
| `operation_manager_node` | `/gimbal/cmd` *(hss_interfaces/GimbalCommand)*,<br>`/op/state` *(hss_interfaces/OpState)* | `/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/ui/mouse_target` *(hss_interfaces/UiMouseTarget)*,<br>`/gimbal/motor_feedback` *(hss_interfaces/GimbalMotorFeedback)*,<br>`/gimbal/status` *(hss_interfaces/GimbalStatus)*,<br>`/gimbal/imu` *(sensor_msgs/Imu)*,<br>`/op/emergency_stop` *(std_msgs/Bool)* | `/op/set_mode` | `/laser/fire` |
| `gimbal_controller_node` | `/gimbal/firmware_cmd` *(hss_interfaces/GimbalCommand)* | `/gimbal/cmd` *(hss_interfaces/GimbalCommand)* | – | – |
| `micro_ros_agent` | `/gimbal/motor_feedback` *(hss_interfaces/GimbalMotorFeedback)*,<br>`/gimbal/status` *(hss_interfaces/GimbalStatus)*,<br>`/gimbal/imu` *(sensor_msgs/Imu)*,<br>`/op/emergency_stop` *(std_msgs/Bool)* | `/gimbal/firmware_cmd` *(hss_interfaces/GimbalCommand)* | `/laser/fire` | – |
| `ground_station_gateway` | `/ui/mouse_target` *(hss_interfaces/UiMouseTarget)*,<br>`/op/emergency_stop` *(std_msgs/Bool)* | `/vision/targets` *(hss_interfaces/TargetArray)*,<br>`/gimbal/motor_feedback` *(hss_interfaces/GimbalMotorFeedback)*,<br>`/gimbal/status` *(hss_interfaces/GimbalStatus)*,<br>`/gimbal/imu` *(sensor_msgs/Imu)*,<br>`/op/state` *(hss_interfaces/OpState)*,<br>`/vision/image_processed` *(sensor_msgs/Image)*,<br>`/camera/image_raw` *(sensor_msgs/Image)* | – | `/op/set_mode`,<br>`/laser/fire` |

---

## 2. Topic ve Service Türleri

### Topic Türleri
- `/camera/image_raw`: `sensor_msgs/msg/Image`
- `/vision/image_processed`: `sensor_msgs/msg/Image`
- `/vision/targets`: `hss_interfaces/msg/TargetArray`
- `/ui/mouse_target`: `hss_interfaces/msg/UiMouseTarget`
- `/gimbal/cmd`: `hss_interfaces/msg/GimbalCommand`
- `/gimbal/firmware_cmd`: `hss_interfaces/msg/GimbalCommand`
- `/gimbal/motor_feedback`: `hss_interfaces/msg/GimbalMotorFeedback`
- `/gimbal/status`: `hss_interfaces/msg/GimbalStatus`
- `/gimbal/imu`: `sensor_msgs/msg/Imu`
- `/op/state`: `hss_interfaces/msg/OpState`
- `/op/emergency_stop`: `std_msgs/msg/Bool`

### Service Türleri
- `/op/set_mode`: `hss_interfaces/srv/SetMode`
- `/laser/fire`: `hss_interfaces/srv/FireCommand`

---

## 3. `hss_interfaces` Paket Taslağı

```
hss_interfaces/
├─ CMakeLists.txt
├─ package.xml
├─ msg/
│  ├─ Target.msg
│  ├─ TargetArray.msg
│  ├─ UiMouseTarget.msg
│  ├─ GimbalCommand.msg
│  ├─ GimbalMotorFeedback.msg
│  ├─ GimbalStatus.msg
│  └─ OpState.msg
└─ srv/
   ├─ SetMode.srv
   └─ FireCommand.srv
```

---

## 4. Mesaj ve Servis Tanımları

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
uint8 MODE_AUTO_KILL_COLOR=3
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

| Topic | Reliability | History/Depth | Durability     | Ek QoS (öneri)                         | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/camera/image_raw`       | BestEffort | KeepLast/5   | Volatile        | lifespan≈200ms                        | Yüksek bant; eski frame’ler değersiz |
| `/vision/image_processed` | BestEffort | KeepLast/5   | Volatile        | lifespan≈300ms                        | GUI canlılığı; gecikmeli kareleri at |
| `/vision/targets`         | Reliable   | KeepLast/10  | Volatile        | deadline≈50ms *(ops.)*                | Hedef listesi kritik |
| `/ui/mouse_target`        | Reliable   | KeepLast/5   | Volatile        | deadline≈100ms *(ops.)*               | Operatör girdisi kaybolmasın |
| `/gimbal/cmd`             | Reliable   | KeepLast/10  | Volatile        | deadline≈30ms *(ops.)*                | Komut hattı güvenilir olmalı |
| `/gimbal/firmware_cmd`    | Reliable   | KeepLast/10  | Volatile        | deadline≈20ms *(ops.)*                | Donanım arayüz komutları |
| `/gimbal/motor_feedback`  | BestEffort | KeepLast/10 | Volatile    | lifespan≈150ms, deadline≈20ms *(ops.)* | En güncel pozisyon; eski veriyi at |
| `/gimbal/status`          | Reliable   | KeepLast/5   | TransientLocal* | —                                     | Sağlık durumu; geç aboneye faydalı |
| `/gimbal/imu`             | BestEffort | KeepLast/50 | Volatile   | lifespan≈150ms                        | Çok yüksek frekans; güncel veri önemli |
| `/op/state`               | Reliable   | KeepLast/10  | TransientLocal | —                                   | UI geç katılımda son durumu görsün |
| `/op/emergency_stop`      | Reliable   | KeepLast/1   | TransientLocal | —                                   | “Latched” benzeri davranış şart |
