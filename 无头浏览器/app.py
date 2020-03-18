# coding=utf-8
import sys
import configparser
import os
import datetime
import time
import xlrd
from selenium import webdriver

pddUrl = None
driver = None
cookieList = None
cookieIndex = 0
helpText = """
=====================================
命令提示:
直接回车会自动跳转到下一个cookie,并跳到验证界面
因为现在没有自动验证了,故请不要连续点击回车,这样会连续跳过多个cookie
输入 0 后在回车,则是相比直接回车 多了一个将当前cookie记录下来的操作,记录在如"跳过cookie_2020-03-18.txt"中
输入 help 后在回车,则是显示命令提示
=====================================
"""


def chrome_init():
    print("启动浏览器中...")
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁用debug.log
    # options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'}) # 经测试以手机模式启动无法完成滑动验证,滑动无效
    # options.add_argument("--auto-open-devtools-for-tabs")  # 默认开启开发者工具
    # options.add_argument("start-maximized")  # 默认最大化启动
    global driver
    driver = webdriver.Chrome(chrome_options=options)
    # driver.minimize_window() # 最小化窗口
    print("启动浏览器成功!")


def getCookie():
    global cookieIndex
    global cookieList
    if cookieIndex > len(cookieList)-1:
        cookieIndex = len(cookieList)-1
        print("======================================")
        print("当前cookie.txt已读取完毕,请更换cookie.txt")
        print("======================================")
    return cookieList[cookieIndex]


def errorCookie(_cookie):
    print("正在记录失效Cookie...")
    path_file_name = './失效cookie_{}.txt'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
    with open(path_file_name, "a") as f:
        f.write(_cookie+"\n")
    print("失效cookie已录入:{}".format(path_file_name))


def skipCookie():
    global cookieIndex
    print("已跳过第{}位Cookie".format(cookieIndex))
    # cookieIndex = cookieIndex+1 # 现在默认回车是下一位 故不用手动+1了
    path_file_name = './跳过cookie_{}.txt'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
    with open(path_file_name, "a") as f:
        f.write(getCookie()+"\n")
    saveConfig(cookieIndex)


def loadConfig():
    print("读取配置文件中...")
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        global pddUrl
        pddUrl = config.get("sys_config", "url")
        global cookieIndex
        cookieIndex = int(config.get("sys_config", "cookieIndex")) - 1  # 现在按 回车 是直接跳到下一个 故在读取配置的时候减 避免跳过启动后的第一条数据
        print("读取配置文件成功")
        return True
    except:
        print("读取配置文件错误")
        return False


def saveConfig(_cookieIndex):
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.set("sys_config", "cookieIndex", str(_cookieIndex))
        config.write(open("config.ini", "w"))
        return True
    except:
        print("修改配置文件错误")
        return False


def toPddHome():
    driver.get("https://{}".format(pddUrl))
    time.sleep(0.5)


def readCookieTxt():
    print("读取cookie.txt中...")
    # 读取cookie.txt中的cookie列表
    with open(r'cookie.txt', encoding="utf-8") as file:
        lines = list(file)
        for i in enumerate(lines):
            lines[i[0]] = lines[i[0]].strip('\n')
        global cookieList
        cookieList = lines
        print("读取cookie.txt成功!")


def chromeOnTap():
    # 浏览器前台置顶
    driver.minimize_window()
    driver.set_window_position(x=0, y=0)
    driver.maximize_window()


def toVerifiy():
    # driver.set_window_size(300, 900)
    if driver.current_url.find("shop_brand_station.html") == -1 or len(driver.find_element_by_tag_name('body').text) <= 60:
        # 不在店铺页就前往店铺页
        # 首先访问分类页
        try:
            driver.get("https://{}/classification.html".format(pddUrl))
            time.sleep(0.5)
        except Exception as e:
            pass
        # 品牌不在屏幕中则无法点击,故先滑动到品牌
        try:
            div = driver.find_element_by_xpath("//*[text()='品牌']")
            driver.execute_script("arguments[0].scrollIntoView();", div)
        except Exception as e:
            pass
        # 在点品牌
        try:
            driver.find_element_by_xpath("//*[text()='品牌']").click()
            time.sleep(0.5)
        except Exception as e:
            pass
        # 推荐品牌会变来变去,故默认点击品牌下的第一个选项
        try:
            driver.find_element_by_css_selector("ul>li:nth-child(1)").click()
            time.sleep(0.5)
        except Exception as e:
            pass
    else:
        # 在店铺页就刷新即可
        driver.refresh()


def testVerifiy():
    print("开始验证第{}位用户是否激活...".format(cookieIndex))
    setCookie()
    toVerifiy()
    time.sleep(1)
    if driver.find_element_by_tag_name('body') and len(driver.find_element_by_tag_name('body').text) > 20:
        if(driver.current_url.find("psnl_verification.html") == -1):
            if(driver.current_url.find("login.html") == -1):
                print("当前用户已激活")
                return True
            else:
                print("当前用户未激活,cookie似乎失效了")
                print("失效cookie:{}".format(getCookie()))
                errorCookie(getCookie())
                print("已跳过第{}位用户的激活".format(cookieIndex))
                return True
        else:
            print("当前用户未激活")
            return False
    else:
        print("当前用户未激活")
        return False


def setCookie():
    if(driver.current_url.find(pddUrl) == -1):
        toPddHome()
    driver.add_cookie({"name": "PDDAccessToken", "value":  getCookie()})


def nextUser():
    print("开始激活第{}位用户...".format(cookieIndex))
    if testVerifiy():
        pass
    else:
        # setCookie()
        # toVerifiy()
        pass


def inputCommand():
    print("________________________")
    command = input("请按回车激活下一个cookie:")
    if command == "":
        # if testVerifiy():
        print("\n-----------------")
        # 如果验证通过,记录更新cookie下一位用户的索引
        global cookieIndex
        cookieIndex = cookieIndex+1
        saveConfig(cookieIndex)
        nextUser()
        inputCommand()
        # else:
        #     print("第{}位用户似乎激活失败了,请重新激活".format(cookieIndex))
        #     inputCommand()
    elif command == "0":
        skipCookie()
        # if testVerifiy():
        print("\n-----------------")
        # 如果验证通过,记录更新cookie下一位用户的索引
        # global cookieIndex
        cookieIndex = cookieIndex+1
        saveConfig(cookieIndex)
        nextUser()
        inputCommand()
        # else:
        #     print("第{}位用户似乎激活失败了,请重新激活".format(cookieIndex))
        #     inputCommand()
    elif command == "help":
        print(helpText)
        inputCommand()
    else:
        inputCommand()


def main():
    print(helpText)
    readCookieTxt()
    loadConfig()
    print("上次激活到 第{}位用户,将从第{}位用户开始继续激活".format(cookieIndex, cookieIndex))
    chrome_init()
    inputCommand()


main()
