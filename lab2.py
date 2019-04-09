import requests
import json
import sys
import time
import sqlite3

reload(sys)
sys.setdefaultencoding('utf8')

def writedb(items) :    
    try:
        conn = sqlite3.connect('DB.db')        
        conn.execute("INSERT INTO detail (name, url, type, likes, love, haha, angry, sad, wow, total_react, created_date) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (items))
        conn.commit()

    except sqlite3.Error as e:
        print('Error %s:' % e.args[0])
    finally:
        conn.close()


def main(since) :
    
    items = []

    ##YanTV Page ID
    page_id='110581908973'

    ##my fb access tokken
    at3='EAAAAZAw4FxQIBAMNi4n0ZAyPwZANAZCnArA3bbZCvw4ZCm6poS0YqQ2tR5ASCHL33ReIR8jNlCW9LaiCZCE7L292FiWl1FPLzgOKDvh7Id9sXIxThGnzkDA6jGB0nFCnk5YFZCXtLsEv9WAzgz0FMfduSnZA5nd3xPW4cPBEjihZAOiwZDZD'

    #posts url format
    post_url = 'https://graph.facebook.com/v3.2/{}/posts?fields=type,message,reactions.type(LIKE).summary(total_count).limit(0).as(like),reactions.type(LOVE).summary(total_count).limit(0).as(love),reactions.type(HAHA).summary(total_count).limit(0).as(haha),reactions.type(ANGRY).summary(total_count).limit(0).as(angry),reactions.type(SAD).summary(total_count).limit(0).as(sad),reactions.type(WOW).summary(total_count).limit(0).as(wow),name,created_time,permalink_url&since={}&access_token={}'    

    #final api url
    url = post_url.format(page_id, since, at3)

    #browser agent
    uAgent = {"User-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1"}

    ###Loop all page since date
    while True :
        ###get data
        print('process page url: ' + url)
        data = requests.get(url, headers = uAgent )

        ##Next page url
        next_page = ''
        if  len(data.json()['data']) >20 :
            next_page = data.json()['paging']['next']

        if next_page == '':
            break
        #print(data.json())
        url = next_page
        #print(next_page)
        time.sleep(0.1)

        ####processing data
        for p in data.json()['data'] :
            #print(p)['message']
            try:
                #print(p['name'] + ' | ' + p['type'] + ' | ' + p['permalink_url'] + ' | ' + p['created_time'])
                #print('name {}, url {}, type {} created_time {}'.format(p['name'], p['permalink_url'], p['type'], p['created_time'])) 
                #print('url {} and parentid {}'.format(p['permalink_url'], p['id']))

                ###Meta Cols
                name = p['name']
                permalink_url = p['permalink_url']
                post_type = p['type']
                ###REACT Cols
                like = p['like']['summary']['total_count']
                love = p['love']['summary']['total_count']
                haha = p['haha']['summary']['total_count']
                angry = p['angry']['summary']['total_count']
                sad = p['sad']['summary']['total_count']
                wow = p['sad']['summary']['total_count']
                total_reactions = like + love + haha + angry + sad + wow
                created_date = p['created_time']

#conn.execute("INSERT INTO post (name, url, type, like, love, haha, angry, sad, wow, total_react, created_date) 
                items = [name, permalink_url, post_type, like, love, haha, angry, sad, wow, total_reactions, created_date]

                print('name {}, url {}, type {}, like {}, love {}, haha {}, angry {}, sad {}, wow {}, total_react {}, created_date {}'.format(name, permalink_url, post_type, like, love, haha, angry, sad, wow, total_reactions, created_date))
                
                writedb(items)
            except:
                print("yeah1")
        
main('2019-01-01')
