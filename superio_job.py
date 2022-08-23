import mysql.connector
import requests
from datetime import datetime
from settings import WP_MYSQL_USER, WP_MYSQL_PASSWORD, WP_MYSQL_HOST, WP_MYSQL_DB, WP_MYSQL_PREFIX, WP_APP_USERNAME, \
    WP_APP_PASSWORD, SITE_URL


class SuperioJob:
    """
    def __init__(self):
        self.db_connected = False
        # open mysql connection

        self.cnx = mysql.connector.connect(
            user=WP_MYSQL_USER,
            password=WP_MYSQL_PASSWORD,
            host=WP_MYSQL_HOST,
            database=WP_MYSQL_DB,
        )
        self.db_connected = True

        self.cnx.autocommit = True
        self.cursor = self.cnx.cursor(prepared=True)

        # WordPress REST API session
        self.session = requests.Session()
        self.session.auth = (WP_APP_USERNAME, WP_APP_PASSWORD)

    def __del__(self):
        if self.db_connected:
            self.cnx.close()  # Close mysql connection

     def __wp_create_post_meta(self, post_id: int, meta_data: dict) -> None:
        """
    #Insert multiple post metas into DB
    #:param meta_data: Dictionary of meta data
    """

    data = [(post_id, key, value) for key, value in meta_data.items()]

    table_name = f"{WP_MYSQL_PREFIX}_postmeta"

    q = f"INSERT INTO {table_name} (post_id, meta_key, meta_value) VALUES (%s, %s, %s)"

    self.cursor.executemany(q, data)

"""
    def __init__(self):
        """
        self.db_connected = False
        # open mysql connection

        self.cnx = mysql.connector.connect(
            user=WP_MYSQL_USER,
            password=WP_MYSQL_PASSWORD,
            host=WP_MYSQL_HOST,
            database=WP_MYSQL_DB,
        )
        self.db_connected = True

        self.cnx.autocommit = True
        self.cursor = self.cnx.cursor(prepared=True)
        """
        # WordPress REST API session
        self.session = requests.Session()
        self.session.auth = (WP_APP_USERNAME, WP_APP_PASSWORD)

    def create_security_job(self, title: str, salary: str, location: str, content: str,
                            job_type: list, location_tag: list) -> None:

        meta_data = {
            "_job_salary": salary,
            "_job_address": location,
            "_job_apply_type": "internal",
            'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "job_listing_location": location_tag,
            #'_job_featured': 'on'
        }

        post_id = self.__wp_create_job_post(
            title=title,
            content=content,
            job_type=job_type,
            categories=[134],  # 134 -> Security
            salary=salary,
            location_tag=location_tag
        )

        print(f"Job with ID {post_id} created.")
        #self.__wp_create_post_meta(post_id=post_id, meta_data=meta_data)
        #print(f"Job meta populated for job #{post_id}.")


    def __wp_create_job_post(self, title: str, content: str, categories: list, job_type: list,
                             salary: str, location_tag: list) -> int:
        """
        Use WP REST API to create a job_listing post
        :param title: Post title
        :param content: HTML content
        :param categories: Security
        :param job_type: Full Time/Part Time
        :return: The post id
        """
        url = f"{SITE_URL}/wp-json/wp/v2/jobs"

        payload = {
            "title": title,
            "status": "publish",
            "content": content,
            "job_listing_category": categories,
            "job_listing_type": job_type,
            "job_listing_location": location_tag,
            "_job_salary": salary,
            'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),

        }

        res = self.session.post(url, data=payload)
        if res.status_code != 201:
            print(res.status_code)
            print(res.content)
            raise Exception("Unable to create a post in WP via REST API")

        data = res.json()

        return int(data["id"])
