import requests
import os
import sys

def crawl(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open("crawing.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            print("Failed to fetch page. Status code:", response.status_code)
            return 

    except Exception as e:
        print("An error occurred:", e)
        return
    
    with open("crawing.txt", "r", encoding = "utf-8") as f:
        content = f.read()

    os.remove("crawing.txt")
 
    
    i = 0
    spaceFlag = True
    links = []

    text = ''
    while i < len(content):
        if content[i] == "<":
            if content[i + 1] == 's' and content[i + 2] == 'c' and content[i + 3] == 'r' and content[i + 4] == 'i'  and content[i + 5] == 'p' and content[i + 6] == 't':
                i = content.find("<", i+2)

            if content[i + 1] == 's' and content[i + 2] == 't' and content[i + 3] == 'y' and content[i + 4] == 'l'  and content[i + 5] == 'e':
                i = content.find("<", i+2)

            if content[i+1] == 'a':
                link_index = content.find('href', i)
                if content[link_index + 6: link_index + 11] == 'https':
                    closing_index = content.find('"', link_index + 6)
                    links.append(content[link_index + 5: closing_index + 1])
        
            i = content.find('>',i+1)


        elif True:
            if content[i].isspace() and spaceFlag:
                text += content[i]
                spaceFlag = False
            
            else:
                if not content[i].isspace():
                    text += content[i]
                    spaceFlag = True
                
        i += 1  

    print(text)

    for link in links:
        print(link)


if __name__=="__main__":
    path = sys.argv[1]
    crawl(path)
