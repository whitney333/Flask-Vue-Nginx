from ..models.user_model import User
import datetime
from mongoengine import ValidationError, DoesNotExist

class UserController:
    @staticmethod
    def create_user(user_data):
        """
        create user
        :return: user object
        """
        try:
            user_data["created_at"] = datetime.datetime.now().isoformat()

            user = User(**user_data)
            user.save()
            return user
        except ValidationError as e:
            raise ValueError(f"Validation error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    def update_user(self):
        pass

    @staticmethod
    def get_single_user_by_firebase_id(firebase_id):
        """
        get user by Firebase ID
        :return: user object
        """
        try:
            return User.objects.get(firebase_id = firebase_id)
        except DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error fetching user: {str(e)}")

    @staticmethod
    def get_single_user_by_email(email):
        """
        get user by email
        :return: user object
        """
        try:
            return  User.objects.get(email=email)
        except DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Error fetching user: {str(e)}")
