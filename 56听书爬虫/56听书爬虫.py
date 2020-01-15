# -*- coding:utf8 -*-
import re as reg
import urllib
import urllib.request
from bs4 import BeautifulSoup
from lxml import html
# from playsound import playsound
import json
import requests
import vlc


def vlcPlay(audio: str):
    """
    play audio from local file or online url, base on libvlc(python-vlc)
    :param audio: audio file path or online url
    :return: None
    """
    vlc_instance = vlc.Instance()                   # creating a basic vlc instance
    media_player = vlc_instance.media_player_new()  # creating an empty vlc media player
    media = vlc_instance.media_new(audio)           # media
    media_player.set_media(media)                   # put the media in the media player
    media.parse()                                   # parse the metadata of the file
    media_player.play()


class BookPlay:
    # 目录列表对象
    def __init__(self, url, title):
        self.url = url
        title = FullwidthToHalfwidth(title)
        self.title = title

    def __str__(self):
        return '{} \r'.format(strFormat(self.title, 30))


class Book:
    # 书籍对象
    def __init__(self, url, img, name, author, content, page, pagecount):
        name = FullwidthToHalfwidth(name)
        author = FullwidthToHalfwidth(author)
        content = FullwidthToHalfwidth(content)
        self.url = url
        self.img = img
        self.name = name
        self.author = author
        self.content = content
        self.page = page
        self.pagecount = pagecount

    def set_playlist(self, playlist):
        self.playlist = playlist

    def __str__(self):
        return '{} {} {} \r'.format(strFormat(self.name, 30), strFormat(self.author, 50), strFormat(self.content, 20))


def getTingChinaUrl(url):
    formdata = {
        'url': url
    }
    # url路径中有中文 http://t44.tingchina.com/yousheng/玄幻奇幻/医统江山_农夫三拳/001.mp3?key=7ee3776ca71f2d3648e720836b0d4e86_628723292
    url = "http://m.ting56.com/fonhen_player/tingchina.php"
    request = urllib.request.Request(url=url)
    formdata = urllib.parse.urlencode(formdata).encode()
    response = urllib.request.urlopen(request, formdata)
    content = response.read().decode('gbk')
    mp3url = chineseToUnicode(json.loads(content)['url'])
    return mp3url


def downloadMp3(mp3url, path):
    urllib.request.urlretrieve(mp3url, path)


def chineseToUnicode(url):
    # 处理链接中的中文部分
    unicodeChinese = ""
    for char in url:
        if '\u4e00' <= char <= '\u9fa5':
            unicodeChinese += urllib.parse.quote_plus(char)
        else:
            unicodeChinese += char
    return unicodeChinese


def getHtmlContent(path):
    url = "http://m.ting56.com"
    response = urllib.request.urlopen(url+path)
    content = response.read().decode('gbk')
    soup = BeautifulSoup(content, 'lxml')
    return soup


def strFormat(_string, _length, _code='gbk'):
    _string = _string.replace("\r\n", "")
    _string = _string.replace("、", "丶")  # 这玩意占三个字节宽,影响美观
    _string = _string.strip()
    _stringlen = _length - len(_string.encode(_code))
    if _stringlen >= 0:
        _string = _string+" "*_stringlen
    return _string


def FullwidthToHalfwidth(ustring):
    # 全角字符转半角字符
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)


def search(bookname):
    # 搜索听书
    # 参数 page int 例子: 1
    # 参数 searchword string 56听书的限制搜索必须提交GBK编码的字符串 例子: %D5%C2%D3%E3
    path = '/search.asp?page=1&searchword=' + urllib.request.quote(bookname.encode('gb2312'))
    html = getHtmlContent(path)
    searchList = html.find_all(class_='list-ov-tw')
    pageCount = html.find(class_='cate-pages').find_all('li')[1].text.split('/')
    nowPageCount = pageCount[0]  # 当前页
    allPageCount = pageCount[1]  # 总页数
    bookList = []  # 搜索结果
    for searchItem in searchList:
        bookUrl = searchItem.find(class_='bt').find('a').attrs['href']
        bookImg = searchItem.find('img').attrs['original']
        bookName = searchItem.find(class_='bt').text
        bookAuthor = searchItem.find_all(class_='zz')[0].text+' ' + searchItem.find_all(class_='zz')[1].text
        bookContent = searchItem.find(class_='nr').text
        book = Book(bookUrl, bookImg, bookName, bookAuthor, bookContent, nowPageCount, allPageCount)
        bookList.append(book)
    return bookList


def showBook(book):
    # 获取书本的目录信息
    html = getHtmlContent(book.url)
    playlist = html.find(id='playlist').find_all('li')
    bookPlayList = []
    for play in playlist:
        url = play.find('a').attrs['href']
        title = play.find('a').attrs['title']
        bookPlayList.append(BookPlay(url, title))
    book.set_playlist(bookPlayList)


def bookPlayer(bookPlay):
    # 56听书的播放页MP3链接有加密,需要通过正则获取转义得到
    html = getHtmlContent(bookPlay.url)
    htmlHead = html.head.find_all('script')
    jsData = htmlHead[len(htmlHead)-1].text
    urllist = reg.findall("FonHen_JieMa\(\'(.+?)\'\).split", jsData)[0].split('*')
    urlstr = ''
    for x in urllist:
        if x != '':
            urlstr += fromCharCode(int(x))
    datas = urlstr.split('&')
    mp3url = ""
    if datas[2] == 'tc':
        # tingchina数据需要额外再次请求
        # /fonhen_player/tingchina.php Post url yousheng/27584/play_27584_0.htm
        urls = datas[0].split('/')
        url = urls[0] + '/' + urls[1] + '/play_' + urls[1] + '_' + urls[2] + '.htm'
        mp3url = getTingChinaUrl(url)
    else:
        mp3url = datas[0]
    # print(mp3url)
    bookPlay.url = mp3url
    # vlcPlay(mp3url)
    # playsound(mp3url)


def fromCharCode(a, *b):
    # 根据 Unicode 编码获取字符
    return chr(a % 65536) + ''.join([chr(i % 65536) for i in b])


def inputInt(tips):
    try:
        intInput = int(input(tips))
        return intInput
    except Exception as e:
        return inputInt(tips)


def inputStr(tips):
    intInput = input(tips)
    return intInput


# # 搜索数据
# searchContent = inputStr('输入搜索内容: ')
# bookList = search(searchContent)
# for index, bookInfo in enumerate(bookList):
#     print(strFormat(str(index), 10), bookInfo)
# # 选择书籍
# bookIndex = inputInt('输入内容编号: ')
# showBook(bookList[bookIndex])
# bookInfo = bookList[bookIndex]
# for index, play in enumerate(bookInfo.playlist):
#     print(strFormat(str(index), 10), play)
# # 选择集数
# bookPlayIndex = inputInt('输入集数编号: ')
# print(bookPlayIndex)
# bookPlayer(bookInfo.playlist[bookPlayIndex])
###############################################
# # 搜索数据
# result = search("章鱼")
# for x in result:
#     print(x)
# 获取目录信息
book = Book("/mp3/4304.html", "bookImg", "章鱼短篇悬疑惊悚故事集", "章鱼", "bookContent", 2, 2)
showBook(book)
for play in book.playlist:
    try:
        bookPlayer(play)
        downloadMp3(play.url, play.title+'.mp3')
        print(play)
    except Exception as e:
        print(play, "============================================================")

    # # 播放某集
    # bookplay = BookPlay('/video/4304-0-0.html', 'sssss')
    # bookPlayer(bookplay)
