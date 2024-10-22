import os
deneme = []
def find_unicode_errors_in_files(directory):
    # Desteklenmeyen karakterleri toplayacağımız liste
    error_files = []

    # Verilen dizindeki tüm dosyaları gez
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        try:
                            line.encode('cp1254')
                        except UnicodeEncodeError as e:
                            print(f"Dosya: {file_path} - Satır: {i}")
                            print(f"Detaylar: {e}")
                            error_files.append(file_path)
                            break  # Dosya içindeki ilk hatayı bulduğumuzda çıkıyoruz
            except Exception as e:
                print(f"Başka bir hata tespit edildi: {file_path}")
                print(f"Detaylar: {e}")

    if error_files:
        
        #print(f"\n{len(error_files)} dosyada UnicodeEncodeError hatası bulundu:")
        for ef in error_files:
            print(ef)
            deneme.append(error_files)
    else:
        print("Hiçbir dosyada UnicodeEncodeError hatası bulunamadı.")

# Kontrol etmek istediğiniz klasörün yolunu buraya girin
find_unicode_errors_in_files("C:/Users/habip/Documents/GitHub/santiye/templates")
print(deneme)