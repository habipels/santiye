from escpos.printer import Usb
import usb.core
import usb.util

try:
    # USB cihazlarını listele
    devices = usb.core.find(find_all=True)
    print("Bağlı USB cihazları:")
    for device in devices:
        print(f"Device: ID {hex(device.idVendor)}:{hex(device.idProduct)}")

    # USB backend kontrolü
    if not usb.core.find(idVendor=0x0483, idProduct=0x5720):
        raise RuntimeError("Yazıcı bulunamadı. Lütfen bağlantıyı ve sürücüyü kontrol edin.")

    # USB yazıcıya bağlan
    p = Usb(0x0483, 0x5720, encoding="utf-8")  # Türkçe karakter desteği için kodlama utf-8 olarak ayarlandı
    print("Yazıcıya başarıyla bağlanıldı.")

    # Ürün listesi
    products = [
        {"name": "Ürün 1", "quantity": 2, "price": 25.00},
        {"name": "Ürün 2", "quantity": 1, "price": 50.00},
        {"name": "Ürün 3", "quantity": 3, "price": 15.00},
    ]

    # Fiş yazdırma
    p.set(bold=True)  # Kalın yazı stili başlat
    p.text("MAŞALLAH KAYA\n".upper())
    p.text("ADRES: ŞERİFİYE MAHALLESİ KÜLTÜR SOKAK 56 VAN /MERKEZ\n".upper())
    p.text("TELEFON: 0123 456 7890\n".upper())
    p.text("-----------------------------\n")
    p.text("ÜRÜNLER:\n".upper())
    p.set(bold=False)  # Kalın yazı stilini kapat

    total = 0
    for product in products:
        line_total = product["quantity"] * product["price"]
        total += line_total
        p.text(f"{product['name'].upper()} x{product['quantity']} - {line_total:.2f} TL\n")

    p.text("-----------------------------\n")
    p.set(bold=True)  # Kalın yazı stili başlat
    p.text(f"TOPLAM: {total:.2f} TL\n".upper())
    p.set(bold=False)  # Kalın yazı stilini kapat
    p.text("TEŞEKKÜR EDERİZ!\n".upper())
    p.cut()

except Exception as e:
    print("Yazıcıya bağlanılamadı. Hata mesajı:")
    print(e)
