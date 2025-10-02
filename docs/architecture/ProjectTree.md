# 🌳 Proje Ağacı ve Bileşen Sorumlulukları

Bu doküman, HSS projesini oluşturan ana ROS 2 düğümlerini ve her birinin temel sorumluluklarını özetler. Her bir düğümün detaylı dokümanına `docs/nodes/` klasöründen ulaşılabilir.

---

## Ana Düğümler (Nodes)

-   **`camera_driver`**
    -   **Rol:** Fiziksel kamera donanımından ham görüntü ve kalibrasyon bilgilerini alıp ROS 2 ağına yayınlar.
    -   **Paket:** `hss_vision`

-   **`vision_processor_node`**
    -   **Rol:** Ham kamera görüntüsünü işleyerek hedef tespiti yapar ve sonuçları (tespit edilen hedefler, işlenmiş görüntü) ROS 2 ağına yayınlar.
    -   **Paket:** `hss_vision`

-   **`operation_manager_node`**
    -   **Rol:** Sistemin merkezi karar alma ve mantık birimidir. Modları yönetir, otonom/manuel komutları üretir ve güvenlik politikalarını uygular.
    -   **Paket:** `hss_op_manager`

-   **`gimbal_controller_node`**
    -   **Rol:** Sistemin **dış kontrol döngüsünü (outer loop)** çalıştırır. Yüksek seviyeli hedefleme verilerini (görüntü koordinatları, UI tıklamaları) işleyerek donanım için hedef açısal hız komutları üretir.
    -   **Paket:** `hss_control`

-   **`micro_ros_agent` (ESP32 Firmware)**
    -   **Rol:** Düşük seviyeli donanım (motorlar, IMU, lazer) ile ROS 2 dünyası arasında köprü kurar. Gimbal'ın **iç kontrol döngüsünü (inner loop)** gerçek zamanlı olarak yürütür.
    -   **Paket:** `hss_firmware`

-   **`ground_station_gateway`**
    -   **Rol:** Operatör için birincil kontrol ve izleme arayüzünü (GUI) sağlar. Kullanıcı etkileşimlerini ROS 2 komutlarına çevirir ve telemetri verilerini gösterir.
    -   **Paket:** `hss_gui`

-   **`robot_state_publisher`**
    -   **Rol:** Sistemin statik parçaları arasındaki (örn: `base_link` -> `gimbal_link`) geometrik ilişkileri URDF dosyasından okuyarak `/tf_static` topic'inde yayınlar.
    -   **Paket:** `robot_state_publisher` (standart ROS 2 paketi)

-   **`hss_bringup`**
    -   **Rol:** Yukarıda listelenen tüm düğümleri ve gerekli konfigürasyonları tek bir komutla (`ros2 launch`) başlatmaktan sorumlu olan launch dosyalarını içerir.
    -   **Paket:** `hss_bringup`