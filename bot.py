# -*- coding: utf-8 -*-
import os
import requests
import random
import time

# GitHub Secrets'tan çektiğimiz kutsal anahtar
SESSION_ID = os.getenv('TIKTOK_SESSION')

def get_trending_videos():
    """
    Bu fonksiyon TikTok'un 'Keşfet' (Trending) kısmındaki 
    popüler video ID'lerini toplar.
    """
    # Buradaki ID'ler örnektir, botun çalışması için 
    # gerçek video ID'lerini çekmesi gerekir.
    return ["7345678901234567890", "7356789012345678901", "7367890123456789012"]

def attack(video_id):
    """Yorumu patlatan ana fonksiyon."""
    comment_text = "cok yalnızım  🇲🇽"
    
    url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={video_id}"
    cookies = {'sessionid': SESSION_ID}
    data = {'text': comment_text}
    
    # iPhone simülasyonu (TikTok'u kandırmak için şart)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.tiktok.com/',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(url, cookies=cookies, data=data, headers=headers)
        if response.status_code == 200:
            print(f"BAŞARILI: {video_id} videosuna yalnızlık çöktü 🇲🇽")
            return True
        else:
            print(f"HATA: Kod {response.status_code}. Session gitmiş olabilir aga.")
            return False
    except Exception as e:
        print(f"PATLADIK: {e}")
        return False

def run():
    if not SESSION_ID:
        print("AGA DUR! Secrets kısmına TIKTOK_SESSION eklememişsin.")
        return

    targets = get_trending_videos()
    for vid in targets:
        success = attack(vid)
        if success:
            # TikTok uyanmasın diye 1-3 dakika arası mola veriyoruz
            wait = random.randint(60, 180)
            print(f"Gözcüleri atlatmak için {wait} saniye siperdeyiz...")
            time.sleep(wait)

if __name__ == "__main__":
    run()
