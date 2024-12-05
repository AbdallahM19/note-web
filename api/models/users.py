"""users.py"""

from typing import Union, Optional
from pydantic import BaseModel
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
from api.database import UserDb, get_session


class BaseUser(BaseModel):
    """User account model"""
    username: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[str] = None
    description: Optional[str] = None


class UserIn(BaseUser):
    """User account model with password"""
    hashed_password: Optional[str] = None


class UserDetails(BaseUser):
    id: int
    hashed_password: Optional[str] = None
    session_id: Optional[str] = None
    time_created: Optional[str] = None
    last_opened: Optional[str] = None


class User():
    """User Class"""
    def __init__(self):
        self.sess = get_session()

    def get_user_by_id(self, user_id):
        """Get user by id function"""
        try:
            user = self.sess.query(UserDb).filter(
                UserDb.id == user_id
            ).first()
            return user
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error getting user by id: {str(e)}") from e
        finally:
            self.sess.close()

    def get_user_by_session_id(self, session_id):
        """Get user by session id function"""
        try:
            user = self.sess.query(UserDb).filter(
                UserDb.session_id == session_id
            ).first()
            return user
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error getting user by session id: {str(e)}") from e
        finally:
            self.sess.close()

    def get_user_by_username(
        self, name: str, skip: Optional[int] = 0, limit: Optional[int] = None
    ) -> Union[list, dict, str]:
        """Get user by username function"""
        try:
            users_data = self.sess.query(UserDb).filter(
                UserDb.username.like(f"%{name.lower()}%")
            ).offset(skip).limit(limit).all()

            if not users_data:
                return f"User with name {name} not found"

            return users_data
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error getting user by username: {e}") from e
        finally:
            self.sess.close()

    def get_all_users_data(
        self,
        skip: Optional[int],
        limit: Optional[int]
    ) -> list:
        """Get all users in list of dict"""
        try:
            users = self.sess.query(UserDb)

            if skip is not None and limit is not None:
                users = users.offset(skip).limit(limit)
            elif skip and limit is None:
                users = users.offset(skip).limit(10)
            elif skip is None and limit:
                users = users.offset(0).limit(limit)

            return users.all()
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error getting all users: {str(e)}") from e
        finally:
            self.sess.close()

    def check_if_user_exists(self, username: str, email: str) -> Optional[UserDb]:
        """Check if user exists in database"""
        try:
            user_existed = self.sess.query(UserDb).filter(
                or_(
                    UserDb.username == username,
                    UserDb.email == email
                )
            ).first()
            if user_existed:
                return user_existed
            return None
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error checking user existence: {str(e)}") from e
        finally:
            self.sess.close()

    # authenticate_user Not Used ⬇
    def authenticate_user(self, username: str, password: str) -> Union[dict, str]:
        """Authenticate user by username and password"""
        try:
            user = self.sess.query(UserDb).filter(
                and_(
                    or_(
                        UserDb.username == username,
                        UserDb.email == username
                    )
                    # UserDb.hashed_password == password
                )
            ).first()
            if user:
                if user.hashed_password == password:
                    return self.convert_class_user_to_object(user)
                return "Invalid password. password not correct"
            return "Invalid username. user not exists"
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error authenticating user: {e}") from e
        finally:
            self.sess.close()

    def insert_new_user(self, **kwargs: dict):
        """Insert new user into database"""
        try:
            new_user = UserDb(**kwargs)
            self.sess.add(new_user)
            self.sess.commit()
            self.sess.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            self.sess.rollback()
            raise SQLAlchemyError(f"Error inserting new user: {e}") from e
        finally:
            self.sess.close()

    def update_user_account(self, kwargs: dict) -> dict:
        """Update user account information"""
        try:
            user = None

            if kwargs['session_id']:
                user = self.sess.query(UserDb).filter(
                    UserDb.session_id == kwargs['session_id']
                ).first()
            elif kwargs['id']:
                user = self.sess.query(UserDb).filter(
                    UserDb.id == kwargs['id']
                ).first()

            if user:
                for key, value in kwargs.items():
                    if key not in ['id', 'session_id'] and value is not None:
                        setattr(user, key, value)
                self.sess.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.sess.rollback()
            raise SQLAlchemyError(f"Error updating user account: {e}") from e
        finally:
            self.sess.close()

    def delete_user(self, user_id: int) -> bool:
        """Delete user Account permanently from database"""
        try:
            user = self.sess.query(UserDb).filter(
                UserDb.id == user_id
            ).first()

            if user:
                self.sess.delete(user)
                self.sess.commit()
                return True

            return False
        except SQLAlchemyError as e:
            self.sess.rollback()
            raise SQLAlchemyError(f"Error deleting user with id ({user_id}): {e}") from e
        finally:
            self.sess.close()

    @classmethod
    def convert_class_user_to_object(cls, user: UserDb) -> dict:
        """Convert a UserDb object to a User dict"""
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "session_id": user.session_id,
            "time_created": user.time_created,
            "last_opened": user.last_opened,
            "date_of_birth": user.date_of_birth,
            "description": user.description,
        }
