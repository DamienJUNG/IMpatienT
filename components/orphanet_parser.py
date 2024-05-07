def get_child(data):
    json = []
    if int(data['@count']) < 1:
        return json
    currLevel = data['ClassificationNode']
    if int(data['@count']) > 1:
        json = [
            {'children':get_child(item['ClassificationNodeChildList']),
                'name':{
                    'text':item['Disorder']['Name']['#text']
                    },'id':item['Disorder']['OrphaCode']
            } for item in currLevel
        ]
    else:
        json = [
            {'children':get_child(currLevel['ClassificationNodeChildList']),
                'name':{
                    'text':currLevel['Disorder']['Name']['#text']
                    },
                    'id':currLevel['Disorder']['OrphaCode']
            }
        ]
    return json

def parse_ontology(data):
    json = []
    currLevel = data['JDBOR']['ClassificationList']
    if int(currLevel['@count']) > 1:
        json = [
            {'children':get_child(item['ClassificationNodeRootList']),
                'name':{
                    'text':item['Name']['#text']
                }
            } for item in currLevel['Classification']
        ]
    elif int(currLevel['@count']) == 1:
        json = [
            {'children':get_child(currLevel['Classification']['ClassificationNodeRootList']),
                'name':{
                    'text':currLevel['Classification']['Name']['#text']
                }
            }
        ]
    return json