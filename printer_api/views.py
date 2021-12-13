import json
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Department, User
from django.http import JsonResponse


# Create your views here.

@csrf_exempt
def testView(request):
    allParams = {'Name': 'blank.pdf', 'Mode': '100', 'Url': 'http://', 'WebUserName': '', 'WebPasswd': '', 'POLICY_SRV_USER_ID': '', 'DocPasswd': '', 'PageMode': '0', 'StartPage': '1', 'EndPage': '1', 'Resolution': '1', 'Gradation': '2', 'HalfToneTxt': '1', 'HalfToneGrp': '2', 'HalfToneImg': '2', 'AstIntensity': '2', 'AstGrap': '1', 'AstText': '0', 'AstImag': '1', 'TrappingSwitch': '0', 'TrappingWidthUp': '1', 'TrappingWidthDown': '1', 'TrappingWidthLeft': '1', 'TrappingWidthRight': '1', 'TrappingDensityC': '4', 'TrappingDensityM': '4', 'TrappingDensityY': '4', 'WidthAdjust': '0', 'WidthAdjustHorizon': '1', 'WidthAdjustVertical': '1', 'WidthAdjustTargCol': '0', 'ColorMode': '0', 'C_Render': '', 'MatchModeRGB': '0', 'MatchModeCMYK': '0', 'C_RGB_Pro': '1', 'RGBDLName': '', 'C_CMYK_Pro': '4', 'CMYKDLName': '', 'C_OUT_ProT': '5',
                 'C_OUT_ProG': '5', 'C_OUT_ProI': '5', 'OUTDLNameT': '', 'OUTDLNameG': '', 'OUTDLNameI': '', 'RGBDevLinkProf': '4', 'DevLinkRgbDLName': '', 'CMYKDevLinkProf': '1', 'DevLinkCmykDLName': '', 'C_Matching': '0', 'C_GRAY_Pro': '1', 'C_Pure_B': '1', 'C_B_OVPrn': '1', 'C_OVR_EFF': '1', 'C_Bright': '100', 'SPOT_Color': '1', 'GrySclCnv': '1', 'DotGainAjst': '2', 'Copies': '1', 'MediaSize': '0', 'MediaType': '33', 'ManualFeed': '0', 'FitSize': '0', 'WidePrn': '0', 'DuplexType': '0', 'NupPrint': '0', 'NupStart': '0', 'Sort': '0', 'PunchPos': '0', 'PunchType': '0', 'StapleType': '0', 'BookType': '2', 'SaddlePress': '0', 'SaddleVal': '0', 'Annotation': '2', 'C_Gray_Com': '', 'StoreBox': '0', 'BoxNo': '0', 'BOXName': '', 'Flag': 'Exec_Data_Pdf', 'Dummy': '1638865814312', 'PrintDocPass': '', 'PolicySrvUserID': '', 'PolicySrvPasswd': ''}
    print(request.FILES)
    allParams['Name'] = request.POST.get('Name')
    allParams['ColorMode'] = request.POST.get('color')
    allParams['MediaSize'] = request.POST.get('pageType')
    print(request.POST.get('cookie'))
    cookie = request.POST.get('cookie')
    cookie = cookie.replace('path=/,', "")
    cookie = cookie.replace('path=/', "")
    print(cookie)
    
    try:
        user = User.objects.get(username=username)
        user.pages = int(user.pages) + int(pages)
        user.save()
    except User.DoesNotExist:
        return HttpResponse("User not found when trying to update pages printed attribute", status=501)
    except Exception:
        return HttpResponse("Something terrible happened :) ", status=501)

    r = requests.post(
        'http://192.168.20.212:8000/rps/pprint.cgi/', data=allParams, files=request.FILES, headers={"Cookie": cookie})
    print(r.status_code)

    return JsonResponse({'status': 'success', 'message': "printed", "params": allParams, "cookie": cookie})


@csrf_exempt
def login(request):
    # check if incoming json is correct
    try:
        data = json.loads(request.read())
        username = data['username']
        password = data['password']

    except:
        return JsonResponse({'status': 'false', 'message': "bad data"}, status=400)

    # check username password match
    try:
        user = User.objects.get(username=username)
        if not user.is_password_correct(password):
            raise Exception('wrong pass')
    except:
        return HttpResponse("wrong username or password", status=401)

    # login into printer
    try:
        payload = {"deptid": user.department.id,
                   "password": user.department.password, "uri": '/'}

        # print(payload)
        r = requests.post('http://192.168.20.212:8000/', payload)
        # print(r.request.headers)
        cookie = r.request.headers['Cookie']
        # print(cookie)

        # getting the IR value
        r2 = requests.post(
            'http://192.168.20.212:8000/rps/nativetop.cgi?RUIPNxBundle=&CorePGTAG=PGTAG_DIRC_PDF', headers={"Cookie": cookie})
        print("r2 headers")
        print(r2.headers)
        cookie2 = r2.headers['Set-Cookie']

        # set final cookie
        finalCookie = cookie + '; ' + cookie2
        print(finalCookie)

        return JsonResponse({"cookie": finalCookie, "username": username})

    except:
        return HttpResponse("printer login failed", status=401)


@csrf_exempt
def register(request):
    data = json.loads(request.read())
    name = data["name"]
    username = data["username"]
    password = data["password"]
    department_id = data["department"]

    # department id check
    try:
        department = Department.objects.get(pk=department_id)
    except:
        JsonResponse(
            {'status': 'false', 'message': "Department does not exists"}, status=500)

    # check username is unique
    if(User.objects.filter(username=username).exists()):
        return JsonResponse({'status': 'false', 'message': "email already exists"}, status=400)

    # create and save new user
    try:
        new_user = User(name=name, username=username,
                        password=password, department=department)
        new_user.save()

        return JsonResponse({'status': "success", "message": "User registeres successfuly"})

    except:
        return JsonResponse({'status': 'false', 'message': "Contact admin"}, status=500)


@csrf_exempt
def success(request):
    data = json.loads(request.read())
    department_id = data["department"]
    pages = int(data["pages"])

    department = Department.objects.get(pk=department_id)
    department.pages_remaining = department.pages_remaining - pages
    department.save()
    # print("success")
    # print(department.pages_remaining)

    return HttpResponse(department.pages_remaining)
