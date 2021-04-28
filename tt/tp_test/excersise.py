# list = [{"name": "推荐食谱", "1": "症状", "name1": "浑身忽冷忽热"}, {"name": "绿豆薏米饭"}, {"name": "芝麻"}]
#
# res = [item[key] for item in list for key in item]
# print(res)
# for item in list:
#     for key in item:
#         print(item[key])



list = [{"name": "推荐食谱", "1": "症状", "name1": "浑身忽冷忽热"}, {"name": "绿豆薏米饭"}, {"name": "芝麻"}]

for item in list:
    for key,value in item.items():
        print(key,value)