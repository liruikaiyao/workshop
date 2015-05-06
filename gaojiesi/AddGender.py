from config.db import user_clear,user_info

user_list = []
for elem in user_clear.find():
    user_list.append(elem['user_id'])
print len(user_list)

count = 0
for elem in user_list:
    check = user_info.find_one({'openid':elem})
    try:
        user_clear.update({'user_id':elem},{"$set":{'gender':check['sex']}})
    except:
        user_clear.remove({'user_id':elem})
        count+=1

print count