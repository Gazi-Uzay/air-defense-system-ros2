# HSS Projesi

Bu workspace, HSS (Hedefleme ve Savunma Sistemi) projesinin ROS2 tabanlı yazılımlarını içermektedir. Sistem, bir gimbal üzerindeki kamera aracılığıyla hedef tespiti, takibi ve yönetimi görevlerini yerine getirmek üzere tasarlanmıştır.

## Workspace Yapısı

Proje, aşağıdaki ROS2 paketlerinden oluşmaktadır:

- `hss_bringup`: Sistemin tüm node'larını başlatan ana launch dosyalarını içerir.
- `hss_firmware`: Gimbal ve sensörleri kontrol eden mikrodenetleyici (muhtemelen bir ESP32 veya benzeri) için PlatformIO tabanlı firmware kodunu barındırır.
- `hss_gimbal_control`: ROS2 üzerinden gelen komutlarla gimbal'ı kontrol eden Python node'unu içerir.
- `hss_gui`: Operatörün sistemi izlemesi ve komut göndermesi için PyQt veya benzeri bir kütüphane ile geliştirilmiş arayüz node'unu içerir.
- `hss_interfaces`: Projeye özgü custom ROS2 mesaj (`.msg`) ve servis (`.srv`) tanımlamalarını barındırır.
- `hss_op_manager`: Sistemin genel operasyon mantığını (örneğin, mod değiştirme, hedef atama) yöneten state machine veya mantık node'unu içerir.
- `hss_vision`: Kamera görüntüsünü işleyerek hedef tespiti ve takibi yapan bilgisayarlı görü node'unu içerir.

## Sistem Gereksinimleri ve Kurulum

Bu bölüm, projenin başarılı bir şekilde kurulması ve çalıştırılması için gereken adımları ve bağımlılıkları detaylandırmaktadır.

### Ön Gereksinimler

- **İşletim Sistemi:** Ubuntu 22.04 LTS
- **ROS 2 Sürümü:** ROS 2 Humble Hawksbill
  - [Resmi Kurulum Talimatları](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
- **PlatformIO Core:** Firmware derlemesi için gereklidir.
  ```bash
  pip install -U platformio
  ```
- **Python:** Python 3.10+

### Workspace Kurulumu

1.  **Depoyu Klonlayın:**
    Projenin kaynak kodunu `src` dizinine klonlayın.
    ```bash
    git clone https://github.com/Gazi-Uzay/air-defense-system-ros2.git hss_ws/src
    ```

2.  **ROS Bağımlılıklarını Kurun:**
    Workspace'in ana dizininde (`hss_ws/`) `rosdep`'i çalıştırarak eksik ROS paketlerini kurun.
    ```bash
    sudo apt-get update
    rosdep install -i --from-path src --rosdistro humble -y
    ```

3.  **Python Paketlerini Kurun:**
    (Eğer varsa) Gerekli Python kütüphanelerini kurun.
    ```bash
    # Proje ana dizininde bir requirements.txt dosyası varsa:
    # pip install -r requirements.txt
    ```

4.  **Workspace'i Derleyin:**
    Geliştirme ortamı için `--symlink-install` kullanarak derleme yapmanız tavsiye edilir.
    ```bash
    colcon build --symlink-install
    ```

## Çalıştırma

Her yeni terminalde workspace'i kaynak olarak göstermeniz gerekmektedir.

```bash
source install/setup.bash
ros2 launch hss_bringup hss_system.launch.py
```

## Dokümantasyon

Proje ile ilgili daha detaylı dokümanlara `doc/` dizini altından ulaşabilirsiniz.
