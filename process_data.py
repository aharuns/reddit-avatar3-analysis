import csv
from textblob import TextBlob
from deep_translator import GoogleTranslator
import time

# --- Dosya İsimleri ---
input_filename = 'reddit_avatar3_posts.csv'
output_filename = 'processed_posts.csv'

# --- Duygu Analizi Fonksiyonu ---
def get_sentiment(text):
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        blob = TextBlob(translated_text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return polarity, 'Pozitif'
        elif polarity < -0.1:
            return polarity, 'Negatif'
        else:
            return polarity, 'Nötr'
            
    except Exception as e:
        print(f"'{text[:30]}...' için analiz hatası: {e}")
        return 0.0, 'N/A'

# --- Ana İşlem ---
print(f"'{input_filename}' dosyası okunuyor...")

with open(input_filename, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
    
    # Okuyucunun da noktalı virgül kullandığından emin olalım
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    headers = next(reader)
    new_headers = headers + ['sentiment_polarity', 'sentiment_label']
    writer.writerow(new_headers)

    for i, row in enumerate(reader):
        # --- GÜNCELLEME VE DÜZELTME BURADA ---
        # Eğer satır boşsa veya yeterli sütun yoksa, bu satırı atla ve bir sonrakine geç
        if not row or len(row) < 2:
            print(f"{i+1}. satır boş veya hatalı, atlanıyor...")
            continue # 'continue' komutu döngünün geri kalanını atlayıp başa döner
        
        title = row[1]
        
        polarity, label = get_sentiment(title)
        
        print(f"{i+1}. başlık işleniyor: {title[:50]}... -> Etiket: {label}")
        
        new_row = row + [polarity, label]
        writer.writerow(new_row)
        
        if (i + 1) % 5 == 0:
            time.sleep(1)

print(f"\nİşlem tamamlandı! İşlenmiş veriler '{output_filename}' dosyasına kaydedildi.")