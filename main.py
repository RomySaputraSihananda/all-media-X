import requests
from json import dumps

params = {
    "variables": dumps({
        "userId": "1057844081315897344",
        "count":20,
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

res = requests.get('https://api.twitter.com/graphql/V1ze5q3ijDS1VeLwLY0m7g/UserTweets', params=params, headers=headers)

print(res)

with open('data.json', 'w') as file:
    file.write(dumps(res.json(), indent=2, ensure_ascii=False))