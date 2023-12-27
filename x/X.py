import os
import re

from dotenv import load_dotenv
from requests import Response
from json import dumps

from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
class X:
    def __init__(self, cookie: str = None) -> None:
        self.__requests: Session = Session()
        self.__cursor: str = None

        match = re.search(r'ct0=([^;]+)', cookie) if cookie else None

        self.__requests.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/110.0.5481.154 Mobile Safari/537.36", 
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "Cookie": cookie,
            "X-Csrf-Token": match.group(1) if match else None,
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

    def __get_user_id(self, username: str) -> str:
        params: dict = {
            "variables": dumps({
                "screen_name": username,
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

    def __build_params(self, username: str) -> dict:
        return {
            "variables": dumps({
                "userId": self.__get_user_id(username),
                "count":200,
                "cursor": self.__cursor,
                "includePromotedContent":True,
                "withQuickPromoteEligibilityTweetFields":True,
                "withVoice":True,
                "withV2Timeline":True
            }),
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
    
    def __filter_urls(self, response: dict):
        datas = response['data']['user']['result']['timeline_v2']['timeline']
        datas = next((instruction for instruction in datas['instructions'] if instruction['type'] == "TimelineAddEntries"), None)['entries']

        self.__cursor = next((entry['content']['value'] for entry in datas[-2:] if entry['content']['cursorType'] == "Bottom"), None)

        for data in datas[:-2]:
            try:
                for media in data['content']['itemContent']['tweet_results']['result']['legacy']["entities"]['media']:
                    match(media["type"]):
                        case "photo":
                            self.__image_urls.append(media['media_url_https'])
                        case "video":
                            bitrate_variants = [variant for variant in media['video_info']['variants'] if "bitrate" in variant]
                            video = max(bitrate_variants, key=lambda x: x["bitrate"])
                            self.__image_urls.append(video['url'])
            except Exception as e:
                continue
    
    def get_by_username(self, username: str) -> None:
        self.__username: str = username
        for i in range(5):
            self.__image_urls: list = []

            response: Response = self.__requests.get('https://api.twitter.com/graphql/V1ze5q3ijDS1VeLwLY0m7g/UserTweets', params=self.__build_params(username))

            self.__filter_urls(response.json())

            with ThreadPoolExecutor() as executor:
                executor.map(self.__download, self.__image_urls)
    
    def search(self, username: str) -> None:
        self.__image_urls: list = []
        self.__username: str = username

        response: Response = self.__requests.get('https://api.twitter.com/graphql/V1ze5q3ijDS1VeLwLY0m7g/UserTweets', params=self.__build_params(username))

        self.__filter_urls(response.json())

        with ThreadPoolExecutor() as executor:
            executor.map(self.__download, self.__image_urls)

# testing
if(__name__ == '__main__'):
    load_dotenv() 
    cookie = os.getenv("cookie") 
    x: X = X(cookie) 
    # x.get_by_username('amortentia0213')
    x.get_by_username('RomySihananda')
