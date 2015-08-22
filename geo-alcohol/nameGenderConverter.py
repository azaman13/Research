"""
Author: Anis Zaman
"""

import argparse
import re
import requests

from bs4 import BeautifulSoup
from genderize import Genderize

def get_gender_using_genderize_api(name):
    """
    :param a string, ideally the first name
    :returns a dictionary of name, gender, % accuracy
    Description:Given a name as a string, this function returns a dic with the
    possible gender
    NOTE: This uses the genderize api
    """
    if name:
        return Genderize().get(name)


def get_gender_using_behind_name_api(name):
    """
    :param a string, ideally the first name
    :returns
    Description:Given a name as a string, this function returns a dic with the
    possible gender
    NOTE: This uses the dictionary from the behind the name api, an open source
    api
    """
    resource_url = "http://www.behindthename.com/api/lookup.php"
    payload = {'key':'an224521'}
    if name:
        payload['name'] = name
        response = requests.get(resource_url, params=payload)
        content = BeautifulSoup(response.content, 'xml')
        name_details = content.find_all('name_detail')
        gender = re.sub(r'</gender>',
                        "",
                        re.sub(r'<gender>',"",str(name_details[0].find('gender')))
                        )
        if gender == 'm':
            return 'male'
        elif gender == 'f':
            return 'female'
        elif gender == 'mf':
            return 'male/female'
        else:
            return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Name to gender converter')
    parser.add_argument(
        '-n','--name', help='Preferably the first name of the person',
        required=True

    )
    args = vars(parser.parse_args())
    if args.get('name'):
        # result = get_gender_using_genderize_api([args.get('name')])
        result = get_gender_using_behind_name_api([args.get('name')])
        print(result)
