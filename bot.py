# -*- coding: utf-8 -*-
import os, requests, random, time, json, re

SESSION_ID = os.getenv('TIKTOK_SESSION')

def load_brain():
    if os.path.exists('brain.json'):
        with open('brain.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"learned_videos": [], "total_comments": 0}

def save_brain(brain):
    with open('brain.json', 'w', encoding='utf-8') as f:
        json.dump(brain, f, indent=4, ensure_ascii=False)

def get_trending_videos():
    """TikTok keşfetinden taze video ID'leri çeker"""
    try:
        # Bu URL trend olan videolara sızar
        url = "https://www.tiktok.com/api/recommend/item_list/?aid=1988&count=10"
        r = requests.get(url)
        # Basitçe video ID'lerini ayıklıyoruz
        ids = re.findall(r'"id":"(\d+)"', r.text)
        return list(set(ids)) # Tekrarları sil
    except:
        return []

def analyze_and_attack():
    brain = load_brain()
    comment_text = "çok yalnızım  🇲🇽"
    
    # Keşfetten taze kurbanlar bul
    print("🔍 Taze videolar aranıyor...")
    target_videos = get_trending_videos()
    
    if not target_videos:
        print("❌ Video bulunamadı, şimdilik eski yöntemle devam.")
        target_videos = ["7419283746501928374"] # Yedek

    for vid in target_videos:
        if vid in brain['learned_videos']:
            continue
            
        url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={vid}"
        cookies = {'sessionid': SESSION_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }
        
        try:
            r = requests.post(url, cookies=cookies, data={'text': comment_text}, headers=headers)
            if r.status_code == 200:
                print(f"✅ BAŞARILI: https://www.tiktok.com/video/{vid}")
                brain['learned_videos'].append(vid)
                brain['total_comments'] += 1
                save_brain(brain)
                break # Her seferinde 1 tane atıp çıksın ki ban yemesin
            else:
                print(f"⚠️ Atılamadı (Kod: {r.status_code})")
        except:
            pass

if __name__ == "__main__":
    if not SESSION_ID:
        print("SECRET'I EKLEMEMİŞSİN AGA!")
    else:
        analyze_and_attack()
