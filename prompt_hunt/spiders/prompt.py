import scrapy
import json
from datetime import datetime

class PromptSpider(scrapy.Spider):
    name = 'prompt'
    
    headers = {
        'authority': 'www.prompthunt.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': '_gcl_au=1.1.728128113.1681794827; _ga=GA1.1.620002841.1681794827; AMP_MKTG_b1ac6ebe69=JTdCJTdE; __Host-next-auth.csrf-token=0846b233871620c812e08d4c1b92d28a4303d15053fe366be0a3afa7b5f06f26%7Cbad43ef484529a5c41b1e8a0804b876f5d91753de1501e30fb162d06e23092f9; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.prompthunt.com%2Fprompt%2Fclfru1iuy000tmd08rzs6gn1w; g_state={"i_p":1682502423245,"i_l":3}; AMP_b1ac6ebe69=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIzMTg2NmExYS02MWE2LTQ0YWMtYWZmNC1jYjUwNzlhMjRiM2ElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjgxODk3NjE2NDc5JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY4MTg5OTgzMTc2NCU3RA==; _ga_6XQ24B75V9=GS1.1.1681897541.6.1.1681899832.0.0.0',
        'if-none-match': 'W/"12xvuuuyv8gsde"'
        }
    
    def start_requests(self):
        url = "https://www.prompthunt.com/api/search?page=1&themeId=clfqdumhy0005l808ezqstf72"
        
        yield scrapy.Request(
                                url,
                                headers=self.headers,
                                method="GEt",
                                meta={"url":url,"currunt_page":1,"count":0},
                                callback=self.parse
                            )

    def parse(self, response):
        data = json.loads(response.text)
        
        for i in data["prompts"]:
            cate1 = []
            cate2 = []
            
            try:
                Id = i["id"]
            except:
                Id = None
            try:
                prompt = i["prompt"]
            except:
                prompt = None
            
            createdAt = i["createdAt"]
            
            date = datetime.fromisoformat(createdAt.replace("Z","+00:00"))
            cre_date = date.strftime("%d-%m-%y %H:%M:%S")
            
            updatedAt = i["updatedAt"]
            date2 = datetime.fromisoformat(str(updatedAt).replace("Z","+00:00"))
            up_date = date2.strftime("%d-%m-%y %H:%M:%S")
               
            try:
                user_id = i["user"]["id"]
            except:
                user_id = None
            try:
                user_name = i["user"]["username"]
            except:
                user_name = None           
            try:
                user_image = i["user"]["image"]
            except:
                user_image = None         
            try:
                user_subscriptionPlan = i["user"]["subscriptionPlan"]
            except:
                user_subscriptionPlan = None                    
            try:
                theme_id = i["theme"]["id"]
            except:
                theme_id = None  
            try:
                theme_name = i["theme"]["name"]
            except:
                theme_name = None
            try:
                theme_image = i["theme"]["image"]
            except:
                theme_image = None
            try:
                thum_theme_image = i["theme"]["thumbnails"]
            except:
                thum_theme_image = None
            
            if "meta" in i:

                for n in i["meta"]["negativeStyles"]:
                   
                    try:
                        nag_name = n["data"]["name"]
                    except:
                        nag_name = None
                    try:
                        nag_type = n["data"]["type"]
                    except:
                        nag_type = None
                                      
                    for c1 in n["data"]["categories"]:    
                        try:
                            cat_name = c1["category"]["name"]
                        except:
                            cat_name = None
                        
                        n_cate ={
                                "nag_name":nag_name,
                                "nag_type":nag_type,
                                "cat_name":cat_name
                        }
                        cate1.append(n_cate)
            if "meta" in i:
                for m in i["meta"]["modifiers"]:
                    try:
                        modi_cat_name = m["name"]
                    except:
                        modi_cat_name = None 
                    try:
                        modi_cat_type = m["type"]
                    except:
                        modi_cat_type = None 
                             
                    for c2 in m["categories"]:
                        try:
                            modi_cat = c2["category"]["name"]
                        except:
                            modi_cat = None
                        m_cate ={
                                "modi_cat_name":modi_cat_name,
                                "modi_cat_type":modi_cat_type,
                                "modi_cat":modi_cat
                        }
                        cate2.append(m_cate) 

            item = {
                    "userId":Id,
                    "prompt":prompt,
                    "createdAt":cre_date,
                    "updatedAt":up_date,
                            "user_details":{
                                    "user_id":user_id,
                                    "user_name":user_name,
                                    "user_image":user_image,
                                    "user_subscriptionPlan":user_subscriptionPlan
                                            },
                            "theme_details":{
                                    "theme_id":theme_id,
                                    "theme_name":theme_name,
                                    "theme_image":theme_image,
                                    "thum_theme_image":thum_theme_image
                            },
                            "n_cate":{
                                    "nag_name":nag_name,
                                    "nag_type":nag_type,
                                    "cat_name":cate1                 

                                    },
                            "m_cate":{
                                    "modi_cat_name":modi_cat_name,
                                    "modi_cat_type":modi_cat_type,
                                    "modi_cat":cate2
                                    }        
                        }
            yield item 
                       
        # if response.meta["currunt_page"] is True or next:
        response.meta["currunt_page"]+=1
        if len(data["prompts"]) != 0:
            url = f"https://www.prompthunt.com/api/search?page={response.meta['currunt_page']}&themeId=clfqdumhy0005l808ezqstf72"
            yield scrapy.Request(
                                    url,
                                    method="GET",
                                    meta={"url":url,"currunt_page":response.meta["currunt_page"],},
                                    callback=self.parse,
                                    headers=self.headers
                                )
