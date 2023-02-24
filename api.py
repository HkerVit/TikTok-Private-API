# www.aithe.dev
# github.com/aithedev/TikTok-Private-API

import requests
import secrets
import hashlib
import urllib
import time

from utils.signature import signature

class TikTok:
    def __init__(
        self,
        session_id: str
        ) -> None:

        self.api_url = "https://api-h2.tiktokv.com/"
        self.session = requests.Session()
        self.headers = {
            "accept-encoding": "gzip",
            "connection": "Keep-Alive",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "host": "api-h2.tiktokv.com",
            "passport-sdk-version": "19",
            "sdk-version": "2",
            "user-agent": "okhttp/3.10.0.1",
            "x-ss-req-ticket": str(int(time.time() * 1000))
        }
        self.session.headers.update(self.headers)
        self.session.cookies = f"sessionid={session_id}" if session_id != None else secrets.token_hex(32)

        self.params = {
            'manifest_version_code': 190103, 
            '_rticket': int(round(time.time() * 1000)), 
            'current_region': 'BE', 
            'app_language': 'en', 
            'app_type': 'normal', 
            'iid': 7183409061831001857, 
            'channel': 'googleplay', 
            'device_type': 'ASUS_Z01QD', 
            'language': 'en', 
            'cpu_support64': 'true', 
            'host_abi': 'armeabi-v7a', 
            'locale': 'en', 
            'resolution': 1600*900, 
            'openudid': '7f8e923db4b22341', 
            'update_version_code': 190103, 
            'ac2': 'wifi', 
            'cdid': 'c7357243-a13f-4d42-94d9-cb318ae73c52', 
            'sys_region': 'US', 
            'os_api': 28, 
            'uoo': 0, 
            'timezone_name': 'Asia/Shanghai', 
            'dpi': 300, 
            'residence': 'BE', 
            'carrier_region': 'BE', 
            'ac': 'wifi', 
            'device_id': 7147445232161539590, 
            'mcc_mnc': 20610, 
            'os_version': 9, 
            'timezone_offset': 28800, 
            'version_code': 190103, 
            'app_name': 'trill', 
            'ab_version': '19.1.3', 
            'version_name': '19.1.3', 
            'device_brand': 'Asus', 
            'op_region': 'BE', 
            'ssmix': 'a', 
            'device_platform': 'android', 
            'build_number': '19.1.3', 
            'region': 'US', 
            'aid': 1180, 
            'ts': int(time.time())
        }
        self.session.params.update(self.params)

    @staticmethod
    def xor(string: str) -> str:
        return "".join([hex(int(x ^ 5))[2:] for x in string.encode('utf-8')])

    @staticmethod
    def query(data: str) -> str:
        return urllib.parse.urlencode(data)

    @staticmethod
    def cookies_to_session(cookies: str) -> str:
        return cookies.split(";")[13].replace(" ", "")

    def edit_profile(self, choice: str, text: str, user_id: int) -> dict: 
        data = {
            "uid": user_id,
            "page_from": 0,
            choice: text,
            "confirmed": 0 
        } 
        data if choice != "username" else data.pop("confirmed")
        
        self.session.headers.update({
            **signature(
                params = self.query(self.session.params),
                data = self.query(data),
                cookies = self.session.cookies
            ).get_value(),
            "x-ss-stub": str(hashlib.md5(self.query(data).encode()).hexdigest()).upper()
        })

        return self.session.post(
            url = self.api_url + "aweme/v1/commit/user/?" if choice != "username" else "passport/login_name/update/?",
            data = data
        ).json()

    def edit_bio(self, bio: str, user_id: int) -> dict:
        """
        Makes a post request to edit the bio of a user.
        :param bio: The text to set as the bio.
        :param user_id: The user id of the user.

        :return: The response (json) after editing the users bio.
        """

        return self.edit_profile("signature", bio, user_id)

    def edit_nickname(self, nickname: str, user_id: int) -> dict:
        """
        Makes a post request to edit the nickname of a user.
        :param nickname: The text to set as the nickname.
        :param user_id: The user id of the user.

        :return: The response (json) after editing the users nickname.
        """

        return self.edit_profile("nickname", bio, user_id)

    def edit_username(self, username: str, user_id: int) -> dict:
        """
        Makes a post request to edit the username of a user.
        :param username: The text to set as the username.
        :param user_id: The user id of the user.

        :return: The response (json) after editing the users username.
        """

        return self.edit_profile("username", bio, user_id, session_id)


    ## Returns blank response, open an issue or pull request if you've found a solution! :)

    def check_username(self, username: str) -> dict:
        """
        Makes a get request to check a username.
        :param username: The username to check.
    
        :return: The response (json) after checking the username.
        """

    
        self.session.params.update({"unique_id": username})
        self.session.headers.update({
            **signature(
                params = self.query(self.params),
                data = None,
                cookies = self.session.cookies
            ).get_value()
        })
    
        return self.session.post(url = self.api_url + "aweme/v1/unique/id/check/?").json()

    def following_followers(self, choice: str, user_id: int, sec_user_id: str, count: int) -> dict:
        self.session.params.update(
            {
                'user_id': user_id, 
                'sec_user_id': sec_user_id, 
                'max_time': 0,
                'count': count,
                'offset': 0,
                'source_type': 1,
                'address_book_access': 1
            }
        )
        self.session.headers.update({
            **signature(
                params = self.query(self.session.params),
                data = None,
                cookies = self.session.cookies
            ).get_value()
        })

        return self.session.get(url = self.api_url + f"aweme/v1/user/{choice}/list/?").json()


    def following_list(self, user_id: int, sec_user_id: str, count: int) -> dict:
        """
        Makes a get request to get the following list of a user.
        :param user_id: The user id of the user.
        :param sec_user_id: The sec_user_id of the user.
        (optional) :param session_id: The session id of your account.
        :param count: The amount of following to show.

        :return: The response (json) after retrieving following list of the user. 
        """

        return self.following_followers("following", user_id, sec_user_id, session_id, count)

    def followers_list(self, user_id: int, sec_user_id: str, count: int) -> dict:
        """
        Makes a get request to get the followers list of a user.
        :param user_id: The user id of the user.
        :param sec_user_id: The sec_user_id of the user.
        (optional) :param session_id: The session id of your account.
        :param count: The amount of followers to show.

        :return: The response (json) after retrieving following list of the user. 
        """

        return self.following_followers("followers", user_id, session_id, count)


    def toggle_like(self, type: int, video_id: int):
        self.session.params.update(
            {
                'aweme_id': video_id, 
                'enter_from': 'homepage_hot', 
                'type': type,
                'channel_id': 0,
            }
        )
        self.session.headers.update({
            **signature(
                params = self.query(self.session.params),
                data = None,
                cookies = self.session.cookies
            ).get_value()
        })

        return self.session.post(url = self.api_url + "aweme/v1/commit/item/digg/?").json()

    def like_video(self, video_id: int) -> dict:
        """
        Makes a post request to like a video.
        :param video_id: The video id of the video.

        :return: The response (json) after liking the video.
        """

        return self.toggle_like(1, video_id)


    def unlike_video(self, video_id: int) -> dict:
        """
        Makes a post request to unlike a video.
        :param video_id: The video id of the video.

        :return: The response (json) after unliking the video.
        """

        return self.toggle_like(0, video_id, session_id)


    def toggle_follow(self, type: int, sec_user_id: int):
        self.session.params.update(
            {
                'city': '',
                'sec_user_id': sec_user_id, 
                'from': 0,
                'from_pre': -1,
                'enter_from': 'homepage_hot', 
                'type': type,
                'channel_id': 3,
            }
        )
        self.session.headers.update({
            **signature(
                params = self.query(self.session.params),
                data = None,
                cookies = self.session.cookies
            ).get_value()
        })

        return self.session.post(url = self.api_url + "aweme/v1/commit/follow/user/?").json()

    def follow(self, sec_user_id: str) -> dict:
        """
        Makes a post request to follow a user.
        :param sec_user_id: The sec_user_id of the user.

        :return: The response (json) after following a user.
        """

        return self.toggle_follow(1, sec_user_id)


    def unfollow(self, sec_user_id: str) -> dict:
        """
        Makes a post request to unfollow a user.
        :param sec_user_id: The sec_user_id of the user.

        :return: The response (json) after unfollowing a user.
        """

        return self.toggle_follow(0, sec_user_id)