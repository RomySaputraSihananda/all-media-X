import os
import re

from time import perf_counter
from dotenv import load_dotenv
from requests import Response
from json import dumps
from tqdm import tqdm

from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from x.helpers import logging

class X:
    def __init__(self, cookie: str = None) -> None:
        self.__requests: Session = Session()
        self.__cursor: str = None
        self.__cookie: str = cookie

        self.__requests.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/110.0.5481.154 Mobile Safari/537.36", 
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "Cookie": self.__cookie,
            "X-Csrf-Token": match.group(1) if (match := re.search(r'ct0=([^;]+)', cookie) if cookie else None) else None,
        })

        self.__get_guest_token()

    def __get_guest_token(self) -> None:
        response: Response = self.__requests.post('https://api.twitter.com/1.1/guest/activate.json')

        self.__requests.headers.update({
            "x-guest-token": response.json()['guest_token'], 
        })
    
    def __change_url(self, url: str):
        if('.mp4' in url): return url

        ekstention: str = url.split(".")[-1]
        return url.replace(f".{ekstention}", f"?format={ekstention}&name=4096x4096") if ekstention else url

    def __download(self, url: str):
        output: str = f'data/{self.__username}'

        if(not os.path.exists(output)):
            os.makedirs(output)

        with open(f'{output}/{url.split("/")[-1].split("?")[0] if ".mp4" in url else url.split("/")[-1]}', 'wb') as file:
            file.write(self.__requests.get(self.__change_url(url)).content)

    def __get_user_id(self) -> str:
        params: dict = {
            "variables": dumps({
                "screen_name": self.__username,
                "withSafetyModeUserFields":True
            }),
            "features": dumps({
                "hidden_profile_likes_enabled":True,
                "hidden_profile_subscriptions_enabled":True,
                "responsive_web_graphql_exclude_directive_enabled":True,
                "verified_phone_label_enabled":False,
                "subscriptions_verification_info_is_identity_verified_enabled":True,
                "subscriptions_verification_info_verified_since_enabled":True,
                "highlights_tweets_tab_ui_enabled":True,
                "responsive_web_twitter_article_notes_tab_enabled":False,
                "creator_subscriptions_tweet_preview_api_enabled":True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,
                "responsive_web_graphql_timeline_navigation_enabled":True
            }),
            "fieldToggles": dumps({
                "withAuxiliaryUserLabels":False
            })
        }

        response: Response = self.__requests.get('https://api.twitter.com/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName', params=params)
        
        return response.json()['data']['user']['result']['rest_id']

    def __build_params(self, **kwargs) -> dict:
        variable: dict = {
            "rawQuery": self.__username,
            "count": 200,
            "cursor": self.__cursor,
            "querySource":"typed_query",
            "product":"Media"
        } if kwargs.get("search", False) else {
            "userId": self.__get_user_id(),
            "count":200,
            "cursor": self.__cursor,
            "includePromotedContent":True,
            "withQuickPromoteEligibilityTweetFields":True,
            "withVoice":True,
            "withV2Timeline":True
        }
        
        return {
            "variables": dumps(variable),
            "features": dumps({
                "responsive_web_graphql_exclude_directive_enabled":True,
                "verified_phone_label_enabled":False,
                "creator_subscriptions_tweet_preview_api_enabled":True,
                "responsive_web_graphql_timeline_navigation_enabled":True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,
                "c9s_tweet_anatomy_moderator_badge_enabled":True,
                "tweetypie_unmention_optimization_enabled":True,
                "responsive_web_edit_tweet_api_enabled":True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,
                "view_counts_everywhere_api_enabled":True,
                "longform_notetweets_consumption_enabled":True,
                "responsive_web_twitter_article_tweet_consumption_enabled":False,
                "tweet_awards_web_tipping_enabled":False,
                "freedom_of_speech_not_reach_fetch_enabled":True,
                "standardized_nudges_misinfo":True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":True,
                "rweb_video_timestamps_enabled":True,
                "longform_notetweets_rich_text_read_enabled":True,
                "longform_notetweets_inline_media_enabled":True,
                "responsive_web_media_download_video_enabled":False,
                "responsive_web_enhance_cards_enabled":False
            })
        }
    
    def __filter_urls(self, response: dict) -> bool:
        if('user' in response['data']):
            try:
                datas = response['data']['user']['result']['timeline_v2']['timeline']
                datas = next((instruction for instruction in datas['instructions'] if instruction['type'] == "TimelineAddEntries"), None)['entries']

                if(len(datas) == 2): raise Exception(e)
                
                if(self.__cookie): self.__cursor = next((entry['content']['value'] for entry in datas[-2:] if entry['content']['cursorType'] == "Bottom"), None)

                for data in datas:
                    try:
                        medias = data['content']['itemContent']['tweet_results']['result']['legacy']["entities"]['media']
                    except Exception as e:
                        raise Exception(e)
                    
                    for media in medias:
                        match(media["type"]):
                            case "photo":
                                self.__media_urls.append(media['media_url_https'])
                            case "video":
                                bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                                video = max(bitrate_variants, key=lambda x: x["bitrate"])
                                self.__media_urls.append(video['url'])

            except Exception as e:
                datas = response['data']['user']['result']['timeline_v2']['timeline']
                try:
                    self.__cursor = next((entry['content']['value'] for entry in next((i for i in datas['instructions'] if i['type'] == "TimelineAddEntries"), None)['entries'][1:] if entry['content']['cursorType'] == "Bottom"), None)
                    datas = next((i for i in datas['instructions'] if i['type'] == "TimelineAddToModule"), None)['moduleItems']
                    
                    for data in datas:
                        for media in data['item']['itemContent']['tweet_results']['result']['legacy']["entities"]['media']:
                            match(media["type"]):
                                case "photo":
                                    self.__media_urls.append(media['media_url_https'])
                                case "video":
                                    bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                                    video = max(bitrate_variants, key=lambda x: x["bitrate"])

                                    self.__media_urls.append(video['url'])

                except Exception as e:
                    datas = next((i for i in datas['instructions'] if i['type'] == "TimelineAddEntries"), None)['entries']

                    if(len(datas) == 2): return True
                    
                    self.__cursor = next((entry['content']['value'] for entry in datas[1:] if entry['content']['cursorType'] == "Bottom"), None)
                    
                    for data in datas[0]['content']['items']:
                        for media in data['item']['itemContent']['tweet_results']['result']['legacy']["entities"]['media']:
                            match(media["type"]):
                                case "photo":
                                    self.__media_urls.append(media['media_url_https'])
                                case "video":
                                    bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                                    video = max(bitrate_variants, key=lambda x: x["bitrate"])

                                    self.__media_urls.append(video['url'])
                
            return
        
        datas = response['data']['search_by_raw_query']['search_timeline']['timeline']

        try:
            self.__cursor = next((entry['content']['value'] for entry in next((i for i in datas['instructions'] if i['type'] == "TimelineAddEntries"), None)['entries'][1:] if entry['content']['cursorType'] == "Bottom"), None)
            datas = next((i for i in datas['instructions'] if i['type'] == "TimelineAddToModule"), None)['moduleItems']
            for data in datas:
                try:
                    for media in data['item']['itemContent']['tweet_results']['result']['legacy']["entities"]['media']:
                        match(media["type"]):
                            case "photo":
                                self.__media_urls.append(media['media_url_https'])
                            case "video":
                                bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                                video = max(bitrate_variants, key=lambda x: x["bitrate"])

                                self.__media_urls.append(video['url'])
                except Exception as e:
                    for media in data['item']['itemContent']['tweet_results']['result']['tweet']['legacy']["entities"]['media']:
                        match(media["type"]):
                            case "photo":
                                self.__media_urls.append(media['media_url_https'])
                            case "video":
                                bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                                video = max(bitrate_variants, key=lambda x: x["bitrate"])

                                self.__media_urls.append(video['url'])

        except Exception as e:
            datas = next((i for i in datas['instructions'] if i['type'] == "TimelineAddEntries"), None)['entries']

            if(len(datas) == 2): return True

            self.__cursor = next((entry['content']['value'] for entry in datas[1:] if entry['content']['cursorType'] == "Bottom"), None)

            for data in datas[0]['content']['items']:
                try:
                    for media in data['item']['itemContent']['tweet_results']['result']['legacy']["entities"]['media']:
                        match(media["type"]):
                            case "photo":
                                self.__media_urls.append(media['media_url_https'])
                            case "video":
                                bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                                video = max(bitrate_variants, key=lambda x: x["bitrate"])

                                self.__media_urls.append(video['url'])
                except Exception as e:
                    for media in data['item']['itemContent']['tweet_results']['result']['tweet']['legacy']["entities"]['media']:
                        match(media["type"]):
                            case "photo":
                                self.__media_urls.append(media['media_url_https'])
                            case "video":
                                bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                                video = max(bitrate_variants, key=lambda x: x["bitrate"])

                                self.__media_urls.append(video['url'])
    
    def __download_wrapper(self, url: str, progress_bar: tqdm) -> None:
        self.__download(url)
        progress_bar.update(1)

    def get_by_username(self, username: str) -> None:
        self.__username: str = username

        if(not self.__cookie):
            self.__media_urls: list = []

            response: Response = self.__requests.get('https://api.twitter.com/graphql/V1ze5q3ijDS1VeLwLY0m7g/UserTweets', params=self.__build_params())
            
            if (self.__filter_urls(response.json()) or response.status_code != 200): return
            
            logging.info(response)

            with tqdm(total=len(self.__media_urls), desc="Downloading", unit="file", ascii=True) as progress_bar:                
                with ThreadPoolExecutor() as executor:
                    executor.map(lambda url: self.__download_wrapper(url, progress_bar), self.__media_urls)
            
            executor.shutdown(wait=True)
            
            return
        
        while(True):
            self.__media_urls: list = []

            response: Response = self.__requests.get('https://api.twitter.com/graphql/oMVVrI5kt3kOpyHHTTKf5Q/UserMedia', params=self.__build_params())
            
            if (self.__filter_urls(response.json()) or response.status_code != 200): break
            
            logging.info(response)
            
            with tqdm(total=len(self.__media_urls), desc="Downloading", unit="file", ascii=True) as progress_bar:                
                with ThreadPoolExecutor() as executor:
                    executor.map(lambda url: self.__download_wrapper(url, progress_bar), self.__media_urls)

        executor.shutdown(wait=True)
    
    def search(self, username: str) -> None:
        self.__username: str = username
        
        if(not self.__cookie): return logging.error("cookie require !!")

        while(True):
            self.__media_urls: list = []

            response: Response = self.__requests.get('https://api.twitter.com/graphql/Aj1nGkALq99Xg3XI0OZBtw/SearchTimeline', params=self.__build_params(search=True))
            
            if (self.__filter_urls(response.json()) or response.status_code != 200): break

            logging.info(response)

            with tqdm(total=len(self.__media_urls), desc="Downloading", unit="file", ascii=True) as progress_bar:                
                with ThreadPoolExecutor() as executor:
                    executor.map(lambda url: self.__download_wrapper(url, progress_bar), self.__media_urls)
            
        executor.shutdown(wait=True)

# testing
if(__name__ == '__main__'):
    load_dotenv() 
    cookie = os.getenv("COOKIE") 
    start = perf_counter()
    x: X = X(cookie)
    # x.get_by_username('amortentia0213')
    # x.get_by_username('djtHobbies')
    # x.search('Freya_JKT48')
    x.search('prabowo')
    # x.get_by_username('sixtysixhistory')
    # x.get_by_username('Freya_JKT48')
    # x.get_by_username('N_ShaniJKT48')
    print(perf_counter() - start)
