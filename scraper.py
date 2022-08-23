import csv
import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from vendors.superio_job import SuperioJob

datetime_str = str(datetime.now().strftime("%d%m%Y"))


class Job:
    """
    Job object
    """

    def __init__(
            self,
            image: str,
            job_name: str,
            company_name: str,
            salary: str,
            job_type: str,
            shift: str,
            link: str,
            content: str,
            location: str = None,
            job_id: str = None,
    ):
        """
        Init the job object with fields. Add more fields when needed
        :param image: Company Logo
        :param job_name: Job name
        :param company_name: Company Name
        :param salary: Job salary
        :param location: Job location
        :param job_type: Full Time/Part Time
        :param shift: Day/Night shift
        :param link: link to Job Info page
        :param job_id: An unique identifier for a specific job, optional
        """
        self.image = image
        self.job_name = job_name
        self.company_name = company_name
        self.salary = salary
        self.location = location
        self.job_type = job_type
        self.shift = shift
        self.link = link
        self.job_id = job_id
        self.content = content

    def json(self) -> str:
        """
        Convert the fields into json format
        :return: job fields in json format
        """
        return json.dumps(self.__dict__)


class BaseScraper:
    """
    Base class for scraper
    """
    name = "Undefined"
    file_name_txt = 'NULL'
    file_name_csv = 'NULL'

    def __init__(self):
        """
        Init
        """
        self.job_list: [Job] = []
        self.file_name_txt: str
        self.file_name_csv: str
        self.limit: int = 20

    def scrape(self) -> [Job]:
        """
        :return: List of Job objects
        """
        raise NotImplemented()

    def censor(self):
        for job in self.job_list:
            # 8 digits starting with 6,9,8
            phone_regex1 = r'(9|8|6)\d{7}'
            # 8 digits starting with 6,9,8 with space between first and last 4 digits
            phone_regex2 = r'(9|8|6)\d{3}( |-)\d{4}'
            # 10 digits starting with 65
            phone_regex3 = r'65\d{8}'
            # websites
            site_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)" \
                         r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+" \
                         r"|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            # emails
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            substitute = '9374 8870'

            job.job_name = re.sub(site_regex, substitute, job.job_name)
            job.job_name = re.sub(email_regex, substitute, job.job_name)
            job.job_name = re.sub(phone_regex1, substitute, job.job_name)
            job.job_name = re.sub(phone_regex2, substitute, job.job_name)
            job.job_name = re.sub(phone_regex3, substitute, job.job_name)

            job.content = re.sub(site_regex, substitute, job.content)
            job.content = re.sub(email_regex, substitute, job.content)
            job.content = re.sub(phone_regex1, substitute, job.content)
            job.content = re.sub(phone_regex2, substitute, job.content)
            job.content = re.sub(phone_regex3, substitute, job.content)


    def save_as_txt(self):
        if len(self.job_list) == 0:
            raise Exception("Job list is empty, please run scrape() first if you haven't.")
        for job in self.job_list:
            with open(self.file_name_txt,'a', encoding= 'utf-8') as f:
                f.write(f'Image: {job.image} Job: {job.job_name} Company: {job.company_name} Salary: {job.salary} '
                        f'Location: {job.location} Job Type: {job.job_type} Shift: {job.shift} Link: {job.link} '
                        f'Content: {job.content}\n\n')

    def save_as_csv(self):
        if len(self.job_list) == 0:
            raise Exception("Job list is empty, please run scrape() first if you haven't.")

        job_dict_list = []
        [job_dict_list.append(job.__dict__) for job in self.job_list]

        keys = job_dict_list[0].keys()
        with open(f'{self.file_name_csv}', mode='w+',newline="", encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(job_dict_list)

    def save_to_wp(self, limit=1):
        """
        Save jobs into WordPress
        :param limit: Number of jobs to post to WordPress
        """
        superio_job = SuperioJob()
        count = 0

        for job in self.job_list:
            if job.location == 'North':
                location_tag = [136]
            elif job.location == 'South':
                location_tag = [137]
            elif job.location == 'East':
                location_tag = [135]
            elif job.location == 'West':
                location_tag = [138]
            elif job.location == 'Central':
                location_tag = [139]
            else:
                location_tag = [147]

            if job.job_type == 'Full-Time' or 'Full Time' or 'Full time':
                job_type = [66]
            elif job.job_type == 'Part-Time' or 'Part Time' or 'Part time':
                job_type = [92]
            else:
                job_type = [103]

            superio_job.create_security_job(
                title=job.job_name,
                content=job.content,
                salary=job.salary,
                location=job.location,
                job_type=job_type,
                location_tag=location_tag

            )
            count += 1

            if count >= limit:
                break

        print(f"Saved {count} jobs into WordPress")


class SXCScraper(BaseScraper):
    name = 'SXC'

    def __int__(self, limit: int = 100):
        super().__init__(limit=limit)

    def __get_job_page_urls(self) -> list:
        page_num = 1
        url_list = []

        print("Getting all job page urls...")
        while True:
            res = requests.get(f"https://sxc.sg/?pagenum={page_num}")
            if res.status_code != 200:
                print("The requested resource is not available at the moment, stopping...")
                return url_list

            soup = BeautifulSoup(res.content, 'html.parser')
            table = soup.select_one('table.gv-table-view > tbody')  # only one table in each page
            rows = table.find_all('tr', recursive=False)

            for row in rows:
                try:
                    url = row.select_one("td.gv-field-5-entry_link > a")['href']
                except TypeError:
                    continue
                url_list.append(url)
                if len(url_list) >= self.limit:
                    return url_list
            page_num += 1

    def scrape(self) -> [Job]:
        url_list = self.__get_job_page_urls()

        job_list = []

        for url in url_list:
            res = requests.get(url)
            if res.status_code != 200:
                raise Exception("The requested resource is not available at the moment")

            soup = BeautifulSoup(res.content, 'html.parser')
            table = soup.select_one('table.gv-table-view-content > tbody')

            job_site_type = table.select_one("#gv-field-5-5 > td").getText()

            if job_site_type == "In-House":
                # Skip those job with in house type
                continue

            job_name = table.select_one("#gv-field-5-3 > td").getText()
            company_name = table.select_one("#gv-field-5-28 > td").getText()
            salary = table.select_one("#gv-field-5-29 > td").getText()
            location = table.select_one("#gv-field-5-4 > td").getText()
            job_type = table.select_one("#gv-field-5-2 > td").getText()
            shift = table.select_one("#gv-field-5-26 > td").getText()
            link = url
            try:
                content = table.select_one("#gv-field-5-16 > td").getText()
            except AttributeError:
                content = ''
            job_obj = Job(
                image='NULL',
                job_name=job_name,
                company_name=company_name,
                salary=salary,
                location=location,
                job_type=job_type,
                shift=shift,
                link=link,
                content=content
            )
            job_list.append(job_obj)
        self.job_list = job_list
        self.file_name_txt = r'sxc%s.txt'%datetime_str
        self.file_name_csv = r'sxc%s.csv'%datetime_str
        return job_list


class OSPScraper(BaseScraper):
    name = "OSP"

    @staticmethod
    def __get_session_auth() -> {}:
        """
        Get JSESSIONID and CSRF token pair
        (The pair must match each other to authenticate the session)
        """
        session = requests.Session()
        res = session.get('https://www.osp.sg/public/security-officer-jobs')
        cookies = session.cookies.get_dict()
        session_id = cookies.get("JSESSIONID", None)  # Get the session id from cookies

        if not session_id:
            raise ValueError("Unable to fetch JSESSIONID, request failed.")

        soup = BeautifulSoup(res.content, 'html.parser')
        csrf = soup.select_one("input[name='_csrf']")["value"]
        return {"jsessionid": session_id, "csrf": csrf}

    def scrape(self) -> [Job]:
        auth = self.__get_session_auth()
        headers = {
            "Host": "www.osp.sg",
            "Origin": "https://www.osp.sg",
            "Referer": "https://www.osp.sg/public/security-officer-jobs",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
            "X-CSRF-TOKEN": auth["csrf"]
        }
        cookies = {'JSESSIONID': auth["jsessionid"]}
        res = requests.post(
            headers=headers,
            cookies=cookies,
            url="https://www.osp.sg/public/jobs2"
        )

        if res.status_code != 200:
            raise Exception(f"Request failed with status code {res.status_code}")

        data = res.json()["viewModel"]

        job_list = []
        for item in data:
            # only scrape ads posted today/yesterday
            startday = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            if item['startDateStr'] < startday:
                continue

            image = item['logo']
            job_name = item["title"]
            company_name = item['shortName']
            salary = item["salaryRangeTitle"]

            region = item["locations"]
            mrt = item['nearbyMrtStation']
            location = f'{region},{mrt}'

            job_type = item["appts"]
            shift = item['shifts']
            link = 'NULL'
            content = item['fullText']

            job_obj = Job(
                image=image,
                job_name=job_name,
                company_name=company_name,
                salary=salary,
                location=location,
                job_type=job_type,
                shift=shift,
                link=link,
                content=content
            )
            job_list.append(job_obj)

        self.job_list = job_list
        self.file_name_txt = r'osp%s.txt'%datetime_str
        self.file_name_csv = r'osp%s.csv'%datetime_str
        return job_list


class JobStreetScraper(BaseScraper):
    name = "JobStreet"

    def scrape(self) -> [Job]:
        page_limit = 10
        url = 'https://www.jobstreet.com.sg/en/job-search/security-officer-jobs/%d/'
        '?createdAt=1d&salary=0&salary-max=2147483647'
        page_num = 1
        job_list = []
        shift = 'NULL'

        while page_num <= page_limit:
            html_text = requests.get(url % page_num).text
            soup = BeautifulSoup(html_text, 'html.parser')
            job_cards = soup.find_all('div', class_ = 'sx2jih0 zcydq89e zcydq88e zcydq872 zcydq87e')
            for job in job_cards:
                job_name = job.find('h1', class_='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvca').text
                location = job.find('span', class_='sx2jih0 zcydq84u zcydq80 iwjz4h0').text
                job_type = job.find_all('dd', class_='sx2jih0 zcydq84y')[-1].text

                try:
                    # AttributeError:'NoneType' object has no attribute 'text'
                    company_name = job.find('span', class_='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca').text
                except AttributeError:
                    company_name = 'NULL'
                try:
                    # TypeError: 'NoneType' object is not subscriptable
                    image = job.find('img', class_='sx2jih0 pXyoU_0')['src']
                except TypeError:
                    image = 'NULL'
                try:
                    # IndexError: list index out of range
                    salary = job.find_all('span', class_='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvc7')[1].text
                except IndexError:
                    salary = 'NULL'

                link = job.find('a', class_='_1hr6tkx5 _1hr6tkx8 _1hr6tkxb sx2jih0 sx2jihf zcydq8h')['href']
                link = 'https://www.jobstreet.com.sg/%s' % link
                res = requests.get(link)
                soup_jobinfo = BeautifulSoup(res.content, 'html.parser')
                """
                for item in soup_jobinfo.find_all('div'):
                    if "data-automation" in item.attrs and item["data-automation"]=="jobDescription":
                        content = item.getText()
                    else:
                        content=''
                """
                try:
                    content = soup_jobinfo.find('div', class_='YCeva_0').text
                except AttributeError:
                    content=''


                job_obj = Job(
                    image=image,
                    job_name=job_name,
                    company_name=company_name,
                    salary=salary,
                    location=location,
                    job_type=job_type,
                    shift=shift,
                    link=link,
                    content=content
                )
                job_list.append(job_obj)
            page_num += 1

        self.job_list = job_list
        self.file_name_txt = r'jobstreet%s.txt'%datetime_str
        self.file_name_csv = r'jobstreet%s.csv'%datetime_str

        return job_list


class FastJobsScraper(BaseScraper):
    name = 'FastJobs'

    def scrape(self) -> [Job]:
        page_limit = 6
        page_num = 1
        job_list = []
        url = f'https://www.fastjobs.sg/singapore-jobs/en/latest-jobs-jobs/security-jobs/' \
              f'security+officer-jobs-search/page-%d/'
        job_type = 'NULL'
        shift = 'NULL'

        while page_num <= page_limit:
            # Solves 403 error
            req = Request(url % page_num, headers={'User-Agent': 'Mozilla/5.0'})
            html_text = urlopen(req).read()
            soup = BeautifulSoup(html_text, 'html.parser')
            # returns cards from 1 page
            job_cards = soup.find_all('a', class_='ad-detail-link adbox')

            for job in job_cards:
                div_tag = job.find('div', class_='col-xs-12')
                job_name = div_tag.find('h2').text

                company_name = job.find('span', class_='visible-xs').text

                location = job.find('span', class_='glyphicon glyphicon-map-marker').next_sibling
                location = " ".join(location.split())

                image = job.find('img', class_='img-coylogo img-responsive')['src']
                try:
                    # AttributeError: 'NoneType' object has no attribute 'text'
                    salary = job.find('span', class_='salmin').text
                    salary = " ".join(salary.split())
                except AttributeError:
                    salary = "NULL"

                link = job['href']
                # ERROR HERE
                req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                html_jobinfo = urlopen(req).read()
                soup_jobinfo = BeautifulSoup(html_jobinfo, 'html.parser')

                try:
                    content = soup_jobinfo.find('div',class_='job-desc').getText()
                except AttributeError:
                    content = ''

                job_obj = Job(
                    image=image,
                    job_name=job_name,
                    company_name=company_name,
                    salary=salary,
                    location=location,
                    job_type=job_type,
                    shift=shift,
                    link=link,
                    content=content
                )
                job_list.append(job_obj)
            page_num += 1

        self.job_list = job_list
        self.file_name_txt = r'fastjobs%s.txt'%datetime_str
        self.file_name_csv = r'fastjobs%s.csv'%datetime_str
        return job_list
