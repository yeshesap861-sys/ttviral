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

def get_real_for_you_videos():
    """TikTok'un ana damarına (Keşfet Akışına) sızar"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.tiktok.com/foryou?lang=tr-TR',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    
    # Keşfetin ana sayfası
    url = "https://www.tiktok.com/foryou?lang=tr-TR"
    
    try:
        print("🔥 Keşfetin kalbine sızılıyor...")
        r = requests.get(url, headers=headers, timeout=20)
        # Sayfanın içindeki gizli JSON verisinden video ID'lerini cımbızla çekiyoruz
        video_ids = re.findall(r'"id":"(\d{19})"', r.text)
        
        if not video_ids:
            # Alternatif yakalama yöntemi
            video_ids = re.findall(r'video/(\d+)', r.text)
            
        if video_ids:
            unique_ids = list(set(video_ids))
            print(f"✅ Keşfette {len(unique_ids)} tane taze et bulundu!")
            return unique_ids
    except Exception as e:
        print(f"❌ Sızma başarısız: {e}")
    
    return []

def execute_attack():
    brain = load_brain()
    comment_text = "BP🇲🇽"
    
    targets = get_real_for_you_videos()
    
    if not targets:
        print("💀 Keşfet kapısı kilitli, 2 dakika sonra tekrar denenecek...")
        return

    for vid in targets:
        if vid in brain['learned_videos']:
            continue
            
        print(f"⚔️ Videoya çökülüyor: {vid}")
        
        url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={vid}"
        cookies = {'sessionid': SESSION_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
                print(f"⚠️ Engel yedik: {r.status_code}")
        except:
            pass
        
        time.sleep(1)

if __name__ == "__main__":
    if not SESSION_ID:
        print("🚨 SESSION_ID YOK!")
    else:
        execute_attack()
