class ChecklistDetail {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.initGeneralNotes();
    }

    bindEvents() {
        // Kontrol kartı toggle
        $(document).on('click', '[data-action="toggle"]', (e) => {
            $(e.currentTarget).closest('.control-card').find('.control-body').slideToggle();
        });

        // Not ekleme paneli
        $(document).on('click', '[data-action="add-note"]', (e) => {
            const item = $(e.currentTarget).closest('.control-item');
            this.openNotesPanel(item);
        });

        // Not paneli kapatma
        $(document).on('click', '[data-action="close-notes"], [data-action="cancel-note"]', () => {
            this.closeNotesPanel();
        });

        // Not kaydetme
        $(document).on('click', '[data-action="save-note"]', () => {
            this.saveNote();
        });

        // Fotoğraf yükleme
        $(document).on('change', '.photo-upload input[type="file"]', (e) => {
            this.handlePhotoUpload(e.target.files);
        });

        // Genel notlar için event binding'ler
        $('#generalPhotosUpload input[type="file"]').on('change', (e) => {
            this.handlePhotoUpload(e.target.files, '#generalPhotosUpload');
        });

        $('#saveGeneralNotes').on('click', () => {
            this.saveGeneralNotes();
        });
    }

    openNotesPanel(item) {
        $('#notesPanel').addClass('active');
        $('#notesPanel').data('item', item);
    }

    closeNotesPanel() {
        $('#notesPanel').removeClass('active');
        // Form temizleme
        $('#notesPanel textarea').val('');
        $('.photo-grid').find('.photo-item').remove();
    }

    saveNote() {
        const item = $('#notesPanel').data('item');
        const note = $('#notesPanel textarea').val();
        
        if (note) {
            // Not ikonunu değiştir
            item.find('.button-note')
                .addClass('has-note')
                .find('span')
                .text('Not Düzenle');
        }
        
        this.closeNotesPanel();
    }

    handlePhotoUpload(files) {
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const photoHtml = `
                    <div class="photo-item">
                        <img src="${e.target.result}" alt="Yüklenen fotoğraf">
                        <button class="photo-remove" onclick="this.parentElement.remove()">
                            <i class="icon icon-trash"></i>
                        </button>
                    </div>
                `;
                $('.photo-upload').before(photoHtml);
            };
            reader.readAsDataURL(file);
        });
    }

    // Genel notları kaydetme
    saveGeneralNotes() {
        const notes = {
            text: $('.general-notes-section textarea').val(),
            photos: this.collectPhotos('.general-notes-section .photo-grid')
        };

        // API'ye kaydetme işlemi burada yapılacak
        console.log('Genel notlar kaydediliyor:', notes);
        
        // Başarılı kayıt bildirimi
        alert('Genel notlar kaydedildi');
    }

    // Fotoğrafları toplama
    collectPhotos(selector) {
        const photos = [];
        $(selector).find('.photo-item img').each(function() {
            photos.push($(this).attr('src'));
        });
        return photos;
    }

    // Genel notları yükleme
    initGeneralNotes() {
        // API'den genel notları çekme işlemi burada yapılacak
        // Örnek veri:
        const savedNotes = {
            text: 'Örnek genel not',
            photos: []
        };

        // Verileri form'a doldurma
        $('.general-notes-section textarea').val(savedNotes.text);
        
        // Fotoğrafları yükleme
        savedNotes.photos.forEach(photoUrl => {
            const photoHtml = `
                <div class="photo-item">
                    <img src="${photoUrl}" alt="Genel not fotoğrafı">
                    <button class="photo-remove" onclick="this.parentElement.remove()">
                        <i class="icon icon-trash"></i>
                    </button>
                </div>
            `;
            $('#generalPhotosUpload').before(photoHtml);
        });
    }
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.checklistDetail = new ChecklistDetail();
}); 