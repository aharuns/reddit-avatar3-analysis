import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Veriyi Yükleme ---
try:
    df = pd.read_csv('processed_posts.csv', delimiter=';')
    print("İşlenmiş veri dosyası başarıyla yüklendi.")
except FileNotFoundError:
    print("Hata: 'processed_posts.csv' dosyası bulunamadı. Lütfen önce process_data.py script'ini çalıştırın.")
    exit()

# --- 2. Temel Analizler ---

print("\n--- Genel Duygu Dağılımı ---")
sentiment_counts = df['sentiment_label'].value_counts()
print(sentiment_counts)

print("\n--- Duyguya Göre Ortalama Upvote (Score) ---")
avg_score_by_sentiment = df.groupby('sentiment_label')['score'].mean().sort_values(ascending=False)
print(avg_score_by_sentiment)

# --- DÜZELTME BURADA: En Popüler Başlıklar ---
print("\n--- En Popüler Başlıklar ---")

# Önce sadece Pozitif olanları filtrele
positive_df = df[df['sentiment_label'] == 'Pozitif']
# Eğer hiç pozitif post yoksa hata vermemesi için kontrol et
if not positive_df.empty:
    # Şimdi SADECE pozitifler içindeki en yüksek skorluyu bul
    top_positive_post = positive_df.loc[positive_df['score'].idxmax()]
    print(f"En Popüler Pozitif Başlık (Score: {top_positive_post['score']}): {top_positive_post['title']}")
else:
    print("Analiz edilecek pozitif başlık bulunamadı.")

# Aynı işlemi Negatif olanlar için de yap
negative_df = df[df['sentiment_label'] == 'Negatif']
if not negative_df.empty:
    top_negative_post = negative_df.loc[negative_df['score'].idxmax()]
    print(f"En Popüler Negatif Başlık (Score: {top_negative_post['score']}): {top_negative_post['title']}")
else:
    print("Analiz edilecek negatif başlık bulunamadı.")


# --- 3. Görselleştirme ---
print("\nDuygu dağılımı grafiği oluşturuluyor...")

plt.figure(figsize=(8, 6))
# Grafiği doğru sırada (Pozitif, Nötr, Negatif) çizmek için reindex kullanalım
order = ['Pozitif', 'Nötr', 'Negatif']
sentiment_counts.reindex(order).plot(kind='bar', color=['green', 'gray', 'red'])

plt.title('Avatar 3 Hakkındaki Postların Duygu Dağılımı')
plt.xlabel('Duygu Etiketi')
plt.ylabel('Post Sayısı')
plt.xticks(rotation=0)
plt.tight_layout()

output_graph_filename = 'sentiment_dagilimi.png'
plt.savefig(output_graph_filename)
print(f"Grafik başarıyla '{output_graph_filename}' olarak kaydedildi.")