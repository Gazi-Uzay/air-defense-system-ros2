# 🚀 HSS (Hava Savunma Sistemi)

Bu workspace, **HSS (Hava Savunma Sistemi)** projesinin ROS 2 tabanlı
yazılımlarını içermektedir.\
Sistem, bir gimbal üzerindeki kamera aracılığıyla hedef tespiti, takibi
ve angajman görevlerini otonom şekilde yerine getirmek üzere
tasarlanmıştır.

------------------------------------------------------------------------

## ⚙️ Sistem Gereksinimleri

  Bileşen               Gereksinim
  --------------------- ------------------------------------
  **İşletim Sistemi**   Ubuntu 22.04 LTS
  **ROS 2 Sürümü**      Humble Hawksbill
  **Python**            3.10 ve üzeri
  **PlatformIO**        Firmware derlemesi için gereklidir

### Gerekli Araçların Kurulumu

Aşağıdaki komutlar, ROS 2 workspace yönetimi, bağımlılık çözümü ve
firmware derlemesi için gerekli araçları yükler:

``` bash
sudo apt update
sudo apt install python3-vcstool python3-colcon-common-extensions -y

pip install -U platformio
```

------------------------------------------------------------------------

## 🧩 Kurulum Adımları

### 1️⃣ Workspace'i Klonlayın

Proje iki farklı şekilde kurulabilir:

#### 🔹 Henüz bir workspace'iniz yoksa

Yeni bir ROS 2 workspace oluşturmak için:

``` bash
git clone https://github.com/Gazi-Uzay/air-defense-system-ros2.git
cd air-defense-system-ros2
```

Ardından `.repos` dosyasında tanımlı tüm alt repoları indirin:

``` bash
vcs import src < hss.repos
```

> Bu komut, `src/` klasörü altına `hss_bringup`, `hss_firmware`,
> `hss_vision` gibi tüm bağımsız paket repolarını otomatik olarak
> klonlar.

------------------------------------------------------------------------

#### 🔹 Zaten bir workspace'iniz varsa (örneğin `~/Desktop/hss_ws`)

Mevcut workspace'inize HSS projesini doğrudan entegre etmek için:

``` bash
cd ~/Desktop/hss_ws
git clone https://github.com/Gazi-Uzay/air-defense-system-ros2.git .
```

> ⚠️ Komutun sonundaki `.` (nokta) çok önemlidir.\
> Tüm dosyalar (`src/`, `hss.repos`, `README.md`, `requirements.txt`,
> `docs/` vb.)\
> doğrudan mevcut workspace'inizin kök dizinine indirilir.\
> Böylece `air-defense-system-ros2/` adlı ekstra bir alt klasör oluşmaz.

Ardından alt repoları indirmek için:

``` bash
vcs import src < hss.repos
```

------------------------------------------------------------------------

### 2️⃣ ROS Bağımlılıklarını Kurun

``` bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

------------------------------------------------------------------------

### 3️⃣ Python Kütüphanelerini Kurun

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

### 4️⃣ Workspace'i Derleyin

``` bash
colcon build --symlink-install
```

Derleme tamamlandıktan sonra her terminalde ortam değişkenlerini
yükleyin:

``` bash
source install/setup.bash
```

> Kalıcı hâle getirmek isterseniz:
>
> ``` bash
> echo "source ~/Desktop/hss_ws/install/setup.bash" >> ~/.bashrc
> ```

------------------------------------------------------------------------

## 🚀 Sistemi Çalıştırma

Sistemi başlatmak için:

``` bash
ros2 launch hss_bringup hss_system.launch.py
```

> Bu launch dosyası; gimbal kontrolü, görüntü işleme, operasyon
> yöneticisi ve kullanıcı arayüzü (GUI) dahil olmak üzere tüm
> bileşenleri otomatik olarak başlatır.

------------------------------------------------------------------------

## 📖 Operasyonel Durumlar (`OpState.detail`)

Sistemin kullanıcı arayüzünde gösterilecek detaylı durum bilgileri, `/op/state` topic'indeki `OpState.msg` mesajının `detail` alanıyla iletilir. Bu, `operation_manager` ve `UI`'ın aynı dili konuşmasını sağlar. Aşağıda, ana modlar için tipik `detail` metinleri listelenmiştir:

| Ana Mod (`mode_text`) | Örnek `detail` Metinleri | Açıklama |
| :--- | :--- | :--- |
| `SAFE` | `"Sistem hazır"`, `"Kalibrasyon bekleniyor"` | Sistemin bekleme veya başlangıç durumları. |
| `MANUAL_TRACK` | `"Operatör kontrolünde"` | Kullanıcının fare ile gimbal'ı yönlendirdiği durum. |
| `AUTO_TRACK` | `"Hedef aranıyor"`, `"Hedef merkezleniyor"`, `"Hedef kilitli"` | Otonom takip modunun alt adımları. |
| `AUTO_KILL` | `"Düşman aranıyor"`, `"Kilitlenme: 1.2sn"`, `"HEDEF KİLİTLENDİ"` | Otonom angajman modunun alt adımları. |
| `EMERGENCY` | `"Acil durum aktif"`, `"Komut zaman aşımı"` | Acil durumun sebebini belirten metinler. |

> **Not:** Bu liste genişletilebilir. UI, bu metinleri doğrudan ekranda göstermeye hazır olmalıdır.

---

## 📖 Proje Dokümantasyonu

Projenin mimarisi, gereksinimleri ve bileşenlerinin detayları `docs/` klasörü altında yapılandırılmıştır.

### 🏛️ Mimari ve Tasarım (`docs/architecture/`)

Bu klasör, projenin üst seviye tasarım kararlarını ve genel yapısını içerir.

-   **📄 Ürün Gereksinimleri Dokümanı (PRD):** Projenin amacını, kapsamını ve genel fonksiyonel gereksinimlerini tanımlar.
-   **📡 İletişim Mimarisi:** Tüm ROS 2 topic, service ve mesaj tanımlarını içeren merkezi iletişim kontratı.
-   **🌳 Proje Ağacı:** Sistemi oluşturan tüm düğümlerin (node) ve paketlerin sorumluluklarını bir bakışta özetler.

### 📦 Düğüm (Node) Detayları (`docs/nodes/`)

Her bir ROS 2 düğümünün detaylı teknik dokümanı bu klasörde bulunur. Her dosya, düğümün görevlerini, iletişim arayüzünü (I/O) ve parametrelerini açıklar.

-   **📸 `camera_driver`:** Kamera donanımından görüntü ve bilgi yayınlar.
-   **👁️ `vision_processor_node`:** Görüntüleri işleyerek hedefleri tespit eder.
-   **🧠 `operation_manager_node`:** Sistemin merkezi karar alma ve mod yönetimi birimidir.
-   **🔄 `gimbal_controller_node`:** Dış kontrol döngüsünü çalıştırarak gimbal için hız komutları üretir.
-   **🤖 `micro_ros_agent`:** Donanım ile ROS 2 arasında köprü kuran iç kontrol döngüsüdür.
-   **🖥️ `ground_station_gateway`:** Operatör arayüzü (GUI) ile ROS 2 ağı arasındaki bağlantıyı sağlar.

------------------------------------------------------------------------

## 🧠 Notlar

-   `src/` klasörü Git tarafından izlenmez (`.gitignore` ile
    dışlanmıştır).\
    Yeni bir ortam kurarken alt repoları indirmek için aşağıdaki komutu
    kullanın:

    ``` bash
    vcs import src < hss.repos
    ```

-   Alt repolarda güncelleme yayınlandıysa, son sürüme çekmek için:

    ``` bash
    vcs pull src
    ```