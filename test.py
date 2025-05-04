stok_talebi_onaylama_olusturma = request.POST.get("stok_talebi_onaylama_olusturma")
        if stok_talebi_onaylama_olusturma:  
            izinler.stok_talebi_onaylama_olusturma = True
        stok_talebi_onaylama_gorme = request.POST.get("stok_talebi_onaylama_gorme")
        if stok_talebi_onaylama_gorme : 
            izinler.stok_talebi_onaylama_gorme = True
        stok_talebi_onaylama_duzenleme = request.POST.get("stok_talebi_onaylama_duzenleme")
        if stok_talebi_onaylama_duzenleme : 
            izinler.stok_talebi_onaylama_duzenleme = True
        stok_talebi_onaylama_silme = request.POST.get("stok_talebi_onaylama_silme")
        if stok_talebi_onaylama_silme : 
            izinler.stok_talebi_onaylama_silme = True
        stok_talebi_onaylama_onaylama = request.POST.get("stok_talebi_onaylama_onaylama")
        if stok_talebi_onaylama_onaylama : 
            izinler.stok_talebi_onaylama_onaylama = True