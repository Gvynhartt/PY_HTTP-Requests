import requests
import time
import datetime
from pprint import pprint
from math import ceil


class StackOverflowQuery:
    QUERY_URL = 'https://api.stackexchange.com/2.3/search'
    PAGE_SIZE = 100  # максимальное число результатов, допускаемое API на странице
    TOTAL_FILTER = '!nNPvSNVZJS'  # включает фильтр, отображающий общее число результатов

    def __init__(self, nmb_days: int = 2, tag: str = 'python', nmb_page: int = 1):
        self.nmb_days = nmb_days
        self.tag = tag
        self.nmb_page = nmb_page

    def run_query(self):
        curr_time = round(time.time())  # Unix epoch time in seconds
        start_time = curr_time - (self.nmb_days * 24 * 3600)
        query_params = {}
        query_params['site'] = 'stackoverflow'
        query_params['fromdate'] = start_time
        query_params['todate'] = curr_time
        query_params['order'] = 'desc'
        query_params['sort'] = 'creation'
        query_params['tagged'] = 'python'
        query_params['filter'] = 'default'
        query_params['page'] = self.nmb_page
        query_params['pagesize'] = self.PAGE_SIZE
        query_params['filter'] = self.TOTAL_FILTER

        query = requests.get(self.QUERY_URL, params=query_params)
        res_obj = query.json()

        total_pages = ceil(res_obj['total'] / self.PAGE_SIZE)
        if (total_pages > 1) and (total_pages - self.nmb_page > 0):
            print(f'Вы находитесь на странице {self.nmb_page} из {total_pages} имеющихся; желаете продолжить поиск?')
        if total_pages - self.nmb_page == 0:
            print(
                f'Вы находитесь на последней странице из {self.nmb_page} найденных; вы нашли то, что искали (ну или смысл в жизни)?')
        return res_obj

    def show_essentials_for_questns(self, results):
        ess_list = []
        for nmb, item in enumerate(results['items']):
            question_info = {}
            question_entry = {}

            title = item['title']
            is_answered = item['is_answered']
            answers_total = item['answer_count']
            cr_time_epoch = item['creation_date']
            cr_time_human = datetime.datetime.fromtimestamp(cr_time_epoch).strftime('%Y-%m-%d %H:%M:%S')
            ts_name = item['owner']['display_name']
            ts_rep = item['owner']['reputation']
            score = item['score']
            link = item['link']

            question_info['subject'] = title
            question_info['has been answered'] = is_answered
            question_info['answers count'] = answers_total
            question_info['time created'] = cr_time_human
            question_info['asked by'] = ts_name
            question_info['askers`s reputation'] = ts_rep
            question_info['score'] = score
            question_info['link'] = link

            question_entry[nmb] = question_info
            ess_list.append(question_entry)

        pprint(ess_list)
