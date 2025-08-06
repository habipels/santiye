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

        // Dosya yükleme
        $(document).on('change', '.file-upload input[type="file"]', (e) => {
            this.handleFileUpload(e.target.files, $(e.currentTarget).closest('.control-item').data('id'));
        });

        // Genel notlar için event binding'ler
        $('#generalFilesUpload input[type="file"]').on('change', (e) => {
            this.handleFileUpload(e.target.files, 'general');
        });

        $('#saveGeneralNotes').on('click', () => {
            this.saveGeneralNotes();
        });

        // Notları ve dosyaları gönderme
        $('#sendNotes').on('click', () => {
            this.sendNotes();
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
        $('.file-grid').find('.file-item').remove();
    }

    saveNote() {
        const item = $('#notesPanel').data('item');
        const note = $('#notesPanel textarea').val();
        const files = this.collectFiles('#notesPanel .file-grid');
        
        if (note || files.length > 0) {
            // Not ikonunu değiştir
            item.find('.button-note')
                .addClass('has-note')
                .find('span')
                .text('Not Düzenle');
        }
        
        this.closeNotesPanel();
    }

    handleFileUpload(files, itemId) {
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const fileHtml = `
                    <div class="file-item">
                        <a href="${e.target.result}" download="${file.name}">${file.name}</a>
                        <input type="hidden" name="file${itemId}" value="${e.target.result}">
                        <button class="file-remove" onclick="this.parentElement.remove()">
                            <i class="icon icon-trash"></i>
                        </button>
                    </div>
                `;
                $(`[data-id="${itemId}"] .file-grid`).before(fileHtml);
            };
            reader.readAsDataURL(file);
        });
    }

    // Genel notları kaydetme
    saveGeneralNotes() {
        const notes = {
            text: $('.general-notes-section textarea').val(),
            files: this.collectFiles('.general-notes-section .file-grid')
        };

        // API'ye kaydetme işlemi burada yapılacak
        console.log('Genel notlar kaydediliyor:', notes);
        
        // Başarılı kayıt bildirimi
        alert('Genel notlar kaydedildi');
    }

    // Dosyaları toplama
    collectFiles(selector) {
        const files = [];
        $(selector).find('.file-item a').each(function() {
            files.push({
                name: $(this).text(),
                url: $(this).attr('href')
            });
        });
        return files;
    }

    // Genel notları yükleme
    initGeneralNotes() {
        // API'den genel notları çekme işlemi burada yapılacak
        // Örnek veri:
        const savedNotes = {
            text: 'Örnek genel not',
            files: []
        };

        // Verileri form'a doldurma
        $('.general-notes-section textarea').val(savedNotes.text);
        
        // Dosyaları yükleme
        savedNotes.files.forEach(file => {
            const fileHtml = `
                <div class="file-item">
                    <a href="${file.url}" download="${file.name}">${file.name}</a>
                    <button class="file-remove" onclick="this.parentElement.remove()">
                        <i class="icon icon-trash"></i>
                    </button>
                </div>
            `;
            $('#generalFilesUpload').before(fileHtml);
        });
    }

    // Notları ve dosyaları gönderme
    sendNotes() {
        const generalNotes = {
            text: $('.general-notes-section textarea').val(),
            files: this.collectFiles('.general-notes-section .file-grid')
        };

        const specificNotes = [];
        $('.control-item').each(function() {
            const noteText = $(this).find('textarea').val();
            const noteFiles = $(this).find('.file-grid .file-item a').map(function() {
                return {
                    name: $(this).text(),
                    url: $(this).attr('href')
                };
            }).get();

            if (noteText || noteFiles.length > 0) {
                specificNotes.push({
                    text: noteText,
                    files: noteFiles
                });
            }
        });

        const data = {
            generalNotes: generalNotes,
            specificNotes: specificNotes
        };

        // API'ye gönderme işlemi burada yapılacak
        console.log('Notlar ve dosyalar gönderiliyor:', data);
        
        // Başarılı gönderim bildirimi
        alert('Notlar ve dosyalar gönderildi');
    }
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.checklistDetail = new ChecklistDetail();
});