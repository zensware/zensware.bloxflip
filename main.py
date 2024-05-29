import json, os, time, requests, cloudscraper
from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_enable = os.getenv['webhook_enabled']
webhookurl = os.getenv['webhook']
winnotif = os.getenv['windows_notification']
minimum = os.getenv['minimum_amount']
ping = os.getenv['webhook_ping']
refresh = os.getenv['refresh_rate']

if webhook_enable == True:
  webhook = DiscordWebhook(url=webhookurl, content=f"{ping}")

while True:
    try:
        scraper = cloudscraper.create_scraper()
        r = scraper.get('https://api.bloxflip.com/chat/history').json()
        check = r['rain']
        if check['active'] == True:
            if check['prize'] >= minimum:
                grabprize = str(check['prize'])[:-2]
                prize = (format(int(grabprize),","))
                host = check['host']
                getduration = check['duration']
                created = check['created']
                umduration = getduration + created
                eduration = umduration/1000
                duration = round(eduration)
                convert = (getduration/(1000*60))%60
                waiting = (convert*60+10)
                sent = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(int(time.time())))
                print(f"Bloxflip Rain!\nRain amount: {prize} R$\nExpiration: {duration} minutes\nHost: {host}\nTimestamp: {sent}\n\n")
                userid = requests.post(f"https://users.roblox.com/v1/usernames/users", json={"usernames": [host]}).json()['data'][0]['id']
                thumburl = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=50x50&format=Png&isCircular=false").json()['data'][0]['imageUrl']
                if webhook_enable == True:
                    embed = DiscordEmbed(title=f"{host} is hosting a chat rain!", url="https://bloxflip.com", color=0xFFC800)
                    embed.add_embed_field(name="Rain Amount", value=f"{prize} R$")
                    embed.add_embed_field(name="Expiration", value=f"<t:{duration}:R>")
                    embed.add_embed_field(name="Host", value=f"[{host}](https://www.roblox.com/users/{userid}/profile)")
                    embed.set_timestamp()
                    embed.set_thumbnail(url=thumburl)
                    webhook.add_embed(embed)
                    webhook.execute()
                    webhook.remove_embed(0)    
            else:
                time.sleep(130)
            time.sleep(waiting)
        elif check['active'] == False:
          time.sleep(refresh)
    except Exception as e:
        print(e)
        time.sleep(refresh)
