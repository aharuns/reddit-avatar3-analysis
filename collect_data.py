import praw
import config

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
post_limit = 15

print(f"'{subreddit}' subreddit'lerinde '{search_query}' için arama yapılıyor...")

# Arama sonuçları üzerinden dönen bir döngü
for submission in subreddit.search(search_query, limit=post_limit):
    # Şimdilik sadece post'un başlığını ve upvote sayısını yazdıralım
    print(f"Başlık: {submission.title}")
    print(f"Upvote Sayısı: {submission.score}")
    print("---")