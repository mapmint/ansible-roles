from bs4 import BeautifulSoup
import requests
import re
import os
print("STATUS: import complete")

url = 'https://cran.r-project.org/src/contrib/'
ext = 'tar.gz'

def listFD(url, ext=''):
    page = requests.get(url).text
    # print(page)
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

print("STATUS: loading data from the server url")
res = listFD(url, ext)

print("STATUS: fetching the required data")
res_e_ver = ""
res_class_int = ""
res_proxy_ver = ""
for file in res:
    if re.match(r"^https://cran\.r-project\.org/src/contrib//e[0-9].*\.tar\.gz$", file):
        res_e_ver = file.split(r"//")[2]
    elif re.match(r"https://cran\.r-project\.org/src/contrib//classInt_.*\.tar\.gz", file):
        res_class_int = file.split(r"//")[2]
    elif re.match(r"https://cran\.r-project\.org/src/contrib//proxy_.*\.tar\.gz", file):
        res_proxy_ver = file.split(r"//")[2]

print(f"STATUS:\n\t{res_e_ver}\n\t{res_class_int}")

old_e_ver = "      - e1071_1.7-2.tar.gz"
old_classInt = "      - classInt_0.4-1.tar.gz"
old_proxyVersion = "      - proxy_0.4-25.tar.gz"

new_e_ver = f"      - {res_e_ver}"
new_classInt = f"      - {res_class_int}"
new_proxyVersion = f"      - {res_proxy_ver}"

file_path = r"dependencies/tasks/r-cran.yml"

os.system(f'sed --in-place "s/{old_e_ver}/{new_e_ver}/g" "{file_path}"')
os.system(f'sed --in-place "s/{old_classInt}/{new_classInt}/g" "{file_path}"')
os.system(f'sed --in-place "s/{old_proxyVersion}/{new_proxyVersion}/g" "{file_path}"')

print("STATUS: successfully updated the versions :)")