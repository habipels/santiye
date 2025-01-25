class ApprovalList {
    constructor() {
        this.init();
    }

    init() {
        this.initDataTable();
        this.bindEvents();
    }

    initDataTable() {
        this.table = $('#approvalList').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/tr.json'
            },
            dom: '<"top"Bf>rt<"bottom"lip>',
            buttons: [
                {
                    text: '<i class="fa-solid fa-file-export"></i> Seçilenleri Dışa Aktar',
                    className: 'button',
                    action: () => this.exportSelected()
                }
            ],
            order: [[4, 'desc']], // Tarihe göre sırala
            pageLength: 10,
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "Tümü"]],
            responsive: true
        });

        // Tüm satırları seçme/seçimi kaldırma
        $('#selectAll').on('change', (e) => {
            $('.row-checkbox').prop('checked', $(e.target).is(':checked'));
        });
    }

    bindEvents() {
        // Onay/Red butonları
        $(document).on('click', '[data-action="approve"]', (e) => {
            this.showApprovalModal('approve', $(e.currentTarget).closest('tr'));
        });

        $(document).on('click', '[data-action="reject"]', (e) => {
            this.showApprovalModal('reject', $(e.currentTarget).closest('tr'));
        });

        // Modal kapatma
        $(document).on('click', '[data-action="close-modal"]', () => {
            this.closeModal();
        });

        // Onay işlemi
        $('#confirmApproval').on('click', () => {
            this.processApproval();
        });
    }

    showApprovalModal(action, row) {
        this.currentAction = action;
        this.currentRow = row;

        const modalTitle = action === 'approve' ? 'Onay İşlemi' : 'Red İşlemi';
        const buttonText = action === 'approve' ? 'Onayla' : 'Red Et';
        const buttonClass = action === 'approve' ? 'button-primary' : 'button-danger';

        $('#approvalModal .modal-header h3').text(modalTitle);
        $('#confirmApproval').text(buttonText).removeClass().addClass(`button ${buttonClass}`);
        
        $('#approvalPassword').val('');
        $('#approvalNote').val('');
        
        $('#approvalModal').addClass('active');
    }

    closeModal() {
        $('#approvalModal').removeClass('active');
    }

    processApproval() {
        const password = $('#approvalPassword').val();
        const note = $('#approvalNote').val();

        if (!password) {
            alert('Lütfen onay şifrenizi girin!');
            return;
        }

        // API'ye gönderilecek veriler
        const data = {
            action: this.currentAction,
            password: password,
            note: note,
            checklistId: this.currentRow.find('td:first').text()
        };

        console.log('İşlem verileri:', data);

        // Başarılı işlem simülasyonu
        this.updateRowStatus(this.currentAction);
        this.closeModal();
    }

    updateRowStatus(action) {
        const statusCell = this.currentRow.find('.approval-status');
        const badge = statusCell.find('.approval-badge');
        
        if (action === 'approve') {
            badge.removeClass('pending').addClass('approved')
                .html('<i class="fa-solid fa-check"></i> Onaylandı');
        } else {
            badge.removeClass('pending').addClass('rejected')
                .html('<i class="fa-solid fa-xmark"></i> Red Edildi');
        }

        // Butonları devre dışı bırak
        this.currentRow.find('.table-actions button').prop('disabled', true);
    }

    exportSelected() {
        const selectedRows = $('.row-checkbox:checked').closest('tr');
        
        if (selectedRows.length === 0) {
            alert('Lütfen dışa aktarmak için en az bir kayıt seçin!');
            return;
        }

        const data = [];
        selectedRows.each((i, row) => {
            const $row = $(row);
            data.push({
                controlNo: $row.find('td:eq(1)').text(),
                block: $row.find('td:eq(2)').text(),
                section: $row.find('td:eq(3)').text(),
                date: $row.find('td:eq(4)').text(),
                inspector: $row.find('td:eq(5)').text(),
                status: $row.find('td:eq(6)').text(),
                progress: $row.find('td:eq(7)').find('span').text(),
                approvalStatus: $row.find('.approval-badge').text()
            });
        });

        // PDF oluştur
        const docDefinition = {
            content: [
                { text: 'Kontrol Listesi Raporu', style: 'header' },
                { text: `Oluşturma Tarihi: ${new Date().toLocaleDateString('tr-TR')}`, style: 'subheader' },
                {
                    table: {
                        headerRows: 1,
                        widths: ['auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto'],
                        body: [
                            ['Kontrol No', 'Blok', 'Bölüm', 'Tarih', 'Kontrol Eden', 'Durum', 'İlerleme', 'Onay Durumu'],
                            ...data.map(item => [
                                item.controlNo,
                                item.block,
                                item.section,
                                item.date,
                                item.inspector,
                                item.status,
                                item.progress,
                                item.approvalStatus
                            ])
                        ]
                    }
                }
            ],
            styles: {
                header: {
                    fontSize: 18,
                    bold: true,
                    margin: [0, 0, 0, 10]
                },
                subheader: {
                    fontSize: 14,
                    bold: true,
                    margin: [0, 0, 0, 20]
                }
            }
        };

        pdfMake.createPdf(docDefinition).download('kontrol-listesi-raporu.pdf');
    }
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.approvalList = new ApprovalList();
}); 