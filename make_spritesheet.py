from PIL import Image
from pprint import pprint
from io import BytesIO
import requests
import urllib.parse
import os.path

SHEET_SMALL_LST = [
    'grinning',
    'grimacing',
    'grin',
    'joy',
    'smiley',
    'smile',
    'sweat_smile',
    'laughing',
    'innocent',
    'wink',
    'blush',
    'slight_smile',
    'upside_down',
    'relaxed',
    'yum',
    'relieved',
    'heart_eyes',
    'kissing_heart',
    'kissing',
    'kissing_smiling_eyes',
    'kissing_closed_eyes',
    'stuck_out_tongue_winking_eye',
    'stuck_out_tongue_closed_eyes',
    'stuck_out_tongue',
    'money_mouth',
    'nerd',
    'sunglasses',
    'hugging',
    'smirk',
    'no_mouth',
    'neutral_Face',
    'expressionless',
    'unamused',
    'rolling_eyes',
    'thinking',
    'flushed',
    'disappointed',
    'worried',
    'angry',
    'rage',
    'pensive',
    'confused',
    'slight_frown',
    'frowning2',
    'persevere',
    'confounded',
    'tired_face',
    'weary',
    'triumph',
    'open_mouth',
]

SHEET_LARGE_LST = SHEET_SMALL_LST + [
    'scream',
    'fearful',
    'cold_sweat',
    'hushed',
    'frowning',
    'anguished',
    'cry',
    'disappointed_relieved',
    'sleepy',
    'sweat',
    'sob',
    'dizzy_face',
    'astonished',
    'zipper_mouth',
    'mask',
    'thermometer_face',
    'head_bandage',
    'sleeping',
    'zzz',
    'poop',
    'smiling_imp',
    'imp',
    'japanese_ogre',
    'japanese_goblin',
    'skull',
    'ghost',
    'alien',
    'robot',
    'smiley_cat',
    'smile_cat',
    'joy_cat',
    'heart_eyes_cat',
    'smirk_cat',
    'kissing_cat',
    'scream_cat',
    'crying_cat_face',
    'pouting_cat',
]


def left(st: str, marker: str) -> str:
    return st.split(marker, 1)[0]


def right(st: str, marker: str) -> str:
    return st.rsplit(marker, 1)[1]


URLS = {}

with open('GoogleEmoji.css') as css:
    css = list(css)
    for ind, line in enumerate(css):
        if 'content: url' not in line:
            continue

        line = right(line, 'content: url(')
        url, emoji = line.split('); } /* ')

        if '->' in emoji:
            emoji = left(emoji, '->').strip()
        else:
            emoji = left(emoji, '*/').strip()

        if ' ' in emoji or '-' in emoji:
            continue

        filename = os.path.basename(urllib.parse.urlparse(url).path)

        cache_path = 'cache/' + filename

        try:
            f = open(cache_path, 'rb')
        except FileNotFoundError:
            print('Getting {}/{}: "{}"'.format(ind, len(css), filename))
            data = URLS[emoji] = requests.get(url).content
            with open(cache_path, 'wb') as f:
                f.write(data)
        else:
            with f:
                URLS[emoji] = f.read()

URLS['smiley'] = URLS['grinning']
URLS['kissing'] = URLS['kissing_heart']

SIZE = 44

for lst, filename, url in [
    (SHEET_SMALL_LST, 'discord_emoji_small', 'https://discordapp.com/assets/4e51af83c4879cf313ad553bdc20dcf7.png'),
    (SHEET_LARGE_LST, 'discord_emoji_large', 'https://discordapp.com/assets/f24711dae4f6d6b28335e866a93e9d9b.png'),
]:
    print('Getting "{}"...'.format(url))
    sheet = Image.open(BytesIO(requests.get(url).content))
    sheet.load()
    cols = sheet.width // SIZE
    rows = sheet.height // SIZE
    print('{} rows, {} cols'.format(rows, cols))
    for ind, name in enumerate(lst):
        try:
            data = BytesIO(URLS[name])
        except KeyError:
            print('"{}" not in list!'.format(name))
            continue

        img = Image.open(data).resize((SIZE, SIZE), resample=Image.LANCZOS)

        sheet.paste(img, (ind % cols * SIZE, ind // cols * SIZE))

    sheet.save(filename + '.png')
