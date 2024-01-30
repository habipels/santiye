window.addEventListener("DOMContentLoaded", ()=>{
    var tahsilatEkle = document.querySelector("body > div.invoice-detail-modal > div > div.modal-body > div.kalan > div > div.ekle > span.mdi.mdi-plus-circle");
    var modal = document.querySelectorAll(".invoice-detail-modal");
    var modalClose = document.querySelector("body > div.invoice-detail-modal > div > div.modal-head > div.invoice-icons > div.icon-item.close-icon > span");
    var tahsilatPopup = document.querySelector(".invoice-detail-modal .tahsilatEkle");
    var tahsilatClose = document.querySelector("body > div.invoice-detail-modal > div > div.modal-body > div.tahsilatEkle > form > div.buttons > span");
    var faturaItems = document.querySelectorAll("#invoice-list-data > tr");
    var deleteModal = document.querySelector(".delete-fatura-modal");
    var deleteBtn = document.querySelector("body > div.invoice-detail-modal > div > div.modal-head > div.invoice-icons > div.icon-item.cancel-icon > span");
    var deleteCancelBtn = document.querySelector("body > div.delete-fatura-modal > div > div.buttons > span");
    var makbuzDeleteBtn = document.querySelector("body > div.tahsilat-makbuzu-modal > div > div.modal-head > div.invoice-icons > div.icon-item.cancel-icon > span");
    var makbuzDeleteCancelBtn = document.querySelector("body > div.delete-makbuz-modal > div > div.buttons > span");
    var makbuzDeleteModal = document.querySelector(".delete-makbuz-modal");
    var tahsilatMakbuzuGoruntuleBtn = document.querySelector("body > div.invoice-detail-modal > div > div.modal-body > div.eklenen-kasa > div > div.makbuz > span.mdi.mdi-text-box-search-outline");
    var tahsilatMakbuzu = document.querySelector(".tahsilat-makbuzu-modal");
    var tahsilatMakbuzuKapat = document.querySelector("body > div.tahsilat-makbuzu-modal > div > div.modal-head > div.invoice-icons > div.icon-item.close-icon > span");
    for(var i = 0; i< faturaItems.length; i++){
        faturaItems[i].addEventListener("click", function(){
            alert(faturaItems[i].id,modal[i].id);
            if (faturaItems[i].id == modal[i].id){
                alert(faturaItems[i].id,modal[i].id);
            modal[i].style.display = "flex";}
        })
    }
    tahsilatEkle.addEventListener("click", function(){
        tahsilatPopup.style.display = "flex";
    });
    tahsilatClose.addEventListener("click", function(){
        tahsilatPopup.style.display = "none";
    });
    modalClose.addEventListener("click", function(){
        modal.style.display = "none";
    });
    deleteBtn.addEventListener("click", function(){
        deleteModal.style.display = "flex";
    });
    deleteCancelBtn.addEventListener("click", function(){
        deleteModal.style.display = "none";
    });
    tahsilatMakbuzuGoruntuleBtn.addEventListener("click", function(){
        tahsilatMakbuzu.style.display = "flex";
    });
    tahsilatMakbuzuKapat.addEventListener("click", function(){
        tahsilatMakbuzu.style.display = "none";
    });
    makbuzDeleteBtn.addEventListener("click", function(){
        makbuzDeleteModal.style.display = "flex";
    });
    makbuzDeleteCancelBtn.addEventListener("click", function(){
        makbuzDeleteModal.style.display = "none";
    });
});