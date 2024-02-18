from requests import Session

# Create a session object to maintain cookies across requests
session = Session()

# Define the URL for requesting the OTP, ensuring all version codes and region settings are consistent
url_get_otp = "https://api16-normal-c-useast1a.tiktokv.com/passport/mobile/get_otp/?next=https%3A%2F%2Ftv.tiktok.com&account_sdk_source=app&passport-sdk-version=18&os_api=25&device_type=ASUS_Z01QD&ssmix=a&manifest_version_code=111012&dpi=240&carrier_region=US&uoo=0&region=US&app_name=tiktok_tv&version_name=11.10.12&timezone_offset=3600&ts=1680991802&ab_version=11.10.12&pass-route=1&cpu_support64=true&pass-region=1&storage_type=1&ac2=wifi&ac=wifi&app_type=normal&host_abi=armeabi-v7a&channel=googleplay&update_version_code=111012&_rticket=1680991802661&device_platform=android&iid=7219304446219192070&build_number=11.10.12&locale=de_DE&op_region=US&version_code=111012&timezone_name=America%2FNew_York&cdid=f03bebda-f46d-48ac-a48c-94c3be811ac2&openudid=d8e48a4690fded4b&sys_region=US&device_id=7191957835704632838&app_language=de&resolution=1280*720&device_brand=Asus&language=de&os_version=12.1&aid=4082&okhttp_version=4.0.71.6-tiktok"

# Headers for the request, adjusted to ensure all version codes and region settings are consistent
headers = {
    "accept-encoding": "gzip",
    "connection": "Keep-Alive",
    "cookie": "store-idc=maliva; store-country-code=us; store-country-code-src=did; install_id=3285777376617822; ttreq=1$61d3b081ce60c998b44f7b7190d5c3006ef38e90; odin_tt=b3d2f53798a67f4f047cfb9ffc40bcc738db759ef09452d06e0a9b19457ea8cad201edc274985908614eb37b8b6bb980a2d8153f700aefd6de7752b84a0e2e44a28c2cf70c02f91d4602a8551ad49ee9; passport_csrf_token=73325592c16331165e9aa4173fb5a3cd; passport_csrf_token_default=73325592c16331165e9aa4173fb5a3cd; msToken=-FKWjXsLY02ElQb95HnVFhQJnYt1FkV7uTTeZ8q56ALTOWmwPBf2hMqSIdPb4NzB-8gjZ1-NaKy1oGSFCyyrh5bMqGmQVC-m-3LJ1ID3w6yMqEWiK5lewNec",
    "host": "api16-normal-c-useast1a.tiktokv.com",
    "passport-sdk-version": "18",
    "sdk-version": "2",
    "user-agent": "com.tiktok.tv/111012 (Linux; U; Android 12.1; de_DE; ASUS_Z01QD; Build/N2G48H;tt-ok/3.10.0.2)",
    "x-gorgon": "840480f60000ffe38555ef116d192387ed21f5b04e675024cf1f",
    "x-khronos": "1685409367",
    "x-ss-req-ticket": "1669254571963",
    "x-tt-passport-csrf-token": "73325592c16331165e9aa4173fb5a3cd",
    "x-tt-store-region": "us",
    "x-tt-store-region-did": "us",
    "x-tt-store-region-src": "did",
    "x-tt-store-region-uid": "",
}

# Request OTP
response_get_otp = session.get(url_get_otp, headers=headers)
data_get_otp = response_get_otp.json()
otp = data_get_otp["data"]["otp"]
print(otp, "https://tv.tiktok.com/activate")

# Replace the URL with the one for checking the OTP, ensuring all version codes and region settings are consistent
url_check_otp = f"https://api16-normal-c-useast1a.tiktokv.com/passport/mobile/check_otp/?otp={otp}&next=https%3A%2F%2Ftv.tiktok.com&client_secret=SC&account_sdk_source=app&passport-sdk-version=18&os_api=25&device_type=ASUS_Z01QD&ssmix=a&manifest_version_code=111012&dpi=240&carrier_region=US&uoo=0&region=US&app_name=tiktok_tv&version_name=11.10.12&timezone_offset=3600&ts=1680992294&ab_version=11.10.12&pass-route=1&cpu_support64=true&pass-region=1&storage_type=1&ac2=wifi&ac=wifi&app_type=normal&host_abi=armeabi-v7a&channel=googleplay&update_version_code=111012&_rticket=1680992294965&device_platform=android&iid=7219304446219192070&build_number=11.10.12&locale=de_DE&op_region=US&version_code=111012&timezone_name=America%2FNew_York&cdid=f03bebda-f46d-48ac-a48c-94c3be811ac2&openudid=d8e48a4690fded4b&sys_region=US&device_id=7191957835704632838&app_language=de&resolution=1280*720&device_brand=Asus&language=de&os_version=12.1&aid=4082&okhttp_version=4.0.71.6-tiktok"
response_check_otp = session.get(url_check_otp, headers=headers)

# Check for the presence of session_key in the response to confirm login success
if "session_key" in response_check_otp.text:
    print("Login successful, fetching cookies...")
    cookies = session.cookies.get_dict()
    print(cookies)
else:
    print("Login failed or OTP expired.")

# Access the main site tiktok.com to pull all cookies
response_tiktok = session.get("https://www.tiktok.com", headers=headers)
cookies_main_site = session.cookies.get_dict()
print("Cookies from tiktok.com:", cookies_main_site)
