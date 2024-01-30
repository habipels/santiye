
var itemCounter = 1; // Başlangıç değeri
window.addEventListener("DOMContentLoaded", () => {
    var addNewItem = document.querySelector("#satis-ekle .card .addNewItem span");
    var table = document.querySelector("#satis-ekle .card .card-body #form2");
    var araToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(1) > span");
    var tumToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(2) > span");
    var itemCounter = 1; // Başlangıç değeri

    /*Add New Item */
    addNewItem.addEventListener("click", function () {
        var newItem = table.firstElementChild.cloneNode(true); // Önceki satırı kopyala
        clearInputs(newItem); // Input alanlarını temizle
        table.appendChild(newItem); // Yeni satırı tabloya ekle

        // ID'leri güncelle
        newItem.querySelectorAll("[id]").forEach(element => {
            element.id += itemCounter; // Her ID'nin sonuna sayı ekle
        });

        // Event listener'ları yeniden kaydet
        newItem.querySelector(".miktarInput").addEventListener("change", hesapla);
        newItem.querySelector(".bfiyatInput").addEventListener("change", hesapla);

        // Toplam fiyatları güncelle
        updateTotal();
        araToplam.textContent = 0 + " $"
        tumToplam.textContent = 0 + " $"

        // Counter'ı artır
        itemCounter++;
    });

    // İlk yükleme için toplam fiyatları güncelle
    updateTotal();
});

// Diğer fonksiyonlar burada...

function clearInputs(element) {
    var inputs = element.querySelectorAll("#searchInput");
    inputs.forEach(input => input.value = "");
    var inpt = element.querySelectorAll(".miktarInput");
    inpt.forEach(inptx => inptx.value = "1");
    var inpt = element.querySelectorAll(".bfiyatInput");
    inpt.forEach(inptx => inptx.value = "0");
    var inpt = element.querySelectorAll(".toplamInput");
    inpt.forEach(inptx => inptx.value = "0");
}

function hesapla(event) {
    var miktarValue = event.target.parentElement.parentElement.querySelector('.miktarInput').value;
    var bFiyatValue = event.target.parentElement.parentElement.querySelector('.bfiyatInput').value;
    var tFiyatValue = miktarValue * bFiyatValue;
    event.target.parentElement.parentElement.querySelector('.toplamInput').value = tFiyatValue;

    // Toplam fiyatları güncelle
    updateTotal();
}

function updateTotal() {
    var maxTotal = 0;
    var toplamInputs = document.getElementsByClassName("toplamInput");
    var araToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(1) > span");
    var tumToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(2) > span");

    for (var i = 0; i < toplamInputs.length; i++) {
        maxTotal += Number(toplamInputs[i].value);
    }

    araToplam.textContent = maxTotal + " $";
    tumToplam.textContent = maxTotal + " $";
}

var addSpec = document.getElementsByClassName("specBtn");
var closeItem = document.getElementsByClassName("closeBtn");
var item = document.getElementsByClassName("table-item");
var toplamInputs = document.getElementsByClassName("toplamInput");

/*Specs Aç / Kapat*/
const specAc = function(event){
    //console.log(event.target);
    event.target.parentElement.children[1].classList.toggle("active");
    var activeSpec = event.target.parentElement.parentElement.parentElement.getElementsByClassName("active");
    console.log(activeSpec)
    if(activeSpec.length > 1){
        activeSpec[0].classList.toggle("active");
    }
}

/*Delete Button function*/
const itemDelete = function(event){
    event.target.parentElement.parentElement.remove();
    if(item.length < 2){
        for(var i = 0; i<item.length; i++){
            closeItem[i].style.display = "none";
        }
    }
    var maxTotal = 0;
    var araToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(1) > span");
    var tumToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(2) > span");
    for(var x = 0; x<toplamInputs.length; x++){
        maxTotal = Number(toplamInputs[x].value) + Number(maxTotal);
    }
    araToplam.textContent = maxTotal + " $";
    tumToplam.textContent = maxTotal + " $";
}

/*Açıklama Ekle Function*/
const aciklamaEkle = function(event){
    //Create Aciklama Element
    var aciklama = document.createElement("div");
    aciklama.setAttribute("class", "aciklama");
    var aciklamaInput = document.createElement("input");
    var aciklamaKapat = document.createElement("span");
    aciklamaKapat.setAttribute("class","mdi mdi-close-box-outline");
    aciklamaKapat.setAttribute("onclick", "aciklamaDelete(event)");
    aciklamaInput.setAttribute("id","aciklama");
    aciklamaInput.setAttribute("name","aciklama");
    aciklamaInput.setAttribute("type", "text");
    aciklamaInput.setAttribute("placeholder","Açıklama Giriniz");
    aciklama.appendChild(aciklamaInput);
    aciklama.appendChild(aciklamaKapat);
    event.target.parentElement.parentElement.parentElement.appendChild(aciklama);
    event.target.style.display = "none";
};

const aciklamaDelete = function(event){
    event.target.parentElement.parentElement.querySelector(".icons .specs .addDesc").style.display = "flex";
    event.target.parentElement.remove();
};

/*İndirim Ekle*/
const indirimEkle = function(event){
    //Create Aciklama Element
    var indirim = document.createElement("div");
    indirim.setAttribute("class", "indirim");
    var indirimInput = document.createElement("input");
    var indirimKapat = document.createElement("span");
    indirimKapat.setAttribute("class","mdi mdi-close-box-outline");
    indirimKapat.setAttribute("onclick", "indirimSil(event)");
    indirimInput.setAttribute("id","indirim");
    indirimInput.setAttribute("name","indirim");
    indirimInput.setAttribute("type", "number");
    indirimInput.setAttribute("placeholder", "İndirim gir %");
    indirim.appendChild(indirimInput);
    indirim.appendChild(indirimKapat);
    event.target.parentElement.parentElement.parentElement.appendChild(indirim);
    event.target.style.display = "none";
};

const indirimSil = function(event){
    event.target.parentElement.parentElement.querySelector(".icons .specs .addSale").style.display = "flex";
    event.target.parentElement.remove();
};

/*HESAPLAR*/
console.log(toplamInputs);
var bFiyatValue;
var miktarValue;
var tFiyatValue;
function hesapla(event){
    miktarValue = event.target.parentElement.parentElement.children[1].children[0].value;
    bFiyatValue = event.target.parentElement.parentElement.children[2].children[0].value;
    tFiyatValue = miktarValue * bFiyatValue;
    event.target.parentElement.parentElement.children[3].children[0].value = tFiyatValue;
    var maxTotal = 0;
    var araToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(1) > span");
    var tumToplam = document.querySelector("#satis-ekle > div.card.hesaplar > div > div:nth-child(2) > span");
    for(var i = 0; i<toplamInputs.length; i++){
        maxTotal = Number(toplamInputs[i].value) + Number(maxTotal);
    }
    araToplam.textContent = maxTotal + " $";
    tumToplam.textContent = maxTotal + " $";
}