import http.client, urllib.request, urllib.parse, urllib.error, base64, json

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
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, '{"url":"http://goldameirspanish.weebly.com/uploads/4/7/0/9/4709551/vocabulary.jpg"}', headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    obj = json.loads(data)
    for region in obj["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                try:
                    print(word["text"], end=" ")
                except UnicodeEncodeError:
                    continue
            print()
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
