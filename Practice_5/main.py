import json
import requests
import sys
import webbrowser


def getGraphizForLib(requiresDist, libName):
    allPath = ""
    nextLine = "%3B%0A%20%20"
    alreadyUsed = [""]

    libName = str(libName).replace('-', '_')

    if requiresDist == None:
        allPath += libName

    else:
        for item in requiresDist:
            if (item != libName):
                if(not(str(item) in alreadyUsed)):
                    allPath += libName + "->" + str(item) + nextLine
                    alreadyUsed.append(str(item))
    return allPath


def getRequiresDist(libName):
    mask = "https://pypi.org/pypi/"
    mask2 = "/json"
    url = mask + libName + mask2
    site = requests.get(url=url)
    if (site.status_code == 404):
        print("The library with this name could not be obtained! Enter another name.")
        return None
    jsonFile = json.loads(site.text)
    return jsonFile

def formatingRequires(requiresDist):
    if not (requiresDist == None):
        for i in range(0, len(requiresDist)):
            requiresDist[i] = \
            str(requiresDist[i]).split('>', 1)[0].split('<', 1)[0].split("extra", 1)[0].split('[', 1)[0].split(';', 1)[
                0].split('=', 1)[0].split('(', 1)[0].split(' ', 1)[0].split('.', 1)[0]
            requiresDist[i] = str(requiresDist[i]).replace('-', '_')
    return requiresDist

def childRequiresDist(requiresDist, childPath="", deep = 0):
    if requiresDist != None:
        for item in requiresDist:
            jsonFile = getRequiresDist(str(item))
            if (jsonFile != None):
                requiresDist = formatingRequires(jsonFile['info']['requires_dist'])
                libName = jsonFile['info']['name']
                childPath += getGraphizForLib(requiresDist, libName)
    return childPath

def childGetRequiresDist(childNames):
    newRequiresDist = ""
    for item in childNames:
        newRequiresDist += getRequiresDist(item)
    return newRequiresDist
if __name__ == "__main__":
    while True:
        if "--script" != sys.argv[1]:
            print("No such command in script")
            exit(-1)
        else:
            ## ЭТАП ПОДКЛЮЧЕНИЯ К САЙТУ
            graphizSite = "https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0A%20%20%20%20"
            graphizSite2 = "%0A%7D"
            allPat = ""
            nextName = ""
            libName = sys.argv[2]

            ## ЭТАП СОЗДАНИЯ JSON
            jsonFile = getRequiresDist(libName)
            requiresDist = jsonFile['info']['requires_dist']
            libName = jsonFile['info']['name']
            requiresDist = formatingRequires(requiresDist)  # ФОРМАТИРОВАНИЕ ТЕКСТА В УДОБНЫЙ ФОРМАТ
            siteReq = graphizSite + getGraphizForLib(requiresDist, libName) # + childRequiresDist(requiresDist=requiresDist) + graphizSite2
            for i in range(0, int(sys.argv[3]) - 2):
                siteReq += childRequiresDist(requiresDist)
                requiresDist = childRequiresDist(requiresDist)
            siteReq += graphizSite2
            # print(siteReq)
            webbrowser.open(siteReq)
            exit(0)
