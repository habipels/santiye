class ReportManager {
    constructor() {
        this.init();
        this.bindEvents();
    }

    init() {
        // Tarih seçici
        this.initDatePicker();
        
        // Sürükle-bırak
        this.initDragAndDrop();
        
        // Şablon seçimi
        this.initTemplates();
    }

    initDatePicker() {
        $('#dateRange').daterangepicker({
            opens: 'left',
            locale: {
                format: 'DD.MM.YYYY',
                separator: ' - ',
                applyLabel: 'Uygula',
                cancelLabel: 'İptal',
                daysOfWeek: ['Pz', 'Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct'],
                monthNames: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                    'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
                firstDay: 1
            },
            startDate: moment().startOf('month'),
            endDate: moment().endOf('month')
        }, (start, end) => {
            $('#reportDateRange').text(start.format('DD.MM.YYYY') + ' - ' + end.format('DD.MM.YYYY'));
        });
    }

    initDragAndDrop() {
        $('.component-item').draggable({
            helper: 'clone',
            appendTo: 'body',
            zIndex: 1000,
            cursor: 'move'
        });

        this.initializeDropZones();
    }

    initializeDropZones() {
        $('.drop-zone').droppable({
            accept: '.component-item',
            hoverClass: 'drop-hover',
            drop: (event, ui) => {
                const type = $(ui.draggable).data('type');
                const component = this.createComponent(type);
                if (component) {
                    $(event.target).replaceWith(component);
                }
            }
        });
    }

    initTemplates() {
        $('.template-item').click((e) => {
            const templateType = $(e.currentTarget).data('template');
            
            $('.template-item').removeClass('selected');
            $(e.currentTarget).addClass('selected');
            
            this.loadTemplate(templateType);
        });
    }

    loadTemplate(type) {
        let template = '';
        
        switch(type) {
            case 'bos':
                template = `
                    <div class="report-card" data-size="full">
                        <div class="drop-zone">
                            <span class="drop-text">Bileşen eklemek için sürükleyin</span>
                        </div>
                    </div>
                `;
                break;
                
            case 'finansal':
                template = `
                    <div class="report-content">
                        <div class="report-card" data-size="medium">
                            <div class="drop-zone">
                                <span class="drop-text">Gelir/Gider grafiği</span>
                            </div>
                        </div>
                        <div class="report-card" data-size="medium">
                            <div class="drop-zone">
                                <span class="drop-text">Kasa durumu</span>
                            </div>
                        </div>
                        <div class="report-card" data-size="medium">
                            <div class="drop-zone">
                                <span class="drop-text">Bütçe analizi</span>
                            </div>
                        </div>
                        <div class="report-card" data-size="medium">
                            <div class="drop-zone">
                                <span class="drop-text">Tahsilat durumu</span>
                            </div>
                        </div>
                        <div class="report-card" data-size="full">
                            <div class="drop-zone">
                                <span class="drop-text">Finansal tablo</span>
                            </div>
                        </div>
                    </div>
                `;
                break;
                
            case 'proje':
                template = `
                    <div class="report-content">
                        <div class="report-card" data-size="large">
                            <div class="drop-zone">
                                <span class="drop-text">Proje durumu</span>
                            </div>
                        </div>
                        <div class="report-card" data-size="small">
                            <div class="drop-zone">
                                <span class="drop-text">Görev dağılımı</span>
                            </div>
                        </div>
                        <div class="report-card" data-size="medium">
                            <div class="drop-zone">
                                <span class="drop-text">Zaman çizelgesi</span>
                            </div>
                        </div>
                        <div class="report-card" data-size="medium">
                            <div class="drop-zone">
                                <span class="drop-text">Kilometre taşları</span>
                            </div>
                        </div>
                    </div>
                `;
                break;
        }
        
        $('#reportPreview').html(template);
        this.initializeDropZones();
    }

    showPdfPreview() {
        const modal = document.getElementById('pdfPreviewModal');
        const pdfPreviewFrame = document.getElementById('pdfPreviewFrame');
        modal.classList.add('active');

        // Loading göster
        const loadingEl = $('<div class="loading">PDF oluşturuluyor...</div>');
        $(pdfPreviewFrame).parent().append(loadingEl);

        // PDF ayarları
        const opt = {
            margin: 0,
            filename: 'rapor.pdf',
            image: { type: 'jpeg', quality: 1 },
            html2canvas: { 
                scale: 2,
                useCORS: true,
                allowTaint: true,
                scrollY: 0
            },
            jsPDF: { 
                unit: 'mm', 
                format: 'a4',
                orientation: 'portrait'
            }
        };

        // Gereksiz elementleri gizle
        $('.card-actions, .component-controls, .report-topbar, .report-sidebar').hide();

        // PDF oluştur
        html2pdf()
            .from(document.querySelector('.preview-container'))
            .set(opt)
            .outputPdf('datauristring')
            .then(uri => {
                // Gizlenen elementleri geri göster
                $('.card-actions, .component-controls, .report-topbar, .report-sidebar').show();
                
                pdfPreviewFrame.src = uri;
                loadingEl.remove();
            })
            .catch(err => {
                // Hata durumunda da gizlenen elementleri geri göster
                $('.card-actions, .component-controls, .report-topbar, .report-sidebar').show();
                
                console.error('PDF oluşturma hatası:', err);
                loadingEl.text('PDF oluşturulurken bir hata oluştu');
            });
    }

    exportToPDF() {
        const element = document.querySelector('.preview-container');
        const paperSize = $('#paperSize').val() || 'a4';
        const orientation = $('input[name="orientation"]:checked').val() || 'portrait';

        // PDF ayarları (showPdfPreview ile aynı ayarları kullan)
        const opt = {
            margin: [10, 10, 10, 10],
            filename: `${this.currentReport?.name || 'rapor'}.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { 
                scale: 2,
                useCORS: true,
                logging: false,
                onclone: function(clonedDoc) {
                    // showPdfPreview'daki aynı DOM düzenlemeleri
                    $(clonedDoc).find('.card-actions, .component-controls').remove();
                    
                    $(clonedDoc).find('.preview-header').css({
                        'margin-bottom': '20mm',
                        'text-align': 'center',
                        'border-bottom': '1px solid #E2E8F0',
                        'padding-bottom': '10mm'
                    });

                    $(clonedDoc).find('.report-logo img').css({
                        'height': '30mm',
                        'width': 'auto'
                    });

                    $(clonedDoc).find('.preview-title').css({
                        'font-size': '24px',
                        'font-weight': 'bold',
                        'margin-bottom': '8px',
                        'color': '#052941'
                    });

                    $(clonedDoc).find('.preview-subtitle').css({
                        'font-size': '14px',
                        'color': '#64748B'
                    });

                    $(clonedDoc).find('.report-card').css({
                        'page-break-inside': 'avoid',
                        'margin-bottom': '15mm'
                    });
                }
            },
            jsPDF: { 
                unit: 'mm', 
                format: paperSize,
                orientation: orientation
            }
        };

        // Loading göster
        const loadingEl = $('<div class="loading-overlay"><div class="loading">PDF indiriliyor...</div></div>');
        $('body').append(loadingEl);

        // PDF'yi oluştur ve indir
        html2pdf().set(opt).from(element).save().then(() => {
            loadingEl.remove();
            this.showNotification('PDF başarıyla indirildi');
            closePdfPreview();
        }).catch(err => {
            console.error('PDF indirme hatası:', err);
            loadingEl.remove();
            this.showNotification('PDF oluşturulurken bir hata oluştu', 'error');
        });
    }

    bindEvents() {
        // PDF export
        $('#exportPDFBtn').click(() => this.showPdfPreview());
        
        // Proje seçimi
        $('#projectSelect').change(() => {
            const projectName = $('#projectSelect option:selected').text();
            $('#reportProject').text(projectName || 'Tüm Projeler');
        });

        // Yeni event'ler
        $('.action-btn[title="Temizle"]').click(() => this.showClearConfirm());
        $('.action-btn[title="Kaydet"]').click(() => this.showSaveForm());
    }

    showClearConfirm() {
        const modal = $(`
            <div class="modal confirm-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>Raporu Temizle</h3>
                        <button class="modal-close" onclick="$(this).closest('.modal').remove()">
                            <i class="icon icon-close"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>Raporu temizlemek istediğinize emin misiniz?</p>
                        <p>Bu işlem geri alınamaz.</p>
                    </div>
                    <div class="modal-footer">
                        <button class="button" onclick="$(this).closest('.modal').remove()">İptal</button>
                        <button class="button button-primary" onclick="window.reportManager.clearReport()">Temizle</button>
                    </div>
                </div>
            </div>
        `);

        $('body').append(modal);
        modal.addClass('active');
    }

    clearReport() {
        // Rapor içeriğini temizle
        $('#reportPreview').html(`
            <div class="drop-zone" data-size="full">
                <span class="drop-text">Bileşen eklemek için sürükleyin</span>
            </div>
        `);

        // Drop zone'ları yeniden aktifleştir
        this.initializeDropZones();

        // Modalı kapat
        $('.confirm-modal').remove();

        // Bildirim göster
        this.showNotification('Rapor temizlendi');
    }

    showSaveForm() {
        const modal = $(`
            <div class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>Raporu Kaydet</h3>
                        <button class="modal-close" onclick="$(this).closest('.modal').remove()">
                            <i class="icon icon-close"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label>Rapor Adı</label>
                            <input type="text" class="form-control" id="reportName" value="${this.currentReport?.name || ''}">
                        </div>
                        <div class="form-group">
                            <label>Açıklama</label>
                            <textarea class="form-control" id="reportDescription">${this.currentReport?.description || ''}</textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="button" onclick="$(this).closest('.modal').remove()">İptal</button>
                        <button class="button button-primary" onclick="window.reportManager.saveReport()">Kaydet</button>
                    </div>
                </div>
            </div>
        `);

        $('body').append(modal);
        modal.addClass('active');
    }

    async saveReport() {
        const name = $('#reportName').val();
        const description = $('#reportDescription').val();

        if (!name) {
            alert('Lütfen rapor adı giriniz');
            return;
        }

        // Rapor verilerini hazırla
        const reportData = {
            name,
            description,
            content: $('#reportPreview').html(),
            dateRange: {
                start: $('#dateRange').data('daterangepicker').startDate.format('YYYY-MM-DD'),
                end: $('#dateRange').data('daterangepicker').endDate.format('YYYY-MM-DD')
            },
            project: $('#projectSelect').val(),
            updatedAt: new Date().toISOString()
        };

        try {
            // API'ye gönder (örnek)
            // const response = await fetch('/api/reports', {
            //     method: 'POST',
            //     headers: { 'Content-Type': 'application/json' },
            //     body: JSON.stringify(reportData)
            // });

            // Başarılı
            this.currentReport = reportData;
            $('.modal').remove();
            this.showNotification('Rapor başarıyla kaydedildi');

        } catch (error) {
            console.error('Rapor kaydetme hatası:', error);
            alert('Rapor kaydedilirken bir hata oluştu');
        }
    }

    showNotification(message) {
        const notification = $(`
            <div class="notification">
                <i class="icon icon-check"></i>
                <span>${message}</span>
            </div>
        `);

        $('body').append(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    createComponent(type) {
        let component;
        
        switch(type) {
            case 'gelir-gider':
                component = $(`
                    <div class="report-card" data-size="medium">
                        <div class="card-header">
                            <div class="card-title">
                                <i class="icon icon-chart"></i>
                                Gelir/Gider Analizi
                            </div>
                            <div class="card-actions">
                                <button class="card-action-btn size-down" title="Küçült">
                                    <i class="icon icon-minus"></i>
                                </button>
                                <button class="card-action-btn size-up" title="Büyült">
                                    <i class="icon icon-plus"></i>
                                </button>
                                <button class="card-action-btn remove" title="Sil">
                                    <i class="icon icon-trash"></i>
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="gelirGiderChart"></div>
                        </div>
                    </div>
                `);
                
                setTimeout(() => {
                    new ApexCharts(component.find('#gelirGiderChart')[0], {
                        series: [{
                            name: 'Gelir',
                            data: [150000, 142000, 165000, 178000, 195000, 188000]
                        }, {
                            name: 'Gider',
                            data: [120000, 115000, 130000, 148000, 150000, 145000]
                        }],
                        chart: {
                            type: 'area',
                            height: 250,
                            toolbar: { show: false }
                        },
                        colors: ['#22D6B5', '#FF4560'],
                        fill: {
                            type: 'gradient',
                            gradient: {
                                shadeIntensity: 1,
                                opacityFrom: 0.7,
                                opacityTo: 0.2
                            }
                        },
                        dataLabels: { enabled: false },
                        stroke: { curve: 'smooth', width: 2 },
                        xaxis: {
                            categories: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran']
                        }
                    }).render();
                }, 100);
                break;

            case 'kasa-durumu':
                component = $(`
                    <div class="report-card" data-size="small">
                        <div class="card-header">
                            <div class="card-title">
                                <i class="icon icon-wallet"></i>
                                Kasa Durumu
                            </div>
                            <div class="card-actions">
                                <button class="card-action-btn size-down" title="Küçült">
                                    <i class="icon icon-minus"></i>
                                </button>
                                <button class="card-action-btn size-up" title="Büyült">
                                    <i class="icon icon-plus"></i>
                                </button>
                                <button class="card-action-btn remove" title="Sil">
                                    <i class="icon icon-trash"></i>
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="stat-value">₺1.250.000</div>
                            <div class="stat-label">Toplam Bakiye</div>
                            <div class="trend trend-up">
                                <i class="icon icon-trending-up"></i>
                                <span>%12.5 artış</span>
                            </div>
                        </div>
                    </div>
                `);
                break;
                
            // Diğer komponentler...
        }
        
        if (component) {
            // Boyutlandırma işlevselliği
            component.find('.size-up, .size-down').click(function() {
                const card = $(this).closest('.report-card');
                const sizes = ['small', 'medium', 'large', 'full'];
                const currentSize = card.attr('data-size') || 'medium';
                const currentIndex = sizes.indexOf(currentSize);
                
                if ($(this).hasClass('size-up') && currentIndex < sizes.length - 1) {
                    card.attr('data-size', sizes[currentIndex + 1]);
                } else if ($(this).hasClass('size-down') && currentIndex > 0) {
                    card.attr('data-size', sizes[currentIndex - 1]);
                }
            });

            // Silme işlevselliği
            component.find('.remove').click(function() {
                const card = $(this).closest('.report-card');
                card.remove();
            });
        }
        
        return component;
    }
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.reportManager = new ReportManager();
});

// Modal fonksiyonları
function closePdfPreview() {
    document.getElementById('pdfPreviewModal').classList.remove('active');
}

function openPageSettings() {
    document.getElementById('pageSettingsModal').classList.add('active');
}

function closePageSettings() {
    document.getElementById('pageSettingsModal').classList.remove('active');
}

function savePageSettings() {
    // Kenar boşlukları
    const margins = {
        top: $('.margin-control[data-margin="top"]').val(),
        right: $('.margin-control[data-margin="right"]').val(),
        bottom: $('.margin-control[data-margin="bottom"]').val(),
        left: $('.margin-control[data-margin="left"]').val()
    };
    
    // Kağıt ayarları
    const paperSize = $('#paperSize').val();
    const orientation = $('input[name="orientation"]:checked').val();
    
    // Ayarları uygula
    Object.entries(margins).forEach(([margin, value]) => {
        $('.preview-container').css(`padding-${margin}`, value + 'mm');
    });

    closePageSettings();
} 