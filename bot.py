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

def get_mobile_foryou():
    """Botu iPhone gibi gösterip gerçek keşfete sızar"""
    print("📱 iPhone 15 Modu: Keşfet akışına sızılıyor...")
    
    # Gerçek bir mobil cihazın gönderdiği başlıklar
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
    }

    try:
        # Mobil keşfet URL'sini zorluyoruz
        url = "https://www.tiktok.com/foryou?is_copy_url=1&is_from_webapp=v1"
        response = requests.get(url, headers=headers, timeout=20)
        
        # Sayfa içinden taze video ID'lerini cımbızla al
        video_ids = re.findall(r'video/(\d{18,20})', response.text)
        
        if video_ids:
            found = list(set(video_ids))
            print(f"✅ Mobilden {len(found)} tane canlı video yakalandı!")
            return found
        else:
            print("❌ Mobil kapı da kilitli görünüyor, TikTok GitHub'ı yemiyor.")
            return []
    except Exception as e:
        print(f"💥 Bağlantı hatası: {e}")
        return []

def attack():
    brain = load_brain()
    comment_text = "be 🇲🇽"
    
    targets = get_mobile_foryou()
    
    if not targets:
        print("💀 Hedef bulunamadı. Beklemedeyiz.")
        return

    for vid in targets:
        if vid in brain['learned_videos']:
            continue
            
        print(f"⚔️ iPhone Moduyla Sızılıyor: {vid}")
        
        url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={vid}"
        cookies = {'sessionid': SESSION_ID}
        
        # Yorum atarken de mobil gibi davranıyoruz
        attack_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
            'Origin': 'https://www.tiktok.com',
            'Referer': f'https://www.tiktok.com/video/{vid}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            r = requests.post(url, cookies=cookies, data={'text': comment_text}, headers=attack_headers)
            if r.status_code == 200:
                print(f"✅ MEKSİKA BAYRAĞI DİKİLDİ! 🇲🇽")
                print(f"🔗 LİNK: https://www.tiktok.com/video/{vid}")
                
                brain['learned_videos'].append(vid)
                brain['total_comments'] += 1
                save_brain(brain)
                break 
            else:
                print(f"⚠️ Engel: {r.status_code}")
        except:
            pass
        
        time.sleep(2)

if __name__ == "__main__":
    if not SESSION_ID:
        print("🚨 SESSION_ID EKSİK AGA!")
    else:
        attack()
