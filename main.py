import cv2
from pyzbar import pyzbar
from pyHES import HES
import json

# hes auth Kullanımı : https://github.com/keyiflerolsun/pyHES#-kullan%C4%B1m
hes_sinifi = HES(
    telefon_numarasi = 5123456789
    id_token         = "xxxxxxxxxxxxx"
)

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        # gelen barcode'un içinden hes kodunu parslama işlemi
        sonuc  = barcode_info[barcode_info.find("|")+1:].split()[0]
        # hes kodunu sağlık bakanlığı sisteminde sorgulama
        hessorgu = hes_sinifi.hes_sorgula(sonuc)
        # hes kodu sorgusundan dönen değerleri ayırma işlemi
        hes_kodu = hessorgu['hes_kodu']
        tc_kimlik_no = hessorgu['tc_kimlik_no']
        adsoyad = hessorgu['ad']+" "+hessorgu['soyad']
        durum = hessorgu['durum']
        gecerlilik = hessorgu['gecerlilik']

        abc = durum + "\n" + " " + adsoyad

        # ekrana yazdırma gösterme
        cv2.putText(
            frame, 
            abc, #text
            (x + 6, y - 6), #position at which writing has to start
            font, #font family
            2.0, #font size
            (255, 255, 255),  #font color
            1 #font stroke
            )
        # gelen hesleri txt e yazma
        with open("gecmis_okunan_hesler.txt", mode ='a') as file:
            file.write(
                "-------------------" + "\n"
                +"Hes Kodu : "+ hes_kodu + "\n"
                +"TC Kimlik No : " + tc_kimlik_no + "\n"
                + "Ad Soyad : " + adsoyad + "\n"
                + "Durum : " + durum + "\n"
                + "Gecerlilik : " + gecerlilik + "\n"+
                "-------------------" + "\n"
            )

        # gelen hesleri log tutma print etme
        print (
                "-------------------" + "\n"
                +"Hes Kodu : "+ hes_kodu + "\n"
                +"TC Kimlik No : " + tc_kimlik_no + "\n"
                + "Ad Soyad : " + adsoyad + "\n"
                + "Durum : " + durum + "\n"
                + "Gecerlilik : " + gecerlilik + "\n"+
                "-------------------" + "\n"
                )
    return frame


def main():
    camera = cv2.VideoCapture(0)
    # 1080p görüntü
    camera.set(3, 1920)
    camera.set(4, 1080)
    ret, frame = camera.read()
    
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        # Full Ekran Yapımı
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("window", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()

# main
if __name__ == '__main__':
    main()
