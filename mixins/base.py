from collections import deque
from urllib.parse import urljoin, urlparse

import requests


class Base:

    URLS = {
        'internal': set(),
        'external': set(),
        'visited': set(),
        'not_visited': deque([])
    }

    def __init__(self, url, threads, headers):
        self.base = url
        self.threads = threads
        self.headers = self.__get_headers(headers)
        self.domain = self.__get_domain(url)
        self._add_not_visited(url)

    def __get_domain(self, url):
        domain = [urlparse(url).netloc]
        if domain[0].startswith('www.'):
            domain.append(domain[0][4:])
        else:
            domain.append('www.' + domain[0])
        return domain

    def __get_headers(self, headers):
        if headers:
            return {
                k.strip(): v.strip() for k, v in (
                    h.split(':') for h in headers.split(','))}

    def _add_not_visited(self, url):
        if (
            url and url not in self.URLS['visited']
                and url not in self.URLS['not_visited']):
            self.URLS['not_visited'].append(url)

    def _add_visited(self):
        url = self.URLS['not_visited'].popleft()
        self.URLS['visited'].add(url)
        if urlparse(url).netloc in self.domain:
            self.URLS['internal'].add(url)
        else:
            self.URLS['external'].add(url)
        return url

    def _get_page_source(self, url):
        return requests.get(
            url, headers=self.headers).text  # , verify=False if needed

    def _process_path(self, url, path):
        if path.startswith('http'):
            return path
        path = urljoin(url, path)
        return path
