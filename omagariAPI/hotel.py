import requests
import time

# あなたのDiscordのURL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1518666519750639756/KGqpvX5TgK8R2Snvf6bF5VhMJhb9WYAaQHieQpkSxzG1ezaF3EzA17NuDSb_rl5ifMnp"

# 🔑 あなたのアプリケーションID（クライアントID）
RAKUTEN_CLIENT_ID = "0d0c8208-34a7-4650-8723-f7bfbf47df83"

# 🔑【ここに入力】あなたのシークレットID（アクセスキー：●●●で隠れていた英数字）
RAKUTEN_CLIENT_SECRET = "pk_fws4ZFqfEjYbogaUJFidO05X1yRe9L4U7pkXk5pl4VH"

def check_rakuten_api_v2_final():
    areas = [
        {"name": "大曲・角館・田沢湖", "middle": "akita", "small": "omagari"},
        {"name": "秋田市周辺", "middle": "akita", "small": "akita"},
        {"name": "盛岡・雫石", "middle": "iwate", "small": "morioka"}
    ]
    
    # 新システム（ハイフン付きID・シークレット）の本当の接続先URL
    url = "https://rakuten-travel.p.rapidapi.com/vacantHotelSearch"
    
    # 2つの鍵（IDとシークレット）を正しくセットした公式ヘッダー
    headers = {
        "X-RapidAPI-Key": RAKUTEN_CLIENT_SECRET,  # シークレット（アクセスキー）はここに入ります
        "X-RapidAPI-Host": "rakuten-travel.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    print("🔄 楽天公式API v2（正式URL・2鍵認証モード）を開始します...")
    
    for area in areas:
        print(f" 🔍 API確認: {area['name']} エリア...")
        
        params = {
            "largeClassCode": "japan",
            "middleClassCode": area["middle"],
            "smallClassCode": area["small"],
            "checkinDate": "2026-08-29",   # 2026年大曲花火大会当日
            "checkoutDate": "2026-08-30",
            "adultNum": 2,
            "applicationId": RAKUTEN_CLIENT_ID # ID（クライアントID）はこちらに入ります
        }
        
        try:
            # ⭕ timeout=25 に伸ばし、混雑時のサーバーの返答をじっくり待ちます！
            response = requests.get(url, headers=headers, params=params, timeout=25)
            
            if response.status_code == 200:
                data = response.json()
                
                if "hotels" in data and data["hotels"]:
                    message = f"🚨【公式API速報】{area['name']}に空室が出ました！\n"
                    for h in data["hotels"]:
                        info = h["hotel"][0]["hotelBasicInfo"]
                        message += f"🏨 {info['hotelName']}\n🔗 {info['hotelInformationUrl']}\n\n"
                        
                    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
                    print(f"  👉 【空室あり】Discordに公式通知を送信しました！")
                else:
                    print(f"  ❌ 現在、空室はありません。")
                    
            elif response.status_code == 404 or response.status_code == 400:
                print(f"  ❌ 現在、空室はありません。")
            else:
                print(f"  ⚠ 楽天APIから返答（ステータス: {response.status_code}）: {response.text}")
                
        except Exception as e:
            print(f"  ⚠ 通信エラーが発生しました: {e}")
            
        time.sleep(10)

# 実行
check_rakuten_api_v2_final()