import os
import requests
import locale
import logging
from json import JSONDecodeError
import base64

# This code example demonstrates how to convert HTML document to PNG images.


from django.http import HttpResponse
from .images import UNKNOWN, UNRATED, BRONZE, SILVER, GOLD, PLATINUM, DIAMOND, RUBY, MASTER, PER, FORK, STAR
from django.urls import reverse
from django.shortcuts import render

import cairosvg
import pygal
from pygal.style import Style
from .models import User

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

logger = logging.getLogger('testlogger')

def test(request):
    users = User.objects.all()
    return render(request, 'index.html', {"users": users})

def svg_to_base64(svg_code):
    png_data = cairosvg.svg2png(bytestring=svg_code)
    # PNG를 base64 문자열로 인코딩
    b64_data = base64.b64encode(png_data).decode('utf-8')
    image_url = f"data:image/png;base64,{b64_data}"
    return image_url

def svg_chart(request):
    custom_style = Style(
        background='transparent',
        plot_background='transparent',
        major_guide_stroke_dasharray='#FFFFFF',
        guide_stroke_dasharray='#FFFFFF',
        foreground_subtle='#FFFFFF',
        foreground_strong='#FFFFFF',
        foreground='#FFFFFF',
        colors=('#FFC1C1', '#E8537A', '#E95355', '#E87653', '#E89B53', '#E89B53', '#E89B53', '#E89B53'),
        guides=('#FFFFFF'),
        guide_stroke_color = 'white',
        major_guide_stroke_color = 'white',
        opacity = '1',
        major_label_font_size = 20,
    )
    radar_chart = pygal.Radar(width=520,height=500,show_major_y_labels=False,show_minor_y_labels=False,y_labels_major_every=2,fill=True,style=custom_style,show_legend=False)
    radar_chart.x_labels = ['', '', '', '', '', '']
    radar_chart.add('Exp', [6395, 8212, 7520, 7218, 12464, 1660])
    chartspider = radar_chart.render()

    response = svg_to_base64(chartspider)

    return response
    
def svg_chart2(request):
    custom_style = Style(
        background='#000000',
        plot_background='transparent',
        major_guide_stroke_dasharray='#FFFFFF',
        guide_stroke_dasharray='#FFFFFF',
        foreground_subtle='#FFFFFF',
        foreground_strong='#FFFFFF',
        foreground='#FFFFFF',
        colors=('#FFC1C1', '#E8537A', '#E95355', '#E87653', '#E89B53', '#E89B53', '#E89B53', '#E89B53'),
        guides=('#FFFFFF'),
        guide_stroke_color = 'white',
        major_guide_stroke_color = 'white',
        opacity = '1',
        major_label_font_size = 20,
    )
    radar_chart = pygal.Radar(width=520,height=500,show_major_y_labels=False,show_minor_y_labels=False,y_labels_major_every=2,fill=True,style=custom_style,show_legend=False)
    radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp']
    radar_chart.add('Exp', [6395, 8212, 7520, 7218, 12464, 1660])
    chartspider = radar_chart.render()

    response = HttpResponse(content_type='image/svg+xml')
    response.write(chartspider)
    
    return response
# Create your views here.
TIERS = (
    "Unrated",
    "Bronze 5", "Bronze 4", "Bronze 3", "Bronze 2", "Bronze 1",
    "Silver 5", "Silver 4", "Silver 3", "Silver 2", "Silver 1",
    "Gold 5", "Gold 4", "Gold 3", "Gold 2", "Gold 1",
    "Platinum 5", "Platinum 4", "Platinum 3", "Platinum 2", "Platinum 1",
    "Diamond 5", "Diamond 4", "Diamond 3", "Diamond 2", "Diamond 1",
    "Ruby 5", "Ruby 4", "Ruby 3", "Ruby 2", "Ruby 1",
    "Master"
)

BACKGROUND_COLOR = {
    'Unknown': ['#AAAAAA', '#666666', '#000000'],
    'Unrated': ['#666666', '#2D2D2D', '#040202'],
    'Bronze': ['#F49347', '#984400', '#492000'],
    'Silver': ['#939195', '#6B7E91', '#1F354A'],
    'Gold': ['#27262A', '#27262A', '#27262A'],
    'Platinum': ['#8CC584', '#45B2D3', '#51A795'],
    'Diamond': ['#96B8DC', '#3EA5DB', '#4D6399', ],
    'Ruby': ['#E45B62', '#E14476', '#CA0059'],
    'Master': ['#83f8fe', '#b297fc', '#fc7ea8'],
}

TIER_IMG_LINK = {
    'Unknown': UNKNOWN,
    'Unrated': UNRATED,
    'Bronze': BRONZE,
    'Silver': SILVER,
    'Gold': GOLD,
    'Platinum': PLATINUM,
    'Diamond': DIAMOND,
    'Ruby': RUBY,
    'Master': MASTER,

}

IMG = {
    'Per' : PER,
    'Star': STAR,
    'Fork': FORK,
}

TIER_RATES = (
    0, # unranked
    30, 60, 90, 120, 150, # bronze
    200, 300, 400, 500, 650, # silver
    800, 950, 1100, 1250, 1400, # gold
    1600, 1750, 1900, 2000, 2100, # platinum
    2200, 2300, 2400, 2500, 2600, # diamond
    2700, 2800, 2850, 2900, 2950, # ruby
    3000 # master
)

class UrlSettings(object):
    def __init__(self, request, MAX_LEN):
        self.api_server = 'https://api.github.com/repos'
        self.name_handle = request.GET.get("name", "eunjineee")
        self.repo_handle = request.GET.get("repo", "RepomonCard")
        self.repo_information_url = self.api_server + '/' + self.name_handle + '/' + self.repo_handle
        # print('🎀')
        # print(self.repo_information_url)


class BojDefaultSettings(object):
    def __init__(self, request, url_set):
        try:
            self.json = requests.get(url_set.repo_information_url).json()
            print(self.json)
            self.rating = self.json['rating']
            self.level = self.boj_rating_to_lv(self.json['rating'])
            self.solved = '{0:n}'.format(self.json['solvedCount'])
            self.boj_class = self.json['class']
            self.boj_class_decoration = ''
            if self.json['classDecoration'] == 'silver':
                self.boj_class_decoration = '+'
            elif self.json['classDecoration'] == 'gold':
                self.boj_class_decoration = '++'

            self.my_rate = self.json['rating']
            if self.level == 31:
                self.prev_rate = TIER_RATES[self.level]
                self.next_rate = TIER_RATES[self.level]
                self.percentage = 100
            else:
                self.prev_rate = TIER_RATES[self.level]
                self.next_rate = TIER_RATES[self.level+1]
                self.percentage = round(
                    (self.my_rate - self.prev_rate) * 100 / (self.next_rate - self.prev_rate))
            self.bar_size = 35 + 2.55 * self.percentage

            self.needed_rate = '{0:n}'.format(self.next_rate)
            self.now_rate = '{0:n}'.format(self.my_rate)
            self.rate = '{0:n}'.format(self.my_rate)

            if TIERS[self.level] == 'Unrated' or TIERS[self.level] == 'Master':
                self.tier_title = TIERS[self.level]
                self.tier_rank = ''
            else:
                self.tier_title, self.tier_rank = TIERS[self.level].split()
        except JSONDecodeError as e:
            logger.error(e)
            self.tier_title = "Unknown"
            url_set.boj_handle = 'Unknown'
            self.tier_rank = ''
            self.solved = '0'
            self.boj_class = '0'
            self.boj_class_decoration = ''
            self.rate = '0'
            self.now_rate = '0'
            self.needed_rate = '0'
            self.percentage = '0'
            self.bar_size = '35'
            self.per = 'per'

    def boj_rating_to_lv(self, rating):
        if rating < 30: return 0
        if rating < 150: return rating // 30
        if rating < 200: return 5
        if rating < 500: return (rating-200) // 100 + 6
        if rating < 1400: return (rating-500) // 150 + 9
        if rating < 1600: return 15
        if rating < 1750: return 16
        if rating < 1900: return 17
        if rating < 2800: return (rating-1900) // 100 + 18
        if rating < 3000: return (rating-2800) // 50 + 27
        return 31


def generate_badge(request):
    MAX_LEN = 15
    per = IMG['Per']
    star = IMG['Star']
    fork = IMG['Fork']
    url_set = UrlSettings(request, MAX_LEN)
    handle_set = BojDefaultSettings(request, url_set)
    svg = '''
    <!DOCTYPE svg PUBLIC
        "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg height="200" width="600"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xml:space="preserve">
    <style type="text/css">
    <frame-options policy="SAMEORIGIN"/>
        <![CDATA[
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=block');
            @keyframes fadeIn {{
                0%{{
                    opacity:0
                }}
                100%{{
                    opacity:1
                }}
            }}
            @keyframes delayFadeIn {{
                0%{{
                    opacity:0
                }}
                80%{{
                    opacity:0
                }}
                100%{{
                    opacity:1
                }}
            }}
            @keyframes rateBarAnimation {{
                0% {{
                    stroke-dashoffset: {bar_size};
                }}
                70% {{
                    stroke-dashoffset: {bar_size};
                }}
                100%{{
                    stroke-dashoffset: 35;
                }}
            }}
            .background {{
                fill: url(#grad);
            }}
            text {{
                fill: white;
                font-family: 'Noto Sans KR', sans-serif;
            }}
            text.boj-handle {{
                font-weight: 700;
                font-size: 1.30em;
                animation: fadeIn 1s ease-in-out forwards;

            }}
            text.tier-text {{
                font-weight: 700;
                font-size: 1.45em;
                opacity: 55%;
            }}
            .repo-exp {{
                fill: #000000;
                font-size: 0.8em;
                font-weight: 700;
                text-anchor: middle;
                animation: delayFadeIn 1.8s ease-in-out forwards;
            }}
            .subtitle {{
                font-weight: 500;
                font-size: 0.7em;
            }}
            .value {{
                font-weight: 400;
                font-size: 0.7em;
            }}
            .percentage {{
                font-weight: 300;
                font-size: 0.8em;
            }}
            .progress {{
                font-size: 0.7em;
            }}
            .item {{
                opacity: 0;
                animation: delayFadeIn 2s ease-in-out forwards;
            }}
            .repomon-img {{
                animation: delayFadeIn 1s ease-in-out forwards;
            }}
            .repo-detail {{
                font-size: 0.8em;
                animation: fadeIn 1.5s ease-in-out forwards;
            }}
            .lang-tag {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }}
            .charttitle {{
                font-size: 0.4em;
            }}
        ]]>
    </style>
<frame-options policy="SAMEORIGIN"/>
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="35%">
            <stop offset="10%" style="stop-color:{color1};stop-opacity:1">
                <animate attributeName="stop-opacity" values="0.7; 0.73; 0.9 ; 0.97; 1; 0.97; 0.9; 0.73; 0.7;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="55%" style="stop-color:{color2};stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.95; 0.93; 0.95; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="100%" style="stop-color:{color3};stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.97; 0.9; 0.83; 0.8; 0.83; 0.9; 0.97; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
        </linearGradient>
    </defs>
    <rect width="600" height="200" rx="10" ry="10" class="background"/>
    
    <text x="190" y="43" class="boj-handle"><!-- 주석{boj_handle} -->아이유정</text>
    <image href="{per}" x="290" y="32" height="13px" width="10px"/><text x="306" y="42" font-size="0.7em">6</text><text x="330" y="42" font-size="0.7em">23.04.20~23.04.27</text>
    <image href="{star}" x="500" y="10" width="12px"/><text x="516" y="20" font-size="0.7em">257</text>
    <image href="{fork}" x="546" y="10" width="9px"/><text x="560" y="20" font-size="0.7em">3.2k</text>
        <text x="190" y="66" class="repo-detail">자녀가 있는 학부모를 위한 부동산 추천 서비스</text>
    <image href="{tier_img_link}" x="18" y="12" height="160px" width="160px" class="repomon-img"/>
    <line x1="40" y1="170" x2="150" y2="170" stroke-width="20" stroke="floralwhite" stroke-linecap="round"/>
    <text x="100" y="175" dz="-20" class="repo-exp"><!-- 주석{tier_rank} -->Exp | 156132</text>
    <g class="item" style="animation-delay: 200ms">
        <text x="190" y="120" class="subtitle">Total Commit</text><text x="270" y="120" class="rate value"><!-- 주석{rate} -->17872 회</text>
    </g>
    <g class="item" style="animation-delay: 400ms">
        <text x="190" y="140" class="subtitle">Total code</text><text x="270" y="140" class="solved value"><!-- 주석{solved} -->127322 줄</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="190" y="160" class="subtitle">Security</text><text x="260" y="160" class="class value"></text>
        <line x1="270" y1="157" x2="290" y2="157" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="270" y1="157" x2="360" y2="157" stroke-width="10" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="190" y="180" class="subtitle">Efficiency</text><text x="260" y="160" class="class value"></text>
        <line x1="270" y1="177" x2="290" y2="177" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="270" y1="177" x2="360" y2="177" stroke-width="10" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
    </g>
    <g transform="translate(190, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/HTML5-E34F26.svg?&amp;style=for-the-badge&amp;logo=HTML5&amp;logoColor=white"/>
    </g>
    <g transform="translate(230, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/JavaScriipt-F7DF1E.svg?&amp;style=for-the-badge&amp;logo=JavaScript&amp;logoColor=black"/>
    </g>
    <g transform="translate(290, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/CSS3-1572B6.svg?&amp;style=for-the-badge&amp;logo=CSS3&amp;logoColor=white"/>
    </g>
    <image href="{chartjjin}" x="425" y="35" height="160px" class="repomon-img"/>
    <text x="505" y="35" class="charttitle">커밋</text>
    <text x="580" y="70" class="charttitle">머지</text>
    <text x="430" y="70" class="charttitle">이슈</text>
    <text x="430" y="145" class="charttitle">리뷰</text>
    <text x="580" y="145" class="charttitle">효율성</text>
    <text x="505" y="180" class="charttitle">보안성</text>
</svg>
    '''.format(color1=BACKGROUND_COLOR[handle_set.tier_title][0],
               color2=BACKGROUND_COLOR[handle_set.tier_title][1],
               color3=BACKGROUND_COLOR[handle_set.tier_title][2],
               boj_handle=url_set.boj_name,
               tier_rank=('M' if handle_set.tier_title == 'Master' else handle_set.tier_rank),
               tier_img_link=TIER_IMG_LINK[handle_set.tier_title],
               solved=handle_set.solved,
               boj_class=handle_set.boj_class,
               boj_class_decoration=handle_set.boj_class_decoration,
               rate=handle_set.rate,
               now_rate=handle_set.now_rate,
               needed_rate=handle_set.needed_rate,
               percentage=handle_set.percentage,
               bar_size=handle_set.bar_size,
               per=per,
               star=star,
               fork=fork,
               chartjjin=svg_chart(handle_set.rate)
               )



    logger.info('[/generate_badge/v2] user: {}, tier: {}'.format(url_set.boj_name, handle_set.tier_title))
    response = HttpResponse(content=svg)
    response['Content-Type'] = 'image/svg+xml'
    response['Cache-Control'] = 'max-age=3600'

    return response
