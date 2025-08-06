class TemplateManager {
    constructor() {
        this.workGroups = []; // İş Grupları
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateWorkGroupSelects();
    }

    bindEvents() {
        // Bölüm ekleme
        $(document).on('click', '#addStructureSection', () => this.addStructureSection());

        // Kategori ve kontrol maddesi ekleme
        $(document).on('click', '.add-category-btn', (e) => this.addCategory(e));
        $(document).on('click', '.add-checklist-item', (e) => this.addChecklistItem(e));

        // Silme işlemleri
        $(document).on('click', '.remove-section', (e) => this.removeSection(e.target));
        $(document).on('click', '.remove-category', (e) => this.removeCategory(e.target));
        $(document).on('click', '.remove-item', (e) => this.removeChecklistItem(e.target));

        // Toggle işlemleri
        $(document).on('click', '.toggle-section', (e) => this.toggleSection(e.target));
        $(document).on('click', '.toggle-category', (e) => this.toggleCategory(e.target));

        // Şablon işlemleri
        $(document).on('click', '#saveTemplate', () => this.saveTemplate());

        // İş Grubu işlemleri
        $('#addWorkGroup').on('click', () => {
            this.addWorkGroup();
            this.updateWorkGroupSelects();
        });
        $(document).on('click', '[data-action="remove"]', (e) => {
            $(e.target).closest('.work-group-item').remove();
            this.updateWorkGroupSelects();
        });
        $(document).on('input', '.work-group-item input', () => this.updateWorkGroupSelects());
    }

    addStructureSection() {
        const sectionHtml = `
            <div class="card section-card">
                <div class="card-header">
                    <div class="card-title">
                        <select class="form-control section-type">
                            <option value="0">Dış Mekan</option>
                            <option value="1">Kat</option>
                            <option value="2">Ortak Alan</option>
                            <option value="3">Daire</option>
                        </select>
                    </div>
                    <div class="card-actions">
                        <button type="button" class="button-icon toggle-section">
                            <i class="icon icon-chevron-down"></i>
                        </button>
                        <button type="button" class="button-icon remove-section">
                            <i class="icon icon-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="categories-list">
                        <button type="button" class="button button-dashed add-category-btn">
                            <i class="icon icon-plus"></i> Yeni İmalat Ekle
                        </button>
                    </div>
                </div>
            </div>
        `;
        $('#structureSections').append(sectionHtml);
    }

    addCategory(event) {
        const categoryHtml = `
            <div class="category-item">
                <div class="category-header">
                    <input type="text" name="imalat_kalemleri" class="form-control" placeholder="İmalat kategorisi adı...">
                    <select name="is_gurubu_imalat_kaleminin" class="form-control work-group-select">
                        <option value="">İş Grubu Seçin</option>
                        ${this.workGroups.map(group => `<option value="${group}">${group}</option>`).join('')}
                    </select>
                    <div class="category-actions">
                        <button type="button" class="button-icon toggle-category">
                            <i class="fa-solid fa-chevron-down"></i>
                        </button>
                        <button type="button" class="button-icon remove-category">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="category-content">
                    <div class="checklist-items"></div>
                    <button type="button" class="button button-dashed add-checklist-item">
                        <i class="fa-solid fa-plus"></i> Kontrol Maddesi Ekle
                    </button>
                </div>
            </div>
        `;
        $(event.target).closest('.categories-list').find('.add-category-btn').before(categoryHtml);
    }

    addChecklistItem(event) {
        const itemHtml = `
            <div class="checklist-item">
                <input type="text" class="form-control" placeholder="Kontrol maddesi">
                <button type="button" class="button-icon remove-item">
                    <i class="icon icon-trash"></i>
                </button>
            </div>
        `;
        $(event.target).closest('.category-content').find('.checklist-items').append(itemHtml);
    }

    toggleSection(button) {
        $(button).closest('.section-card').find('.card-body').slideToggle();
    }

    toggleCategory(button) {
        $(button).closest('.category-item').find('.category-content').slideToggle();
    }

    removeSection(button) {
        if (confirm('Bu bölümü silmek istediğinize emin misiniz?')) {
            $(button).closest('.section-card').remove();
        }
    }

    removeCategory(button) {
        if (confirm('Bu imalatı silmek istediğinize emin misiniz?')) {
            $(button).closest('.category-item').remove();
        }
    }

    removeChecklistItem(button) {
        $(button).closest('.checklist-item').remove();
    }

    saveTemplate() {
        const template = {
            santiyeId: $('#santiye').val(),
            name: $('#templateName').val(),
            projectType: $('#projectType').val(),
            sections: this.getSectionsData()
        };

        $.ajax({
            url: '/createsiteprojectsablone/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(template),
            success: (response) => {
                alert('Şablon başarıyla kaydedildi!');
            },
            error: (xhr, status, error) => {
                alert('Şablon kaydedilirken bir hata oluştu.');
            }
        });
    }

    getSectionsData() {
        const sections = [];
        $('.section-card').each((i, el) => {
            const section = {
                type: $(el).find('.section-type').val(),
                categories: this.getSectionCategories($(el))
            };
            sections.push(section);
        });
        return sections;
    }

    getSectionCategories(section) {
        const categories = [];
        section.find('.category-item').each((i, el) => {
            const category = {
                name: $(el).find('input[name="imalat_kalemleri"]').val(),
                workGroup: $(el).find('select[name="is_gurubu_imalat_kaleminin"]').val(),
                checklistItems: this.getChecklistItems($(el))
            };
            categories.push(category);
        });
        return categories;
    }

    getChecklistItems(category) {
        const items = [];
        category.find('.checklist-items .checklist-item input').each((i, input) => {
            items.push($(input).val());
        });
        return items;
    }

    addWorkGroup() {
        const workGroupHtml = `
            <div class="work-group-item">
                <input name="is_grubu" type="text" class="form-control" placeholder="İş grubu adı...">
                <button type="button" class="button-icon" data-action="remove">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        `;
        $('#workGroupsList').append(workGroupHtml);
    }

    updateWorkGroupSelects() {
        this.workGroups = [];
        $('.work-group-item input').each((i, input) => {
            const name = $(input).val().trim();
            if (name) this.workGroups.push(name);
        });

        $('.work-group-select').each((i, select) => {
            const $select = $(select);
            const currentValue = $select.val();

            $select.empty();
            $select.append('<option value="">İş Grubu Seçin</option>');
            this.workGroups.forEach(group => {
                $select.append(`<option value="${group}">${group}</option>`);
            });

            if (currentValue && this.workGroups.includes(currentValue)) {
                $select.val(currentValue);
            }
        });
    }
}

// Sayfa yüklendiğinde başlat
$(document).ready(() => {
    window.templateManager = new TemplateManager();
});
