class ProjectManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateNumberingPreview();
    }

    bindEvents() {
        // Daire numaralandırma önizleme
        $('#floorCount, #unitsPerFloor, #startNumber').on('input', () => {
            this.updateNumberingPreview();
        });

        // Ortak alan ekleme
        $('#addCommonArea').on('click', () => {
            this.addCommonArea();
        });

        // Cephe ekleme
        $('#addFacade').on('click', () => {
            this.addFacade();
        });

        // Silme işlemleri
        $(document).on('click', '.remove-area', (e) => {
            $(e.target).closest('.area-item').remove();
        });

        $(document).on('click', '.remove-facade', (e) => {
            $(e.target).closest('.facade-item').remove();
        });

        // Proje kaydetme
        $('#saveProject').on('click', () => {
            this.saveProject();
        });

        // Görünüm değiştirme
        $('.preview-filter').on('click', (e) => {
            $('.preview-filter').removeClass('active');
            $(e.currentTarget).addClass('active');
            this.updateNumberingPreview();
        });
    }

    updateNumberingPreview() {
        const floorCount = parseInt($('#floorCount').val()) || 0;
        const unitsPerFloor = parseInt($('#unitsPerFloor').val()) || 0;
        const startNumber = parseInt($('#startNumber').val()) || 101;
        const view = $('.preview-filter.active').data('view');
        
        const preview = $('#numberingPreview');
        preview.empty();

        if (view === 'floors') {
            // Kat bazlı görünüm
            for (let floor = 0; floor < floorCount; floor++) {
                const floorNumber = Math.floor(startNumber / 100) + floor;
                const floorHtml = `
                    <div class="floor-group">
                        <div class="floor-header">${floorNumber}. Kat</div>
                        <div class="preview-list">
                            ${this.generateUnitsHtml(floorNumber, unitsPerFloor)}
                        </div>
                    </div>
                `;
                preview.append(floorHtml);
            }
        } else {
            // Liste görünümü
            preview.append('<div class="preview-list">');
            for (let floor = 0; floor < floorCount; floor++) {
                const floorNumber = Math.floor(startNumber / 100) + floor;
                preview.find('.preview-list').append(this.generateUnitsHtml(floorNumber, unitsPerFloor));
            }
            preview.append('</div>');
        }
    }

    generateUnitsHtml(floorNumber, unitsPerFloor) {
        let html = '';
        for (let unit = 0; unit < unitsPerFloor; unit++) {
            const unitNumber = (floorNumber * 100) + (unit + 1);
            html += `
                <div class="preview-item">
                    Daire ${unitNumber}
                </div>
            `;
        }
        return html;
    }

    addCommonArea() {
        const areaHtml = `
            <div class="area-item">
                <input type="text" class="form-control" placeholder="Ortak alan adı...">
                <select class="form-control">
                    <option value="">Alan Tipi Seçin</option>
                    <option value="corridor">Koridor</option>
                    <option value="stairs">Merdiven</option>
                    <option value="entrance">Giriş</option>
                    <option value="other">Diğer</option>
                </select>
                <button class="button-icon remove-area">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        `;
        $('#commonAreasList').append(areaHtml);
    }

    addFacade() {
        const facadeHtml = `
            <div class="facade-item">
                <input type="text" class="form-control" placeholder="Cephe adı...">
                <select class="form-control">
                    <option value="">Yön Seçin</option>
                    <option value="north">Kuzey</option>
                    <option value="south">Güney</option>
                    <option value="east">Doğu</option>
                    <option value="west">Batı</option>
                </select>
                <button class="button-icon remove-facade">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        `;
        $('#facadesList').append(facadeHtml);
    }

    saveProject() {
        const project = {
            blockName: $('#blockName').val(),
            floorCount: $('#floorCount').val(),
            unitsPerFloor: $('#unitsPerFloor').val(),
            startNumber: $('#startNumber').val(),
            commonAreas: this.collectCommonAreas(),
            facades: this.collectFacades()
        };

        console.log('Proje kaydediliyor:', project);
        // API'ye kaydetme işlemi burada yapılacak
        alert('Proje başarıyla kaydedildi!');
    }

    collectCommonAreas() {
        const areas = [];
        $('.area-item').each(function() {
            areas.push({
                name: $(this).find('input').val(),
                type: $(this).find('select').val()
            });
        });
        return areas;
    }

    collectFacades() {
        const facades = [];
        $('.facade-item').each(function() {
            facades.push({
                name: $(this).find('input').val(),
                direction: $(this).find('select').val()
            });
        });
        return facades;
    }
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.projectManager = new ProjectManager();
}); 