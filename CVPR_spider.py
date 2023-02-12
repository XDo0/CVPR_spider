import os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests

TARGET_URL="https://openaccess.thecvf.com/CVPR2022?day=all"
RES_FILE="cvpr_info.csv"

# 以下两个变量需要在html确定出可以区分的词
from_paper="PoseTrack21"
# end_paper需要多数一个
end_paper="Privacy-Preserving"

#get web context
def get_context(url):
    """
    params: 
        url: link
    return:
        web_context
    """
    web_context = requests.get(url)
    return web_context.text

def get_pdfs(html):
    soup=BeautifulSoup(html,'lxml')
    dd=soup.find_all("dd")[2:]
    prefix_url="http://openaccess.thecvf.com/"
    count=len(dd)
    print("Total:",int(count/2),"papers.")
    flag=False
    for i in range(count):
        if i%2 == 0:
            pdf1 = prefix_url + str(dd[i].find('a'))[9:-9]
            pos = pdf1.find('papers')+7
            paper_key = pdf1[pos:]
            paper_key=paper_key[:-20]
            paper_list=paper_key.split("_")[1:]
            join_str=" "
            paper_name=join_str.join(paper_list)
            if  from_paper in paper_name:
                flag=True
            if end_paper in paper_name:
                flag=False
                break
            if flag==True:
                pdff = requests.get(pdf1).content
                print("Downloading",int(i/2+1),"paper.")
                with open("CVPR2022_100/"+paper_name+".pdf", 'wb') as handler:
                    handler.write(pdff)
                print("Download "+paper_name+" Successfully!")



def get_pdf_info(pdf_file):
    ...
    

if __name__ =='__main__':
    html_content=get_context(TARGET_URL)
    get_pdfs(html_content)
    
    # TODO 可以用pdfminer,regex加上些逻辑解析pdf




