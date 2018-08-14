import datetime
import json
import random
import urllib
import traceback
import os
import re


ZATSUDAN_TOKEN = os.environ['ZATSUDAN_TOKEN']
ALL_TOKEN = os.environ['ALL_TOKEN']
MAIDNAME = os.environ['MAIDNAME']


ERROR_MESSAGE = '(ﾉД`)ご主人様助けて〜シクシク {} だよー'
OHAYO_MESSAGE = '＼（⌒∇⌒）／ おはようごさいます！ <@{}> 様'
OYASUMI_MESSAGE = '(｡･ω･｡)ﾉ おやすみなさいませ。 <@{}> 様'
OKAERI_MESSAGE = 'おかえりなさいませ！ <@{}> 様 （*´▽｀*）'
ITERA_MESSAGE = '(★･∀･)ﾉ〃行ってらっしゃいませ！ <@{}> 様'
OTSUKARE_MESSAGE = 'お疲れ様です。 <@{}> 様 ＼(^o^)／'
TERE_MESSAGES = ["ありがとう！ (〃'∇'〃)ゝｴﾍﾍ",
                 "そんなことないよ！（*´▽｀*）"]


def http_handler(event, contect):
    try:
        body = parse_body(event)
        if body.get('user_id') == 'USLACKBOT':
            return None  # 無限ループ対策
        if body.get('text') is None:
            return None
        if body.get('token') in ZATSUDAN_TOKEN.split(','):
            print('zatsudan token recieved:', body)
            result = zatsudan_main(body)
            if result:
                return message(result)
            else:
                respond(400, {'message': 'unsupported message'})
                
        if body.get('token') in ALL_TOKEN.split(','):
            print('all_message recieved:', body)
            result = all_main(body)
            if result:
                return message(result)
            else:
                respond(400, {'message': 'unsupported message'})

        

    except Exception as e:
        print(traceback.format_exc())
        return message(ERROR_MESSAGE.format(str(e)))


def parse_body(event):
   return {k: v for k, v in urllib.parse.parse_qsl(event['body'])}


def respond(status, res):
    print('respond:', res)
    return {
        'statusCode': status,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def message(text):
    return respond(200, {
        "text": text,
        "username": MAIDNAME,
        "icon_emoji": ":maidchan:"
    })
    

def in_keyword(text, *keyword):
    for k in keyword:
        if k in text:
            return True
    return False


def zatsudan_main(body):
    text = body['text']
    
    for suffix in ('どれがいいかな', 'どっちがいいかな', 'どれがいいかな？', 'どっちがいいかな？'):
        if text.endswith(suffix):
            selection = text[:-len(suffix)].replace('、', ' ').split()
            choosed = random.choice(selection)
            return 'どうしようかなあ。。。じゃあ {} が良いと思う！'.format(choosed)

    if ('かわいい' in text or '可愛い' in text) and MAIDNAME in text:
        return random.choice(TERE_MESSAGES)
        
    if text.startswith('占って！'):
        birthday = text[-4:]
        return uranai(body.get('user_id'), birthday)
    
    if in_keyword(text, 'おはよう', 'おはよー'):
        return OHAYO_MESSAGE.format(body.get('user_id'))
        
    if in_keyword(text, 'おやすみ'):
        return OYASUMI_MESSAGE.format(body.get('user_id'))

    if in_keyword(text, '帰', 'ただいま', 'きたく', 'かえる'):
        return OKAERI_MESSAGE.format(body.get('user_id'))

    if in_keyword(text, '疲', 'つかれ', '終', 'おわた', 'おわった'):
        return OTSUKARE_MESSAGE.format(body.get('user_id'))
        
    if in_keyword(text, '行ってきます', 'いってきます', '出かけ', '行きます', 'いきます', '出発'):
        return ITERA_MESSAGE.format(body.get('user_id'))
    
    if 'XXX' == text:
        # 例外テスト
        print(10/0)

    
def uranai(user_id, birthday):
    # The uranai() function is:
    #
    #    Copyright (c) 2016 beproud
    #    https://github.com/beproud/beproudbot
    today = datetime.date.today().strftime('%Y/%m/%d')
    response = urllib.request.urlopen('http://api.jugemkey.jp/api/horoscope/free/{}'.format(today))
    data = json.loads(response.read().decode('utf8'))
    month, day = int(birthday[:2]), int(birthday[2:])
    period = [20, 19, 21, 20, 21, 22, 23, 23, 23, 24, 22, 23]
    n = (month + 8 + (day >= period[(month - 1) % 12])) % 12
    d = data['horoscope'][today][n]
    for s in ['total', 'love', 'money', 'job']:
        d[s] = star(d[s])
    return """\
<@{}> 様の今日の運勢はこちらです！
{rank}位 {sign}
総合: {total}
恋愛運: {love}
金運: {money}
仕事運: {job}
ラッキーカラー: {color}
ラッキーアイテム: {item}
{content}""".format(user_id, **d)


def star(n):
    # The star() function is:
    #
    #    Copyright (c) 2016 beproud
    #    https://github.com/beproud/beproudbot
    return '★' * n + '☆' * (5 - n)


def all_main(body):
    text = body['text']
    
    if text.startswith('メイドちゃん！') and text.endswith('を褒めて！'):
        return plusplus(
            text[len('メイドちゃん！'):-len('を褒めて') - 1],
            body.get('user_id')
        )
        
def plusplus(text, user_id):
    who = ''
    for m in re.finditer('<(.+?)>', text):
        who += f'<{m.group(1)}>さん、'
    riyu = text
    for m in reversed(list(re.finditer('<(.+?)>', text))):
        riyu = riyu[0:m.start()] + riyu[m.end():]
    
    return who + riyu + 'すごーい！'