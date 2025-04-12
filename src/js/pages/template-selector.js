// Şablon yapıları için temel bir yapı

// Şablon seçici JS

// Şablon verisi
const templates = [
    {
        id: 'bos',
        layout: 'empty'
    },
    {
        id: 'finansal',
        layout: 'financial'
    }
];

// Şablon seçme fonksiyonu
function selectTemplate(templateId) {
    console.log('Şablon seçildi:', templateId);
    
    // Aktif şablonu işaretle
    document.querySelectorAll('.template-item').forEach(item => {
        if (item.getAttribute('data-template') === templateId) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
    
    // Şablonu html sayfasındaki loadTemplate fonksiyonu ile yükle
    if (typeof loadTemplate === 'function') {
        loadTemplate(templateId);
    } else {
        console.error('loadTemplate fonksiyonu bulunamadı');
    }
    
    // Olay tetikle
    document.dispatchEvent(new CustomEvent('templateSelected', { 
        detail: { templateId: templateId } 
    }));
}

// Şablonları listeleme fonksiyonu
function listTemplates() {
    const templateList = document.getElementById('template-list');
    if (!templateList) {
        console.error('template-list elementi bulunamadı');
        return;
    }
    
    console.log('Şablonlar listeleniyor, toplam:', templates.length);
    
    // HTML içinde şablonlar zaten tanımlandığından bu fonksiyon sadece 
    // var olmayan şablonları ekleyecek
    templates.forEach(template => {
        // Şablon zaten eklenmiş mi kontrol et
        const existingTemplate = templateList.querySelector(`[data-template="${template.id}"]`);
        if (existingTemplate) {
            console.log(`Şablon zaten mevcut: ${template.id}`);
            return;
        }
        
        const templateItem = document.createElement('div');
        templateItem.className = 'template-item';
        templateItem.setAttribute('data-template', template.id);
        
        const preview = document.createElement('div');
        preview.className = 'template-preview';
        preview.textContent = `${template.id} Şablonu`;
        
        const name = document.createElement('div');
        name.className = 'template-name';
        name.textContent = template.id === 'bos' ? 'Boş Şablon' : 
                           template.id === 'finansal' ? 'Finansal Rapor' : 
                           template.id;
        
        templateItem.appendChild(preview);
        templateItem.appendChild(name);
        
        // Tıklama olayını ekle
        templateItem.addEventListener('click', function() {
            selectTemplate(template.id);
        });
        
        templateList.appendChild(templateItem);
    });
}

// Sayfa yüklendiğinde şablonları listele
document.addEventListener('DOMContentLoaded', function() {
    console.log('Şablon seçici JS yüklendi');
    listTemplates();
    
    // Şablon öğelerine tıklama olaylarını ekle (mevcut öğeler için)
    document.querySelectorAll('.template-item').forEach(item => {
        item.addEventListener('click', function() {
            const templateId = this.getAttribute('data-template');
            selectTemplate(templateId);
        });
    });
});

// Global olarak kullanılabilir yap
window.selectTemplate = selectTemplate;
window.listTemplates = listTemplates; 