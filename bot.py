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

def get_automatic_targets():
    """Hashtag sayfasından gerçek video ID'lerini kazır"""
    tags = ["kesfet", "fyp", "turkiye", "komedi"]
    selected_tag = random.choice(tags)
    url = f"https://www.tiktok.com/tag/{selected_tag}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        print(f"🔍 #{selected_tag} etiketinde kurban aranıyor...")
        r = requests.get(url, headers=headers, timeout=15)
        # Video linklerindeki ID'leri yakalıyoruz (Örn: /video/7345...)
        video_ids = re.findall(r'/video/(\[0-9]+)', r.text)
        
        if video_ids:
            return list(set(video_ids)) # Aynı ID'leri temizle
    except Exception as e:
        print(f"❌ Arama sırasında hata: {e}")
    
    return []

def attack():
    brain = load_brain()
    comment_text = "cok yalnızım 🇲🇽"
    
    targets = get_automatic_targets()
    
    if not targets:
        print("❌ Sahada canlı video bulunamadı, pusuda bekleniyor...")
        return

    print(f"🎯 {len(targets)} potansiyel hedef belirlendi.")

    for vid in targets:
        if vid in brain['learned_videos']:
            continue
            
        print(f"⚔️ Hedefe sızılıyor: {vid}")
        
        url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={vid}"
        cookies = {'sessionid': SESSION_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': f'https://www.tiktok.com/video/{vid}'
        }
        
        try:
            r = requests.post(url, cookies=cookies, data={'text': comment_text}, headers=headers)
            if r.status_code == 200:
                print(f"✅ MEKSİKA BAYRAĞI DİKİLDİ!")
                print(f"🔗 LİNK: https://www.tiktok.com/video/{vid}")
                
                brain['learned_videos'].append(vid)
                brain['total_comments'] += 1
                save_brain(brain)
                break # 2 dakikada bir çalıştığı için her turda 1 tane yeterli
            else:
                print(f"⚠️ TikTok kapıyı kapattı (Hata: {r.status_code})")
                if r.status_code == 403: print("🚨 SessionID patlamış olabilir!")
        except:
            print("💥 Bağlantı koptu.")
        
        time.sleep(2)

if __name__ == "__main__":
    if not SESSION_ID:
        print("🚨 TIKTOK_SESSION bulunamadı!")
    else:
        attack()
