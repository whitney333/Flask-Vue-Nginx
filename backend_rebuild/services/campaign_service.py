from .instagram_service import InstagramService
from .youtube_service import YoutubeService
from .tiktok_service import TiktokService
from .spotify_service import SpotifyService
from .bilibili_service import BilibiliService
from .weibo_service import WeiboService
from models.artist_model import Artists
from models.campaign_model import Campaign
from datetime import timedelta


class CampaignService:

    @staticmethod
    def get_campaign_list_by_artist(user_id, artist_id=None):
        """
            Get campaigns for a specific user, optionally filtered by artist
            :param user_id: Firebase user id
            :param artist_id: optional artist id to filter campaigns
            :return: list of campaigns
        """
        query = {
            "user_id": user_id,
            "status__in": ["approved"]
        }

        if artist_id:
            query["artist_id"] = artist_id

        campaigns = Campaign.objects(**query).order_by("-approved_at")

        result = []
        for c in campaigns:
            result.append({
                "id": str(c.id),
                "campaign_name": c.campaign_id,
                "approved_at": c.approved_at.isoformat() if c.approved_at else None,
                "status": c.status
            })

        return result

    @staticmethod
    def get_campaign_follower_growth(campaign):
        """

        :param campaign:
        :return:
        """
        if not campaign.approved_at:
            return None

        start = campaign.approved_at
        end = campaign.approved_at + timedelta(days=14)

        # query artist
        artist = campaign.artist_id.fetch()
        artist_name = f"{artist['english_name']} ({artist['korean_name']})"

        # default value
        spotify_result = None
        youtube_result = None
        tiktok_result = None
        instagram_result = None
        instagram_threads_result = None
        bilibili_result = None
        weibo_result = None

        # spotify
        if artist.spotify_id:
            spotify_result = SpotifyService.get_follower_growth(
                spotify_id=artist.spotify_id,
                campaign_start=start
            )

        # youtube
        if artist.youtube_id:
            youtube_result = YoutubeService.get_follower_growth(
                youtube_id=artist.youtube_id,
                campaign_start=start
            )

        # tiktok
        if artist.tiktok_id:
            tiktok_result = TiktokService.get_follower_growth(
                tiktok_id=artist.tiktok_id,
                campaign_start=start
            )

        # instagram
        if artist.instagram_id:
            instagram_result = InstagramService.get_follower_growth(
                instagram_id=artist.instagram_id,
                campaign_start=start
            )
            instagram_threads_result = InstagramService.get_threads_follower_growth(
                instagram_id=artist.instagram_id,
                campaign_start=start
            )

        # bilibili
        if artist.bilibili_id:
            bilibili_result = BilibiliService.get_follower_growth(
                bilibili_id=artist.bilibili_id,
                campaign_start=start
            )

        # weibo
        if artist.weibo_id:
            weibo_result = WeiboService.get_follower_growth(
                weibo_id=artist.weibo_id,
                campaign_start=start
            )

        return {
            "campaign_id": str(campaign.campaign_id),
            "artist": artist_name,
            "spotify_id": artist.spotify_id,
            "period": {
                "start": start.isoformat(),
                "end": end.isoformat()
            },
            "followers_growth": {
                "spotify": spotify_result,
                "youtube": youtube_result,
                "tiktok": tiktok_result,
                "instagram": instagram_result,
                "threads": instagram_threads_result,
                "bilibili": bilibili_result,
                "weibo": weibo_result
            }
        }
