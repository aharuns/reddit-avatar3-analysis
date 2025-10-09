import praw
import config
import csv 

# --- 1. Adım: Rediit'E Bağlanma ---
# PRAW, config dosyasındaki bilgileri kullanarak bir Reddit nesnesi oluşturu.
try:
    reddit = praw.Reddit(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        user_agent=config.USER_AGENT,
    )
    print("Reddit API'sine başarıyla bağlandı!")
except Exception as e:
    print(f"Bağlantı hatası: {e}")
    exit()

# --- 2. Adım: Veri Çekme ---
# 'movies' ve 'avatar' subreddit'lerini birleştirerek arama yapıyoruz.
# Arama sorgumuz 'Avatar 3'. Şimdilik test için sadece 15 post çekiyorum.
subreddit = reddit.subreddit("movies+avatar")
search_query = "Avatar 3"
post_limit = 50

# --- Yeni Bölüm: CSV Dosyasını Hazırlama ---
# Kaydedeceğimiz dosyanın adı ve sütun başlıkları
filename = "reddit_avatar3_posts.csv"
headers = ["post_id", "title", "score", "author", "url", "comment_count"]

print(f"Veriler toplanıyor ve '{filename}' dosyasını kaydedilecek...")

print(f"'{subreddit}' subreddit'lerinde '{search_query}' için arama yapılıyor...")

# CSV dosyasını yazma modunda açıyoruz
# encoding=2utf-8' Türkçe karakterler ve emojiler için önemlidir.
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')

    # İlk satır olarak başlıkları yazıyoruz
    writer.writerow(headers)

    # Arama sonuçları üzerinden dönen döngü
    for submission in subreddit.search(search_query, limit=post_limit):
        # Her post için  verileri bir listeye topluyoruz
        post_data = [
            submission.id,
            submission.title,
            submission.score,
            str(submission.author), 
            submission.url,
            submission.num_comments
        ]

        # Bu listeyi CSV dosyasına yeni bir satır olarak yazıyoruz
        writer.writerow(post_data)

print(f"İşlem tamamlandı! {post_limit} post incelendi ve veriler başarıyla kaydedildi.")
