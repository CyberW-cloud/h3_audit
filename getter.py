import requests as r


class Getter:
    def __init__(self):
        pass

    def work(self, url_list):
        """
        :return: list(dict(status_code, html))
        """
        result = self._get_html(url_list)
        return result

    def _get_html(self, url_list):
        """
        :return: list(dict(url, status_code, html))
        """
        result = list()

        session = r.Session()
        headers = {'user-agent':
                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) '
                       'Gecko/20100101 Firefox/80.0'}
        for url in url_list:
            custom_status = 0
            try:
                response = session.get(url, headers=headers)
            except r.exceptions.ConnectionError as e:
                custom_status = 1001
            except r.exceptions.Timeout as e:
                custom_status = 1002
            except Exception as e:
                custom_status = 1013
            finally:
                url_result = {
                    'url': url,
                    'status_code': custom_status if custom_status
                    else response.status_code,
                    'html': '' if custom_status else response.text
                }
                result.append(url_result)

        return result


if __name__ == '__main__':
    getter = Getter()
    res = getter.work('https://nv.ua/')
    print(res)