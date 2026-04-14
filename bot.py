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

def google_ghost_scan():
    """TikTok kapısı kilitliyse, Google üzerinden sızar"""
    print("👻 Ghost Scan: Google üzerinden taze et aranıyor...")
    
    # Google'da TikTok videolarını aratıyoruz
    search_url = "https://www.google.com/search?q=site:tiktok.com+%22video%22&tbs=qdr:d" # Son 24 saatteki videolar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(search_url, headers=headers, timeout=15)
        # Google sonuçlarındaki TikTok video ID'lerini yakalıyoruz
        video_ids = re.findall(r'video/(\d{18,20})', r.text)
        
        if video_ids:
            found = list(set(video_ids))
            print(f"✅ Google üzerinden {len(found)} tane CANLI video sızdırıldı!")
            return found
    except:
        pass
    
    return []

def attack():
    brain = load_brain()
    comment_text = "be 🇲🇽"
    
    targets = google_ghost_scan()
    
    if not targets:
        print("💀 Google bile yardımcı olamadı, TikTok bizi tamamen izole etmiş.")
        return

    for vid in targets:
        if vid in brain['learned_videos']:
            continue
            
        print(f"⚔️ Ghost Moduyla Saldırı: {vid}")
        
        url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={vid}"
        cookies = {'sessionid': SESSION_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
            'Referer': f'https://www.tiktok.com/video/{vid}'
        }
        
        try:
            r = requests.post(url, cookies=cookies, data={'text': comment_text}, headers=headers)
            if r.status_code == 200:
                print(f"✅ MEKSİKA BAYRAĞI DİKİLDİ! 🇲🇽")
                print(f"🔗 LİNK: https://www.tiktok.com/video/{vid}")
                brain['learned_videos'].append(vid)
                brain['total_comments'] += 1
                save_brain(brain)
                break 
            else:
                print(f"⚠️ Yorum engeli: {r.status_code}")
        except:
            pass
        time.sleep(2)

if __name__ == "__main__":
    if not SESSION_ID:
        print("🚨 SESSION_ID EKSİK!")
    else:
        attack()
