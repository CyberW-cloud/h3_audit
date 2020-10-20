from bs4 import BeautifulSoup
import re


class Extractor:
    """
    Designed for extraction tags in self.tag_dict from HTML
    """

    def __init__(self):
        self.tag_dict = {'title': 'title',
                         'description': {'name': 'description'},
                         'keywords': {'name': 'keywords'},
                         'h1': 'h1',
                         'h2': 'h2',
                         'h3': 'h3',
                         'a': 'a'}

    def work(self, raw_html, base_url):
        """
        Collects all node lists to dict
        :return:dict(list(str))
        """
        soup = BeautifulSoup(raw_html, "html.parser")
        result = dict()
        for tag, tag_value in self.tag_dict.items():
            extract_tags = soup.find_all(tag_value)
            if extract_tags:
                if tag == 'a':
                    result[tag] = self._clear_a(extract_tags, base_url)
                else:
                    result[tag] = [item.getText() for item in extract_tags]
            else:
                extract_tags = soup.find_all('meta', attrs=tag_value)
                result[tag] = [item.get('content') for item in extract_tags]
        return result

    def _clear_a(self, a_list, base_url):
        unique_a = set()
        # whitelist = ['/', './', 'https://', 'http://']
        pattern = '(^\.\/)|(^\/(?!\/))|(^http:\/\/(?!\/)|https:\/\/(?!\/))|(^w{3}\.)'
        for tag in a_list:
            href = tag.get('href')
            check = re.match(pattern, href)
            if check:
                if check.groups():
                    url = tag.get('href')
                    if not any((url.startswith('www'), url.startswith('http'))):
                        # TODO: add case when url starts with ./
                        url = f'{base_url}{url}'
                    unique_a.add(url)
        return unique_a


if __name__ == "__main__":
    import requests
    headers = {'user-agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    response = requests.get('https://www.python.org', headers=headers)
    # print(response.text)
    extractor = Extractor()
    print(extractor.work(response.text, 'https://www.python.org'))
