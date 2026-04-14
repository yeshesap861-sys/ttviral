# -*- coding: utf-8 -*-
import os
import requests
import random
import time
import json

# GitHub'daki kutsal anahtarın
SESSION_ID = os.getenv('TIKTOK_SESSION')

def load_brain():
    """Hafızayı tazele"""
    if os.path.exists('brain.json'):
        with open('brain.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"learned_videos": [], "total_comments": 0}

def save_brain(brain):
    """Öğrenilenleri kaydet"""
    with open('brain.json', 'w', encoding='utf-8') as f:
        json.dump(brain, f, indent=4, ensure_ascii=False)

def analyze_and_attack():
    brain = load_brain()
    
    # Senin o tek ve efsane mesajın
    comment_text = "cok yalnızım  🇲🇽"
    
    # Örnek video listesi (Gerçekte buraya keşfet API'si gelir)
    target_videos = ["7345678901234567890", "7356789012345678901"] 

    for vid in target_videos:
        # ÖĞRENME: Eğer bu videoyu daha önce gördüysek es geç
        if vid in brain['learned_videos']:
            print(f"Aga bu videoyu zaten biliyorum, geçtik: {vid}")
            continue
            
        # SALDIRI:
        url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={vid}"
        cookies = {'sessionid': SESSION_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.tiktok.com/'
        }
        
        try:
            r = requests.post(url, cookies=cookies, data={'text': comment_text}, headers=headers)
            if r.status_code == 200:
                print(f"Meksika bayrağı dikildi 🇲🇽: {vid}")
                brain['learned_videos'].append(vid)
                brain['total_comments'] += 1
                save_brain(brain) # Her adımda öğreniyoruz
                time.sleep(random.randint(60, 150)) # Uyanmasınlar
        except:
            print("Sıkıntı çıktı, beklemedeyiz.")

if __name__ == "__main__":
    if not SESSION_ID:
        print("SECRET'I EKLEMEMİŞSİN AGA!")
    else:
        analyze_and_attack()
