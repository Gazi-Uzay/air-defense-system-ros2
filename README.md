# 🚀 HSS (Hava Savunma Sistemi)

Bu workspace, **HSS (Hava Savunma Sistemi)** projesinin ROS 2
tabanlı yazılımlarını içermektedir.\
Sistem, bir gimbal üzerindeki kamera aracılığıyla hedef tespiti, takibi
ve angajman görevlerini otonom şekilde yerine getirmek üzere
tasarlanmıştır.

------------------------------------------------------------------------

## ⚙️ Sistem Gereksinimleri

  Bileşen               Gereksinim
  --------------------- ------------------------------------
  **İşletim Sistemi**   Ubuntu 22.04 LTS
  **ROS 2 Sürümü**      Humble Hawksbill
  **Python**            3.10+
  **PlatformIO**        Firmware derlemesi için gereklidir

### Gerekli Araçların Kurulumu

Aşağıdaki komutlar ROS 2 workspace yönetimi, bağımlılık çözümü ve
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

Bu yöntem, `src/`, `hss.repos`, `README.md`, `requirements.txt`,
`LICENSE` ve `docs/` klasörlerini içeren tam bir **workspace**
oluşturur.

------------------------------------------------------------------------

#### 🔹 Zaten bir workspace'iniz varsa (örneğin `~/Desktop/hss_ws`):

Mevcut workspace'inize HSS projesini doğrudan entegre etmek için:

``` bash
cd ~/Desktop/hss_ws
git clone https://github.com/Gazi-Uzay/air-defense-system-ros2.git .
```

> Bu komutun sonundaki `.` (nokta) çok önemlidir.\
> Tüm dosyalar (`src/`, `hss.repos`, `README.md`, `requirements.txt`,
> `docs/` vb.)\
> doğrudan mevcut workspace'inizin köküne indirilir.\
> Böylece `air-defense-system-ros2/` gibi ekstra bir alt klasör
> oluşturulmaz.

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

> Kalıcı yapmak isterseniz:
>
> ``` bash
> echo "source ~/Desktop/hss_ws/install/setup.bash" >> ~/.bashrc
> ```

------------------------------------------------------------------------

## 🚀 Çalıştırma

Sistemi başlatmak için:

``` bash
ros2 launch hss_bringup hss_system.launch.py
```

> Bu launch dosyası, gimbal kontrolü, görüntü işleme, operasyon
> yöneticisi ve GUI dahil olmak üzere tüm bileşenleri çalıştırır.

------------------------------------------------------------------------

## 📚 Dokümantasyon

Proje ile ilgili detaylı teknik belgeler ve diyagramlara `docs/`
klasöründen ulaşabilirsiniz.\
Her alt paketin kendi deposunda da `README.md` ve `docs/` klasörleri
bulunmaktadır.

------------------------------------------------------------------------

## 🧠 Notlar

-   `src/` klasörü Git tarafından izlenmez (`.gitignore` ile
    dışlanmıştır).\
    Her geliştirici `vcs import` komutu ile kendi ortamını
    oluşturmalıdır.\

-   Alt repoları güncellemek için:

    ``` bash
    vcs pull src
    ```