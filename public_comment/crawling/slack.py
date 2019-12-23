import channels
import datetime

def send(stack):
    now = datetime.datetime.now()#現在時刻
    now.strftime("%Y年%m月%d日%H時%M分")
    text = "*{}の新着情報*".format(now)
    for x in stack:
        text += x[0] + "¥n" + "https://search.e-gov.go.jp/servlet/" + x[1] + "¥n¥n"
    
    channels.send(text[:-1])
    

