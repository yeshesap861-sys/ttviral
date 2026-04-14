# -*- coding: utf-8 -*-
import os
import requests
import random
import time
import json

# GitHub Secrets
SESSION_ID = os.getenv('TIKTOK_SESSION')

def load_brain():
    """Botun hafızasını (brain.json) yükler."""
    if os.path.exists('brain.json'):
        with open('brain.json', 'r') as f:
            return json.load(f)
    return {"learned_videos": []}

def save_brain(brain):
    """Botun yeni öğrendiği videoları kaydeder."""
    with open('brain.json', 'w') as f:
        json.dump(brain, f, indent=4)

def get_trending_videos():
    """Türkiye Keşfet listesini simüle eder."""
    # Buraya gerçek bir scraping modülü eklenebilir.
    # Şimdilik taze video ID'leri listesi (Örnektir):
    return ["7345678901234567890", "7356789012345678901", "7367890123456789012"]

def attack(video_id):
    comment_text = "cok yalnızım  🇲🇽"
    url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={video_id}"
    cookies = {'sessionid': SESSION_ID}
    data = {'text': comment_text}
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.tiktok.com/'
    }
    
    try:
        response = requests.post(url, cookies=cookies, data=data, headers=headers)
        return response.status_code == 200
    except:
        return False

def run():
    if not SESSION_ID:
        print("SİSTEM DURDURULDU: TIKTOK_SESSION bulunamadı!")
        return

    brain = load_brain()
    targets = get_trending_videos()
    new_learned = False

    for vid in targets:
        # ÖĞRENME KONTROLÜ: Eğer video zaten hafızadaysa atla!
        if vid in brain['learned_videos']:
            print(f"Atlanıyor: {vid} zaten yalnız bırakıldı.")
            continue
            
        success = attack(vid)
        if success:
            print(f"Yalnızlık çöktü: {vid} 🇲🇽")
            brain['learned_videos'].append(vid)
            new_learned = True
            # İnsan gibi bekleme (Bot olduğu anlaşılmasın)
            time.sleep(random.randint(60, 150))
    
    if new_learned:
        save_brain(brain)

if __name__ == "__main__":
    run()
