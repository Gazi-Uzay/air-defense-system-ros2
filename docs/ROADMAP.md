# HSS Projesi Geliştirme Yol Haritası (Roadmap)

Bu doküman, `Product_Requirements_Document.md` ve `Communication_Architecture.md` belgelerine dayanarak projenin geliştirme adımlarını ve hedeflerini tanımlar. Geliştirme süreci, her biri belirli hedeflere sahip 4 ana sprint'e bölünmüştür.

---

## Sprint 1: Temel Altyapı ve Donanım Kontrolü (2 Hafta)

Bu sprint'in ana hedefi, projenin temel iskeletini oluşturmak ve donanım katmanının ROS 2 ile haberleşmesini sağlamaktır.

**Görevler:**
1.  **`hss_interfaces` Paketini Tamamla:**
    -   `Communication_Architecture.md` dosyasında tanımlanan tüm `.msg` ve `.srv` dosyalarının (`Target.msg`, `GimbalCommand.msg`, `SetMode.srv` vb.) `src/hss_interfaces` klasöründe doğru içerikle oluşturulduğunu doğrula.
    -   Eksik veya hatalı tanımları dokümana göre tamamla.
2.  **ROS 2 Workspace'ini Derle:**
    -   `colcon build` komutu ile çalışma alanını derleyerek arayüzlerin tüm sistem tarafından tanınmasını sağla.
3.  **`hss_firmware` Geliştirmesi (Mikrodenetleyici):
    -   **PID Kontrolü:** Step motorlar için temel bir PID kontrol döngüsü iskeleti oluştur.
    -   **micro-ROS Entegrasyonu:**
        -   `/gimbal/cmd` topic'ine abone olarak PID döngüsü için hedef açı (setpoint) alacak altyapıyı kur.
        -   `/gimbal/motor_feedback` topic'inde sahte (dummy) veya gerçek sensör verisi yayınlamaya başla.

**Sprint Hedefi:** Gimbal'ın, `ros2 topic pub` komutuyla gönderilen manuel açı komutlarına tepki verebilir hale gelmesi.

---

## Sprint 2: Görüntüleme ve Algılama (2 Hafta)

Bu sprint, sistemin "gözlerini" oluşturmaya odaklanır. Kamera görüntüsünün alınması ve bu görüntüden anlamlı veriler çıkarılması hedeflenir.

**Görevler:**
1.  **`hss_vision` Paketini Geliştir:**
    -   **`camera_publisher_node`:** Kameradan görüntüleri alıp `/camera/image_raw` topic'inde yayınlayan düğümü oluştur.
    -   **`vision_node` (Temel):** `/camera/image_raw` topic'ine abone olan düğüm iskeletini oluştur.
2.  **Hedef Tespiti Algoritması:**
    -   Basit bir hedef tespit algoritması (örneğin, renk tabanlı thresholding veya kontur tespiti) implemente et.
    -   Tespit edilen hedeflerin koordinatlarını ve temel özelliklerini `hss_interfaces/TargetArray` formatına dönüştür.
3.  **Topic Yayınları:**
    -   İşlenmiş hedef verilerini `/vision/targets` topic'inde yayınla.
    -   Hata ayıklama amacıyla, tespit sonuçlarının (örn. sınırlayıcı kutular) çizildiği video akışını `/vision/image_processed` topic'inde yayınla.

**Sprint Hedefi:** Kameradan alınan canlı video akışında hareketli nesnelerin tespit edilmesi ve konumlarının ROS 2 topic'leri üzerinden yayınlanması.

---

## Sprint 3: Merkezi Mantık ve Manuel Kontrol (2 Hafta)

Bu sprint, operatörün sistemi manuel olarak kontrol edebilmesini sağlayan merkezi mantık ve kullanıcı arayüzü temellerini atmayı hedefler.

**Görevler:**
1.  **`hss_op_manager` Paketini Geliştir:**
    -   **Durum Makinesi:** `SAFE` ve `MANUAL_TRACK` modlarını içeren temel bir durum makinesi (state machine) yapısı kur.
    -   **Manuel Kontrol Mantığı:** `/ui/mouse_target` topic'ine abone ol. `MANUAL_TRACK` modundayken, bu veriyi işleyerek `/gimbal/cmd` topic'inde gimbal için hedef açı komutları yayınla.
    -   `/op/state` topic'inde mevcut sistem modunu yayınla.
2.  **`hss_gui` Paketini Geliştir:**
    -   **Temel Arayüz:** `/vision/image_processed` video akışını gösterecek basit bir UI penceresi oluştur.
    -   **Fare Etkileşimi:** UI üzerindeki fare hareketlerini ve tıklamalarını yakalayarak `/ui/mouse_target` topic'inde yayınla.
3.  **`hss_bringup` Paketini Oluştur:**
    -   Bu sprint'te geliştirilen tüm düğümleri (`camera_publisher`, `vision_node`, `op_manager`, `gui_node`) birlikte başlatan bir `launch.py` dosyası oluştur.

**Sprint Hedefi:** Operatörün, kullanıcı arayüzündeki video ekranına tıklayarak gimbal'ı manuel olarak hedefe yönlendirebilmesi.

---

## Sprint 4: Otonom Yetenekler ve Tam Entegrasyon (3 Hafta)

Bu son sprint, projenin otonom modlarını, güvenlik mekanizmalarını ve kalan tüm özellikleri entegre ederek sistemi tamamlamayı hedefler.

**Görevler:**
1.  **`hss_op_manager` Yeteneklerini Genişlet:**
    -   `AUTO_TRACK` ve `AUTO_KILL` modlarını implemente et. Bu modlar, `/vision/targets` verisini dinleyerek otonom olarak `/gimbal/cmd` komutları üretmelidir.
    -   **Servis Entegrasyonu:** `/op/set_mode` servisini implemente et. `/laser/fire` servisine istek gönderecek client kodunu ekle.
2.  **`hss_gui` Arayüzünü Tamamla:**
    -   Tüm telemetri verilerini (`/op/state`, `/gimbal/motor_feedback` vb.) gösterecek panelleri ekle.
    -   Mod değiştirme, lazer ateşleme ve acil durum butonlarını arayüze ekle ve ilgili ROS 2 arayüzlerine bağla.
3.  **`hss_firmware` Fonksiyonlarını Tamamla:**
    -   `/laser/fire` servis sunucusunu tam olarak implemente ederek lazer donanımını kontrol et.
4.  **Güvenlik Mekanizmaları:**
    -   `/op/emergency_stop` topic'ini dinleyerek tüm sistemi durduran mantığı `op_manager` ve `firmware` seviyelerinde entegre et.
5.  **Test ve Doğrulama:**
    -   PRD'de listelenen tüm fonksiyonel test senaryolarını (mod geçişleri, hedef tespiti, angajman vb.) uçtan uca çalıştır.

**Sprint Hedefi:** PRD'de tanımlanan tüm gereksinimleri karşılayan, stabil, test edilmiş ve tam fonksiyonel bir sistemin ortaya çıkması.
