from tkinter import *
from tkinter import font
from tkinter import messagebox
from xml.dom.minidom import parseString  # minidom 모듈의 파싱 함수를 임포트합니다.
from xml.etree import ElementTree
import urllib.request

import spam

OilDoc = []  # XML문서 파싱한 후 반환된 DOC 객체 변수
key = "W3mkZxFNhPwgUkfjphd6SwD820FBnSKJ0UF6YzyvR3Q0AMU1skw3oiH2sD%2BKi17i%2Bs2eHCN%2Ftg3e9MrIEMTxaA%3D%3D"

g_Tk = Tk()
g_Tk.geometry("1100x650+750+200")        #tk윈도우 크기
DataList = []
startClick = 0
start = 0


def InitTopText():  # 제목
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="[전국 고속도로 LPG 주유소 검색 APP]")
    MainText.pack()
    MainText.place(x=20)

def InitSearchListBox():  # 검색필터
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=50)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont,
                            activestyle='none', width=10, height=1, borderwidth=12,
                            relief='ridge', yscrollcommand=ListBoxScrollbar.set)

    SearchListBox.insert(1, "회사")
    SearchListBox.insert(2, "고속도로")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=50)
    ListBoxScrollbar.config(command=SearchListBox.yview)


def InitInputLabel():  # 검색창
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    InputLabel = Entry(g_Tk, font=TempFont, width=38, borderwidth=12, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=105)


def InitSearchButton():         # 검색버튼
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=470, y=110)

def InitInformationButton():  # 이메일버튼
    TempFont= font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    informationButton = Button(g_Tk, font=TempFont, text="도움말", command=InformationAction)
    informationButton.pack()
    informationButton.place(x=400, y=550)


def SearchButtonAction():         # 검색버튼 누름
    global SearchListBox
    global RenderText
    global searchStatus
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    iSearchIndex = SearchListBox.curselection()[0]
    if iSearchIndex == 0:
        SearchCompany()
    elif iSearchIndex == 1:
        SearchHighway()

    RenderText.configure(state='disabled')

def InitEmailSubjectText():  # 이메일 제목 텍스트
    TempFont = font.Font(g_Tk, size=17, weight='bold', family='Consolas')
    EmilText = Label(g_Tk, font=TempFont, text="=결과 메일 전송")
    EmilText.pack()
    EmilText.place(x=555,y=65)

def InitEmailText():  # 이메일 텍스트
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    EmilText = Label(g_Tk, font=TempFont, text="E-Mail : ")
    EmilText.pack()
    EmilText.place(x=545,y=114)

def InitReceiveEmailLabel():  # 받는 이메일 창
    global receiveEmailLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    receiveEmailLabel = Entry(g_Tk, font=TempFont, width=32, borderwidth=12, relief='ridge')
    receiveEmailLabel.pack()
    receiveEmailLabel.place(x=665, y=105)

def InitEmailButton():          # 이메일버튼
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    EmailButton = Button(g_Tk, font=TempFont, text="검색 결과 Gmail 전송", command=EmailButtonAction)
    EmailButton.pack()
    EmailButton.place(x=890, y=160)

def InitCompanyButton():          # 회사 목록 버튼
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    CompanyButton = Button(g_Tk, font=TempFont, text="회사 목록", command=CompanyButtonAction)
    CompanyButton.pack()
    CompanyButton.place(x=200, y=50)
def InitHighwayButton():  # 고속도로 목록 버튼
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    HighwayButton = Button(g_Tk, font=TempFont, text="고속도로 목록", command=HighwayButtonAction)
    HighwayButton.pack()
    HighwayButton.place(x=300, y=50)

def CompanyButtonAction():  # 이메일버튼 누름
    messagebox.showinfo(title="회사목록", message="GS-Caltex\nS-Oil\nSK\n현대\n알뜰")

def HighwayButtonAction():  # 이메일버튼 누름
    messagebox.showinfo(title="고속도로 목록", message="경부선\n남해선\n무안광주선, 광주대구선\n서해안선\n익산포항선\n"
                                              "호남선,논산천안선\n순천완주선\n당진영덕선\n중부선, 통영대전선\n"
                                              "평택제천선\n중부내륙선\n영동선\n중앙선, 신대구부산선\n"
                                              "서울양양선, 서울춘천선\n동해선, 부산울산선\n서울외곽순환선\n"
                                              "남해제2지선\n인천국제공항선\n서천공주선\n제2서해안선, 평택시흥선\n"
                                              "호남선의지선\n중부내륙선의지선")

def MakeHtmlDoc(OILList):       #검색결과를 HTML로 전환
    from xml.dom.minidom import getDOMImplementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    body = newdoc.createElement('body')

    for oilitem in OILList:
        b = newdoc.createElement('b')
        routeText = newdoc.createTextNode(oilitem[0])
        b.appendChild(routeText)

        body.appendChild(b)

        br = newdoc.createElement('br')

        body.appendChild(br)

        p = newdoc.createElement('p')
        nameText = newdoc.createTextNode(oilitem[1])
        p.appendChild(nameText)

        body.appendChild(p)

        br = newdoc.createElement('br')

        body.appendChild(br)

        p = newdoc.createElement('p')
        nameText = newdoc.createTextNode(oilitem[2])
        p.appendChild(nameText)

        body.appendChild(p)
        body.appendChild(br)  # line end

    # append Body
    top_element.appendChild(body)

    return newdoc.toxml()

def SearchHighwayTitle(keyword):                #입력된 고속도로 명으로 doc을 만든다.
    mailDoc = LoadXMLFromURL()
    retlist = []
    if not checkDocument():
        return None
    for i in range(3):
        try:
            tree = ElementTree.fromstring(str(mailDoc[i].toxml()))  # ElementTree는 사전 형식으로 만들어준다.
        except Exception:
            print("Element Tree parsing Error : maybe the xml document is not corrected.")
            return None

        # OilStation 엘리먼트 리스트를 가져 옵니다.
        OilStationElements = tree.getiterator("list")
        for item in OilStationElements:
            strOilCompany = item.find("oilCompany")
            routeName = item.find("routeName")
            serviceAreaName = item.find("serviceAreaName")
            if (keyword == '호남선,논산천안선'):
                if routeName.text.find('호남선,논산천안선') >= 0 or routeName.text.find('호남선,논산-천안선') >= 0:
                    retlist.append(
                        ("고속도로 명 : " + routeName.text, "주유소 이름 : " + serviceAreaName.text,
                         "회사 이름 :" + strOilCompany.text))
            elif (routeName.text.find(keyword) >= 0):
                retlist.append(
                    ("고속도로 명 : " + routeName.text, "주유소 이름 : " + serviceAreaName.text, "회사 이름 :" + strOilCompany.text))

    return retlist

def EmailButtonAction():         # 이메일버튼 누름
    global startClick
    if startClick == 1:
        import mysmtplib
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText

        global recipentMail
        global InputLabel
        global searchStatus
        host = "smtp.gmail.com"  # your smtp address
        port = "587"
        htmlFileName = "logo.html"

        sendMail = "arkimist@gmail.com"
        recipientMail = receiveEmailLabel.get()
        msgtext = "당신의 검색결과 입니다."

        # 헤더에 첨부 파일에 대한 정보를 추가 시킨다.
        msg = MIMEBase("multipart", "alternative")
        msg['Subject'] = "전국 고속도로 LPG 주유소 검색"
        msg['From'] = sendMail
        msg['To'] = recipientMail

        html = MakeHtmlDoc(SearchHighwayTitle(InputLabel.get()))

        msgPart = MIMEText(msgtext, 'plain')
        oilPart = MIMEText(html, 'html', _charset = 'UTF-8')

        # MIME 문서를 생성합니다.
        htmlFD = open(htmlFileName, 'rb')
        HtmlPart = MIMEText(htmlFD.read(), 'html', _charset='UTF-8')
        htmlFD.close()

        # 메세지에 생성한 MIME 문서를 첨부합니다.
        msg.attach(HtmlPart)
        msg.attach(msgPart)
        msg.attach(oilPart)

        # 메일을 발송한다.
        print ("connect smtp server ... ")
        s = mysmtplib.MySMTP(host, port)

        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("arkimist@gmail.com","9692gyawkd")
        s.sendmail(sendMail , [recipientMail], msg.as_string())
        s.close()

        messagebox.showinfo(title="완료", message="최근 고속도로 명 결과가 메일로 전송되었습니다.")
    else:
        messagebox.showinfo(title="주의!", message="고속도로 명을 검색 하고 난 뒤에 눌러주세요.")

def InformationAction():         # 이메일버튼 누름
        messagebox.showinfo(title="도움말", message="1.이메일 전송 기능은 고속도로명을 검색 한 뒤에만 가능합니다.\n"
                                                 "2.검색어는 상단의 '회사목록','고속도로목록'을 눌러서 확인할 수 있습니다.")

def LoadXMLFromURL():
    doc = []
    for i in range (3):
        url = "http://data.ex.co.kr/exopenapi/business/lpgServiceAreaInfo?serviceKey=" + key + "&type=xml&numOfRows=99&pageSize=99&pageNo="+str(i+1)+"&startPage=1"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            dom = response.read()
            doc.append(parseString(dom))
            print("XML 파일",i+1 ,"페이지를 성공적으로 불러왔습니다.")
        else:
            print("XML 파일",i+1 ,"페이지를 불러오지 못했습니다.")

    if checkDoc(doc):
        return doc
    return None

def SearchCompany():
    global OilDoc
    global RenderText
    global startClick
    for i in range (3):
        url = "http://data.ex.co.kr/exopenapi/business/lpgServiceAreaInfo?serviceKey=" + key + "&type=xml&numOfRows=99&pageSize=99&pageNo="+str(i+1)+"&startPage=1"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        OilDoc.append(response.read())


    global DataList
    DataList.clear()


    for i in range(0,3):
        if OilDoc[i] == None:
            print("에러!")
        else:
            parseData = parseString(OilDoc[i])
            GeoInfoComapny = parseData.childNodes
            olist = GeoInfoComapny[0].childNodes

            for c in olist:
                if c.nodeName == "list":
                    subc = c.childNodes
                    if subc[1].firstChild.nodeValue == InputLabel.get():
                        DataList.append((subc[3].firstChild.nodeValue, subc[5].firstChild.nodeValue, subc[1].firstChild.nodeValue))

    for i in range(len(DataList)):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i + 1)
        RenderText.insert(INSERT, "] ")
        RenderText.insert(INSERT, "고속도로 명: ")
        RenderText.insert(INSERT, DataList[i][0])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "주유소 이름: ")
        RenderText.insert(INSERT, DataList[i][1])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "회사 이름: ")
        RenderText.insert(INSERT, DataList[i][2])
        RenderText.insert(INSERT, "\n\n")

def SearchHighway():
    global OilDoc
    global RenderText
    global startClick
    for i in range (3):
        url = "http://data.ex.co.kr/exopenapi/business/lpgServiceAreaInfo?serviceKey=" + key + "&type=xml&numOfRows=99&pageSize=99&pageNo="+str(i+1)+"&startPage=1"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        OilDoc.append(response.read())


    global DataList
    DataList.clear()


    for i in range(0,3):
        if OilDoc[i] == None:
            print("에러!")
        else:
            parseData = parseString(OilDoc[i])
            GeoInfoComapny = parseData.childNodes
            olist = GeoInfoComapny[0].childNodes

            for c in olist:
                if c.nodeName == "list":
                    subc = c.childNodes
                    if subc[3].firstChild.nodeValue == InputLabel.get():
                        DataList.append((subc[1].firstChild.nodeValue, subc[5].firstChild.nodeValue, subc[3].firstChild.nodeValue))

    for i in range(len(DataList)):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i + 1)
        RenderText.insert(INSERT, "] ")
        RenderText.insert(INSERT, "고속도로 명: ")
        RenderText.insert(INSERT, DataList[i][0])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "주유소 이름: ")
        RenderText.insert(INSERT, DataList[i][1])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "회사 이름: ")
        RenderText.insert(INSERT, DataList[i][2])
        RenderText.insert(INSERT, "\n\n")
    startClick = 1

def InitRenderText():  # 검색 결과 출력
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, font = TempFont, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

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

InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitInformationButton()
InitCompanyButton()
InitHighwayButton()
InitEmailSubjectText()
InitEmailText()
InitReceiveEmailLabel()
InitEmailButton()
InitRenderText()
if start == 0:
    messagebox.showinfo(title="어서오세요!", message=spam.enterLine())
    start = 1
g_Tk.mainloop()
