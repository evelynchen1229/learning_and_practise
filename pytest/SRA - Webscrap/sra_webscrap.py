import requests
import json
import cx_Oracle
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import logging

logging.basicConfig(filename='log.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level='INFO')
logging.info('Code Started')

class ScrapSRA:

    def __init__(self):
        self.target_username = ''
        self.target_password = ''
        self.target_host = ''
        self.target_connection = ''
        self.sra_organisations = []
        self.base_url='https://www.sra.org.uk/consumers/register/organisation/?sraNumber='
        self._database_connection()
        self.data ={
            'sra_numbers': [],
           # 'organisation': [],
            'sol_sra_number': [],
            'sol_role': [],
            'sol_name': [],
           # 'sra_regulation': [],
            'sol_works_at': [],
            'sol_sub_role': []
            }

    def _database_connection(self):
        with open('config.json') as f:
            config_data = json.load(f)
        
        self.target_username = config_data['target_connection']['username']
        self.target_password = config_data['target_connection']['password']
        self.target_host = config_data['target_connection']['host']

        self.target_connection = cx_Oracle.connect(self.target_username, self.target_password, self.target_host)
    
    def fetch_sra_organisations(self):
        cursor = self.target_connection.cursor()
        self.sra_organisations = cursor.execute("select sranumber from pdl.sra_practice where webscraped_sol_flg is null and sys_current_flg='Y'").fetchall()
        cursor.close()

    def download_sites(self):
        count=0
        with requests.Session() as session:
            for rec in self.sra_organisations:
                start_time = time.time()
                self.download_site(self.base_url + str(rec[0]), session, rec[0])
                count+=1
                print(f'Count: {count}, SRA: {rec[0]}')
                duration = time.time() - start_time
                logging.info(f'Duration per practice {rec[0]} {duration}')
            
    def save_solicitor_data(self, table_rows, sra_num, practice_closure_dt):

        df = pd.DataFrame(self.data)
        
        for tr in table_rows:
            href = tr.find('a').attrs['href']
            sra_idx = href.find('sraNumber=')
            sol_sra_number = href[sra_idx + len('sraNumber='):]
            name = tr.find('h2').text
            role = tr.find('p').text.strip()
            sol_works_at = tr.find('p', {'class': 'label__sm__block__location'}).get_text()
            sol_works_at = re.sub('\s+',' ',sol_works_at).replace('Works at','').strip()
            
            try:
                sol_sub_role = tr.find('p', {'label__sm__block__subline__neutral-no-icon'}).get_text()
            except AttributeError:
                sol_sub_role=''
            
            df = df.append(pd.Series([sra_num, sol_sra_number, role, name,sol_works_at,sol_sub_role], index=df.columns), ignore_index=True)

        # df['organisation'] = df['organisation'].apply(lambda x: str(x).encode("ascii", "replace").decode("utf-8"))
        df['sol_works_at'] = df['sol_works_at'].apply(lambda x: str(x).encode("ascii", "replace").decode("utf-8"))
        df['sol_name'] = df['sol_name'].apply(lambda x: str(x).encode("ascii", "replace").decode("utf-8"))

        insert_fields = '(PRAC_SRANUMBER, SOL_SRANUMBER, SOL_ROLE, SOL_NAME, SOL_WORKSAT, SOL_SUB_ROLE)'
        insert_values = '(:1, :2, :3, :4, :5, :6)'
        rows_to_insert = list(map(tuple, df[['sra_numbers','sol_sra_number','sol_role','sol_name','sol_works_at','sol_sub_role']].to_numpy(dtype=object)))

        cursor = self.target_connection.cursor()
        cursor.execute(f"update pdl.sra_solicitor set sys_current_flg='N' where prac_sranumber ={sra_num} and (sys_current_flg='Y' or sys_current_flg is null)")
        cursor.close()
        self.target_connection.commit()
        
        cursor = self.target_connection.cursor()
        cursor.executemany("insert into pdl.sra_solicitor" + insert_fields + " values " + insert_values
                ,rows_to_insert)
        cursor.close()
        self.target_connection.commit()

        cursor = self.target_connection.cursor()
        cursor.execute(f"update pdl.sra_solicitor set sys_current_flg='Y', sys_loaded_dt=sysdate where sys_current_flg is null and prac_sranumber ={sra_num}")
        cursor.close()
        self.target_connection.commit()
        
        cursor = self.target_connection.cursor()
        cursor.execute(f"update pdl.sra_practice set webscraped_sol_flg = 'Y',webscraped_sol_dt = sysdate, webscraped_prac_close_dt = '{practice_closure_dt}' where sranumber = {sra_num} and sys_current_flg='Y'")
        cursor.close()
        self.target_connection.commit()
        
    
    def download_site(self, url, session, sra_num):
        with session.get(url) as response:
            home_soup = BeautifulSoup(response.content)
            show_more = home_soup.find('div', {'class': 'lookup__search__result__listctrl__btn'})
            table_rows = []

            if show_more is None:
                try:
                    table_rows = home_soup.find('ul', {'class': 'lookup__person__result__list'}).findAll('li')
                except AttributeError:
                    table_rows = []
            else:
                try:
                    num_people = str(home_soup.find('div',{'id':'headingPracticePeople'}).find('span').string)[1:-1] # e.g.: returns 360 instead of (360)
                except AttributeError:
                    num_people=0
                people_page = session.get(f'https://www.sra.org.uk/consumers/register/organisation/GetPeople/?numberOfResults={num_people}',allow_redirects=True)
                people_soup = BeautifulSoup(people_page.content)
                table_rows = people_soup.find('ul', {'class': 'lookup__person__result__list'}).findAll('li')

            try:
                practice_closure_dt = home_soup.find('a',{'class': 'h5 h2-no-border detail collapsed'}).get_text()
                practice_closure_dt = re.sub('\s+',' ',practice_closure_dt).replace('Closure Date:','').strip()
                practice_closure_dt = str(practice_closure_dt)
            except AttributeError:
                practice_closure_dt = ''
            
            
            self.save_solicitor_data(table_rows, sra_num, practice_closure_dt)
            

    def close_database_connection(self):
        self.target_connection.close()
        logging.info('Code Finished')
    




if __name__ == '__main__':
    start_time = time.time()
    scrap = ScrapSRA()
    scrap.fetch_sra_organisations()
    scrap.download_sites()
    scrap.close_database_connection()
    duration = time.time() - start_time
    print(f'Process took {duration}')
    logging.info(f'Process took {duration}')


