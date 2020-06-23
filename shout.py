import dl72
import re
import random
import os.path
import requests
import datetime
import random
import tweepy
import sys

def get_api():
    with open("tweettoken") as f:
        c_k = f.readline().strip()
        c_s = f.readline().strip()
        a_k = f.readline().strip()
        a_s = f.readline().strip()
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    api = tweepy.API(auth)
    return api

def tweet(text):
    api = get_api()
    api.update_status(text)



def get_random_wikipedia(t=0):
    try:
        dl = dl72.DL72(
            "https://ja.wikipedia.org/wiki/%E7%89%B9%E5%88%A5:%E3%81%8A%E3%81%BE%E3%81%8B%E3%81%9B%E8%A1%A8%E7%A4%BA"
        )
        soup = dl.soup
        content = soup.select_one("#mw-content-text").select_one("p")
        ruby = re.search(
            "(（.+?）)", content.text).group(0)[1:].replace("（", "").replace("）", "")
        ruby = ruby.replace(" ", "").replace(
            "　", "").split(",")[0].split("、")[0]
        body = re.search(
            "^(.+?)（", content.text).group(0).replace("（", "").replace("）", "")
        categories = soup.select_one("#mw-normal-catlinks").select("li")
        categories = [c.select_one("a").text for c in categories]
        for c in categories:
            ignores = ["人","学校","大学","年生","年没","世紀生","世紀没","画像提供依頼","の神社","駅","法律","の寺院","の郵便局","氏","の企業","の建築物","の河川","のダム","の法","の公園","設立","市の","町の","村の","区の","の市","の町","の村","の区","市域の","県の","番組","ドラマ","のシングル","のアルバム","の廃止市町村","の一覧","年代","不詳","不明","小説","者","家","組合","条例"]
            for ignore in ignores:
                if ignore in c :
                    raise Exception
        for r in ruby:
            if not ((r >= "あ" and r <= "ん") or (r >= "ア" and r <= "ン")):
                raise Exception
        if ruby in ["しゅような","いちらん"] :
            raise Exception
        for e in ["もく","か"]:
            if ruby.endswith(e):
                raise Exception
        if body in categories:
            raise Exception
        #tmpruby = ""
        #for r in ruby:
        #    if r >= "あ" and r <= "ん":
        #        tmpruby += r
        #    else:
        #        tmpruby += chr(ord(r) - 96)
        #ruby = tmpruby
        return {
            "ruby": ruby,
            "name": body,
            "categories": categories,
            "url": dl.got.url
        }
    except Exception as e:
        print("failure")
        return get_random_wikipedia(t + 1)


tmpfilepath = "/tmp/sprintshout-tweet.txt"
def sprint_shaut():
    wiki = get_random_wikipedia()
    if wiki == None:
        return "失敗しました..."
    result = ""
    with open(tmpfilepath, "w") as f:
        f.write(wiki["ruby"] + " (" + wiki["name"] + ")\n" + wiki["url"])
    shout = ""
    rand = random.randint(0, len(wiki["ruby"])-1)
    for i, r in enumerate(wiki["ruby"]):
        if i == rand:
            shout += r
        else:
            shout += "◯"
    result += "今回の問題 : " + shout + "("+str(len(wiki["ruby"]))+"文字)"
    result += "\n" + "ヒント:" + ",".join(wiki["categories"])
    result += "\n答えは15分後発表！"
    return result

def answer():
    result = ""
    with open(tmpfilepath, "r") as f:
        result += "答えは " + "".join(f.readlines()) + "\n"
    result += "\n当てられなかった人は徳を貯めて次回頑張ろうね！"
    return result
if __name__ == "__main__":
    if len(sys.argv) == 2 :
        tweet(sprint_shaut())
    else:
        tweet(answer())

