# 📄 Product Requirements Document (PRD) - HSS Projesi

**Proje:** ROS 2 Tabanlı Yönlendirilmiş Savunma Sistemi
**Kaynak Doküman:** `HSS ROS 2 İletişim Mimarisi.md`
**Sürüm:** 2.2
**Tarih:** 26/09/2025

---

## 1. Amaç

Bu doküman, ROS 2 mimarisi üzerine kurulu, hedef tespiti, takibi ve angajman yeteneklerine sahip bir savunma sisteminin gereksinimlerini tanımlar. Sistemin temel amacı, bir kamera aracılığıyla hedefleri tespit etmek, bir operatör arayüzü üzerinden sistemi yönetmek ve bir gimbal üzerine monte edilmiş bir lazer ile hedeflere angajman sağlamaktır.

---

## 2. Kapsam

-   **Gerçek Zamanlı Görüntü Aktarımı:** Ham ve işlenmiş video akışlarının yer istasyonuna iletilmesi.
-   **Görüntü İşleme:** Görüntü üzerinden hedef tespiti, renk ve QR kod bilgilerinin çıkarılması.
-   **Operasyon Yönetimi:** Sistemin farklı çalışma modları arasında (Güvenli, Manuel Takip, Otomatik Takip, Otomatik İmha) geçiş yapmasını sağlayan merkezi bir mantık birimi.
-   **Gimbal Kontrolü:** Merkezi yönetim biriminden gelen komutlarla gimbal'ın hedefe yönlendirilmesi.
-   **Donanım Arayüzü:** Düşük seviyeli donanım (motorlar, IMU, lazer) ile ROS 2 dünyası arasında köprü kuran bir mikrodenetleyici.
-   **Yer İstasyonu Arayüzü:** Operatörün sistemi izlemesine, manuel olarak kontrol etmesine ve komutlar göndermesine olanak tanıyan bir kullanıcı arayüzü.
-   **Güvenlik Mekanizmaları:** Sistem genelinde geçerli bir acil durum durdurma (E-Stop) mekanizması.

---

## 3. Fonksiyonel Gereksinimler

Projenin fonksiyonel gereksinimleri, her bir ROS 2 düğümünün sorumluluklarını tanımlayan modüler bir yapıya bölünmüştür.

-   Proje bileşenlerinin genel bir özeti için **ProjectTree.md** dosyasına bakınız.
-   Her bir düğümün detaylı görevleri, iletişim arayüzleri ve parametreleri için **`../nodes/`** klasöründeki ilgili dokümanı inceleyiniz.
    -   `nodes/camera_driver.md`
    -   `nodes/vision_processor_node.md`
    -   `nodes/operation_manager_node.md`
    -   `nodes/gimbal_controller_node.md`
    -   `nodes/micro_ros_agent.md`
    -   `nodes/ground_station_gateway.md`

---

## 4. İletişim Mimarisi Özeti

Bu gereksinimler, HSS ROS 2 İletişim Mimarisi.md dokümanında detaylandırılan ROS 2 topic ve service yapısı ile karşılanacaktır. Kritik veriler (komutlar, hedef listesi) Reliable, yüksek frekanslı telemetri verileri (görüntü, IMU) ise Best Effort QoS profilleri ile iletilecektir. Acil durum sinyalleri, kayıpsız teslimat garantisi için Reliable olacaktır.
Sistem performans testlerinde, kritik topic'ler için hem ideal gecikme hedefleri (deadline) hem de maksimum toleranslar (zaman aşımı) doğrulanmalıdır. Örneğin, `/gimbal/cmd_rate` için ideal hedef **20 ms** iken, sistemin kararlılığını bozacak üst sınır **100 ms**'dir.
### 4.1. İki Katmanlı Kontrol Mimarisi (Outer–Inner Loop)

Bu mimari, sistemin kontrol görevlerini iki ana katmana ayırır:

#### Dış Açı Döngüsü – ROS 2 (`gimbal_controller_node`)
*   **Girdi:** Kaynaklardan (UI tıklaması, `vision_processor_node`, `operation_manager_node`) gelen açısal hata.
*   **İşlem:** Açı PI kontrolcüsü ile hedef açısal hız komutu (`/gimbal/cmd_rate`) üretir.
*   **Özellikler:** Komut frekansı ~30–100 Hz. Ağ gecikmelerine dayanıklı, yüksek seviyeli karar mantığı burada çalışır.

#### İç Hız Döngüsü – ESP32 (Firmware)
*   **Girdi:** Dış döngüden gelen hedef açısal hız (`ω_cmd`).
*   **İşlem:** Anlık hızı (`ω_meas`) IMU'dan okur ve aradaki hatayı ~1 kHz'de çalışan bir Rate PID kontrolcüsü ile kapatır.
*   **Özellikler:** Motor sürüşü, limitler, anti-windup, jerk/slew sınırlama gibi gerçek zamanlı işlevler burada yürütülür. Telemetri ve IMU verileri ROS 2'ye geri yayınlanır.


Basitleştirilmiş Veri Akışı Diyagramı:
```mermaid
graph LR
    UI[Ground Station / HUD] -->|/ui/mouse_target| GC[gimbal_controller_node (Outer Loop)]
    V[vision_processor_node] -->|/vision/targets| GC
    OM[operation_manager_node] -->|/gimbal/cmd (opsiyonel açı SP)| GC
    GC -->|/gimbal/cmd_rate (ω_cmd)| MCU[ESP32 Firmware (Inner Loop)]
    MCU -->|/gimbal/state, /gimbal/imu| GC
    OM -->|/laser/fire (client)| MCU
    GS[Ground Station] -->|/op/request_fire| OM
    MCU -->|PWM/Driver| MOTORS[(Yaw & Pitch Motors)]
```
```
