from bs4 import BeautifulSoup
import requests
import re
import os
print("STATUS: import complete")

url = 'http://download.documentfoundation.org/libreoffice/stable/'
ext = 'tar.gz'

def listFD(url, ext=''):
    page = requests.get(url).text
    # print(page)
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

print("STATUS: loading data from the server url")
res = listFD(url, '')
res_list = []
for i in res:
    if re.match(r".*[0-9]+\.[0-9]+\.[0-9]+/$", i):
        res_list.append(i)

final_ver1 = res_list[-1]
final_ver2 = final_ver1[final_ver1.rfind(r"//") + 2:-1]
print(f"STATUS: lo_version = {final_ver2}")

print()
file_path = r"dependencies/vars/main.yml"
old_lo_version = r"lo_version: 6.2.5"
new_lo_version = rf"lo_version: {final_ver2}"

os.system(f'sed --in-place "s/{old_lo_version}/{new_lo_version}/g" {file_path}')

print("STATUS: successfully updated the versions :)")
print(f"{old_lo_version}   --->   {new_lo_version}")
