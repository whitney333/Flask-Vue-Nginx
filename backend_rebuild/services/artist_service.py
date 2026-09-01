from models.artist_model import Artists
from models.tenant_model import Tenant
from bson import ObjectId


class ArtistService:

    @staticmethod
    def get_artist(artist_id):
        """
        get artist document
        """
        artist = Artists.objects(id=artist_id).first()
        if not artist:
            raise ValueError("Artist not found")
        return artist

    @staticmethod
    def get_artist_info(artist_id):
        artist = Artists.objects(
            id=ObjectId(artist_id)
        ).first()

        if not artist:
            return []

        return [{
            "_id": str(artist.id),
            "artist_id": artist.artist_id,
            "artist": artist.english_name,
            "korean_name": artist.korean_name,
            "debut_year": artist.debut_year,
            "nation": artist.nation,
            "pronouns": artist.pronouns,
            "type": artist.type,
            "birth": artist.birth,
            "fandom": artist.fandom,
            "belong_group": [
                {
                    "_id": str(group.id),
                    "artist_id": group.artist_id,
                    "english_name": group.english_name,
                    "korean_name": group.korean_name,
                    "image": group.image_url,
                }
                for group in (artist.belong_group or [])
            ],
            "instagram_id": artist.instagram_id,
            "instagram_user": artist.instagram_user,
            "threads": artist.threads,
            "youtube_id": artist.youtube_id,
            "tiktok_id": artist.tiktok_id,
            "spotify_id": artist.spotify_id,
            "melon_id": artist.melon_id,
            "genie_id": artist.genie_id,
            "apple_id": artist.apple_id,
            "bilibili_id": artist.bilibili_id,
            "weibo_id": artist.weibo_id,
            "image": artist.image_url
        }]

    @staticmethod
    def get_bilibili_id(artist_id):
        """
        return bilibili_id（for BilibiliService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.bilibili_id:
            raise ValueError("Missing bilibili_id")

        return artist.bilibili_id

    @staticmethod
    def get_instagram_id(artist_id):
        """
        return instagram_id（for InstagramService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.instagram_id:
            raise ValueError("Missing instagram_id")

        return artist.instagram_id

    @staticmethod
    def get_spotify_id(artist_id):
        """
        return spotify_id（for SpotifyService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.spotify_id:
            raise ValueError("Missing spotify_id")

        return artist.spotify_id

    @staticmethod
    def get_tiktok_id(artist_id):
        """
        return tiktok_id（for TiktokService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.tiktok_id:
            raise ValueError("Missing tiktok_id")

        return artist.tiktok_id

    @staticmethod
    def get_youtube_id(artist_id):
        """
        return youtube_id（for YoutubeService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.youtube_id:
            raise ValueError("Missing youtube_id")

        return artist.youtube_id

    @staticmethod
    def get_melon_id(artist_id):
        """
        return melon_id（for MelonService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.melon_id:
            raise ValueError("Missing melon_id")

        return artist.melon_id

    @staticmethod
    def get_weibo_id(artist_id):
        """
        return weibo_id（for WeiboService）
        """
        artist = ArtistService.get_artist(artist_id)

        if not artist.weibo_id:
            raise ValueError("Missing weibo_id")

        return artist.weibo_id

    @staticmethod
    def get_db_artist():
        """
        Get all artists' necessary info for trending calculation
        """
        artists = Artists.objects(artist_id__ne=None)\
            .only(
                "artist_id",
                "type",
                "english_name",
                "korean_name",
                "instagram_id",
                "instagram_user",
                "youtube_id",
                "tiktok_id",
                "spotify_id",
                "melon_id",
                "bilibili_id",
                "weibo_id"
        ).as_pymongo()

        return list(artists)

    @staticmethod
    def get_all_artists_by_tenant(tenant_id):
        """
        return list of artists under tenant
        """
        artists = Artists.objects(tenant_id=tenant_id).order_by("english_name")

        artist_data = []
        for a in artists:
            artist_data.append({
                "artist_name": a.english_name.lower() if a.english_name else None,
                "korean_name": a.korean_name,
                "artist_id": a.artist_id,
                "artist_objId": str(a.id),
                "imageURL": a.image_url
            })

        return sorted(artist_data, key=lambda x: x["artist_name"] or "")

    @classmethod
    def get_group_artists(cls):
        groups = Artists.objects(
            pronouns="C",
            is_active=True
        )

        return sorted(
            [
                {
                    "id": str(group.id),
                    "english_name": group.english_name.lower() if group.english_name else None,
                    "korean_name": group.korean_name
                }
                for group in groups
            ],
            key=lambda x: x["english_name"] or ""
        )

    @staticmethod
    def get_all_artists_with_tenant(search="", limit=20, page=1):
        """
        帶分頁與關鍵字搜尋的全量藝人查詢
        """

        tenants = Tenant.objects()
        tenant_map = {str(t.id): t.tenant_name for t in tenants}

        # 1. 建立 Base Query 條件
        query = Artists.objects()
        if search:
            query = query.filter(
                __raw__={
                    "$or": [
                        {"english_name": {"$regex": search, "$options": "i"}},
                        {"korean_name": {"$regex": search, "$options": "i"}}
                    ]
                }
            )

        # 2. 轉為整型並計算 skip
        try:
            page = max(int(page), 1)
            limit = max(int(limit), 1)
        except (ValueError, TypeError):
            page = 1
            limit = 20

        skip = (page - 1) * limit

        # 3. 確保只選擇需要的欄位，先排序、設定 collation，最後再執行 skip 與 limit
        artists = (
            query.only(
                "english_name",
                "korean_name",
                "birth",
                "artist_id",
                "id",
                "image_url",
                "tenant_id"
            )
            .collation({"locale": "en", "strength": 2})
            .order_by("english_name", "id")
            .skip(skip)
            .limit(limit)
        )

        artist_data = []
        for a in artists:
            tenant = a.tenant_id
            tenant_id = str(tenant.id) if tenant else None

            artist_data.append({
                "artist_name": a.english_name,
                "korean_name": a.korean_name,
                "artist_id": a.artist_id,
                "artist_objId": str(a.id),
                "birth": a.birth,
                "imageURL": a.image_url,
                "tenant_id": tenant_id,
                "tenant_name": tenant_map.get(tenant_id, "Unknown")
            })

        return artist_data
