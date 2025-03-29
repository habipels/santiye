@register.simple_tag
def calismalari_cek_2(personel, tarih_baslangic, tarih_bitis):
    tarih = str(tarih).split("-")
    yil = tarih[0]
    ay = tarih[1]
    date_obj = datetime(int(yil), int(ay), int(gun))
    sonuc = get_object_or_none(calisanlar_calismalari, calisan=get_object_or_404(calisanlar, id=personel), tarihi=date_obj)
    if sonuc:
        return { 'normal_saat': sonuc.normal_calisma_saati, 'mesai_saati': sonuc.mesai_calisma_saati}
    else:
        return { 'normal_saat': 0, 'mesai_saati': 0}