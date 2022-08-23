"""
types = requests.get('https://coursemology.sg/jobs/wp-json/wp/v2/types') print(types) for info on all post types

"job_listing":{"slug":"job_listing","taxonomies":["job_listing_type",
"job_listing_category","job_listing_location","job_listing_tag"],"rest_base":"job_listing","rest_namespace":"wp\\/v2",
"_links":{"collection":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/types"}],
"wp:items":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/job_listing"}],
"curies":[{"name":"wp","href":"https:\\/\\/api.w.org\\/{rel}","templated":true}]}}

b'[{"id":8052,"date":"2022-07-12T20:39:09","date_gmt":"2022-07-12T12:39:09","guid":{"rendered":"https:\\/\\/coursemology.sg\\/jobs\\/employer\\/coursemology\\/"},"modified":"2022-07-12T20:39:09","modified_gmt":"2022-07-12T12:39:09","slug":"coursemology","status":"publish","type":"employer","link":"https:\\/\\/coursemology.sg\\/jobs\\/employer\\/coursemology\\/","title":{"rendered":"coursemology"},"content":{"rendered":"","protected":false},"featured_media":0,"comment_status":"open","ping_status":"closed","template":"","employer_category":[],"employer_location":[],"metas":{"_employer_featured_image":"","_employer_cover_photo":"","_employer_email":"ZLIEW005@e.ntu.edu.sg","_employer_phone":"","_employer_website":"","_employer_founded_date":"","_employer_company_size":"","_employer_category":[],"_employer_video_url":"","_employer_profile_url":"","_employer_profile_photos":"","_employer_team_members":"","_employer_employees":"","_employer_socials":"","_employer_location":[],"_employer_address":"","_employer_map_location":{"address":"","latitude":"","longitude":""}},"_links":{"self":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/employer\\/8052"}],"collection":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/employer"}],"about":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/types\\/employer"}],"replies":[{"embeddable":true,"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/comments?post=8052"}],"wp:attachment":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/media?parent=8052"}],"wp:term":[{"taxonomy":"employer_category","embeddable":true,"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/employer_category?post=8052"},{"taxonomy":"employer_location","embeddable":true,"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/employer_location?post=8052"}],"curies":[{"name":"wp","href":"https:\\/\\/api.w.org\\/{rel}","templated":true}]}}]'

"""
import requests, json, base64
from datetime import datetime
import pandas as pd
from settings import WP_APP_USERNAME, WP_APP_PASSWORD
datetime_str = datetime.now().strftime("%d%m%Y")

username = WP_APP_USERNAME
password = WP_APP_PASSWORD

creds = username + ':' + password
cred_token = base64.b64encode(creds.encode())

header = {'Authorization': 'Basic ' + cred_token.decode('utf-8'),
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
          }

url = 'https://coursemology.sg/jobs/wp-json'
output_file = 'output%s.csv'%datetime_str

"""
df = pd.read_csv(output_file)
i = 0
try:
    for row in df.iterrows():
        title = df.iloc[i]['job_name']
        if df.iloc[i]['job_type'] == 'Full-Time' or 'Full Time' or 'Full time':
            job_listing_type = 66
        elif df.iloc[i]['job_type'] == 'Part-Time' or 'Part Time' or 'Part time':
            job_listing_type = 92
        else:
            job_listing_type = 103

        salary = df.iloc[i]['salary']
        location = df.iloc[i]['location']
        image = df.iloc[i]['image']
        content = df.iloc[i]['content']
        post = {
                "title":title,
                #'content': content,
                'status': 'publish',
                'categories': 5,
                'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "type": "job_listing",
                "job_listing_type": [job_listing_type],
                #"134":"Security"
                "job_listing_category": [134],
                #"135":"East", '136':'North','137':'South','138':'West','139':'Central'
                "job_listing_location": [135],
                # NOT WORKING
                "metas": {
                "_job_salary": salary,
                "_job_photos": {"2482": image},
                "_job_address": location,}
                }

        #res = requests.post(url + '/wp/v2/job_listing/7066?_locale=user' , headers=header , json=post)
        i+=1
except FileNotFoundError:
    print('Run scraper.scrape(), scraper.save_as_csv(), and scraper.merge_csv() first')


post = {
    "title":'hello there',
    #'content': content,
    'status': 'publish',
    'categories': 5,
    'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "type": "job_listing",
    "job_listing_type": [103],
    #"134":"Security"
    "job_listing_category": [134],
    #"135":"East", '136':'North','137':'South','138':'West','139':'Central', '147':'Singapore'
    "job_listing_location": [135],
    "metas": {
    "_job_salary": '2700',
    "_job_photos": {"2482": '202011/402c0762-e57a-49a5-b1f9-12107f22226d.png'},
    "_job_address": 'Orchard'}
}



res = requests.post(url + '/wp/v2/employer' , headers=header , json=post)

print(res)
"""
post = {
    "_employer_title": 'Coursemology',
    "_employer_featured_image": 'coursemology_logo.png'
    }
#res = requests.post(url + '/wp/v2/employer' , headers=header , json=post)

#print(res)
types = requests.get('https://coursemology.sg/jobs/wp-json/wp/v2/jobs/')
print(types.content)


"""

"metas":{"_job_category":{"52":"Design","60":"Development"},"_job_type":{"66":"Full Time"},
    "_job_salary":"$151 - $180 \\/ week",
    "_job_photos":{"2482":"https:\\/\\/www.demoapus-wp1.com\\/superio-import2\\/wp-content\\/uploads\\/2021\\/04\\/blog6.jpg"},
    "_job_address":"102 Hicks St, Brooklyn, NY","_job_location":{"85":"New York"},}
    
{"id":4540,
"slug":"junior-graphic-designer-web","status":"publish","link":"https:\\/\\/coursemology.sg\\/jobs\\/job\\
/junior-graphic-designer-web\\/","title":{"rendered":"Junior Graphic Designer (Web)"},"content":{"rendered":"<div class=\\"space-b-50\\
">As a Product Designer, you will work within a Product Delivery Team fused with UX, engineering, product and data talent. 
You will help the team design beautiful interfaces that solve business challenges for our clients. We work with a number
 of Tier 1 banks on building web-based applications for AML, KYC and Sanctions List management workflows. This role is ideal
  if you are looking to segue your career into the FinTech or Big Data arenas.<\\/div>\\n<h3 class=\\"title\\">Key Responsibilities<
  \\/h3>\\n<ul class=\\"list-circle space-b-50\\">\\n<li>Be involved in every step of the product design cycle from discovery to developer
   handoff and user acceptance testing.<\\/li>\\n<li>Work with BAs, product managers and tech teams to lead the Product Design<\\/li>\\
   n<li>Maintain quality of the design process and ensure that when designs are translated into code they accurately reflect the design 
   specifications.<\\/li>\\n<li>Accurately estimate design tickets during planning sessions.<\\/li>\\n<li>
   Contribute to sketching sessions involving non-designersCreate, iterate and maintain UI deliverables including sketch files, style guides,
    high fidelity prototypes, micro interaction specifications and pattern libraries.<\\/li>\\n<li>Ensure design choices are
     data led by identifying assumptions to test each sprint, and work with the analysts in your team to plan moderated usability test sessions.
     <\\/li>\\n<li>Design pixel perfect responsive UI\\u2019s and understand that adopting common interface patterns is better 
     for UX than reinventing the wheel<\\/li>\\n<li>Present your work to the wider business at Show &amp; Tell sessions.
     <\\/li>\\n<\\/ul>\\n<h3 class=\\"title\\">Skill &amp; Experience<\\/h3>\\n<ul class=\\"list-circle\\">\\n<li>You have 
     at least 3 years\\u2019 experience working as a Product Designer.<\\/li>\\n<li>You have experience using Sketch and 
     InVision or Framer X<\\/li>\\n<li>You have some previous experience working in an agile environment \\u2013 Think 
     two-week sprints.<\\/li>\\n<li>You are familiar using Jira and Confluence in your workflow<\\/li>\\n<\\/ul>\\n",
     "protected":false},
     "job_listing_type":[66],"job_listing_category":[52,60],"job_listing_location":[85],
     "metas":{"_job_featured_image":"","_job_category":{"52":"Design","60":"Development"},"_job_type":{"66":"Full Time"},
   "_job_gender":"Both",
     "_job_apply_url":"themeforest.net","_job_apply_email":"example@apus.com","_job_salary_type":"weekly",
     "_job_salary":"$151 - $180 \\/ week","_job_experience":"4 Year","_job_career_level":"Officer","_job_qualification":"Bachelor Degree",
     "_job_video_url":"https:\\/\\/www.youtube.com\\/watch?v=7e90gBu4pas","_job_photos":{"2482":"https:\\/\\/www.demoapus-wp1.com\\
     /superio-import2\\/wp-content\\/uploads\\/2021\\/04\\/blog6.jpg","2481":"https:\\/\\/www.demoapus-wp1.com\\/superio-import2\\
     /wp-content\\/uploads\\/2021\\/04\\/blog5.jpg","2480":"https:\\/\\/www.demoapus-wp1.com\\/superio-import2\\/wp-content\\
     /uploads\\/2021\\/04\\/blog4.jpg","2479":"https:\\/\\/www.demoapus-wp1.com\\/superio-import2\\/wp-content\\/uploads\\
     /2021\\/04\\/blog3.jpg","2478":"https:\\/\\/www.demoapus-wp1.com\\/superio-import2\\/wp-content\\/uploads\\/2021\\/04\\
     /blog2.jpg","2477":"https:\\/\\/www.demoapus-wp1.com\\/superio-import2\\/wp-content\\/uploads\\/2021\\/04\\/blog1.jpg"},
     "_job_application_deadline_date":"05\\/18\\/2026","_job_address":"102 Hicks St, Brooklyn, NY","_job_location":{"85":"New York"},
     "_job_map_location":{"address":"102 Hicks St, Brooklyn, NY","latitude":"40.69865478041131","longitude":"-73.99426069264436"},
     "custom-text-28357132":"","custom-textarea-29836138":"","custom-wysiwyg-30244579":"","custom-date-31151308":"",
     "custom-number-32635225":"","custom-url-33890532":"","custom-email-34940612":""},"_links":{"self":[{"href":"https:\\/\\/coursemology.sg
     \\/jobs\\/wp-json\\/wp\\/v2\\/job_listing\\/4540"}],"collection":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\
     /wp\\/v2\\/job_listing"}],"about":[{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/types\\/job_listing"}],
     "author":[{"embeddable":true,"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/users\\/2"}],"replies":
     [{"embeddable":true,"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/comments?post=4540"}],"wp:attachment":
     [{"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/media?parent=4540"}],"wp:term":[{"taxonomy":"job_listing_type"
     ,"embeddable":true,"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/job_listing_type?post=4540"},
     {"taxonomy":"job_listing_category","embeddable":true,"href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\
     /job_listing_category?post=4540"},{"taxonomy":"job_listing_location","embeddable":true,"href":"https:\\/\\/coursemology.sg
     \\/jobs\\/wp-json\\/wp\\/v2\\/job_listing_location?post=4540"},{"taxonomy":"job_listing_tag","embeddable":true,
     "href":"https:\\/\\/coursemology.sg\\/jobs\\/wp-json\\/wp\\/v2\\/job_listing_tag?post=4540"}],"curies":[{"name":"wp",
     "href":"https:\\/\\/api.w.org\\/{rel}","templated":true}]}}

"""