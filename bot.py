# -*- coding: utf-8 -*-
import os, requests, random, time, json

SESSION_ID = os.getenv('TIKTOK_SESSION')

def load_brain():
    if os.path.exists('brain.json'):
        with open('brain.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"learned_videos": [], "total_comments": 0}

def save_brain(brain):
    with open('brain.json', 'w', encoding='utf-8') as f:
        json.dump(brain, f, indent=4, ensure_ascii=False)

def analyze_and_attack():
    brain = load_brain()
    comment_text = "cok yalnızım  🇲🇽"
    
    # BURAYA GERÇEK VİDEO ID'LERİNİ YAZMAN LAZIM AGA
    # TikTok'ta gördüğün videonun linkindeki uzun rakamları buraya ekle
    target_videos = ["7419283746501928374"] 

    for vid in target_videos:
        if vid in brain['learned_videos']:
            print(f"--- BU VİDEOYA ZATEN YORUM ATMIŞIZ AGA: {vid}")
            continue
            
        url = f"https://www.tiktok.com/api/comment/publish/?aweme_id={vid}"
        cookies = {'sessionid': SESSION_ID}
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.tiktok.com/'
        }
        
        try:
            r = requests.post(url, cookies=cookies, data={'text': comment_text}, headers=headers)
            if r.status_code == 200:
                # İŞTE BURASI KRİTİK: LİNKİ SANA VERİYOR
                print(f"🚀 MEKSİKA BAYRAĞI DİKİLDİ!")
                print(f"🔗 VİDEO LİNKİ: https://www.tiktok.com/video/{vid}")
                
                brain['learned_videos'].append(vid)
                brain['total_comments'] += 1
                save_brain(brain)
                time.sleep(random.randint(30, 60))
            else:
                print(f"❌ Hata: TikTok izin vermedi. Status: {r.status_code}")
        except Exception as e:
            print(f"💥 Sistem patladı: {e}")

if __name__ == "__main__":
    if not SESSION_ID:
        print("SECRET'I EKLEMEMİŞSİN AGA!")
    else:
        analyze_and_attack()
