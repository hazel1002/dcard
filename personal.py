import requests
import json
import pymysql

if __name__ == '__main__':
    resp = requests.get('https://www.dcard.tw/service/api/v2/posts?popular=true&limit=100')
    json_resp = json.loads(resp.text)
    with open('Dcard_articles.json', 'w', encoding='utf-8') as f:
        json.dump(json_resp, f, indent=2,
                  sort_keys=True, ensure_ascii=False)
                  
with open('Dcard_articles.json') as f:
  dcard_data=json.load(f)

def get_information(column):
  content=[]
  for i in dcard_data:
    content.append(i[column])
  return content

titles=get_information("title")
id=get_information("id")
excerpt=get_information("excerpt")


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="12345678",
    db="dcard",
    port=3306,
)

cursor=conn.cursor()
for i in range(len(id)):
    d=id[i]
    t=titles[i]
    e=excerpt[i]
    command="INSERT INTO basic(id,title,excerpt) VALUES (%s,%s,%s)"
    data=(d,t,e)
    try:
        cursor.execute(command,data)
        conn.commit()
        print('success')
    except Exception as e:
        conn.rollback()
        print('error')
        print(e)