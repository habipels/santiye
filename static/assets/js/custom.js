function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "flex";
    }
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "none";
    }
}

window.addEventListener("DOMContentLoaded", () => {
    var faturaItems = document.querySelectorAll("#invoice-list-data > tr");
    var tahsilatEkle = document.querySelectorAll("body > div.invoice-detail-modal > div > div.modal-body > div.kalan > div > div.ekle > span.mdi.mdi-plus-circle");
    var tahsilatPopup = document.querySelector(".invoice-detail-modal .tahsilatEkle");
    var tahsilatClose = document.querySelectorAll("body > div.invoice-detail-modal > div > div.modal-body > div.tahsilatEkle > form > div.buttons > span");
    for (var i = 0; i < faturaItems.length; i++) {
        faturaItems[i].addEventListener("click", function() {
            var modalId = "invoice-detail-modal" + this.id;
            openModal(modalId);
        });
    }
    for (var i = 0; i < tahsilatEkle.length; i++) {
        tahsilatEkle[i].addEventListener("click", function() {
            var da = "tahsilatEkle" + this.id;
            openModal(da);
        });
    }

    for (var i = 0; i < tahsilatClose.length; i++) {
        tahsilatClose[i].addEventListener("click", function() {
            var da = "tahsilatEkle" + this.id;
            closeModal(da);
        });
    }
    

    var closeButtons = document.querySelectorAll(".close-icon > span");
    closeButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var modalId = this.closest(".invoice-detail-modal").id;
            closeModal(modalId);
        });
    });

    var cancelButtons = document.querySelectorAll(".cancel-icon > span");
    cancelButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            closeModal("delete-fatura-modal");
            closeModal("delete-makbuz-modal");
        });
    });

    var tahsilatMakbuzuGoruntuleBtn = document.querySelector("body > div.invoice-detail-modal > div > div.modal-body > div.eklenen-kasa > div > div.makbuz > span.mdi.mdi-text-box-search-outline");
    var tahsilatMakbuzuKapat = document.querySelector("body > div.tahsilat-makbuzu-modal > div > div.modal-head > div.invoice-icons > div.icon-item.close-icon > span");
    tahsilatMakbuzuGoruntuleBtn.addEventListener("click", function() {
        openModal("tahsilat-makbuzu-modal");
    });
    tahsilatMakbuzuKapat.addEventListener("click", function() {
        closeModal("tahsilat-makbuzu-modal");
    });

    var makbuzDeleteBtn = document.querySelector("body > div.tahsilat-makbuzu-modal > div > div.modal-head > div.invoice-icons > div.icon-item.cancel-icon > span");
    var makbuzDeleteCancelBtn = document.querySelector("body > div.delete-makbuz-modal > div > div.buttons > span");
    makbuzDeleteBtn.addEventListener("click", function() {
        openModal("delete-makbuz-modal");
    });
    makbuzDeleteCancelBtn.addEventListener("click", function() {
        closeModal("delete-makbuz-modal");
    });
});
