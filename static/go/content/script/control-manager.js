class ControlManager {
    constructor() {
        this.init();
        
        // PDF oluşturma için özel proje özeti stil fonksiyonunu global olarak erişilebilir yap
        window.html2pdf = window.html2pdf || {};
        window.html2pdf.styleProjeOzeti = this.styleProjeOzetiForPDF;
    }

    init() {
        this.bindEvents();
        this.initSections();
        this.initPageTabs();
        this.initTinyMCE();
        this.initDragAndDrop();
        this.initResizeHandles();
    }

    initTinyMCE() {
        if (typeof tinymce !== 'undefined') {
            tinymce.init({
                selector: '.tinymce-editor',
                height: 300,
                menubar: false,
                plugins: [
                    'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
                    'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
                    'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
                ],
                toolbar: 'undo redo | formatselect | ' +
                    'bold italic backcolor | alignleft aligncenter ' +
                    'alignright alignjustify | bullist numlist outdent indent | ' +
                    'removeformat | help',
                content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
            });
        }
    }

    bindEvents() {
        // Bölüm açma/kapama
        $(document).on('click', '[data-toggle="collapse"]', (e) => {
            const target = $(e.currentTarget).data('target');
            this.toggleSection(target);
        });

        // Filtreler
        $('#workGroupFilter, #statusFilter').on('change', () => {
            this.filterUnits();
        });

        // Sayfa tab işlemleri
        $(document).on('click', '.add-page-tab', () => this.addNewPage());
        $(document).on('click', '.remove-page-tab', (e) => {
            e.stopPropagation();
            this.removePage($(e.currentTarget).closest('.page-tab'));
        });
        $(document).on('click', '.page-tab', (e) => {
            if (!$(e.target).hasClass('remove-page-tab')) {
                this.switchPage($(e.currentTarget));
            }
        });

        // Şablon seçici
        $(document).on('click', '.template-item', (e) => {
            const templateId = $(e.currentTarget).data('template');
            this.loadTemplate(templateId);
        });

        // Resize event
        $(window).on('resize', () => this.updateMaxWidth());
    }

    updateMaxWidth() {
        const container = $('.report-container');
        if (container.length) {
            const maxWidth = container[0].clientWidth;
            $('.page-content').css('max-width', `${maxWidth}px`);
        }
    }

    initPageTabs() {
        // İlk sayfayı aktif yap
        $('.page-tab').first().addClass('active');
        this.showPage($('.page-tab').first().data('page'));
    }

    addNewPage() {
        const pageCount = $('.page-tab').length;
        const newPageNumber = pageCount + 1;
        
        const newTab = $(`
            <div class="page-tab" data-page="page-${newPageNumber}">
                <span>Sayfa ${newPageNumber}</span>
                <button class="remove-page-tab"><i class="fas fa-times"></i></button>
            </div>
        `);
        
        const newPage = $(`
            <div class="page-content" id="page-${newPageNumber}">
                <div class="tinymce-editor">
                    <!-- TinyMCE editör buraya gelecek -->
                </div>
            </div>
        `);
        
        $('.page-tabs').append(newTab);
        $('.pages-container').append(newPage);
        
        this.switchPage(newTab);
        
        // Yeni sayfada TinyMCE'yi başlat
        if (typeof tinymce !== 'undefined') {
            tinymce.init({
                selector: `#page-${newPageNumber} .tinymce-editor`,
                height: 300,
                menubar: false,
                plugins: [
                    'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
                    'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
                    'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
                ],
                toolbar: 'undo redo | formatselect | ' +
                    'bold italic backcolor | alignleft aligncenter ' +
                    'alignright alignjustify | bullist numlist outdent indent | ' +
                    'removeformat | help',
                content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
            });
        }
    }

    removePage(tab) {
        if ($('.page-tab').length <= 1) {
            alert('En az bir sayfa olmalıdır!');
            return;
        }
        
        const pageId = tab.data('page');
        const nextTab = tab.next('.page-tab').length ? tab.next('.page-tab') : tab.prev('.page-tab');
        
        // TinyMCE editörü kaldır
        if (typeof tinymce !== 'undefined') {
            tinymce.remove(`#${pageId} .tinymce-editor`);
        }
        
        tab.remove();
        $(`#${pageId}`).remove();
        
        if (nextTab.length) {
            this.switchPage(nextTab);
        }
    }

    switchPage(tab) {
        $('.page-tab').removeClass('active');
        tab.addClass('active');
        
        const pageId = tab.data('page');
        this.showPage(pageId);
    }

    showPage(pageId) {
        $('.page-content').removeClass('active').hide();
        $(`#${pageId}`).addClass('active').show();
    }

    toggleSection(targetId) {
        const content = $(targetId);
        const header = $(`[data-target="${targetId}"]`);
        
        content.slideToggle(300);
        header.toggleClass('active');
        
        // İkon rotasyonu
        header.find('i').toggleClass('fa-rotate-180');
    }

    filterUnits() {
        const workGroup = $('#workGroupFilter').val();
        const status = $('#statusFilter').val();

        $('.unit-card').each((i, card) => {
            const $card = $(card);
            let show = true;

            if (workGroup !== 'all') {
                const hasWorkGroup = $card.find(`.work-badge:contains("${workGroup}")`).length > 0;
                show = show && hasWorkGroup;
            }

            if (status !== 'all') {
                const hasStatus = $card.find(`.status-badge.${status}`).length > 0;
                show = show && hasStatus;
            }

            $card.toggle(show);
        });
    }

    initSections() {
        // İlk bölümü açık göster
        $('.section-content').first().show();
        $('.section-header').first().addClass('active');
    }

    initDragAndDrop() {
        $('.component-item').each((i, item) => {
            $(item).attr('draggable', true);
        });

        $('.page-content').each((i, content) => {
            $(content).on('dragover', (e) => {
                e.preventDefault();
                $(content).addClass('drag-over');
            }).on('dragleave', () => {
                $(content).removeClass('drag-over');
            }).on('drop', (e) => {
                e.preventDefault();
                $(content).removeClass('drag-over');
                
                const componentType = e.originalEvent.dataTransfer.getData('text/plain');
                this.addComponent(componentType, $(content));
            });
        });
    }

    initResizeHandles() {
        $(document).on('mousedown', '.component-resize', (e) => {
            e.preventDefault();
            const component = $(e.target).closest('.component');
            const startX = e.pageX;
            const startY = e.pageY;
            const startWidth = component.outerWidth();
            const startHeight = component.outerHeight();
            const direction = $(e.target).data('direction');
            const minWidth = 200;
            const minHeight = 100;

            const handleMouseMove = (e) => {
                e.preventDefault();
                const deltaX = e.pageX - startX;
                const deltaY = e.pageY - startY;
                let newWidth = startWidth;
                let newHeight = startHeight;

                switch(direction) {
                    case 'nw':
                        newWidth = Math.max(minWidth, startWidth - deltaX);
                        newHeight = Math.max(minHeight, startHeight - deltaY);
                        component.css({
                            width: newWidth,
                            height: newHeight,
                            left: startX - e.pageX + component.offset().left,
                            top: startY - e.pageY + component.offset().top
                        });
                        break;
                    case 'ne':
                        newWidth = Math.max(minWidth, startWidth + deltaX);
                        newHeight = Math.max(minHeight, startHeight - deltaY);
                        component.css({
                            width: newWidth,
                            height: newHeight,
                            top: startY - e.pageY + component.offset().top
                        });
                        break;
                    case 'sw':
                        newWidth = Math.max(minWidth, startWidth - deltaX);
                        newHeight = Math.max(minHeight, startHeight + deltaY);
                        component.css({
                            width: newWidth,
                            height: newHeight,
                            left: startX - e.pageX + component.offset().left
                        });
                        break;
                    case 'se':
                        newWidth = Math.max(minWidth, startWidth + deltaX);
                        newHeight = Math.max(minHeight, startHeight + deltaY);
                        component.css({
                            width: newWidth,
                            height: newHeight
                        });
                        break;
                }

                // Tablo genişliğini ayarla
                const tableContainer = component.find('.table-container');
                if (tableContainer.length) {
                    tableContainer.css({
                        width: '100%',
                        maxWidth: '100%'
                    });
                }
            };

            const handleMouseUp = () => {
                $(document).off('mousemove', handleMouseMove);
                $(document).off('mouseup', handleMouseUp);
            };

            $(document).on('mousemove', handleMouseMove);
            $(document).on('mouseup', handleMouseUp);
        });
    }

    addComponent(type, container) {
        let component;
        
        switch(type) {
            case 'text':
                component = $(`
                    <div class="component text-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="editable-text-container">
                            <div class="editable-text" contenteditable="true" spellcheck="false" data-placeholder="Metni buraya yazın"></div>
                        </div>
                    </div>
                `);
                break;
            case 'image':
                component = $(`
                    <div class="component image-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <input type="file" accept="image/*" class="image-upload">
                    </div>
                `);
                break;
            case 'table':
                component = $(`
                    <div class="component table-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <table class="minimal-table">
                            <thead>
                                <tr>
                                    <th>Başlık 1</th>
                                    <th>Başlık 2</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Veri 1</td>
                                    <td>Veri 2</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                `);
                break;
            case 'chart':
                component = $(`
                    <div class="component chart-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="chart-container"></div>
                    </div>
                `);
                break;
            case 'progress-chart':
                component = $(`
                    <div class="component progress-chart-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="progress-chart"></div>
                    </div>
                `);
                this.initProgressChart(component.find('.progress-chart'));
                break;

            case 'task-table':
                component = $(`
                    <div class="component task-table-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="table-container">
                            <table class="minimal-table task-table">
                                <thead>
                                    <tr>
                                        <th>Görev</th>
                                        <th>Atanan</th>
                                        <th>Başlangıç</th>
                                        <th>Bitiş</th>
                                        <th>Durum</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Örnek Görev 1</td>
                                        <td>Ahmet Yılmaz</td>
                                        <td>01.01.2024</td>
                                        <td>15.01.2024</td>
                                        <td><span class="status completed">Tamamlandı</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `);
                break;

            case 'staff-table':
                component = $(`
                    <div class="component staff-table-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="table-container">
                            <table class="minimal-table staff-table">
                                <thead>
                                    <tr>
                                        <th>Personel</th>
                                        <th>Departman</th>
                                        <th>Pozisyon</th>
                                        <th>İletişim</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>
                                            <img src="{% static 'go/content/images/avatar.png' %}" class="avatar" alt="Avatar">
                                            Ahmet Yılmaz
                                        </td>
                                        <td><span class="department">İnşaat</span></td>
                                        <td>Şantiye Şefi</td>
                                        <td>ahmet@example.com</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `);
                break;

            case 'time-sheet':
                component = $(`
                    <div class="component time-sheet-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="table-container">
                            <table class="minimal-table time-sheet-table">
                                <thead>
                                    <tr>
                                        <th class="date">Tarih</th>
                                        <th class="hours">Giriş</th>
                                        <th class="hours">Çıkış</th>
                                        <th class="hours">Toplam</th>
                                        <th>Not</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>01.01.2024</td>
                                        <td>08:00</td>
                                        <td>17:00</td>
                                        <td>9 saat</td>
                                        <td>Normal mesai</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `);
                break;

            case 'leave-table':
                component = $(`
                    <div class="component leave-table-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="table-container">
                            <table class="minimal-table leave-table">
                                <thead>
                                    <tr>
                                        <th>Personel</th>
                                        <th>İzin Türü</th>
                                        <th>Başlangıç</th>
                                        <th>Bitiş</th>
                                        <th>Gün</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Ahmet Yılmaz</td>
                                        <td><span class="leave-type annual">Yıllık İzin</span></td>
                                        <td>01.01.2024</td>
                                        <td>15.01.2024</td>
                                        <td>15</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `);
                break;

            case 'income-expense':
                component = $(`
                    <div class="component income-expense-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="table-container">
                            <table class="minimal-table">
                                <thead>
                                    <tr>
                                        <th>Tarih</th>
                                        <th>Açıklama</th>
                                        <th>Gelir</th>
                                        <th>Gider</th>
                                        <th>Bakiye</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>01.01.2024</td>
                                        <td>Örnek İşlem</td>
                                        <td class="text-success">1.000,00 ₺</td>
                                        <td class="text-danger">500,00 ₺</td>
                                        <td class="text-primary">500,00 ₺</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `);
                break;

            case 'cash-status':
                component = $(`
                    <div class="component cash-status-component" draggable="true">
                        <div class="component-resize nw" data-direction="nw"></div>
                        <div class="component-resize ne" data-direction="ne"></div>
                        <div class="component-resize sw" data-direction="sw"></div>
                        <div class="component-resize se" data-direction="se"></div>
                        <div class="table-container">
                            <table class="minimal-table">
                                <thead>
                                    <tr>
                                        <th>Kasa</th>
                                        <th>Bakiye</th>
                                        <th>Son İşlem</th>
                                        <th>Durum</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Ana Kasa</td>
                                        <td class="text-primary">10.000,00 ₺</td>
                                        <td>01.01.2024</td>
                                        <td><span class="status completed">Aktif</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `);
                break;
        }

        container.append(component);
        
        if (type === 'text') {
            const editableText = component.find('.editable-text');
            
            // Tıklama olayı
            editableText.on('focus', function() {
                $(this).closest('.component').addClass('editing');
            }).on('blur', function() {
                $(this).closest('.component').removeClass('editing');
                
                // Boş ise placeholder'ı göster
                if ($(this).text().trim() === '') {
                    $(this).empty();
                }
            });
            
            // İlk metin komponentini otomatik olarak odakla
            if (container.find('.text-component').length === 1) {
                setTimeout(() => {
                    editableText.focus();
                }, 100);
            }
        }

        // Tabloları içeren tüm komponentler için
        if (component.find('.minimal-table').length) {
            // Tabloyu içeren komponenti genişliğe göre ayarla
            component.css({
                'width': '100%',
                'max-width': '100%',
                'overflow': 'hidden'
            });
            
            // Minimal tablo container'ı ayarla
            if (!component.find('.table-container').length) {
                // Tabloyu table-container içine al
                component.find('.minimal-table').wrap('<div class="table-container"></div>');
            }
            
            // Table container stillerini ayarla
            component.find('.table-container').css({
                'width': '100%',
                'max-width': '100%',
                'overflow-x': 'auto',
                'border': '1px solid #e9ecef',
                'border-radius': '4px'
            });
        }

        // div.minimal-table içindeki tabloları düzenle
        if (component.find('div.minimal-table').length) {
            // div içindeki tabloları işaretle
            component.find('div.minimal-table table').each(function() {
                // Eğer tablo minimal-table sınıfına sahip değilse ekle
                if (!$(this).hasClass('minimal-table')) {
                    $(this).addClass('minimal-table');
                }
                
                // Eğer tablo henüz bir table-container içinde değilse sar
                if (!$(this).parent('.table-container').length) {
                    $(this).wrap('<div class="table-container"></div>');
                }
            });
            
            // Tüm table-container'lara stil uygula
            component.find('.table-container').css({
                'width': '100%',
                'max-width': '100%',
                'overflow-x': 'auto',
                'border': '1px solid #e9ecef',
                'border-radius': '4px'
            });
        }
    }

    initProgressChart(container) {
        const options = {
            series: [{
                name: 'İlerleme',
                data: [30, 40, 35, 50, 49, 60, 70, 91]
            }],
            chart: {
                type: 'line',
                height: 300,
                toolbar: {
                    show: false
                }
            },
            colors: ['#007bff'],
            stroke: {
                curve: 'smooth',
                width: 2
            },
            grid: {
                borderColor: '#e9ecef',
                strokeDashArray: 4
            },
            xaxis: {
                categories: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos'],
                labels: {
                    style: {
                        colors: '#6c757d',
                        fontSize: '12px'
                    }
                }
            },
            yaxis: {
                labels: {
                    style: {
                        colors: '#6c757d',
                        fontSize: '12px'
                    }
                }
            },
            tooltip: {
                theme: 'light',
                style: {
                    fontSize: '12px'
                }
            }
        };

        const chart = new ApexCharts(container[0], options);
        chart.render();
    }

    /**
     * Proje özeti komponentini PDF için özel olarak stillendirir
     * PDF oluşturma fonksiyonlarındaki onclone callback'inden çağrılır
     * @param {Document} clonedDoc - HTML2PDF tarafından klonlanan döküman
     */
    styleProjeOzetiForPDF(clonedDoc) {
        // JQuery varsa kullan, yoksa document API'sini kullan
        const $ = window.jQuery || null;
        
        if ($) {
            // Proje özeti kartlarını bul ve optimize et
            $(clonedDoc).find('.report-card[data-type="proje-ozeti"]').each(function() {
                // Proje özeti kartını daha küçük ve minimal hale getir
                const projeOzeti = $(this);
                
                // İç grid yapısını düzenle
                projeOzeti.find('.report-charts, .card-body[data-columns]').css({
                    'display': 'grid',
                    'grid-template-columns': 'repeat(12, 1fr)',
                    'gap': '10px', // Daha dar boşluk
                    'padding': '5px', // Daha küçük padding
                    'margin-bottom': '10px'
                });
                
                // Chart kartlarını ölçeklendir ve düzenle
                projeOzeti.find('.report-card').css({
                    'grid-column': 'span 4', // Tüm kartları 3 sütunda (12/3 = 4) göster
                    'padding': '5px',
                    'margin-bottom': '5px',
                    'box-shadow': 'none',
                    'border': '1px solid #eaeaea'
                });
                
                // Chart başlıklarını daha küçük ve öz hale getir
                projeOzeti.find('.card-header').css({
                    'padding': '5px',
                    'font-size': '10px',
                    'font-weight': 'bold',
                    'border-bottom': '1px solid #eaeaea'
                });
                
                // Chart ölçeklerini düşür, boyutları küçült
                projeOzeti.find('.chart-container, .apexcharts-canvas').css({
                    'max-height': '150px', // Daha küçük grafikler
                    'overflow': 'hidden'
                });
                
                // ApexCharts küçültme
                projeOzeti.find('.apexcharts-title-text').css('font-size', '10px');
                projeOzeti.find('.apexcharts-legend-text').css('font-size', '8px');
                projeOzeti.find('.apexcharts-yaxis-label, .apexcharts-xaxis-label').css('font-size', '8px');
                
                // Gereksiz bölümleri kaldır
                projeOzeti.find('.apexcharts-toolbar, .apexcharts-menu-icon').hide();
            });
        } else {
            // JQuery yoksa vanilla JavaScript kullan
            const projeOzetiCards = clonedDoc.querySelectorAll('.report-card[data-type="proje-ozeti"]');
            projeOzetiCards.forEach(function(card) {
                // Grid yapılarını düzenle
                const gridContainers = card.querySelectorAll('.report-charts, .card-body[data-columns]');
                gridContainers.forEach(function(container) {
                    container.style.display = 'grid';
                    container.style.gridTemplateColumns = 'repeat(12, 1fr)';
                    container.style.gap = '10px';
                    container.style.padding = '5px';
                    container.style.marginBottom = '10px';
                });
                
                // İç kartları düzenle
                const childCards = card.querySelectorAll('.report-card');
                childCards.forEach(function(childCard) {
                    childCard.style.gridColumn = 'span 4';
                    childCard.style.padding = '5px';
                    childCard.style.marginBottom = '5px';
                    childCard.style.boxShadow = 'none';
                    childCard.style.border = '1px solid #eaeaea';
                });
                
                // Card başlıklarını düzenle
                const headers = card.querySelectorAll('.card-header');
                headers.forEach(function(header) {
                    header.style.padding = '5px';
                    header.style.fontSize = '10px';
                    header.style.fontWeight = 'bold';
                    header.style.borderBottom = '1px solid #eaeaea';
                });
                
                // Chart konteynerlerini düzenle
                const chartContainers = card.querySelectorAll('.chart-container, .apexcharts-canvas');
                chartContainers.forEach(function(chart) {
                    chart.style.maxHeight = '150px';
                    chart.style.overflow = 'hidden';
                });
                
                // ApexCharts elemanlarını düzenle
                const titleTexts = card.querySelectorAll('.apexcharts-title-text');
                titleTexts.forEach(function(text) {
                    text.style.fontSize = '10px';
                });
                
                const legendTexts = card.querySelectorAll('.apexcharts-legend-text');
                legendTexts.forEach(function(text) {
                    text.style.fontSize = '8px';
                });
                
                const axisLabels = card.querySelectorAll('.apexcharts-yaxis-label, .apexcharts-xaxis-label');
                axisLabels.forEach(function(label) {
                    label.style.fontSize = '8px';
                });
                
                // Toolbar elemanlarını gizle
                const toolbars = card.querySelectorAll('.apexcharts-toolbar, .apexcharts-menu-icon');
                toolbars.forEach(function(toolbar) {
                    toolbar.style.display = 'none';
                });
            });
        }
    }

    loadTemplate(templateId) {
        // Şablon yükleme işlemleri
        console.log('Şablon yükleniyor:', templateId);
        
        // Tüm şablonları temizle ve seçilen şablonu işaretle
        $('.template-item').removeClass('active selected');
        $(`.template-item[data-template="${templateId}"]`).addClass('active selected');
        
        let templateHTML = '';
        
        // Şablon türüne göre HTML oluştur
        switch(templateId) {
            case 'bos':
            case 'empty':
                // Boş şablon - minimal içerik
                templateHTML = `
                    <div class="report-row">
                        <div class="report-column">
                            <div class="report-component">
                                <h1 class="editable" contenteditable="true">Yeni Rapor</h1>
                                <p class="editable" contenteditable="true">Raporunuzun içeriğini buraya ekleyin.</p>
                            </div>
                        </div>
                    </div>
                `;
                break;
                
            case 'proje':
            case 'project':
                // Proje raporu şablonu - A4 formatına uygun minimal tasarım
                templateHTML = `
                    <div class="report-row">
                        <div class="report-column">
                            <div class="report-card" data-type="proje-ozeti" data-size="full">
                                <div class="card-header">
                                    <div class="card-title">
                                        <i class="fas fa-project-diagram"></i>
                                        Proje Özeti
                                    </div>
                                    <div class="card-actions">
                                        <button class="card-action-btn remove" title="Sil">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                                <div class="card-body" data-columns="3">
                                    <!-- Proje durumu -->
                                    <div class="report-card" data-size="medium">
                                        <div class="card-header">
                                            <div class="card-title">Proje Durumu</div>
                                        </div>
                                        <div class="card-body">
                                            <div class="chart-container" style="height: 150px;"></div>
                                        </div>
                                    </div>
                                    
                                    <!-- Görev dağılımı -->
                                    <div class="report-card" data-size="medium">
                                        <div class="card-header">
                                            <div class="card-title">Görev Dağılımı</div>
                                        </div>
                                        <div class="card-body">
                                            <div class="chart-container" style="height: 150px;"></div>
                                        </div>
                                    </div>
                                    
                                    <!-- Zaman planı -->
                                    <div class="report-card" data-size="medium">
                                        <div class="card-header">
                                            <div class="card-title">Zaman Planı</div>
                                        </div>
                                        <div class="card-body">
                                            <div class="chart-container" style="height: 150px;"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="report-row">
                        <div class="report-column">
                            <div class="report-component">
                                <table class="minimal-table">
                                    <thead>
                                        <tr>
                                            <th style="width: 5%;">#</th>
                                            <th style="width: 25%;">İş Paketi</th>
                                            <th style="width: 15%;">Sorumlu</th>
                                            <th style="width: 10%;">Başlangıç</th>
                                            <th style="width: 10%;">Bitiş</th>
                                            <th style="width: 10%;">Durum</th>
                                            <th style="width: 25%;">Not</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>1</td>
                                            <td>Temel İş Paketi</td>
                                            <td>Ahmet Yılmaz</td>
                                            <td>01.06.2023</td>
                                            <td>15.06.2023</td>
                                            <td>Tamamlandı</td>
                                            <td>İş paketi zamanında tamamlandı</td>
                                        </tr>
                                        <tr>
                                            <td>2</td>
                                            <td>İkinci İş Paketi</td>
                                            <td>Mehmet Demir</td>
                                            <td>16.06.2023</td>
                                            <td>30.06.2023</td>
                                            <td>Devam Ediyor</td>
                                            <td>İş paketi üzerinde çalışılıyor</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                `;
                break;
                
            case 'finansal':
            case 'financial':
                // Finansal rapor şablonu
                templateHTML = `
                    <div class="report-row">
                        <div class="report-column">
                            <div class="report-component">
                                <h1 class="editable" contenteditable="true">Finansal Rapor</h1>
                                <p class="editable" contenteditable="true">Finansal durum özeti</p>
                            </div>
                        </div>
                    </div>
                    <div class="report-row">
                        <div class="report-column">
                            <div class="report-card" data-size="medium">
                                <div class="card-header">
                                    <div class="card-title">
                                        <i class="fas fa-chart-line"></i>
                                        Gelir/Gider Analizi
                                    </div>
                                </div>
                                <div class="card-body">
                                    <div class="chart-container" style="height: 200px;"></div>
                                </div>
                            </div>
                        </div>
                        <div class="report-column">
                            <div class="report-card" data-size="medium">
                                <div class="card-header">
                                    <div class="card-title">
                                        <i class="fas fa-chart-pie"></i>
                                        Harcama Dağılımı
                                    </div>
                                </div>
                                <div class="card-body">
                                    <div class="chart-container" style="height: 200px;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                break;
                
            default:
                console.error(`Bilinmeyen şablon: ${templateId}`);
                return;
        }
        
        // Şablonu sayfaya uygula
        $('#reportPreview').html(templateHTML);
        
        // Özel olay tetikle
        document.dispatchEvent(new CustomEvent('templateLoaded', { 
            detail: { templateId: templateId } 
        }));
        
        // Kartları yeniden düzenle
        if (typeof organizeReportCards === 'function') {
            setTimeout(organizeReportCards, 200);
        }
        
        // Proje özeti kartlarını kontrol et
        if (typeof showProjeOzetiCards === 'function') {
            setTimeout(function() {
                const projeOzetiCards = document.querySelectorAll('.report-card[data-type="proje-ozeti"]');
                projeOzetiCards.forEach(showProjeOzetiCards);
            }, 300);
        }
    }
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.controlManager = new ControlManager();
}); 