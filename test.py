import win32print
import win32api

try:
    # Varsayılan yazıcıyı al
    printer_name = win32print.GetDefaultPrinter()
    print(f"Varsayılan yazıcı: {printer_name}")

    # Yazıcıya basit bir metin gönder
    text = """
    MAŞALLAH KAYA
    ADRES: ŞERİFİYE MAHALLESİ KÜLTÜR SOKAK 56 VAN /MERKEZ
    TELEFON: 0123 456 7890
    -----------------------------
    ÜRÜNLER:
    Ürün 1 x2 - 50.00 TL
    Ürün 2 x1 - 50.00 TL
    -----------------------------
    TOPLAM: 100.00 TL
    TEŞEKKÜR EDERİZ!
    """
    hprinter = win32print.OpenPrinter(printer_name)
    job = win32print.StartDocPrinter(hprinter, 1, ("Fiş Yazdırma", None, "RAW"))
    win32print.StartPagePrinter(hprinter)
    win32print.WritePrinter(hprinter, text.encode("utf-8"))
    win32print.EndPagePrinter(hprinter)
    win32print.EndDocPrinter(hprinter)
    win32print.ClosePrinter(hprinter)
    print("Fiş başarıyla yazdırıldı.")
except Exception as e:
    print(f"Yazıcıya bağlanılamadı. Hata: {e}")
