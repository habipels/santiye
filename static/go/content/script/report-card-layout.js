/**
 * Report Card Düzenleme
 * Her satırda 3 kart olacak şekilde kartları düzenler (12 sütunlu bir grid içinde).
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Report Card Düzenleme: Script yüklendi');
    
    // Sayfa ilk yüklendiğinde veya bileşen değiştiğinde çalışsın
    setTimeout(organizeReportCards, 500);
    
    // Kart boyutlandırma işlevselliğini sayfaya ekle
    setTimeout(initializeCardResizing, 800);
    
    // Masonry grid yapısını uygula
    setTimeout(initializeMasonryLayout, 1000);
    
    // Olay dinleyicileri
    document.addEventListener('componentAdded', function() {
        console.log('Bileşen eklendi, kartlar düzenleniyor...');
        setTimeout(organizeReportCards, 200);
        
        // Yeni eklenen proje özeti komponentine sütun kontrollerini ekle
        setTimeout(addColumnControlsToProjeOzeti, 300);
        
        // Proje özeti bileşenlerini görünür yap
        setTimeout(function() {
            const projeOzetiCards = document.querySelectorAll('.report-card[data-type="proje-ozeti"]');
            projeOzetiCards.forEach(showProjeOzetiCards);
        }, 300);
        
        // Yeni eklenen kartlara boyutlandırma işlevselliği ekle
        setTimeout(initializeCardResizing, 400);
        
        // Masonry grid yapısını güncelle
        setTimeout(initializeMasonryLayout, 500);
    });
    
    document.addEventListener('componentRemoved', function() {
        console.log('Bileşen kaldırıldı, kartlar düzenleniyor...');
        setTimeout(organizeReportCards, 200);
        setTimeout(initializeMasonryLayout, 300); // Masonry grid yapısını güncelle
    });
    
    // Şablon değiştiğinde
    document.addEventListener('templateSelected', function(e) {
        console.log('Şablon değişti, kartlar yeniden düzenlenecek:', e.detail.templateId);
        setTimeout(organizeReportCards, 200);
        setTimeout(initializeCardResizing, 300);
        setTimeout(initializeMasonryLayout, 400); // Masonry grid yapısını güncelle
    });
    
    // Pencere yeniden boyutlandırıldığında masonry düzeni güncelle
    window.addEventListener('resize', debounce(function() {
        console.log('Pencere boyutu değişti, masonry düzen yeniden hesaplanıyor...');
        initializeMasonryLayout();
    }, 250)); // 250ms debounce
    
    // Proje özeti komponentlerine sütun kontrollerini ekle
    setTimeout(addColumnControlsToProjeOzeti, 1000);
    
    // Bir element gösterildiğinde/saklandığında (display değişimi için)
    // Mutation Observer ekleyelim
    const observer = new MutationObserver(function(mutations) {
        let layoutChanged = false;
        
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                console.log('Stil değişimi algılandı, kartlar düzenleniyor...');
                layoutChanged = true;
                
                // Görünürlük değişiminde proje özeti komponentlerine sütun kontrollerini ekle
                setTimeout(addColumnControlsToProjeOzeti, 300);
                
                // Proje özeti bileşenlerini görünür yap
                if (mutation.target.classList && 
                    mutation.target.classList.contains('report-card') && 
                    mutation.target.getAttribute('data-type') === 'proje-ozeti') {
                    setTimeout(function() {
                        showProjeOzetiCards(mutation.target);
                    }, 300);
                }
                
                // Yeni görünür kartlara boyutlandırma özelliği ekle
                setTimeout(initializeCardResizing, 400);
            }
        });
        
        if (layoutChanged) {
            setTimeout(organizeReportCards, 200);
            setTimeout(initializeMasonryLayout, 300); // Masonry grid yapısını güncelle
        }
    });
    
    // Gözlemlenecek elementleri belirle
    document.querySelectorAll('.report-charts, .report-card').forEach(function(element) {
        observer.observe(element, { attributes: true });
    });
    
    // DOM değişikliklerini izle
    const domObserver = new MutationObserver(function(mutations) {
        let hasNewComponents = false;
        let hasNewProjeOzeti = false;
        let newProjeOzetiCard = null;
        
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) {
                        // Yeni bileşen kontrolü
                        if (node.classList && (
                            node.classList.contains('report-card') || 
                            node.classList.contains('report-charts') ||
                            node.querySelector('.report-card')
                        )) {
                            hasNewComponents = true;
                        }
                        
                        // Proje özeti kartı kontrolü
                        if (node.classList && 
                            node.classList.contains('report-card') && 
                            node.getAttribute('data-type') === 'proje-ozeti') {
                            hasNewProjeOzeti = true;
                            newProjeOzetiCard = node;
                        }
                    }
                });
            }
        });
        
        if (hasNewComponents) {
            console.log('DOM değişimi algılandı, yeni bileşenler eklendi');
            setTimeout(organizeReportCards, 200);
            setTimeout(addColumnControlsToProjeOzeti, 300);
            setTimeout(initializeCardResizing, 400);
            setTimeout(initializeMasonryLayout, 500); // Masonry grid yapısını güncelle
        }
        
        if (hasNewProjeOzeti && newProjeOzetiCard) {
            console.log('Yeni proje özeti kartı eklendi');
            setTimeout(function() {
                showProjeOzetiCards(newProjeOzetiCard);
            }, 300);
        }
    });
    
    // Tüm belgeyi izle
    domObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Sayfa yüklendiğinde mevcut proje özeti kartlarını kontrol et
    setTimeout(function() {
        const projeOzetiCards = document.querySelectorAll('.report-card[data-type="proje-ozeti"]');
        if (projeOzetiCards.length > 0) {
            console.log('Mevcut proje özeti kartları bulundu:', projeOzetiCards.length);
            projeOzetiCards.forEach(showProjeOzetiCards);
        }
    }, 1000);
});

// Debounce fonksiyonu - sık çağrılan olayları kontrol altına almak için
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            func.apply(context, args);
        }, wait);
    };
}

/**
 * Kartların yeniden boyutlandırılabilir olmasını sağlar
 */
function initializeCardResizing() {
    console.log('Kart boyutlandırma başlatılıyor...');
    
    // Tüm kartları bul
    const cards = document.querySelectorAll('.report-card:not(.resizable-initialized)');
    
    cards.forEach(function(card) {
        // Kartın zaten boyutlandırılabilir olup olmadığını kontrol et
        if (card.classList.contains('resizable-initialized')) {
            return;
        }
        
        // Kenar tutamaçlarını ekle
        const rightHandle = document.createElement('div');
        rightHandle.className = 'card-resize-handle card-resize-right';
        rightHandle.title = 'Genişliği değiştirmek için sürükleyin';
        
        const leftHandle = document.createElement('div');
        leftHandle.className = 'card-resize-handle card-resize-left';
        leftHandle.title = 'Genişliği değiştirmek için sürükleyin';
        
        const bottomHandle = document.createElement('div');
        bottomHandle.className = 'card-resize-handle card-resize-bottom';
        bottomHandle.title = 'Yüksekliği değiştirmek için sürükleyin';
        
        const cornerHandle = document.createElement('div');
        cornerHandle.className = 'card-resize-handle card-resize-corner';
        cornerHandle.title = 'Boyutu değiştirmek için sürükleyin';
        
        // Tutamaçları karta ekle
        card.appendChild(rightHandle);
        card.appendChild(leftHandle);
        card.appendChild(bottomHandle);
        card.appendChild(cornerHandle);
        
        // Görünürlük kontrolü ekle
        if (!card.querySelector('.visibility-toggle')) {
            const cardActions = card.querySelector('.card-actions');
            
            if (cardActions) {
                // Görünürlük butonunu oluştur
                const visibilityBtn = document.createElement('button');
                visibilityBtn.className = 'card-action-btn visibility-toggle';
                visibilityBtn.title = 'Görünürlüğü değiştir (PDF raporunda gösterme)';
                visibilityBtn.innerHTML = '<i class="fas fa-eye"></i>';
                
                // Tıklama olayı ekle
                visibilityBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Görünürlük durumunu değiştir
                    toggleCardVisibility(card);
                });
                
                // Butonu kart aksiyonlarına ekle
                cardActions.insertBefore(visibilityBtn, cardActions.firstChild);
            }
        }
        
        // jQuery ile boyutlandırma işlemleri
        
        // Sağ kenar boyutlandırma
        $(rightHandle).on('mousedown', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const startX = e.pageX;
            const startWidth = $(card).width();
            const parent = $(card).parent();
            const parentWidth = parent.width();
            
            // Grid uyumu için
            const minWidth = Math.floor(parentWidth / 12);
            
            // Taşıma işlemi
            $(document).on('mousemove.resize', function(e) {
                const newWidth = startWidth + (e.pageX - startX);
                
                // Genişliği güncelle
                if (newWidth >= minWidth) {
                    $(card).width(newWidth + 'px');
                    
                    // span değerini ayarla (grid uyumu için)
                    updateCardSpanFromWidth(card, newWidth, parent.width());
                }
            });
            
            // Taşıma bitti
            $(document).on('mouseup.resize', function() {
                $(document).off('mousemove.resize mouseup.resize');
                
                // Card boyutunu sonlandır ve yerleşimi güncelle
                setTimeout(function() {
                    initializeMasonryLayout();
                }, 100);
            });
            
            $(card).addClass('resizing');
            $('body').css('cursor', 'ew-resize');
        });
        
        // Sol kenar boyutlandırma
        $(leftHandle).on('mousedown', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const startX = e.pageX;
            const startWidth = $(card).width();
            const startLeft = $(card).position().left;
            const parent = $(card).parent();
            const parentWidth = parent.width();
            
            // Grid uyumu için
            const minWidth = Math.floor(parentWidth / 12);
            
            // Taşıma işlemi
            $(document).on('mousemove.resize', function(e) {
                const dx = startX - e.pageX;
                const newWidth = startWidth + dx;
                
                // Genişliği güncelle
                if (newWidth >= minWidth) {
                    $(card).width(newWidth + 'px');
                    
                    // span değerini ayarla (grid uyumu için)
                    updateCardSpanFromWidth(card, newWidth, parent.width());
                }
            });
            
            // Taşıma bitti
            $(document).on('mouseup.resize', function() {
                $(document).off('mousemove.resize mouseup.resize');
                
                // Card boyutunu sonlandır ve yerleşimi güncelle
                setTimeout(function() {
                    initializeMasonryLayout();
                }, 100);
            });
            
            $(card).addClass('resizing');
            $('body').css('cursor', 'ew-resize');
        });
        
        // Alt kenar boyutlandırma
        $(bottomHandle).on('mousedown', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const startY = e.pageY;
            const startHeight = $(card).height();
            
            // Taşıma işlemi
            $(document).on('mousemove.resize', function(e) {
                const newHeight = startHeight + (e.pageY - startY);
                
                // Yüksekliği güncelle
                if (newHeight >= 100) {
                    $(card).height(newHeight + 'px');
                }
            });
            
            // Taşıma bitti
            $(document).on('mouseup.resize', function() {
                $(document).off('mousemove.resize mouseup.resize');
                
                // Card boyutunu sonlandır ve yerleşimi güncelle
                setTimeout(function() {
                    initializeMasonryLayout();
                }, 100);
            });
            
            $(card).addClass('resizing');
            $('body').css('cursor', 'ns-resize');
        });
        
        // Köşe boyutlandırma
        $(cornerHandle).on('mousedown', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const startX = e.pageX;
            const startY = e.pageY;
            const startWidth = $(card).width();
            const startHeight = $(card).height();
            const parent = $(card).parent();
            const parentWidth = parent.width();
            
            // Grid uyumu için
            const minWidth = Math.floor(parentWidth / 12);
            
            // Taşıma işlemi
            $(document).on('mousemove.resize', function(e) {
                const newWidth = startWidth + (e.pageX - startX);
                const newHeight = startHeight + (e.pageY - startY);
                
                // Genişlik ve yüksekliği güncelle
                if (newWidth >= minWidth) {
                    $(card).width(newWidth + 'px');
                    
                    // span değerini ayarla (grid uyumu için)
                    updateCardSpanFromWidth(card, newWidth, parent.width());
                }
                
                if (newHeight >= 100) {
                    $(card).height(newHeight + 'px');
                }
            });
            
            // Taşıma bitti
            $(document).on('mouseup.resize', function() {
                $(document).off('mousemove.resize mouseup.resize');
                
                // Card boyutunu sonlandır ve yerleşimi güncelle
                setTimeout(function() {
                    initializeMasonryLayout();
                }, 100);
            });
            
            $(card).addClass('resizing');
            $('body').css('cursor', 'nwse-resize');
        });
        
        // Boyutlandırma tamamlandığında resizing sınıfını kaldır
        $(document).on('mouseup', function() {
            $(card).removeClass('resizing');
            $('body').css('cursor', '');
        });
        
        // Kartı başlatıldı olarak işaretle
        card.classList.add('resizable-initialized');
        
        // Konum için relative ekle
        if (getComputedStyle(card).position === 'static') {
            card.style.position = 'relative';
        }
    });
    
    console.log('Kart boyutlandırma başlatıldı');
}

/**
 * Kartın genişliğinden grid span değerini hesaplar ve günceller
 * @param {HTMLElement} card - Kart elementi
 * @param {number} width - Kart genişliği
 * @param {number} parentWidth - Parent container genişliği
 */
function updateCardSpanFromWidth(card, width, parentWidth) {
    // Grid sütun sayısı
    const columns = 12;
    
    // Genişlikten span hesapla
    const span = Math.max(1, Math.min(columns, Math.round((width / parentWidth) * columns)));
    
    // Span değerini ve data-size özelliğini güncelle
    card.style.gridColumn = `span ${span}`;
    
    // Kart boyut sınıfını güncelle
    updateCardSizeAttribute(card, span, columns);
    
    console.log(`Kart genişliği ${width}px, hesaplanan span: ${span}`);
}

/**
 * Masonry grid düzenini uygular
 * Farklı yükseklikteki kartları sıkıştırarak boşlukları azaltır
 */
function initializeMasonryLayout() {
    console.log('Masonry düzeni uygulanıyor...');
    
    // Tüm preview-grid veya report-charts konteynerlerini bul
    const gridContainers = document.querySelectorAll('.preview-grid, .report-charts, .card-body[data-columns]');
    
    gridContainers.forEach(function(grid) {
        // jQuery ile temel masonry duzenlemesi uygula
        const $grid = $(grid);
        
        // CSS grid düzenini temizle
        $grid.find('.report-card').each(function() {
            const $card = $(this);
            const cardWidth = $card.width();
            
            // Width değerini koru ama grid pozisyonu kaldır
            if (!$card.attr('data-original-width')) {
                $card.attr('data-original-width', cardWidth);
            }
        });
        
        // Masonry düzenini uygula
        applySimpleMasonry(grid);
    });
    
    console.log('Masonry düzeni uygulandı');
}

/**
 * Basit masonry düzeni uygular
 * @param {HTMLElement} container - Masonry düzenini uygulanacak konteyner
 */
function applySimpleMasonry(container) {
    const containerWidth = $(container).width();
    const columnCount = 12; // 12 sütunlu grid
    const gap = 20; // gap değeri (px)
    
    // Tüm kartları bul
    const $cards = $(container).find('.report-card:visible');
    
    if ($cards.length === 0) return;
    
    // Masonry pozisyonlama için hazırlık
    const columnWidth = (containerWidth - (gap * (columnCount - 1))) / columnCount;
    const columns = Array(columnCount).fill(0); // Her sütunun mevcut yüksekliği
    
    // Kartları mevcut boyutlarına göre düzenle
    $cards.each(function() {
        const $card = $(this);
        const cardWidth = $card.width();
        const span = Math.max(1, Math.min(12, Math.round((cardWidth / containerWidth) * columnCount)));
        
        // Span değerini güncelle
        $card.css('gridColumn', `span ${span}`);
        
        // En kısa sütun grubunu bul
        let minHeight = Infinity;
        let minColIndex = 0;
        
        for (let i = 0; i <= columnCount - span; i++) {
            // Bu sütun aralığında maksimum yüksekliği bul
            let maxColHeight = 0;
            for (let j = 0; j < span; j++) {
                maxColHeight = Math.max(maxColHeight, columns[i + j]);
            }
            
            if (maxColHeight < minHeight) {
                minHeight = maxColHeight;
                minColIndex = i;
            }
        }
        
        // Kartı pozisyonla
        const startColumn = minColIndex + 1;
        const endColumn = startColumn + span;
        $card.css({
            'gridColumn': `${startColumn} / ${endColumn}`,
            'gridRow': minHeight + 1
        });
        
        // Sütun yüksekliğini güncelle
        const cardHeight = $card.outerHeight(true) + gap;
        for (let i = minColIndex; i < minColIndex + span; i++) {
            columns[i] = minHeight + 1;
        }
    });
}

/**
 * Kartın mevcut grid column span değerini alır
 */
function getCardSpan(card) {
    const gridColStyle = card.style.gridColumn || '';
    let spanValue = 4; // Varsayılan değer
    
    if (gridColStyle) {
        const spanMatch = gridColStyle.match(/span\s+(\d+)/);
        if (spanMatch) {
            spanValue = parseInt(spanMatch[1]);
        } else if (gridColStyle.includes('/')) {
            const parts = gridColStyle.split('/').map(p => parseInt(p.trim()));
            if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
                spanValue = parts[1] - parts[0];
            }
        }
    } else {
        // Grid column değeri yoksa, data-size'a göre al
        const cardSize = card.getAttribute('data-size') || 'medium';
        if (cardSize === 'small') spanValue = 4;
        else if (cardSize === 'medium') spanValue = 4;
        else if (cardSize === 'large') spanValue = 8;
        else if (cardSize === 'full') spanValue = 12;
    }
    
    return spanValue;
}

/**
 * Kart gösterme/gizleme işlemini gerçekleştirir
 * @param {HTMLElement} card - İşlem yapılacak kart
 */
function toggleCardVisibility(card) {
    // Mevcut görünürlük durumunu kontrol et
    const isHidden = card.classList.contains('hide-in-pdf');
    
    if (isHidden) {
        // Kartı görünür yap
        card.classList.remove('hide-in-pdf');
        
        // İkon değiştir
        const visibilityBtn = card.querySelector('.visibility-toggle');
        if (visibilityBtn) {
            visibilityBtn.innerHTML = '<i class="fas fa-eye"></i>';
            visibilityBtn.title = 'Görünürlüğü değiştir (PDF raporunda gösterme)';
        }
    } else {
        // Kartı gizle
        card.classList.add('hide-in-pdf');
        
        // İkon değiştir
        const visibilityBtn = card.querySelector('.visibility-toggle');
        if (visibilityBtn) {
            visibilityBtn.innerHTML = '<i class="fas fa-eye-slash"></i>';
            visibilityBtn.title = 'Görünürlüğü değiştir (PDF raporunda göster)';
        }
    }
    
    console.log(`Kart görünürlüğü değiştirildi: ${isHidden ? 'Görünür' : 'Gizli'}`);
}

/**
 * Span değerine göre data-size özniteliğini günceller
 */
function updateCardSizeAttribute(card, span, totalCols) {
    // Toplam sütun sayısına bölünerek göreceli boyut hesapla
    const relativeSize = span / totalCols;
    
    let newSize;
    if (relativeSize <= 0.25) {
        newSize = 'small';
    } else if (relativeSize <= 0.5) {
        newSize = 'medium';
    } else if (relativeSize <= 0.75) {
        newSize = 'large';
    } else {
        newSize = 'full';
    }
    
    // Veri özniteliğini güncelle
    card.setAttribute('data-size', newSize);
}

/**
 * Proje özeti komponentlerine sütun kontrolü ekler
 */
function addColumnControlsToProjeOzeti() {
    // Proje özeti komponentlerini bul
    const projeOzetiCards = document.querySelectorAll('.report-card[data-size="large"]:not(.column-controls-added)');
    
    projeOzetiCards.forEach(function(card) {
        const cardHeader = card.querySelector('.card-header');
        const cardActions = card.querySelector('.card-actions');
        
        if (!cardHeader || !cardActions) return;
        
        // Kontrolün zaten eklenip eklenmediğini kontrol et
        if (cardActions.querySelector('.column-selector')) return;
        
        // 2 ve 3 sütun seçeneklerini içeren bir div ekle
        const columnSelector = document.createElement('div');
        columnSelector.className = 'column-selector';
        columnSelector.style.display = 'flex';
        columnSelector.style.marginRight = '10px';
        
        // 2 sütun butonu
        const twoColBtn = document.createElement('button');
        twoColBtn.className = 'card-action-btn column-btn two-col';
        twoColBtn.title = '2 Sütun';
        twoColBtn.innerHTML = '<i class="fas fa-columns"></i><span>2</span>';
        twoColBtn.style.position = 'relative';
        twoColBtn.style.marginRight = '5px';
        
        // 2 sütun sayı stili
        const twoColSpan = twoColBtn.querySelector('span');
        twoColSpan.style.fontSize = '10px';
        twoColSpan.style.position = 'absolute';
        twoColSpan.style.bottom = '2px';
        twoColSpan.style.right = '2px';
        
        // 3 sütun butonu
        const threeColBtn = document.createElement('button');
        threeColBtn.className = 'card-action-btn column-btn three-col';
        threeColBtn.title = '3 Sütun';
        threeColBtn.innerHTML = '<i class="fas fa-columns"></i><span>3</span>';
        threeColBtn.style.position = 'relative';
        
        // 3 sütun sayı stili
        const threeColSpan = threeColBtn.querySelector('span');
        threeColSpan.style.fontSize = '10px';
        threeColSpan.style.position = 'absolute';
        threeColSpan.style.bottom = '2px';
        threeColSpan.style.right = '2px';
        
        // Olayları dinle
        twoColBtn.addEventListener('click', function() {
            setCardColumnLayout(card, 2);
        });
        
        threeColBtn.addEventListener('click', function() {
            setCardColumnLayout(card, 3);
        });
        
        // Butonları ekle
        columnSelector.appendChild(twoColBtn);
        columnSelector.appendChild(threeColBtn);
        
        // Sütun seçiciyi kart aksiyonlarının başına ekle
        cardActions.insertBefore(columnSelector, cardActions.firstChild);
        
        // İşaretleme için sınıf ekle
        card.classList.add('column-controls-added');
        
        console.log('Proje özeti komponentine sütun kontrolleri eklendi');
    });
}

/**
 * Kartın içindeki öğeleri belirtilen sütun sayısına göre düzenler
 * @param {HTMLElement} card - Düzenlenecek kart
 * @param {number} columns - Sütun sayısı (2 veya 3)
 */
function setCardColumnLayout(card, columns) {
    // Kart içindeki report-charts elementlerini bul
    const chartContainers = card.querySelectorAll('.report-charts');
    
    chartContainers.forEach(function(container) {
        // Görünür düzenini güncelle
        if (container.style.display === 'none') {
            container.style.display = 'grid';
        }
        
        // Sütun sayısını güncelle
        container.setAttribute('data-columns', columns);
        
        // Grid içindeki kartları düzenle
        const childCards = container.querySelectorAll('.report-card');
        
        childCards.forEach(function(childCard) {
            if (columns === 2) {
                childCard.style.gridColumn = 'span 6'; // 2 sütun = 12/2 = 6 column
            } else if (columns === 3) {
                childCard.style.gridColumn = 'span 4'; // 3 sütun = 12/3 = 4 column
            }
        });
    });
    
    // İç içe olmayan kartları doğrudan bul
    const directChildCards = Array.from(card.children)
        .filter(child => child.classList && child.classList.contains('report-card'));
    
    directChildCards.forEach(function(childCard) {
        if (columns === 2) {
            childCard.style.gridColumn = 'span 6'; // 2 sütun
        } else if (columns === 3) {
            childCard.style.gridColumn = 'span 4'; // 3 sütun
        }
    });
    
    // report-card içindeki tüm other-elements sınıfını da düzenleme
    const cardBody = card.querySelector('.card-body');
    if (cardBody) {
        cardBody.setAttribute('data-columns', columns);
        
        // Eğer grid düzeni yok ise ekle
        if (getComputedStyle(cardBody).display !== 'grid') {
            cardBody.style.display = 'grid';
            cardBody.style.gridTemplateColumns = 'repeat(12, 1fr)';
            cardBody.style.gap = '20px';
        }
        
        // Doğrudan kart gövdesi içindeki kartları düzenle
        const bodyCards = cardBody.querySelectorAll(':scope > .report-card');
        bodyCards.forEach(function(bodyCard) {
            if (columns === 2) {
                bodyCard.style.gridColumn = 'span 6'; // 2 sütun
            } else if (columns === 3) {
                bodyCard.style.gridColumn = 'span 4'; // 3 sütun
            }
        });
    }
    
    console.log(`Kart düzeni ${columns} sütunlu olarak güncellendi`);
}

/**
 * Report kartlarını 3 sütunlu grid olarak düzenler
 * Bu fonksiyon her satırda 3 kart olacak şekilde grid düzenlemesi yapar
 */
function organizeReportCards() {
    console.log('Report kartları düzenleniyor...');
    
    // Doğrudan sayfa içindeki kartlar
    const reportCards = document.querySelectorAll('.report-card');
    
    if (reportCards.length === 0) {
        console.log('Düzenlenecek report-card bulunamadı');
    } else {
        console.log('Toplam doğrudan report-card sayısı:', reportCards.length);
        organizeCards(reportCards);
    }
    
    // Report-charts içindeki kartlar
    const reportCharts = document.querySelectorAll('.report-charts');
    reportCharts.forEach(function(chartContainer, index) {
        const nestedCards = chartContainer.querySelectorAll('.report-card');
        if (nestedCards.length > 0) {
            console.log(`İç içe report-card sayısı (konteyner ${index + 1}):`, nestedCards.length);
            
            // Konteyner data-columns özniteliğini kontrol et
            const columns = chartContainer.getAttribute('data-columns');
            if (columns === '2') {
                // 2 sütunlu düzen
                nestedCards.forEach(card => {
                    card.style.gridColumn = 'span 6';
                });
            } else {
                // Varsayılan 3 sütunlu düzen
                organizeCards(nestedCards);
            }
        }
    });
    
    console.log('Report kartları düzenleme tamamlandı');
}

/**
 * Belirtilen kartları düzenler
 * @param {NodeList} cards - Düzenlenecek kartlar
 */
function organizeCards(cards) {
    cards.forEach((card, index) => {
        // Kartın görünür olup olmadığını kontrol et
        const isVisible = window.getComputedStyle(card).display !== 'none';
        
        // Kart görünür değilse atla
        if (!isVisible) {
            return;
        }
        
        // Kart boyutunu hesapla (3 sütunlu grid için)
        const cardSize = card.getAttribute('data-size') || 'medium';
        
        // Inline stillerle class atamasının önüne geçme
        if (cardSize === 'small') {
            card.style.gridColumn = 'span 4'; // 3 sütun = 12/3 = 4 column
        } else if (cardSize === 'medium') {
            card.style.gridColumn = 'span 4'; // 3 sütun = 12/3 = 4 column
        } else if (cardSize === 'large') {
            card.style.gridColumn = 'span 8'; // 2 sütun = 12/2 = 6 column (fazladan büyük)
        } else if (cardSize === 'full') {
            card.style.gridColumn = 'span 12'; // Tam genişlik
        }
    });
}

/**
 * Proje özeti kartlarını görünür hale getirir
 * @param {HTMLElement} card - Görünür yapılacak kart
 */
function showProjeOzetiCards(card) {
    if (!card || !card.classList.contains('report-card') || card.getAttribute('data-type') !== 'proje-ozeti') {
        return;
    }
    
    console.log('Proje özeti kartı bulundu, görünür yapılıyor...');
    
    // Kart içindeki tüm report-charts elementlerini bul
    const chartContainers = card.querySelectorAll('.report-charts');
    chartContainers.forEach(function(container) {
        // Display değerini güncelle ve görünür yap
        if (container.style.display === 'none') {
            container.style.display = 'grid';
            container.setAttribute('data-columns', '3'); // Varsayılan olarak 3 sütunlu gösterim
        }
    });
    
    // Tüm card-body elementlerini kontrol et
    const cardBodies = card.querySelectorAll('.card-body');
    cardBodies.forEach(function(body) {
        if (body.style.display === 'none') {
            body.style.display = 'grid';
            body.style.gridTemplateColumns = 'repeat(12, 1fr)';
            body.style.gap = '20px';
            body.setAttribute('data-columns', '3'); // Varsayılan olarak 3 sütunlu gösterim
        }
    });
    
    // İç içe kartları düzenle
    const childCards = card.querySelectorAll('.report-card');
    childCards.forEach(function(childCard) {
        childCard.style.gridColumn = 'span 4'; // 3 sütun = 12/3 = 4 column
    });
    
    console.log('Proje özeti kartları görünür hale getirildi ve düzenlendi');
}

// Global olarak kullanılabilir yap
window.organizeReportCards = organizeReportCards;
window.addColumnControlsToProjeOzeti = addColumnControlsToProjeOzeti;
window.setCardColumnLayout = setCardColumnLayout;
window.showProjeOzetiCards = showProjeOzetiCards;
window.initializeCardResizing = initializeCardResizing;
window.toggleCardVisibility = toggleCardVisibility;
window.initializeMasonryLayout = initializeMasonryLayout; 