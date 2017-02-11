import http.client, urllib.request, urllib.parse, urllib.error, base64, json, random, csv
from xml.etree import ElementTree
from flask import Flask, render_template

def api_vision_ocr(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '8b0a9610561245a0893539a6bf1aad64',
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'language': 'unk',
        'detectOrientation ': 'true',
    })
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body = '{"url":"' + url + '"}', headers = headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        obj = json.loads(data)
        conn.close()
        return obj
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def api_vision_describe(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '8b0a9610561245a0893539a6bf1aad64',
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'maxCandidates': '1',
    })
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/describe?%s" % params, body = '{"url":"' + url + '"}', headers = headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        obj = json.loads(data)
        conn.close()
        return obj
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def api_bing_images_search(query):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '4095908f60d14316b00bc6e8e6828cac'
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'q': query,
        'mkt': 'en-us',
        'aspect': 'square',
        'count': '10',
        'safeSearch': 'strict'
    })
    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, headers = headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        obj = json.loads(data)
        conn.close()
        return obj
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def api_translate_text(text, lang):
    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
    conn.request("POST", "/sts/v1.0/issueToken?Subscription-Key=eefc7a053aa54f4aa2961f8900fe6da6")
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    finalToken = "Bearer " + data
    params = urllib.parse.urlencode({
        'appid': finalToken,
        'text': text,
        'to': lang
    })
    try:
        conn = http.client.HTTPSConnection('api.microsofttranslator.com')
        conn.request("GET", "/v2/Http.svc/Translate?%s" % params)
        response = conn.getresponse()
        data = ElementTree.fromstring(response.read()).text
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def main():
    ocr = api_vision_ocr("http://i.imgur.com/08i857w.png")
    lines = [" ".join([word["text"]  for word in line["words"]]) for region in ocr["regions"] for line in region["lines"]]
    for line in lines:
        print(line.encode('utf8'))
        results = api_bing_images_search(api_translate_text(line, 'en'))
        picurl = random.choice(results["value"])["thumbnailUrl"]
        print("<img src='"+picurl+"'></img>")
        description = api_vision_describe(picurl)
        captions = [caption["text"] for caption in description["description"]["captions"]]
        for caption in captions:
            print(api_translate_text(caption, 'es'))
        print()
main()