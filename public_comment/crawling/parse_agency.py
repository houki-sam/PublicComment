import re

#省庁局データをperse
def ministry_parser(string):
    dictionary = {}
    ministry = re.search(r"(?P<ministry>.*省)*(?P<agency>.*庁)*(?P<station>.*局)*.*", string)#正規表現でurlパラメータを取得

    for x in ["ministry","agency","station"]:
        dictionary[x] = ministry[x]
    return dictionary