import re
import sqlite3
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from utils.db import insert_course, insert_prereq, insert_student, insert_completed_course, get_eligible_courses
from utils.models import Course, Major, Student

def fetch_webpage(url):
    """gets beautifulSoup object of specified webpage"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # print(f"Successfully fetched webpage")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Failed to fetch webpage. HTTP Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error occurred while fetching webpage: {e}")
        return None
    
def scrape_courses(major):
    """scrapes courses from university bulletin"""

    url = f"https://catalog.stonybrook.edu/content.php?filter%5B27%5D={major}&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=7&expand=&navoid=225&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter"

    soup = fetch_webpage(url)

    if soup:
        td = soup.find('td', class_='block_content')
        if td:
            tables = td.find_all('table', class_='table_default', recursive=False)
            if len(tables) > 1:
                table = tables[1]
            else:
                raise
        else:
            raise

        courses = table.find_all('tr')

        if courses:
            major_courses = []
        else:
            major_courses = None


        for course in courses:
            a = course.find('a')
            if a and 'href' in a.attrs:
                soup2 = fetch_webpage('https://catalog.stonybrook.edu/'+a['href'])

                if soup2:
                    c_obj = scrape_course('major', soup2)

                    if c_obj:
                        major_courses.append(c_obj)

        return major_courses if major_courses else None

def scrape_course(major, soup):
    """helper to scrape individual course link"""

    td = soup.find('td', class_='block_content')
    if td:
        # for i, item in enumerate(td.contents[3]):
        #     print(f'{i}: {item}')

        tags = td.contents[3]
        blob = [el if isinstance(el, Tag) else str(el).strip() for el in tags.contents]
        h1 = blob[0].text
        description = blob[2]

        strongs = tags.find_all('strong')
        credits = int(strongs[0].text[0])

        prereqs = []
        for strong in strongs[1:]:
            if 'Prerequisite' in strong.text:
                s = ''
                
                for i,sib in enumerate(strong.next_siblings):
                    if isinstance(sib, Tag):
                        s += sib.text.strip().replace(' ', '')
                    else:
                        s += ' ' + sib.strip() + ' '

                s = s.split(';')
                s = [item.strip() for item in s]

                for req in s:
                    matches = re.findall(r'[A-Z]{3}[0-9]{3}', req)
                    if matches:
                        # if len(matches) == 1:
                        #     prereqs.append(matches[0])
                        # else:
                        prereqs.append(matches)

                break

            # TODO: parse antirequisites (rare)
            elif 'Anti' in strong.text:
                pass

        course_code = h1[:3] + h1[4:7]
        title = h1[10:]

        course = Course(course_code, title, description, credits, prereqs if prereqs else None)
        # print(course)

        return course
    return None

def test_scrape_course():
    """test for scrape_course"""
    soup = fetch_webpage('https://catalog.stonybrook.edu/preview_course_nopop.php?catoid=7&coid=5795')
    print(scrape_course('CSE', soup))

def insert_major_data(major):
    courses = scrape_courses(major)

    conn = sqlite3.connect("data/new_sbu.db") # if cd is backend
    cur = conn.cursor()

    cur.connection.row_factory = sqlite3.Row

    for course in courses:
        insert_course(cur, course)
        prereqs = course.prerequisites
        if prereqs:
            i = 0
            for req in prereqs:
                for req_op in req:
                    insert_prereq(cur, course.code, req_op, i)
                i += 1
        print(course.code)

    conn.commit()
    conn.close()

def insert_cc_data(cur):
    insert_completed_course(cur, 1, 'CSE101')
    insert_completed_course(cur, 1, 'CSE114')
    insert_completed_course(cur, 1, 'CSE214')
    insert_completed_course(cur, 1, 'CSE215')
    insert_completed_course(cur, 1, 'CSE216')
    insert_completed_course(cur, 1, 'CSE220')

if __name__ == "__main__":
    # insert_cse_data()
    # test_scrape_course()
    # db_test()
    # insert_major_data('AMS')
    pass