import os
import requests
import locale
import logging
from json import JSONDecodeError
import base64

# This code example demonstrates how to convert HTML document to PNG images.


from django.http import HttpResponse
from .images import PER, FORK, STAR, IMG
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
        opacity = '0.9',
        major_label_font_size = 20,
    )
    radar_chart = pygal.Radar(width=520,height=500,show_major_y_labels=False,show_minor_y_labels=False,y_labels_major_every=2,fill=True,style=custom_style,show_legend=False)
    radar_chart.x_labels = ['', '', '', '', '', '']
    radar_chart.add('Exp', request)
    chartspider = radar_chart.render()

    response = svg_to_base64(chartspider)

    return response
    
# def svg_chart2(request):
#     custom_style = Style(
#         background='#000000',
#         plot_background='transparent',
#         major_guide_stroke_dasharray='#FFFFFF',
#         guide_stroke_dasharray='#FFFFFF',
#         foreground_subtle='#FFFFFF',
#         foreground_strong='#FFFFFF',
#         foreground='#FFFFFF',
#         colors=('#FFC1C1', '#E8537A', '#E95355', '#E87653', '#E89B53', '#E89B53', '#E89B53', '#E89B53'),
#         guides=('#FFFFFF'),
#         guide_stroke_color = 'white',
#         major_guide_stroke_color = 'white',
#         opacity = '1',
#         major_label_font_size = 20,
#     )
#     radar_chart = pygal.Radar(width=520,height=500,show_major_y_labels=False,show_minor_y_labels=False,y_labels_major_every=2,fill=True,style=custom_style,show_legend=False)
#     radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp']
#     radar_chart.add('Exp', [6395, 8212, 7520, 7218, 12464, 1660])
#     chartspider = radar_chart.render()

#     response = HttpResponse(content_type='image/svg+xml')
#     response.write(chartspider)
    
#     return response

# Create your views here.
IMG = {
    'Per' : PER,
    'Star': STAR,
    'Fork': FORK,
    'Img' : IMG,
}


class UrlSettings(object):
    def __init__(self, request, MAX_LEN):
        self.api_server = 'https://k8e105.p.ssafy.io/api/v1/repo/'
        self.repo_handle = request.GET.get("repoId", "5")
        self.repo_information_url = self.api_server + '{' +'repoId' + '}' + '/card/detail?repoId=' + self.repo_handle


class BojDefaultSettings(object):
    def __init__(self, request, url_set):
        try:
            self.json = requests.get(url_set.repo_information_url).json()
            # print('🎀')
            # print(self.json)
            self.repoName = self.json['repoName']
            self.repoDescription = self.json['repoDescription']
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
            self.efficiency = self.json['efficiency']
            self.efficiency_percent = self.percent(self.json['efficiency'])
            self.security = self.json['security']
            self.security_percent = self.percent(self.json['security'])
            self.totalcommit = self.json['totalcommit']
            self.totalcode = self.json['totalcode']
            self.chart = svg_chart([self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security])
    
        except JSONDecodeError as e:
            logger.error(e)
            self.repoName = '아이유정'
            self.repoDescription = '아이유정'
            self.repoExp = '456421'
            self.starCnt = '4'
            self.forkCnt = '54'
            self.repoStart = '23.03.10'
            self.repoEnd = '23.04.20'
            self.languages = self.json['languages']
            self.contributers = '6'
            self.commits = '546546'
            self.issues = '12345'
            self.merges = '6565'
            self.reviews = '123213'
            self.efficiency = '340'
            self.efficiency_percent = '80'
            self.security = '340'
            self.security_percent = '80'
            self.totalcommit = '213546'
            self.totalcode = '668712'
            self.chart = svg_chart([self.commits, self.merges, self.issues, self.reviews, self.efficiency, self.security])

    def day(self, day):
        if day != None:
            new_day = str(day[2:4])+'.'+str(day[5:7])+'.'+str(day[8:10]) 
            return new_day
        else:
            return ''
        
    def percent(self, num):
        percent = 270 + round(num/100*90)
        return percent



def repo_card(request):
    MAX_LEN = 15
    per = IMG['Per']
    star = IMG['Star']
    fork = IMG['Fork']
    img = IMG['Img']
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
    
    <image href="{img}" x="18" y="12" height="160px" width="160px" class="repomon-img"/>
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
               efficiency_percent = handle_set.efficiency_percent,
               security = handle_set.security,
               security_percent = handle_set.security_percent,
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


def repo_personal_card(request):
    MAX_LEN = 15
    per = IMG['Per']
    star = IMG['Star']
    fork = IMG['Fork']
    img = IMG['Img']
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
    
    <image href="{img}" x="18" y="12" height="160px" width="160px" class="repomon-img"/>
    <line x1="40" y1="170" x2="150" y2="170" stroke-width="20" stroke="floralwhite" stroke-linecap="round"/>
    <text x="100" y="175" dz="-20" class="repo-exp">Exp | {repoExp}</text>

    <text x="190" y="40" class="boj-handle">{repoName}</text>
    <image href="{per}" x="300" y="30" height="13px" width="10px"/><text x="313" y="41" font-size="0.7em">{contributers}</text>
    <text x="335" y="40" font-size="0.7em">{repoStart} ~ {repoEnd}</text>

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
               efficiency_percent = handle_set.efficiency_percent,
               security = handle_set.security,
               security_percent = handle_set.security_percent,
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

def user_card(request):
    MAX_LEN = 15
    per = IMG['Per']
    star = IMG['Star']
    fork = IMG['Fork']
    img = IMG['Img']
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
    
    <image href="{img}" x="18" y="12" height="160px" width="160px" class="repomon-img"/>
    <line x1="40" y1="170" x2="150" y2="170" stroke-width="20" stroke="floralwhite" stroke-linecap="round"/>
    <text x="100" y="175" dz="-20" class="repo-exp">Exp | {repoExp}</text>

    <text x="190" y="40" class="boj-handle">{repoName}</text>
    <image href="{per}" x="300" y="30" height="13px" width="10px"/><text x="313" y="41" font-size="0.7em">{contributers}</text>
    <text x="335" y="40" font-size="0.7em">{repoStart} ~ {repoEnd}</text>

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
               efficiency_percent = handle_set.efficiency_percent,
               security = handle_set.security,
               security_percent = handle_set.security_percent,
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

