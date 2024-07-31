def gelir_faturasi_kaydet_2(request,hash):
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        musteri_bilgisi  = request.POST.get("musteri_bilgisi")
        daterange = request.POST.get("daterange")
        gelir_kategorisii = request.POST.get("gelir_kategorisi")
        cari_aciklma = request.POST.get("cari_aciklma")
        etiketler = request.POST.getlist("etiketler")
        faturano = request.POST.get("faturano")
        urunadi = request.POST.getlist("urunadi")
        miktari = request.POST.getlist("miktari")
        bfiyatInput = request.POST.getlist("bfiyatInput")
        indirim = request.POST.getlist("indirim")
        aciklama = request.POST.getlist("aciklama")
        doviz_kuru = request.POST.get("doviz_kuru")

        cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = users)
        if cari_bilgisi:
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gelir_Bilgisi.objects.create(gelir_kime_ait_oldugu = users,
            cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = users),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
                                         )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i])
                    if urun:
                        if indirim[i] == "":
                            a = 0
                        else:
                            a = indirim[i]
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(a),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=users,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )

        else:
            cari_bilgisi = cari.objects.create(cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = users,aciklama = cari_aciklma)
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gelir_Bilgisi.objects.create(gelir_kime_ait_oldugu = users,
            cari_bilgisi = get_object_or_none(cari,id = cari_bilgisi.id),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
            )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i])
                    if urun:
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=users,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
        gelir_qr.objects.create(gelir_kime_ait_oldugu = get_object_or_none(Gelir_Bilgisi,id = new_project.id))
    return redirect("accounting:gelirler_sayfasi")