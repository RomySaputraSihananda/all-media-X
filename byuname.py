import requests
from json import dumps

params = {
    "variables": dumps({
        "screen_name":"RomySihananda",
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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "content-type": "application/json",
    "x-guest-token": "1738559611849023890",
    "x-twitter-client-language": "en",
    "x-twitter-active-user": "yes",
    "x-client-transaction-id": "2S/JMTMO6gYovw3reLcNsIf6dpc0j5QEQ2fYtFwJJ7Kar/Zik27fZ35/uapLJv/b4ptR7thUDFEkZBZqqv3zQmiwDBMI2A",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
}

res = requests.get('https://api.twitter.com/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName', params=params, headers=headers)

print(res)

with open('byudata.json', 'w') as file:
    file.write(dumps(res.json(), indent=2, ensure_ascii=False))