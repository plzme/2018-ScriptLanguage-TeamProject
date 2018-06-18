# -*- coding: utf-8 -*-
from xml.dom.minidom import parse, parseString  # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree
import urllib.request


loopFlag = 1  # 무한 루프 제어 변수
xmlFD = -1  # XML문서 파일 디스크립터
OilDoc = []  # XML문서 파싱한 후 반환된 DOC 객체 변수
key = "W3mkZxFNhPwgUkfjphd6SwD820FBnSKJ0UF6YzyvR3Q0AMU1skw3oiH2sD%2BKi17i%2Bs2eHCN%2Ftg3e9MrIEMTxaA%3D%3D"
##lpg = urllib.request.Request("data.ex.co.kr/exopenapi/business/lpgServiceAreaInfo?serviceKey="+key+"&type=xml&numOfRows=10&pageSize=10&pageNo=1&startPage=1")
#url = "http://data.ex.co.kr/exopenapi/business/lpgServiceAreaInfo?serviceKey="+key+"&type=xml&numOfRows=10&pageSize=10&pageNo=1&startPage=1"
#request = urllib.request.Request(url)
#response = urllib.request.urlopen(request)
#rescode = response.getcode()
#if(rescode==200):
#    response_body = response.read()
#    print(response_body.decode('UTF-8'))
#else:
#    print("X")
#print(lpg.getresponse())
#req = url.getresponse()
#if int(parts.status) == 200:
#        dom = parts.read()
#        print(dom.decode('utf-8'))



#### Menu  implementation
def printMenu():
    print('\n')
    print("전국 고속도로 LPG 주유소 검색 입니다.(ver.xml)")
    print("========Menu==========")
    print("xml 불러오기 : l")
    print("Print dom to xml : p")
    print("프로그램 종료 : q")
    print("주유소 목록 출력 : b")
    print("고속도로 내 주유소 이름 검색 : e")
    print("==================")


def launcherFunction(menu):
    global OilDoc  # 전역 변수 선언으로 함수 호출이 끝나도 사용 가능
    if menu == 'l':
        OilDoc = LoadXMLFromFile()
    elif menu == 'q':
        QuitOilStationMgr()
    elif menu == 'p':
        PrintDOMtoXML()
    elif menu == 'b':
        PrintOilStationNameList()
    elif menu == 'e':
        keyword = str(input('키워드를 입력해주세요 :'))
        PrintOilStationList(SearchOilStationTitle(keyword))
    else:
        print ("error : 알수없는 메뉴 키")


#### xml function implementation
def LoadXMLFromFile():
    global xmlFD
    doc = []
    for i in range (3):
        url = "http://data.ex.co.kr/exopenapi/business/lpgServiceAreaInfo?serviceKey=" + key + "&type=xml&numOfRows=99&pageSize=99&pageNo="+str(i+1)+"&startPage=1"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            dom = response.read()
            doc.append(parseString(dom))
            print(doc[i])
            print("XML 파일",i+1 ,"페이지를 성공적으로 불러왔습니다.")
        else:
            print("XML 파일",i+1 ,"페이지를 불러오지 못했습니다.")

    if checkDoc(doc):
        return doc
    return None


def OilStationsFree():
    if checkDocument():
        OilDoc.unlink()  # minidom 객체 해제합니다.


def QuitOilStationMgr():
    global loopFlag
    loopFlag = 0
    OilStationsFree()


def PrintDOMtoXML():
    if checkDocument():
        for i in range(3):
            print(OilDoc[i].toxml())

'''
def PrintOilStationNameList(tags):
    global OilDoc
    if not checkDocument():  # DOM이 None인지 검사합니다.
        return None

    oslist = OilDoc.childNodes
    OilStation = oslist[0].childNodes
    for item in OilStation:
        if item.nodeName == "list":  # 엘리먼트를 중 list인 것을 골라 냅니다.
            subitems = item.childNodes  # list에 들어 있는 노드들을 가져옵니다.
            for atom in subitems:
                if atom.nodeName in tags:
                    print("주유소 이름=", atom.firstChild.nodeValue)  # 책 목록을 출력 합니다.
'''
def PrintOilStationNameList():
    global OilDoc
    if not checkDocument():  # DOM이 None인지 검사합니다.
        return None
    for i in range(3):
        oslist = OilDoc[i].childNodes
        OilStation = oslist[0].childNodes
        for item in OilStation:
            if item.nodeName == "list":  # 엘리먼트를 중 list인 것을 골라 냅니다.
                subitems = item.childNodes  # list에 들어 있는 노드들을 가져옵니다.
                for atom in subitems:
                    if atom.nodeName in ["routeName",]:
                        print("고속도로 명:", atom.firstChild.nodeValue,end='')
                    if atom.nodeName in ["serviceAreaName",]:
                        print(" //// 주유소 이름(방향) :", atom.firstChild.nodeValue)



def SearchOilStationTitle(keyword):
    global OilDoc
    retlist = []
    if not checkDocument():
        return None
    for i in range(3):
        try:
                tree = ElementTree.fromstring(str(OilDoc[i].toxml()))  # ElementTree는 사전 형식으로 만들어준다.
        except Exception:
            print ("Element Tree parsing Error : maybe the xml document is not corrected.")
            return None

        # OilStation 엘리먼트 리스트를 가져 옵니다.
        OilStationElements = tree.getiterator("list")
        for item in OilStationElements:
            oilCompany = item.find("oilCompany")
            routeName = item.find("routeName")
            serviceAreaName = item.find("serviceAreaName")
            if (routeName.text.find(keyword) >= 0):
                retlist.append(("고속도로 명 : " + routeName.text, "주유소 이름 : " + serviceAreaName.text, "회사 이름 :" + oilCompany.text))

    return retlist


def PrintOilStationList(olist):
    for res in olist:
        print(res)


def checkDocument():
    global OilDoc
    for i in range(3):
        if OilDoc[i] == None:
            return False
    return True

def checkDoc(doc):
    for i in range(3):
        if doc[i] == None:
            return False
    return True



##### run #####
while (loopFlag > 0):
    printMenu()
    menuKey = str(input('select menu :'))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")

