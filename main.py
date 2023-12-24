import requests
from json import dumps

def ubah_format_link(link, format_tujuan="jpg"):
    ekstensi_asli = link.split(".")[-1]
    return link.replace(f".{ekstensi_asli}", f"?format={ekstensi_asli}&name=4096x4096") if ekstensi_asli else link

def download(link):
    with open(f'data/{link.split("/")[-1]}', 'wb') as file:
        file.write(requests.get(ubah_format_link(link)).content)

params = {
    "variables": dumps({
        # "userId": "4722555409",
        "userId": "1572207728415895559",
        "count":200,
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

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/110.0.5481.154 Mobile Safari/537.36", 
    "x-guest-token": "1738834257072771466", 
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
}

data = requests.get('https://api.twitter.com/graphql/V1ze5q3ijDS1VeLwLY0m7g/UserTweets', params=params, headers=headers).json()

# print(data)

with open('data.json', 'w') as file:
    file.write(dumps(data, indent=2, ensure_ascii=False))

datas = data['data']['user']['result']['timeline_v2']['timeline']['instructions'][-2]['entries']

links = []

for data2 in datas:
    try:
        for media in data2['content']['itemContent']['tweet_results']['result']['legacy']["entities"]['media']:
            links.append(media['media_url_https'])

    # print(data2['content']['itemContent']['tweet_results']['result']['legacy']["full_text"])
    except Exception as e:
        continue


from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    executor.map(download, links)

