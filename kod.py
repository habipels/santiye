import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import SpectralClustering
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import random

# 1. Excel dosyasını oku
#file_path = input("Excel (.xlsx veya .xls) dosyasının yolunu giriniz: ")
df = pd.read_excel("crime.xlsx")

# 2. Gereksiz kolonları at (Row ID gibi)
if 'Row ID' in df.columns:
    df = df.drop(columns=['Row ID'])

# 3. Kategorik sütunları sayısala çevir (Label Encoding)
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))

# 4. RobberyRate sütununu seç
if 'RobberyRate' not in df.columns:
    raise ValueError("RobberyRate sütunu bulunamadı!")

selected_cols = ['RobberyRate']

# Sadece RobberyRate sütununda random eksik veri oluştur
missing_info = {}
indices = df['RobberyRate'].dropna().sample(frac=0.1, random_state=42).index
missing_info['RobberyRate'] = indices
original_values = df.loc[indices, 'RobberyRate'].copy()

a = df['RobberyRate']

# Rastgele %10 indeks seçelim
drop_indices = a.sample(frac=0.1, random_state=42).index

# Bu indekslerdeki değerleri NaN yapalım
a.loc[drop_indices] = np.nan
toplam = a.sum()

print(original_values,"degerler")

df.loc[indices, 'RobberyRate'] = np.nan

# Eksik verileri listele
print("\nEksik verisi olan satırlar:")
print(df[df.isnull().any(axis=1)])

# 5. Özellikleri seçelim ve eksikleri sıfırla (geçici)
X = df[selected_cols].copy()
X = X.fillna(0)
X = X.apply(pd.to_numeric)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. KNN Graph kur
k_neighbors = int(np.sqrt(X_scaled.shape[0]))
print(f"KNN için otomatik belirlenen komşu sayısı: {k_neighbors}")

neighbors = NearestNeighbors(n_neighbors=k_neighbors)
neighbors.fit(X_scaled)
kneighbors_graph = neighbors.kneighbors_graph(X_scaled, mode='connectivity')

# 7. Similarity hesapla (cosine similarity)
similarity_matrix = cosine_similarity(X_scaled)

# 8. Affinity Matrix (KNN bazlı similarity)
affinity_matrix = kneighbors_graph.multiply(similarity_matrix)
affinity_matrix = affinity_matrix.toarray()

# 9. Spectral Clustering ile kümeleme
n_clusters = 3
spectral = SpectralClustering(n_clusters=n_clusters, affinity='precomputed', random_state=42)
spectral_labels = spectral.fit_predict(affinity_matrix)

# 10. Eksik verileri doldurma işlemi
df_completed = df.copy()
missing_indices = indices

for idx in missing_indices:
    cluster_label = spectral_labels[idx]
    cluster_members = df[(spectral_labels == cluster_label) & (~df['RobberyRate'].isnull())]
    if not cluster_members.empty:
        estimated_value = cluster_members['RobberyRate'].mean()
        df_completed.at[idx, 'RobberyRate'] = estimated_value

# Silinen verilerin orijinal ve tahmin edilen toplamları
original_total = original_values.sum()
completed_total = df_completed.loc[missing_indices, 'RobberyRate'].sum()

# 11. Oranları hesapla
ratio = completed_total / original_total
print("\nGerçek ve Tahmin Sonrası Toplamlar Oranı:")
print(ratio,original_total, completed_total,toplam)


# 12. PCA ile 2D indir
n_components = min(X_scaled.shape[0], X_scaled.shape[1], 2)  # Dinamik bileşen sayısı
pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X_scaled)
# ...existing code...

# ...existing code...

# 13. Görselleştirme
plt.figure(figsize=(12, 8))

# Eğer PCA yalnızca bir bileşen ürettiyse, ikinci bileşen için sabit bir değer kullan
if X_pca.shape[1] == 1:
    pos = {i: (X_pca[i, 0], 0) for i in range(len(X_pca))}  # İkinci bileşen 0 olarak ayarlanır
else:
    pos = {i: (X_pca[i, 0], X_pca[i, 1]) for i in range(len(X_pca))}

G = nx.from_numpy_array(affinity_matrix)
nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.5)

unique_labels = set(spectral_labels)
colors = plt.get_cmap('tab10', len(unique_labels))  # Matplotlib uyarısını düzelt

for label in unique_labels:
    mask = (spectral_labels == label)
    mask_indices = np.where(mask)[0]
    x = X_pca[mask_indices, 0]
    y = X_pca[mask_indices, 1] if X_pca.shape[1] > 1 else np.zeros_like(x)
    
    plt.scatter(x, y, label=f'Cluster {label}', alpha=0.8, s=50)

if len(missing_indices) > 0:
    missing_pca = X_pca[list(missing_indices)]
    x_missing = missing_pca[:, 0]
    y_missing = missing_pca[:, 1] if X_pca.shape[1] > 1 else np.zeros_like(x_missing)
    
    plt.scatter(x_missing, y_missing, color='red', marker='x', s=150, linewidths=3, label="Eksik Verisi Doldurulanlar")

plt.legend()
plt.title('Hibrit Kümeleme: KNN + Similarity + Affinity + Spectral')
plt.xlabel('PCA Bileşen 1')
plt.ylabel('PCA Bileşen 2' if X_pca.shape[1] > 1 else 'Sabit Bileşen')
plt.grid(True)
plt.show()