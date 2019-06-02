import urllib.parse
import requests



""" Dictionary keys in Items Json request:
'id'            (number) = Item id
'chat_link'     (string) = chat link
'name'          (string) = name of item
'icon'          (string) = Full icon URL
'description'   (string) = The item description
'type'          (string) = Armor, Back (Back Item), Bag, Consumable, Container, CraftingMaterial (Crafting Materials), 
                           Gathering, Gizmo, MiniPet (Miniatures), Tool (Salvage Kits), Trait (Trait Guides), Trinket, 
                           Trophy, UpgradeComponent, Weapon
'rarity'        (string) = Junk, Basic, Fine, Masterwork, Rare, Exotic, Ascended, Legendary
'level'         (number) = The required level
'vendor_value'  (number) = The value in coins when selling to a vendor. (Can be non-zero even if has NoSell flag
'flags'         (array of strings) = AccountBindOnUse (Account bound on use), 
                                     Account Bound (Account bound on aquire), 
                                     Attuned (Upgraded in Mystic Forge to gain additional infusion slot), 
                                     BulkConsume (if the item can be bulk consumed), 
                                     DeleteWarning (if the item will prompt the player with a warning when deleting), 
                                     Hidesuffix (hide the suffix of the upgrade component),
                                     Infused (if the item is infused,
                                     MonsterOnly,
                                     NoMysticForge (not usable in the Mystic Forge,
                                     NoSalvage (not salvageable),
                                     NoSell (not sellable),
                                     NotUpgradable (not upgradable),
                                     NoUnderwater (not available underwater),
                                     SoulbindOnAquire (soulbound on aquire),
                                     Tonic (if the item is a tonic),
                                     Unique (unique)
'game_types'    (array of strings) = Activity (usable in activities),
                                     Dungeon (usable in dungeon),
                                     Pve (Usable in general PvE),
                                     PvP (Usable in PvP),
                                     PvpLobby (Usable in Heart of the Mists
                                     WvW (Usable in World v World)
'restrictions'  (array of strings) = Asura, Charr, Human, Norn, Sylvari, Elementalist, Engineer, Guardian, Mesmer,
                                     Necromancer, Ranger, Theif, Warrior
'details'       (object, optional) = Additional item details if applicable, depending on the type of the item
"""

""" Separates ID numbers into groups of 200 and stores them in a list"""
def count_by_200(main_api, sub_api):
    ids = get_json_data_ids_only(main_api, sub_api)
    index_number_list = []
    index_numbers = ""
    count = 0
    list_count = 0
    for i in ids:
        if(count < 200):
            if(count == 199):
                index_numbers += str(i)
                count = count + 1
            elif(i == ids[len(ids) - 1]):
                index_number_list.append(index_numbers)
            else:
                temp = str(i) + ", "
                index_numbers += temp
                count = count + 1
        else:
            index_number_list.append(index_numbers)
            count = 0
            index_numbers = ""
    return index_number_list


""" Returns all ids associated with a sub_api """
def get_json_data_ids_only(main_api, sub_api):
    url = main_api + sub_api
    json_data = requests.get(url).json()
    return json_data

def update_dictionary_all_items():
    for item in json_data:
        item_id = str(item['id'])
        dictionary_all_items.update(item_id,item)

def get_basic():
    list_of_keys = json_dictionary_keys['basic']
    print(list_of_keys)
    for key in list_of_keys:
        print(key + ': ' + str(json_data[key]))


def get_all():
    """
    dictionary format:
    Dictionary_All_Items = {id_number : {'id': id_number, 'name': name, ect....}}
    """
    dictionary_all_items.update(json_data['id'],{'id':json_data['id']})
    list_of_keys = json_dictionary_keys['all']
    print(list_of_keys)
    for key in list_of_keys:
        print(key + ': ' + json_data[key])
        dictionary_all_items[json_data['id']].update(key,json_data['key'])




"""Guild Wars 2 Base API URL"""
main_api = 'https://api.guildwars2.com/v2'

""" Sub-category of API URL call for single item"""
single_item_sub_api = '/commerce/listings'

""" Sub-category of API URL call for up to 200 items"""
multi_item_sub_api = '/commerce/listings?ids='

""" List of sub-category index numbers split into largest usable segments"""
index_number_list = count_by_200(main_api, single_item_sub_api)

index_number = '/19699'

""" Create API call url, indicate which group of 200 to call using index_number_list"""
url = main_api + multi_item_sub_api + index_number_list[0]
print(url)

""" Perform api call """
json_data = requests.get(url).json()
print(json_data)
for list_item in json_data:
    #print(key)
    for key in list_item:
        #print(sub_key)
        if(key == 'name'):
            print(list_item[key])
        elif(key == 'id'):
            print(list_item[key])

json_dictionary_keys = {'basic' : ['id','name','type'], 'all' : ['chat_link','name','icon','description','type','rarity','level','vendor_value','default_skin','flags','game_types','restrictions','details']}

dictionary_all_items = {}

print(len(index_number_list))

"""update_dictionary_all_items()"""

