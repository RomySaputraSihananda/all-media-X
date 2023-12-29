from json import dumps

class ParamsBuilder:
    def get_user_id(self, variables: dict) -> dict:
        return {
            "variables": dumps(variables),
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
    
    def get_media(self, variable: dict) -> dict:
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