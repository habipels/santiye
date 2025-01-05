class ControlManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.initSections();
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
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.controlManager = new ControlManager();
}); 