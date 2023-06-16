# Meskenlerin Güvenliğini Sağlamak Amacıyla Yabancı Kişi Tanıma Ve Bildirim Sistemi
Bu sistem, konutlarda yaşayan kişilerin güvenliğini artırmak ve yabancı kişilerin evlere girmesini önlemek için tasarlanmıştır. 

## Tanımlama

Tasarlanan sistem **donanım** ve **yazılım** olmak üzere iki bölümden oluşmaktadır.
Donanım bölümü **sistem bilgisayarı**, **kapı titreşim sensörü** ve **kamera olmak** üzere 3 kısımdan oluşmaktadır.
Yazılım bölümünde ise **yabancı kişileri tanımlama** ve **bildirme** olarak iki alt sistem olarak hazırlanmıştır.


## Uygulamaya Başlarken

### Bağımlılıklar

* Uygulama, Linux dağıtımlarında ve Rasbian işletim sistemi versiyonlarında çalıştırılmalıdır.
* Uygulama Ubuntu ve Raspberry pi b+ board'u üzerinde rasbian raspios-buster-2021-05-07 sürümü üzerinde test edilmiştir.
* Python 3.8.x versiyonu kullanılmalıdır.
* Mail gönderimi yapılacak mail giriş yetkilerinden third party uygulama girişlerine izin verilmelidir.
* Sensör verilerini aldığımız seri port executable izni verilmelidir.
* Uygulama için önyükleme şartı olan kütüphaneler: time, threading, serial, imutils, face_recognition, pickle, cv2, smtp ve email

### Kurulum
Sistem terminali (Ctrl+Alt+T) açılır ve aşağıdaki yüklemeler yapılır.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt install cmake build-essential pkg-config git
sudo apt install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
sudo apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt install libatlas-base-dev liblapacke-dev gfortran
sudo apt install libhdf5-dev libhdf5-103
sudo apt install python3-dev python3-pip python3-numpy
pip3 install opencv-python
pip3 install imutils
pip3 install face-recogniton
pip3 install smtplib
```
Kurulumların başarılı olması durumunda, ön koşul olarak belirtilen seri port executable izni verilmelir.

```
sudo chmod 777 /dev/ttyACM0
```

### Uygulama Çalıştırılması

* Sistem terminali (Ctrl+Alt+T) açılır ve aşağıdaki komut girilmelidir.

```
python3 Secure_cam_app.py
```

## Yardım

Herhangi bir problem veya soru olması durumunda repo issues başlığından sorabilirsiniz.

## Geliştirici

Atabey SAHIN

## Version History

* 0.2
    * Uygulama tamamlandı ve test edildi.
    * Yapılan değişiklikler [commit change]() or See [release history]()
* 0.1
    * İlk yayın

## License

Bu proje [Apache-2.0 license] lisansı ile lisanslanmıştır. Lisans detaylarına LICENSE.md dosyasından bakabilirsiniz.

## Acknowledgments

Keyifli bir yüksek lisans projesi geliştirmeye destek olduğu için hocam Serkan AYDIN ve dönem arkadaşlarıma teşekkür ederim.
