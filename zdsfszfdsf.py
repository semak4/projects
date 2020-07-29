import vk_api
import vk_messages
import os
import urllib
import time
#__\\n__ - enter in text

SAVE_photos = True
VK = ""
person = "id17326"
    # "dmitrydemidov92"
ENCODE = "utf-8-sig" #with smiles, before it was cp1251
ID_ = ""
init_vkname = '+79002003736'
init_vkpass = 'vktester321'
WORK_dir = 'F:\\vk_expert\\'
WORK_dir_flag = False
PLATFORM_dic = {
    1:'mobile site (m.vk.com)',
    2:'iPhone App',
    3:'iPad App',
    4:'Android App',
    5:'WindowsPhone',
    6:'WindowsApp (win10)',
    7:'Desktop site (PC/Notebook)'
}

def main():

    setup()

    # if id!=digit person = id, id=""
    ID_ = get_VkId(person)



    # getUserInfo(ID_)
    # getVideos(ID_)
    # getFriendsFile(ID_)
    getWall(ID_)
    # getPhotos(ID_)
    # getGroups(ID_)

    # getMessages()
  # получить информацию о пользователе по id
  # response_u = vk.users.get(user_ids=friends[0:-1])
 # print(response_u)


def getMessages():
    messages = vk_messages.MessagesAPI(login=init_vkname, password=init_vkpass,
                           two_factor=False, cookies_save_path='F:\\sessions\\')
    conversations = messages.method('messages.getConversations', offset=0,count=200)
    file = open("F:\\vk_messages.csv", "w", encoding='cp1251', errors='replace',
                newline='')  # если без кодировки то UnicodeEncodeError: 'charmap' codec can't encode character
    file.write("date;from;companion;out;text\n")
    for item in conversations.get("items"):
        peer_id=item.get('conversation').get('peer').get("id")
        conversations = messages.method('messages.getHistory', peer_id = peer_id, offset=0, count=200) #max 200 sms
        for message in conversations.get('items'):
            # print(message)
            file.write(str(message.get('date'))+";")
            file.write(str(message.get('from_id'))+";")
            file.write(str(message.get("peer_id"))+";")
            file.write(str(message.get("out"))+";")
            file.write(message.get('text')+"\n")
            # fwd, attach?


def getVideos(user_id):
    print("__getVideos__")
    checkWorkDir(user_id)
    file = open(WORK_dir+"vk_viedos_"+str(user_id)+".csv", "w",encoding=ENCODE, errors='replace', newline='') # если без кодировки то UnicodeEncodeError: 'charmap' codec can't encode character
    file.write("adding_date; date;owner_id; views; comments; duration; description; titile; photo_800; player\n")

    try:
        response_videos = vk.video.get(owner_id=user_id)
        print(response_videos)
        for video in response_videos['items']:
            file.write(timeconvert(video['adding_date']) + ";")
            file.write(timeconvert(video['date']) + ";")
            file.write(str(video['owner_id']) + ";")
            file.write(str(video['views']) + ";")
            file.write(str(video['comments']) + ";")
            file.write(str(video['duration']) + ";")
            file.write(video['description'].replace("\n", "__") + ";")
            file.write(str(video['title']).replace("\n", "__") + ";")
            file.write(video['photo_320'] + ";")
            file.write(video['player'] + "\n")
        file.close()
    except Exception as e:
        print(str(user_id)+str(e))

def getWall(user_id):
    print("__getWall__")

    checkWorkDir(user_id)
    response_wall = vk.wall.get(owner_id=user_id)
    file = open(WORK_dir + "vk_wall_" + str(user_id) + ".csv", "w", encoding=ENCODE, errors='replace',
                newline='')  # если без кодировки то UnicodeEncodeError: 'charmap' codec can't encode character
    file.write("id_post;from_userId;owner_id;date;text;device;comments;likes;views;attachments_type; attachment; geo; "
               "repost; repost_owner; repost_id; repost_date;repost_text; repost_attach_type; repost_attachment\n")

    for post in response_wall['items']:
        print(post)
        file.write(str(post['id']) + ";")
        file.write(str(post['from_id']) + ";")
        file.write(str(post['owner_id']) + ";")
        file.write(timeconvert(post['date']) + ";")
        file.write(post['text'].replace("\n", "__\\n__").replace(";", "__P__") + ";")
        if 'platform' in post['post_source']:
            file.write(post['post_source']['platform'] + ";")
        else:
            file.write('-;')

        file.write(str(post['comments']['count']) + ";")
        file.write(str(post['likes']['count']) + ";")

        if ('views' in post):
            file.write(str(post['views']['count']) + ";")
        else:
            file.write(";")

        if ('attachments' in post):
            attachments_checker(post.get('attachments'), file)
            file.write(';')
        else:
            file.write("-;-;")

        if ('geo' in post):
            file.write(str(post.get("geo").get("coordinates")) + ";")
        else:
            file.write("-;")

# repost info

        if ('copy_history' in post):
            file.write("repost" + ";")
            club = str(post['copy_history'][0].get("owner_id"))
            if (club[0] == '-'):
                file.write("https://www.vk.com/club" + club[1:])
            else:
                file.write("https://www.vk.com/club" + club)
            file.write(";")

            file.write(str(post['copy_history'][0].get("id")) + ";")
            file.write(timeconvert(post['copy_history'][0].get("date")) + ";")
            file.write(str(post['copy_history'][0].get("text")).replace("\n", "__\\n__").replace(";", "__P__") + ";")

            if ('attachments' in post['copy_history'][0]):
                attachments_checker(post['copy_history'][0].get("attachments"), file)
                file.write('\n')
        else:
            file.write("-;-;-;-;-;-;-\n")


def getUserInfo(user_id):
    print("__getUserInfo__")
    global WORK_dir
    checkWorkDir(user_id)
    response_info = vk.users.get(user_id=user_id, fields='about, activities, bdate, books, career, city, connections, country,'
                                                         'education, games, home_town, interests, last_seen, maiden_name, military,'
                                                         'movies, music, nickname, online, personal, photo_max_orig, quotes, relatives,'
                                                         'relation, schools, sex, site, status, tv, universities, domain')
    print(response_info)
    file = open(WORK_dir + "vk_userInfo_" + str(user_id) + ".csv", "w", encoding=ENCODE, errors='replace', newline='')  # если без кодировки то UnicodeEncodeError: 'charmap' codec can't encode character
    file.write("id; first_name; last_name; bdate; photo; career; country; city; last_seen_time; last_device; domain \n")
    # main info:
    # id; first_name; last_name; bdate; photo_max_orig; career; country; city; last_seen_time; domain
    #
    # add person info:
    # connections (skype,insta etc); about; status; home_town; last_seen; last_platformbdate; sex; nickname; site; online;
    #
    # education, universities, schools,
    #  followers_count, nickname, relatives,relation, personal (smoke politic etc),
    # exports (vk,twitter),activities, interests, music, movies, tv, books, games, about, quotes,maiden_name (girls previos name), military

    # not used-----photo_id, verified,  has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, has_mobile, contacts, common_count, occupation??,
    #  can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name,  \
    # crop_photo, is_friend, friend_status, , blacklisted, blacklisted_by_me, can_be_invited_group.

    file.write(str(response_info[0]["id"])+ ";")
    file.write(response_info[0]['first_name'] + ";")
    file.write(response_info[0]['last_name'] + ";")
    if ('bdate' in response_info[0]):
        file.write(str(response_info[0]['bdate']) + ";")
    else:
        file.write("NOT_EXIST;")
    file.write(response_info[0]['photo_max_orig'] + ";")

    if SAVE_photos:
        urllib.request.urlretrieve(response_info[0]["photo_max_orig"], WORK_dir + str(response_info[0]["id"]) + ".jpg")

    if ('career' in response_info[0]):
        if(len(response_info[0]['career'])>0):
            if('group_id' in response_info[0]['career'][0]):
                file.write('https://vk.com/club'+str(response_info[0]['career'][0].get('group_id')) + ";")
            else:
                file.write(str(response_info[0]['career'][0]) + ";")
        else:
            file.write("NOT_EXIST;")
    else:
        file.write("NOT_EXIST;")
    if 'country' in response_info[0]:
        file.write(response_info[0]['country']['title'] + ";")
    else:
        file.write("NOT_EXIST;")
    if 'city' in response_info[0]:
        file.write(response_info[0]['city']['title'] + ";")
    else:
        file.write("NOT_EXIST;")
    if 'last_seen' in response_info[0]:
        file.write(timeconvert(response_info[0]['last_seen']['time']) + ";") #in your time zone
        file.write(PLATFORM_dic[response_info[0]['last_seen']['platform']] + ";")
    else:
        file.write('-;-;')
    file.write('https://vk.com/'+response_info[0]['domain'] + "\n")
    file.close()



def getPhotos(user_id):
    #albums wall, profile
    #album saved - only for your user
    response_albums = vk.photos.getAlbums(user_id =user_id)
    file = open("F:\\vk_userPhotos.csv", "w", encoding='cp1251', errors='replace',
                newline='')  # если без кодировки то UnicodeEncodeError: 'charmap' codec can't encode character
    file.write("album_id;photo_id;date;photo\n")
    # get system albums
    response = vk.photos.get(owner_id=user_id, album_id="profile")
    for photo in response.get('items'):
        file.write("profile;")
        file.write(str(photo.get('id')) + ";")
        file.write(str(photo.get('date')) + ";")
        file.write(str(photo.get('sizes')[-1].get('url')) + "\n")
        print(response)

    response = vk.photos.get(owner_id=user_id, album_id="wall")
    for photo in response.get('items'):
        file.write("wall;")
        file.write(str(photo.get('id')) + ";")
        file.write(str(photo.get('date')) + ";")
        file.write(str(photo.get('sizes')[-1].get('url')) + "\n")
        print(response)


    for album in response_albums.get('items'):
        response = vk.photos.get(owner_id =user_id,album_id = album.get("id"))
        for photo in response.get('items'):
            file.write(str(album.get("id")) + ";")
            file.write(str(photo.get('id')) + ";")
            file.write(str(photo.get('date')) + ";")
            file.write(str(photo.get('sizes')[-1].get('url')) + "\n")
        print(response)

def getGroups(user_id):
    response_groups = vk.users.getSubscriptions(user_id=user_id, extended=1)
    groupfile = open("f:\\vk_groups.csv",'a')
    groupfile.write("id;name;closed;admin\n")
    for group in response_groups.get('items'):
        groupfile.write(str(group.get("id"))+";")
        groupfile.write(group.get("name") + ";")
        groupfile.write(str(group.get("is_closed")) + ";")
        groupfile.write(str(group.get("is_admin")) + "\n")
    groupfile.close()


def get_friend_list(id_in):
    response = vk.friends.get(user_id = id_in)
    save_friends(response['items'])


def getFriendsFile(user_id):
    print("__getFriendsFile__")
    checkWorkDir(user_id)
    friendfile = open(WORK_dir+"vk_FriendList_"+str(user_id)+".csv", "w", encoding=ENCODE, errors='replace',newline='')  # если без кодировки то UnicodeEncodeError: 'charmap' codec can't encode character
    friendfile.write("id;first_name;last_name;bdate;photo \n")
    try:
        response = vk.friends.get(user_id=user_id)
        total = len(response['items'])
        counter=0

        if SAVE_photos:
            friends_dir=WORK_dir+"\\FriendsOf_"+str(user_id)+"\\"
            if not os.path.exists(friends_dir):
                os.mkdir(friends_dir)

        for friend_id in response['items']:
            print (friend_id)
            counter = counter+1
            print(str(counter)+"\\"+str(total))
            info = vk.users.get(user_id=friend_id, fields='about, activites, bdate, photo_max')
            print (info[0])
            friendfile.write(str(info[0]["id"]) + ";")
            friendfile.write(info[0]["first_name"]+";")
            friendfile.write(info[0]["last_name"] + ";")
            if("bdate" in info[0]):
                friendfile.write(info[0]["bdate"] + ";")
            else:
                friendfile.write("None" + ";")
            friendfile.write(info[0]["photo_max"] + "\n")

            if SAVE_photos:
                urllib.request.urlretrieve(info[0]["photo_max"], friends_dir+str(info[0]["id"])+".jpg")

        friendfile.close()
    except Exception as e:
        print(str(user_id) + str(e))


def saveToFile(info_in):
    global COUNT
    COUNT = COUNT + 1
    res_file.write(str(COUNT) + ";")
    print(COUNT)
    # print(str(info_in).split("'id': ")[1].split(",")[0])
    res_file.write(str(info_in).split("'id': ")[1].split(",")[0] + ";")
    res_file.write(str(info_in).split("'first_name': ")[1].split(",")[0] + ";")
    res_file.write(str(info_in).split("'last_name': ")[1].split(",")[0] + ";")
    if('bdate' in str(info_in)):
        res_file.write(str(info_in).split("'bdate': ")[1].split(",")[0] + ";")
    res_file.write(str(info_in).split("'photo_50': ")[1].split(",")[0] + ";\n")



def save_friends(friendsList):
    for f in friendsList:
        print(f)
        file.write(str(f)+"\n")
    file.close()

def get_VkId(person_in):
    response = vk.utils.resolveScreenName(screen_name=person_in)
    return response['object_id']


def init_vklibs(lgn, passwd):
    global vk
    vk_session = vk_api.VkApi(lgn, passwd)
    print("vk session openned: "+ str(vk_session))
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    vk = vk_session.get_api()


def checkWorkDir(user_id):
    global WORK_dir_flag
    if not WORK_dir_flag:
        global WORK_dir
        WORK_dir = WORK_dir + str(user_id) + "\\"
        if not os.path.exists(WORK_dir):
            os.mkdir(WORK_dir)

        WORK_dir_flag=True


def timeconvert(time_epoch):
    return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(time_epoch))


def attachments_checker(post_wtih_attach, file):
    Attach_TYPES = set()
    for element in post_wtih_attach:
        Attach_TYPES.add(element.get('type'))
    file.write(str(Attach_TYPES) + ";")
    for element in post_wtih_attach:
        if (element.get('type') == 'market'):
            file.write(element.get('market').get('category').get('name') + "_|_")
            file.write(element.get('market').get('description') + "_|_")
            file.write(element.get('market').get('price').get('text') + "_|_")
            file.write(element.get('market').get('thumb_photo') + "_|_")

        if (element.get('type') == 'poll'):
            file.write(element.get("poll").get("question") + "_|_")
            file.write(str(element.get("poll").get("votes")) + "_|_")
            for answer in element.get("poll").get("answers"):
                file.write(answer.get('text') + "-" + str(answer.get('votes')) + "_|_")
        if (element.get('type') == 'photo'):
            file.write(element.get("photo").get("sizes")[-1].get("url") + ", ")
        if (element.get('type') == 'doc'):
            file.write(element.get("doc").get("url") + ", ")
        if (element.get('type') == 'link'):
            file.write(element.get("link").get("url") + ", ")
        if (element.get(
                'type') == 'audio'):  # ссылку на аудио не отдает, https://vk.com/mp3/audio_api_unavailable.mp3 (борьба с пиратами)
            file.write('audio_id:' + str(element.get("audio").get("id")) + "-" + element.get("audio").get(
                "artist") + "-" + element.get("audio").get("title"))
        if (element.get('type') == 'video'):
            videos_param = str(element.get('video').get('owner_id')) + "_" + str(element.get('video').get('id'))
            print (videos_param)
            response_videos = vk.video.get(owner_id=element.get('video').get('owner_id'), videos=videos_param)
            if(len(response_videos.get('items'))>0):
                file.write(response_videos.get('items')[0].get('player') + ", ")
            else:
                file.write("youtube maybe,")

def setup():
    init_vklibs(init_vkname, init_vkpass)
    if not os.path.exists(WORK_dir):
        os.mkdir(WORK_dir)


if __name__ == '__main__':
    main()
