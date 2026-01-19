from models.sns.instagram_model import Instagram, InstagramDailySnapshot, PostDetails
from models.artist_model import Artist
import datetime
from datetime import timedelta
from flask import jsonify, request
import pandas as pd
import numpy as np


class InstagramController:

    @staticmethod
    def get_follower(artist_id, date_end, days=7):
        """
        Get Instagram follower count data for a specific time range
        :param artist_id: The ID of the artist to get follower data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param days: The number of days to analyze
        :return: JSON response containing follower data with dates and counts
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not days:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            # Define range mapping
            # Get number of days from range mapping, default to 7 days if range not found
            start_date = date_end - datetime.timedelta(days=days)

            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404

            instagram_data = InstagramDailySnapshot.objects(
                artist=artist,
                datetime__lte=date_end,
                datetime__gt=start_date
            ).order_by('datetime').only('datetime', 'follower_count')
            result = [
                {
                    'date': data.datetime.strftime('%Y-%m-%d'),
                    'follower_count': data.follower_count
                }
                for data in instagram_data
            ]

            return jsonify({
                'status': 'success',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_post_count(artist_id, date_end, days=7):
        """
        Get Instagram media counts for a specific time range
        :param artist_id: The ID of the artist to get post data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param range: The time range to analyze ('7d', '28d', '90d', '180d', '365d')
        :return: JSON response containing post count data with dates and counts
         Get Instagram media counts for a specific time range
        :param artist_id: The ID of the artist to get post data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param days: The number of days to analyze
        :return: JSON response containing post count data with dates and counts
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not days:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            start_date = date_end - datetime.timedelta(days=days)

            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            instagram_data = InstagramDailySnapshot.objects(
                artist=artist,
                datetime__lte=date_end,
                datetime__gt=start_date
            ).order_by('datetime').only('datetime', 'media_count')
            result = [
                {
                    'date': data.datetime.strftime('%Y-%m-%d'),
                    'media_count': data.media_count
                }
                for data in instagram_data
            ]

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_threads_follower(artist_id, date_end, days):
        """
        Get Instagram threads follower count data for a specific time range
        :param artist_id: The ID of the artist to get threads follower data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param days: The number of days to analyze
        :return: JSON response containing threads follower data with dates and counts
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not days:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            start_date = date_end - datetime.timedelta(days=days)

            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            instagram_data = InstagramDailySnapshot.objects(
                artist=artist,
                datetime__lte=date_end,
                datetime__gt=start_date
            ).order_by('datetime').only('datetime', 'threads_follower')
            result = [
                {
                    'date': data.datetime.strftime('%Y-%m-%d'),
                    'threads_follower': data.threads_follower
                }
                for data in instagram_data
            ]

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_likes(artist_id, date_end, days=7):
        """
        Get total likes and likes per post for the latest posts within a specified time range
        :param artist_id: The ID of the artist to get like data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param days: The number of days to analyze
        :return: JSON response containing like data with dates, total likes, and likes per post
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not days:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            start_date = date_end - datetime.timedelta(days=days)
            
            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            instagram_data = InstagramDailySnapshot.objects(
                artist=artist,
                datetime__lte=date_end,
                datetime__gt=start_date
            ).order_by('datetime').only('datetime', 'total_likes', 'media_count')
            result = [
                {
                    'date': data.datetime.strftime('%Y-%m-%d'),
                    'total_likes': data.total_likes,
                    'likes_per_post': data.total_likes / data.media_count
                }
                for data in instagram_data
            ]

            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_comments(artist_id, date_end, days=7):
        """
        Get total comments and comments per post for the latest posts within a specified time range
        :param artist_id: The ID of the artist to get comment data for
        :param date_end: The end date for the data range in format 'YYYY-MM-DD'
        :param days: The number of days to analyze
        :return: JSON response containing comment data with dates, total comments, and comments per post
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400
        if not date_end:
            return jsonify({'err': 'Missing date_end parameter'}), 400
        if not days:
            return jsonify({'err': 'Missing range parameter'}), 400

        try:
            # Validate and parse date
            format = "%Y-%m-%d"
            try:
                date_end = datetime.datetime.strptime(date_end, format)
            except ValueError:
                return jsonify({'err': 'Invalid date format. Use YYYY-MM-DD'}), 400

            start_date = date_end - datetime.timedelta(days=days)

            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            instagram_data = InstagramDailySnapshot.objects(
                artist=artist,
                datetime__lte=date_end,
                datetime__gt=start_date
            ).order_by('datetime').only('datetime', 'total_comments', 'media_count')
            result = [
                {
                    'date': data.datetime.strftime('%Y-%m-%d'),
                    'total_comments': data.total_comments,
                    'comments_per_post': data.total_comments / data.media_count
                }
                for data in instagram_data
            ]
            # Check if we got any results
            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_posts_likes_and_comments(artist_id, posts_count=12):
        """
        get instagram latest 12 posts index
        :param artist_id: The ID of the artist to get posts data for
        :param posts_count: The number of posts to return
        :return: JSON response containing posts data with dates, user_id, code, username, taken_at, media_type, product_type, comment_count, like_count, play_count, caption_text, thumbnail, engagement_rate, url
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:

            # retrieve artist
            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            posts_data = PostDetails.objects(artist=artist).order_by('datetime').limit(posts_count)
            result = [
                {
                    "date": data.datetime.strftime('%Y-%m-%d'),
                    "user_id": data.user_id,
                    "code": data.code,
                    "username": data.username,
                    "taken_at": data.taken_at,
                    "media_type": data.media_type,
                    "product_type": data.product_type,
                    "comment_count": data.comment_count,
                    "like_count": data.like_count,
                    "play_count": data.play_count,
                    "caption_text": data.caption_text,
                    "thumbnail": data.thumbnail,
                    "engagement_rate": data.engagement_rate,
                    "hashtags": data.hashtags,
                    "url": f"https://instagram.com/p/{data.code}/"
                }
                for data in posts_data
            ]

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            }), 500

    @staticmethod
    def get_instagram_latest_posts(artist_id, posts_count=12):

        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            posts_data = PostDetails.objects(artist=artist).order_by('datetime').limit(posts_count)
            result = [
                {
                    "date": data.datetime.strftime('%Y-%m-%d'),
                    "user_id": data.user_id,
                    "taken_at": data.taken_at,
                    "media_type": data.media_type,
                    "product_type": data.product_type,
                    "caption_text": data.caption_text,
                    "comment_count": data.comment_count,
                    "like_count": data.like_count,
                    "play_count": data.play_count,
                    "hashtags": data.hashtags,
                    "hashtags_count": data.hashtags_count,
                    "engagement_rate": data.engagement_rate,
                    "thumbnail": data.thumbnail,
                    "url": f"https://instagram.com/p/{data.code}/"
                }
                for data in posts_data
            ]

            if not result:
                return jsonify({
                    'status': 'success',
                    'data': [],
                    'message': 'No data found for the specified range'
                }), 200

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    @staticmethod
    def extract_hashtags_keyword(text):
        """
        extract keywords with hashtag from string
        """
        # initializing hashtag_list variable
        hashtag_list = []

        # splitting the text into words
        for word in text.split():
            # checking the first character of every word
            if word[0] == '#':
                # adding the word to the hashtag_list
                hashtag_list.append(word[1:])
        return hashtag_list

    @staticmethod
    def get_latest_follower_count(artist_id):
        """
        Get the latest follower count of the artist
        :param artist_id: The ID of the artist to get follower data for
        :return: JSON response containing follower data with dates and counts
        """
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            follower = Instagram.objects(artist=artist).order_by('datetime').only('follower_count').first()
            return jsonify({
                'status': 'success',
                'data': {
                    'follower_count': follower.follower_count
                }
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

    ### Most-used hashtags methods
    @staticmethod
    def get_hashtags_most_used(artist_id, count=5):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            posts_data = PostDetails.objects(artist=artist).order_by('datetime').only('hashtags')
            dict_hashtags = {}
            for data in posts_data:
                for hashtag in data.hashtags:
                    dict_hashtags[hashtag] = dict_hashtags.get(hashtag, 0) + 1
            result = sorted(dict_hashtags.items(), key=lambda x: x[1], reverse=True)[:count]

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })


    ### Most-engaged hashtags methods
    @staticmethod
    def get_hashtags_most_engaged(artist_id, count=5):
        # Validate required parameters
        if not artist_id:
            return jsonify({'err': 'Missing artist_id parameter'}), 400

        try:
            # fetch follower count
            artist = Artist.objects(id=artist_id).first()
            if not artist:
                return jsonify({'err': 'Artist not found'}), 404
                
            follower = InstagramDailySnapshot.objects(artist=artist).order_by('datetime').limit(1).only('follower_count').first()
            if not follower:
                return jsonify({'err': 'No follower data found'}), 404
                
            follower_count = follower.follower_count

            # sub_total = like_count + comment_count
            # _eng_rate = sub_total / follower_count
            # group by hashtag name
            # sort by _eng_rate descending
            # limit 10
            posts_data = PostDetails.objects(artist=artist).order_by('datetime').only('engagement_rate', 'hashtags_count', 'hashtags')
            
            dict_hashtags = {}

            for data in posts_data:
                if data.hashtags_count > 0:
                    eng_rate_per_hashtag = data.engagement_rate / data.hashtags_count
                    for hashtag in data.hashtags:
                        dict_hashtags[hashtag] = dict_hashtags.get(hashtag, 0) + eng_rate_per_hashtag

            result = sorted(dict_hashtags.items(), key=lambda x: x[1], reverse=True)[:count]

            return jsonify({
                'status': 'success',
                'data': result
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'err': str(e)
            })

