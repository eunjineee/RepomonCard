import requests
import locale
import logging
from json import JSONDecodeError
import base64

# This code example demonstrates how to convert HTML document to PNG images.


from django.http import HttpResponse
from .images import PER, FORK, STAR, POCKET, img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16,img17,img18,img19,img20,img21,img22,img23,img24,img25,img26,img27,img28,img29,img30

import cairosvg
import pygal
from pygal.style import Style

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

logger = logging.getLogger('testlogger')


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
        colors=('#989DFA', '#E8537A', '#E95355', '#E87653', '#E89B53', '#E89B53', '#E89B53', '#E89B53'),
        guides=('#FFFFFF'),
        guide_stroke_color = 'white',
        major_guide_stroke_color = 'white',
        opacity = '0.9',
        major_label_font_size = 20,
    )
    radar_chart = pygal.Radar(width=520,height=500,show_major_y_labels=False,show_minor_y_labels=False,y_labels_major_every=2,fill=True,style=custom_style,show_legend=False)
    radar_chart.x_labels = ['', '', '', '', '', '']
    radar_chart.add('Exp', request)
    chartspider = radar_chart.render()

    response = svg_to_base64(chartspider)

    return response

def svg_chart_personal(request, request2):
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
        opacity = '0.9',
        major_label_font_size = 20,
    )
    radar_chart = pygal.Radar(width=520,height=500,show_major_y_labels=False,show_minor_y_labels=False,y_labels_major_every=2,fill=True,style=custom_style,show_legend=False)
    radar_chart.x_labels = ['', '', '', '', '', '']
    radar_chart.add('Exp', request)
    radar_chart.add('My Exp', request2)
    chartspider = radar_chart.render()

    response = svg_to_base64(chartspider)

    return response


# Create your views here.
IMG = {
    'Per' : PER,
    'Star': STAR,
    'Fork': FORK,
    'pocket': POCKET,
    'img1': img1,
    'img2': img2,
    'img3': img3,
    'img4': img4,
    'img5': img5,
    'img6': img6,
    'img7': img7,
    'img8': img8,
    'img9': img9,
    'img10': img10,
    'img11': img11,
    'img12': img12,
    'img13': img13,
    'img14': img14,
    'img15': img15,
    'img16': img16,
    'img17': img17,
    'img18': img18,
    'img19': img19,
    'img20': img20,
    'img21': img21,
    'img22': img22,
    'img23': img23,
    'img24': img24,
    'img25': img25,
    'img26': img26,
    'img27': img27,
    'img28': img28,
    'img29': img29,
    'img30': img30,
}

ELLIPSE_TYPE = {
    1 : 'elli1',
    2 : 'elli2',
    3 : 'elli3',
}

class UrlSettings(object):
    def __init__(self, request, repo_type):
        if repo_type == 'repo':
            print('🎨',repo_type)
            self.api_server = 'https://repomon.kr/api/v1/repo/'
            self.repo_handle = request.GET.get("repoId", "5")
            self.repo_information_url = self.api_server + '{' +'repoId' + '}' + '/card/detail?repoId=' + self.repo_handle
            print('🎨',self.repo_information_url)
        elif repo_type == 'repo_personal':
            print('🎨',repo_type)
            self.api_server = 'https://repomon.kr/api/v1/repo/'
            self.repo_handle = request.GET.get("repoId", "1")
            self.user_handle = request.GET.get("userId", "1")
            self.repo_information_url = self.api_server + '{' +'repoId' + '}' + '/card/personal?repoId=' + self.repo_handle + '&userId=' + self.user_handle
            print('🎨🖼',self.repo_information_url)
        elif repo_type == 'user':
            print('🎨',repo_type)
            self.api_server = 'https://repomon.kr/api/v1/repo/'
            self.repo_handle = request.GET.get("repoId", "5")
            self.repo_information_url = self.api_server + '{' +'repoId' + '}' + '/card/detail?repoId=' + self.repo_handle
            print('🎨🖼',self.repo_information_url)
    

class RepoDefaultSettings(object):
    def __init__(self, request, url_set):
        try:
            self.json = requests.get(url_set.repo_information_url).json()
            print('🎀')
            print(self.json)
            self.repoName = self.json['repoName']
            self.repoDescription = self.is_none(self.json['repoDescription'])
            self.repoExp = self.json['repoExp']
            self.starCnt = self.json['starCnt']
            self.forkCnt = self.json['forkCnt']
            self.repoStart = self.day(self.json['repoStart'])
            self.repoEnd = self.day(self.json['repoEnd'])
            self.languages = self.json['languages']
            self.contributers = self.json['contributers']
            self.commits = self.json['commits']
            self.issues = self.json['issues']
            self.merges = self.json['merges']
            self.reviews = self.json['reviews']
            self.efficiency = int(self.json['efficiency'])
            self.efficiency_percent = self.percent(self.json['efficiency'])
            self.security = int(self.json['security'])
            self.security_percent = self.percent(self.json['security'])
            self.totalcommit = self.json['totalcommit']
            self.totalcode = self.json['totalcode']
            print(self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security)
            self.chart = svg_chart([self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security])
    
        except JSONDecodeError as e:
            logger.error(e)
            self.repoName = '레포몬'
            self.repoDescription = '나의 레포몬을 불러보세요'
            self.repoExp = '123456'
            self.starCnt = '7'
            self.forkCnt = '66'
            self.repoStart = '23.03.10'
            self.repoEnd = '23.04.20'
            self.languages = ''
            self.contributers = '6'
            self.commits = 543 
            self.issues = 123
            self.merges = 321
            self.reviews = 123
            self.efficiency = 80
            self.efficiency_percent = 80
            self.security = 80
            self.security_percent = 80
            self.totalcommit = '123456'
            self.totalcode = '654321'
            self.chart = svg_chart([self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security])

    def day(self, day):
        if day != None:
            new_day = str(day[2:4])+'.'+str(day[5:7])+'.'+str(day[8:10]) 
            return new_day
        else:
            return ''
        
    def percent(self, num):
        percent = round(num/100*90)
        return percent
    
    def is_none(self, data):
        if data == None:
            return ''
        else:
            return data


def repo_card(request):
    per = IMG['Per']
    star = IMG['Star']
    fork = IMG['Fork']
    img = IMG['Img']
    url_set = UrlSettings(request, 'repo')
    print(url_set)
    handle_set = RepoDefaultSettings(request, url_set)
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
            .repo-percent {{
                fill: #000000;
                font-size: 0.6em;
                font-weight: 700;
                text-anchor: middle;
            }}
        ]]>
    </style>
<frame-options policy="SAMEORIGIN"/>
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="35%">
            <stop offset="10%" style="stop-color:'#AAAAAA';stop-opacity:1">
                <animate attributeName="stop-opacity" values="0.7; 0.73; 0.9 ; 0.97; 1; 0.97; 0.9; 0.73; 0.7;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="55%" style="stop-color:'#666666';stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.95; 0.93; 0.95; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="100%" style="stop-color:'#000000';stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.97; 0.9; 0.83; 0.8; 0.83; 0.9; 0.97; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
        </linearGradient>
    </defs>
    <rect width="600" height="200" rx="10" ry="10" class="background"/>
    
    <image href="{img}" x="16" y="12" height="160px" width="160px" class="repomon-img"/>
    <line x1="40" y1="170" x2="150" y2="170" stroke-width="20" stroke="floralwhite" stroke-linecap="round"/>
    <text x="100" y="175" dz="-20" class="repo-exp">Exp | {repoExp}</text>

    <text x="190" y="40" class="boj-handle">{repoName}</text>
    <image href="{per}" x="300" y="30" height="13px" width="10px"/><text x="313" y="41" font-size="0.7em">{contributers}</text>
    <text x="335" y="41" font-size="0.7em">{repoStart} ~ {repoEnd}</text>

    <image href="{star}" x="515" y="11" width="11px"/><text x="530" y="20" font-size="0.6em">{starCnt}</text>
    <image href="{fork}" x="550" y="11" width="8px"/><text x="563" y="20" font-size="0.6em">{forkCnt}</text>
        <text x="190" y="60" class="repo-detail">{repoDescription}</text>

    <g class="item" style="animation-delay: 200ms">
        <text x="190" y="120" class="subtitle">Total Commit</text><text x="270" y="120" class="rate value">{totalcommit} 회</text>
    </g>
    <g class="item" style="animation-delay: 400ms">
        <text x="190" y="140" class="subtitle">Total code</text><text x="270" y="140" class="solved value">{totalcode} 줄</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="190" y="160" class="subtitle">Security</text><text x="260" y="160" class="class value"></text>
        <line x1="270" y1="157" x2="{security_percent}" y2="157" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="270" y1="157" x2="360" y2="157" stroke-width="10" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
        <text x="320" y="161" dz="-30" class="repo-percent">{security} %</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="190" y="180" class="subtitle">Efficiency</text><text x="260" y="160" class="class value"></text>
        <line x1="270" y1="177" x2="{efficiency_percent}" y2="177" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="270" y1="177" x2="360" y2="177" stroke-width="10" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
        <text x="320" y="181" dz="-20" class="repo-percent">{efficiency} %</text>
    </g>

    <g transform="translate(190, 70)">
        <image height="12px" xlink:href="https://img.shields.io/badge/HTML5-E34F26.svg?&amp;style=for-the-badge&amp;logo=HTML5&amp;logoColor=white"/>
    </g>
    <g transform="translate(230, 70)">
        <image height="12px" xlink:href="https://img.shields.io/badge/JavaScriipt-F7DF1E.svg?&amp;style=for-the-badge&amp;logo=JavaScript&amp;logoColor=black"/>
    </g>
    <g transform="translate(290, 70)">
        <image height="12px" xlink:href="https://img.shields.io/badge/CSS3-1572B6.svg?&amp;style=for-the-badge&amp;logo=CSS3&amp;logoColor=white"/>
    </g>

    <image href="{chart}" x="425" y="40" height="160px" class="repomon-img"/>
    <text x="505" y="40" class="charttitle">커밋</text>
    <text x="580" y="85" class="charttitle">머지</text>
    <text x="432" y="85" class="charttitle">이슈</text>
    <text x="432" y="152" class="charttitle">리뷰</text>
    <text x="578" y="152" class="charttitle">효율성</text>
    <text x="504" y="193" class="charttitle">보안성</text>
</svg>
    '''.format(repoName = handle_set.repoName,
               repoDescription = handle_set.repoDescription,
               repoExp = handle_set.repoExp,
               starCnt = handle_set.starCnt,
               forkCnt = handle_set.forkCnt,
               repoStart = handle_set.repoStart,
               repoEnd = handle_set.repoEnd,
               contributers = handle_set.contributers,
               commits = handle_set.commits,
               issues = handle_set.issues,
               merges = handle_set.merges,
               reviews = handle_set.reviews,
               efficiency = handle_set.efficiency,
               efficiency_percent = handle_set.efficiency_percent + 270,
               security = handle_set.security,
               security_percent = handle_set.security_percent + 270,
               totalcommit = handle_set.totalcommit,
               totalcode = handle_set.totalcode,
               per=per,
               star=star,
               fork=fork,
               img=img,
               chart=handle_set.chart
               )

    logger.info('[/generate_badge/repocard] repo: {}, repoExp: {}'.format(handle_set.repoName, handle_set.repoExp))
    response = HttpResponse(content=svg)
    response['Content-Type'] = 'image/svg+xml'
    response['Cache-Control'] = 'max-age=3600'

    return response


class RepoPersonalDefaultSettings(object):
    def __init__(self, request, url_set):
        try:
            self.json = requests.get(url_set.repo_information_url).json()
            print('🎀')
            print(self.json)
            self.repoName = self.json['repoName']
            self.repomonId = self.json['repomonId']
            self.repoDescription = self.is_none(self.json['repoDescription'])
            self.repoExp = self.json['repoExp']
            self.starCnt = self.json['starCnt']
            self.forkCnt = self.json['forkCnt']
            self.repoStart = self.day(self.json['repoStart'])
            self.repoEnd = self.day(self.json['repoEnd'])
            self.languages = self.json['languages']
            self.contributers = self.json['contributers']
            self.commits = self.json['commits']
            self.issues = self.json['issues']
            self.merges = self.json['merges']
            self.reviews = self.json['reviews']
            self.efficiency = int(self.json['efficiency'])
            self.efficiency_percent = self.percent(self.json['efficiency'])
            self.security = int(self.json['security'])
            self.security_percent = self.percent(self.json['security'])
            self.totalcommit = self.json['totalcommit']
            self.totalcode = self.json['totalcode']
            self.contribution = self.json['mycontribution']
            self.gitname = self.json['userName'] 
            self.avatarUrl = self.json['avatarUrl'] 

            self.mycommits = self.json['mytotalcommit']
            self.myissues = self.json['myissues']
            self.mymerges = self.json['mymerges']
            self.myreviews = self.json['myreviews']
            self.mytotalcommit = self.json['mytotalcommit']
            self.mytotalcode = self.json['mytotalcode']
            self.myefficiency = int(self.json['myefficiency'])            
            self.mysecurity = int(self.json['mysecurity'])
            self.chart = svg_chart_personal([self.commits, self.issues, self.reviews, self.security, self.efficiency, self.merges],[self.mycommits, self.myissues, self.myreviews, self.mysecurity, self.myefficiency, self.mymerges])
    
        except JSONDecodeError as e:
            logger.error(e)
            self.repoName = '레포몬'
            self.repoDescription = '나의 레포몬을 불러보세요나의 레포몬을 불러보세요'
            self.repoExp = '123456'
            self.starCnt = '7'
            self.forkCnt = '66'
            self.repoStart = '23.03.10'
            self.repoEnd = '23.04.20'
            self.languages = ''
            self.contributers = '6'
            self.commits = 543 
            self.issues = 123
            self.merges = 321
            self.reviews = 123
            self.efficiency = 80
            self.efficiency_percent = 80
            self.security = 80
            self.security_percent = 80
            self.totalcommit = '123456'
            self.totalcode = '654321'
            self.contribution = 33
            self.gitname = 'becoding'
            self.chart = svg_chart_personal([self.commits*2, self.merges*2, self.issues*2, self.reviews*2, self.efficiency*2, self.security*2],[self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security])

    def day(self, day):
        if day != None:
            new_day = str(day[2:4])+'.'+str(day[5:7])+'.'+str(day[8:10]) 
            return new_day
        else:
            return ''
        
    def percent(self, num):
        percent = round(num/100*90)
        return percent
    
    def is_none(self, data):
        if data == None:
            return ''
        else:
            return data

def repo_personal_card(request):
    per = IMG['Per']
    star = IMG['Star']
    fork = IMG['Fork']
    url_set = UrlSettings(request, 'repo_personal')
    handle_set = RepoPersonalDefaultSettings(request, url_set)
    svg = '''
    <!DOCTYPE svg PUBLIC
        "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg height="230" width="600"
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
            .value2 {{
                font-weight: 400;
                font-size: 0.5em;
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
            .repo-percent {{
                fill: #000000;
                font-size: 0.6em;
                font-weight: 700;
                text-anchor: middle;
            }}
            .elli1 {{
                fill: #FFF9C1;
                cx: 95px;
                cy: 155px;
                rx: 50px;
                ry: 15px;
            }}
            .elli2 {{
                fill: #C1E9FF;
                cx: 95px;
                cy: 155px;
                rx: 58px;
                ry: 20px;
            }}
            .elli3 {{
                fill: #FF93B3;
                cx: 95px;
                cy: 145px;
                rx: 60px;
                ry: 30px;
            }}
        ]]>
    </style>
<frame-options policy="SAMEORIGIN"/>
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="35%">
            <stop offset="10%" style="stop-color:'#AAAAAA';stop-opacity:1">
                <animate attributeName="stop-opacity" values="0.7; 0.73; 0.9 ; 0.97; 1; 0.97; 0.9; 0.73; 0.7;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="55%" style="stop-color:'#666666';stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.95; 0.93; 0.95; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="100%" style="stop-color:'#000000';stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.97; 0.9; 0.83; 0.8; 0.83; 0.9; 0.97; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
        </linearGradient>
    </defs>
    <rect width="600" height="230" rx="10" ry="10" class="background"/>
    
    <image href="{avatarUrl}" x="18" y="12" height="22px" width="22px" class="repomon-img"/>
    <text x="45" y="25" font-size="0.7em">{gitname}</text>
    
    <ellipse class="{ellipsetype}"/>
    <rect  x="25" y="52" width="140px" height="112px" style="stroke: red; stroke-width: 2px; fill: none;" />
    <image href="{img}" x="25" y="52" width="140px" height="112px" class="repomon-img"/>
    <line x1="40" y1="188" x2="150" y2="188" stroke-width="20" stroke="floralwhite" stroke-linecap="round"/>
    <text x="100" y="193" dz="-20" class="repo-exp">Exp | {repoExp}</text>
    <text x="39" y="215" font-size="0.7em">My contribution : {contribution}%</text>

    <text x="190" y="45" class="boj-handle">{repoName}</text>
    <image href="{per}" x="300" y="33" height="13px" width="10px"/><text x="313" y="44" font-size="0.7em">{contributers}</text>
    <text x="335" y="43" font-size="0.7em">{repoStart} ~ {repoEnd}</text>

    <image href="{star}" x="515" y="16" width="11px"/><text x="530" y="25" font-size="0.6em">{starCnt}</text>
    <image href="{fork}" x="550" y="16" width="8px"/><text x="563" y="25" font-size="0.6em">{forkCnt}</text>
        <text x="190" y="65" class="repo-detail">{repoDescription}</text>

    <g transform="translate(190, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/HTML5-E34F26.svg?&amp;style=for-the-badge&amp;logo=HTML5&amp;logoColor=white"/>
    </g>
    <g transform="translate(230, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/JavaScriipt-F7DF1E.svg?&amp;style=for-the-badge&amp;logo=JavaScript&amp;logoColor=black"/>
    </g>
    <g transform="translate(290, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/CSS3-1572B6.svg?&amp;style=for-the-badge&amp;logo=CSS3&amp;logoColor=white"/>
    </g>

    <g class="item" style="animation-delay: 200ms">
        <text x="190" y="134" class="subtitle">Total Commit</text><text x="270" y="134" class="rate value">{mytotalcommit} 회</text><text x="330" y="134" class="solved value2">/ {totalcommit} 줄</text>
    </g>
    <g class="item" style="animation-delay: 400ms">
        <text x="190" y="156" class="subtitle">Total code</text><text x="270" y="156" class="solved value">{mytotalcode} 줄</text><text x="330" y="156" class="solved value2">/ {totalcode} 줄</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="190" y="178" class="subtitle">Security</text><text x="260" y="178" class="class value"></text>
        <line x1="270" y1="175" x2="{security_percent}" y2="175" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="270" y1="175" x2="360" y2="175" stroke-width="10" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
        <text x="320" y="179" dz="-30" class="repo-percent">{security} %</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="190" y="200" class="subtitle">Efficiency</text><text x="260" y="170" class="class value"></text>
        <line x1="270" y1="197" x2="{efficiency_percent}" y2="197" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="270" y1="197" x2="360" y2="197" stroke-width="10" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
        <text x="320" y="201" dz="-20" class="repo-percent">{efficiency} %</text>
    </g>



    <image href="{chart}" x="407" y="62" height="170px" class="repomon-img"/>
    <text x="492" y="77" class="charttitle"> commit</text>
    <text x="563" y="111" class="charttitle"> merge</text>
    <text x="425" y="111" class="charttitle">issue</text>
    <text x="425" y="183" class="charttitle">review</text>
    <text x="563" y="183" class="charttitle">star</text>
    <text x="491" y="217" class="charttitle">fork</text>
</svg>
    '''.format(repoName = handle_set.repoName,
               repoDescription = handle_set.repoDescription,
               repoExp = handle_set.repoExp,
               starCnt = handle_set.starCnt,
               forkCnt = handle_set.forkCnt,
               repoStart = handle_set.repoStart,
               repoEnd = handle_set.repoEnd,
               contributers = handle_set.contributers,
               efficiency = handle_set.efficiency,
               efficiency_percent = handle_set.efficiency_percent + 270,
               security = handle_set.security,
               security_percent = handle_set.security_percent + 270,
               totalcommit = handle_set.totalcommit,
               totalcode = handle_set.totalcode,
               contribution = handle_set.contribution,
               gitname = handle_set.gitname,
               avatarUrl = handle_set.avatarUrl,
               mytotalcommit = handle_set.mytotalcommit,
               mytotalcode = handle_set.mytotalcommit,
               per=per,
               star=star,
               fork=fork,
            #    img=IMG['img'+str(handle_set.repomonId)],
            #    ellipsetype=ELLIPSE_TYPE[handle_set.repomon_tier],
               ellipsetype=ELLIPSE_TYPE[3],
               img=IMG['img24'],
               chart=handle_set.chart
               )

    logger.info('[/generate_badge/repocard] repo: {}, repoExp: {}'.format(handle_set.repoName, handle_set.repoExp))
    response = HttpResponse(content=svg)
    response['Content-Type'] = 'image/svg+xml'
    response['Cache-Control'] = 'max-age=3600'

    return response


class UserDefaultSettings(object):
    def __init__(self, request, url_set):
        try:
            self.json = requests.get(url_set.repo_information_url).json()
            print('🎀')
            print(self.json)
            self.repoName = self.json['repoName']
            self.repoDescription = self.is_none(self.json['repoDescription'])
            self.repoExp = self.json['repoExp']
            self.starCnt = self.json['starCnt']
            self.forkCnt = self.json['forkCnt']
            self.repoStart = self.day(self.json['repoStart'])
            self.repoEnd = self.day(self.json['repoEnd'])
            self.languages = self.json['languages']
            self.contributers = self.json['contributers']
            self.commits = self.json['commits']
            self.issues = self.json['issues']
            self.merges = self.json['merges']
            self.reviews = self.json['reviews']
            self.efficiency = int(self.json['efficiency'])
            self.efficiency_percent = self.percent(self.json['efficiency'])
            self.security = int(self.json['security'])
            self.security_percent = self.percent(self.json['security'])
            self.totalcommit = self.json['totalcommit']
            self.totalcode = self.json['totalcode']
            self.contribution = self.json['contribution']
            self.gitname = self.json['gitname'] 
            print(self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security)
            self.chart = svg_chart([self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security])
    
        except JSONDecodeError as e:
            logger.error(e)
            self.repoName = '레포몬'
            self.repoDescription = '나의 레포몬을 불러보세요나의 레포몬을 불러보세요'
            self.repoExp = '123456'
            self.starCnt = '7'
            self.forkCnt = '66'
            self.repoStart = '23.03.10'
            self.repoEnd = '23.04.20'
            self.languages = ''
            self.contributers = '6'
            self.commits = 543 
            self.issues = 123
            self.merges = 321
            self.reviews = 123
            self.efficiency = 80
            self.efficiency_percent = 80
            self.security = 80
            self.security_percent = 80
            self.totalcommit = '123456'
            self.totalcode = '654321'
            self.contribution = 33
            self.gitname = 'becoding'
            # self.gitimg = 'becoding'
            self.chart = svg_chart([self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security])

    def day(self, day):
        if day != None:
            new_day = str(day[2:4])+'.'+str(day[5:7])+'.'+str(day[8:10]) 
            return new_day
        else:
            return ''
        
    def percent(self, num):
        percent = round(num/100*90)
        return percent
    
    def is_none(self, data):
        if data == None:
            return ''
        else:
            return data


def user_card(request):
    per = IMG['Per']
    star = IMG['Star']
    fork = IMG['Fork']
    img = IMG['Img']
    pocket = IMG['Pocket']
    url_set = UrlSettings(request, 'user')
    handle_set = UserDefaultSettings(request, url_set)
    svg = '''
    <!DOCTYPE svg PUBLIC
        "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg height="230" width="600"
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
            .background {{
                fill: url(#grad);
            }}
            text {{
                fill: white;
                font-family: 'Noto Sans KR', sans-serif;
            }}
            text.repo-handle {{
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
                font-size: 0.6em;
            }}
            .value {{
                font-weight: 400;
                font-size: 0.6em;
            }}
            .value2 {{
                font-weight: 400;
                font-size: 0.5em;
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
            .repo-percent {{
                fill: #000000;
                font-size: 0.6em;
                font-weight: 700;
                text-anchor: middle;
            }}
        ]]>
    </style>
<frame-options policy="SAMEORIGIN"/>
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="35%">
            <stop offset="10%" style="stop-color:'#AAAAAA';stop-opacity:1">
                <animate attributeName="stop-opacity" values="0.7; 0.73; 0.9 ; 0.97; 1; 0.97; 0.9; 0.73; 0.7;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="55%" style="stop-color:'#666666';stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.95; 0.93; 0.95; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
            <stop offset="100%" style="stop-color:'#000000';stop-opacity:1">
                <animate attributeName="stop-opacity" values="1; 0.97; 0.9; 0.83; 0.8; 0.83; 0.9; 0.97; 1;" dur="4s" repeatCount="indefinite" repeatDur="01:00"></animate>
            </stop>
        </linearGradient>
    </defs>
    <rect width="600" height="230" rx="10" ry="10" class="background"/>
    
    <image href="{img}" x="191" y="21" height="44px" width="44px" class="repomon-img"/>
    <text x="240" y="41" class="repo-handle">{gitname}</text>
    <text x="275" y="62" font-size="0.7em">This is 배코딩</text>
    <image href="{pocket}" x="241" y="50" width="14px"/><text x="256" y="61" font-size="0.6em">{starCnt}</text>

    <image href="{img}" x="16" y="15" height="160px" width="160px" class="repomon-img"/>
    <line x1="40" y1="170" x2="150" y2="170" stroke-width="20" stroke="floralwhite" stroke-linecap="round"/>
    <text x="100" y="175" dz="-20" class="repo-exp">Exp | {repoExp}</text>
    <text x="77" y="198" font-size="0.8em">{repoName}</text>
    <text x="39" y="215" font-size="0.7em">My contribution : {contribution}%</text>

    

    <g transform="translate(195, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/HTML5-E34F26.svg?&amp;style=for-the-badge&amp;logo=HTML5&amp;logoColor=white"/>
    </g>
    <g transform="translate(235, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/JavaScriipt-F7DF1E.svg?&amp;style=for-the-badge&amp;logo=JavaScript&amp;logoColor=black"/>
    </g>
    <g transform="translate(295, 75)">
        <image height="12px" xlink:href="https://img.shields.io/badge/CSS3-1572B6.svg?&amp;style=for-the-badge&amp;logo=CSS3&amp;logoColor=white"/>
    </g>

    <g class="item" style="animation-delay: 200ms">
        <text x="195" y="125" class="subtitle">Total Exp</text><text x="270" y="125" class="rate value">{totalcommit} 점</text>
    </g>
    <g class="item" style="animation-delay: 200ms">
        <text x="195" y="143" class="subtitle">Total Code</text><text x="270" y="143" class="rate value">{totalcode} 줄</text>
    </g>
    <g class="item" style="animation-delay: 400ms">
        <text x="195" y="161" class="subtitle">Total Commit</text><text x="270" y="161" class="solved value">{totalcommit} 회</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="195" y="179" class="subtitle">Average Security</text><text x="260" y="178" class="class value"></text>
        <line x1="305" y1="175" x2="{security_percent}" y2="175" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="305" y1="175" x2="370" y2="175" stroke-width="9" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
        <text x="330" y="179" dz="-30" class="repo-percent">{security} %</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="195" y="197" class="subtitle">Average Efficiency</text><text x="260" y="170" class="class value"></text>
        <line x1="305" y1="193" x2="{efficiency_percent}" y2="193" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="305" y1="193" x2="370" y2="193" stroke-width="9" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
        <text x="330" y="197" dz="-20" class="repo-percent">{efficiency} %</text>
    </g>
    <g class="item" style="animation-delay: 600ms">
        <text x="195" y="215" class="subtitle">Average Contribution</text><text x="260" y="215" class="class value"></text>
        <line x1="305" y1="211" x2="{efficiency_percent}" y2="211" stroke-width="10" stroke="floralwhite" stroke-linecap="round"/>
        <line x1="305" y1="211" x2="370" y2="211" stroke-width="9" stroke-opacity="40%" stroke="floralwhite" stroke-linecap="round"/>
        <text x="330" y="215" dz="-20" class="repo-percent">{efficiency} %</text>
    </g>



    <image href="{chart}" x="358" y="5" height="240px" class="repomon-img"/>
    <text x="484" y="20" class="charttitle"> 커밋</text>
    <text x="577" y="74" class="charttitle"> 머지</text>
    <text x="391" y="74" class="charttitle">이슈</text>
    <text x="391" y="173" class="charttitle">리뷰</text>
    <text x="577" y="173" class="charttitle">효율성</text>
    <text x="483" y="220" class="charttitle">보안성</text>
</svg>
    '''.format(repoName = handle_set.repoName,
               repoDescription = handle_set.repoDescription,
               repoExp = handle_set.repoExp,
               starCnt = handle_set.starCnt,
               forkCnt = handle_set.forkCnt,
               repoStart = handle_set.repoStart,
               repoEnd = handle_set.repoEnd,
               contributers = handle_set.contributers,
               commits = handle_set.commits,
               issues = handle_set.issues,
               merges = handle_set.merges,
               reviews = handle_set.reviews,
               efficiency = handle_set.efficiency,
               efficiency_percent = handle_set.efficiency_percent + 270,
               security = handle_set.security,
               security_percent = handle_set.security_percent + 270,
               totalcommit = handle_set.totalcommit,
               totalcode = handle_set.totalcode,
               contribution = handle_set.contribution,
               gitname = handle_set.gitname,
               per=per,
               star=star,
               fork=fork,
               img=img,
               pocket=pocket,
               chart=handle_set.chart
               )

    logger.info('[/generate_badge/repocard] repo: {}, repoExp: {}'.format(handle_set.repoName, handle_set.repoExp))
    response = HttpResponse(content=svg)
    response['Content-Type'] = 'image/svg+xml'
    response['Cache-Control'] = 'max-age=3600'

    return response

