#!/usr/bin/env python3
from collections import deque
import re
from urllib.parse import unquote
import sys
import asyncio
import time

try:
    import httpx
except ModuleNotFoundError:
    import pip
    pip.main(['install', '--quiet', 'httpx'])
    import httpx

# 1) Поставить aiohttp/ httpx
# 2) Взять д/з 3 из прошлого семестра («философия»)
# 3) Нужно переделать в асинхронный с использованием aiohttp/httpx, сделать бенчмарки

def equals(a, b):
    return a.replace('_', ' ').lower() == b.replace('_', ' ').lower()


MAX_REQUESTS = 500
MAX_DEPTH = 7
MAX_ASYNCS_COUNT = 10


async def get_content(client, name):
    name = name.replace(' ', '_')
    url = f'https://ru.wikipedia.org/wiki/{name}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 '
                      '(contact: 111solovyovadasha111@gmail.com)',
        'Accept-Language': 'ru,en;q=0.9',
    }
    try:
        response = await client.get(url, headers=headers, follow_redirects=True, timeout=15.0)
        response.raise_for_status()
        return response.text
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        return None


def extract_content(page):
    if not page:
        return 0, 0
    start = page.find('id="mw-content-text"')
    end = page.find('id="catlinks"', start)
    if start == -1:
        return 0, 0
    if end == -1:
        return start, len(page)
    return start, end


def extract_links(page):
    links = set()

    pattern = r'href=["\']([^"\']+)["\']'
    matches = re.findall(pattern, page, flags=re.IGNORECASE)

    for href in matches:
        name = None

        if '/wiki/' in href:
            name = href.split('/wiki/')[-1]
        elif href.startswith('./'):
            name = href[2:]

        if name is None:
            continue

        if ":" in name:
            continue

        clean_name = name.split('#')[0].split('?')[0]

        if clean_name:
            links.add(unquote(clean_name))

    return links


async def find_chain(start, finish):
    if equals(start, finish):
        return [start]

    async with httpx.AsyncClient() as client:
        page = await get_content(client, start)
        if not page:
            return None

        queue = deque()
        queue.append((start, [start]))
        visited_links = {start.lower().replace('_', ' ')}
        requests_count = 1

        while queue and requests_count < MAX_REQUESTS:
            pages = []
            while queue and len(pages) < MAX_ASYNCS_COUNT:
                pages.append(queue.popleft())

            tasks = []
            for this_page, path in queue:
                if len(path) == 1:
                    tasks.append(asyncio.sleep(0, result=page))
                else:
                    tasks.append(get_content(client, this_page))
            contents = await asyncio.gather(*tasks)

            for this_page, path, content in zip(pages, contents):
                if len(path) > MAX_DEPTH or not content:
                    continue

                page_start, page_end = extract_content(content)
                if page_start == 0 and page_end == 0:
                    continue

                links = extract_links(content[page_start:page_end])

                for link in links:
                    if equals(link, finish):
                        result = path + [link]
                        return result

                    good_link = link.lower().replace('_', ' ')

                    if good_link not in visited_links:
                        visited_links.add(good_link)
                        queue.append((link, path + [link]))

        return None


async def main():
    if len(sys.argv) < 2:
        return

    start = sys.argv[1]
    end = "Философия"
    path = await find_chain(start, end)

    if path:
        for link in path:
            print(link)
    else:
        print('Цепочка не найдена', file=sys.stderr)





if __name__ == '__main__':
    asyncio.run(main())