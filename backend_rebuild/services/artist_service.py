from models.artist_model import Artists


class ArtistService:
    @staticmethod
    def get_artist_by_mid(artist_id):
        artist = Artists.objects(mid=artist_id).first()
        if not artist:
            raise ValueError("Artist not found")
        return artist

    @staticmethod
    def get_bilibili_id(artist_id):
        artist = ArtistService.get_artist_by_mid(artist_id)

        if not artist.bilibili_id:
            raise ValueError("Missing bilibili id")

        return artist.bilibili_id

    #TODO ADD OTHER PLATFORMS GET_ID METHODS