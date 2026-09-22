#!/usr/bin/env python3
from collections import deque
import re
from urllib.parse import unquote
import sys

try:
    import httpx
except ModuleNotFoundError:
    import pip
    pip.main(['install', '--quiet', 'httpx'])
    import httpx


def equals(a, b):
    return a.replace('_', ' ').lower() == b.replace('_', ' ').lower()


MAX_REQUESTS = 500
MAX_DEPTH = 7
DEBUG = True


def get_content(name):
    name = name.replace(' ', '_')
    url = f'https://ru.wikipedia.org/wiki/{name}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 '
                      '(contact: 111solovyovadasha111@gmail.com)',
        'Accept-Language': 'ru,en;q=0.9',
    }
    try:
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=15.0)
        if DEBUG:
            print(f'[get_content] {name!r} -> {response.status_code}', file=sys.stderr)
        response.raise_for_status()
        return response.text
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        if DEBUG:
            print(f'[get_content] {name!r} FAILED: {e}', file=sys.stderr)
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


def find_chain(start, finish):
    if equals(start, finish):
        return [start]

    page = get_content(start)
    if not page:
        return None

    queue = deque()
    queue.append((start, [start]))
    visited_links = {start.lower().replace('_', ' ')}
    requests_count = 1

    while queue and requests_count < MAX_REQUESTS:
        this_page, path = queue.popleft()

        if len(path) > MAX_DEPTH:
            continue

        if len(path) == 1:
            content = page
        else:
            content = get_content(this_page)
            requests_count += 1

        if not content:
            continue

        page_start, page_end = extract_content(content)
        if page_start == 0 and page_end == 0:
            continue

        links = extract_links(content[page_start:page_end])

        if DEBUG:
            print(f'[debug] {this_page!r}: links_found={len(links)}', file=sys.stderr)

        for link in links:
            if equals(link, finish):
                result = path + [link]
                return result

            good_link = link.lower().replace('_', ' ')

            if good_link not in visited_links:
                visited_links.add(good_link)
                queue.append((link, path + [link]))

    return None


def main():
    if len(sys.argv) < 2:
        return

    start = sys.argv[1]
    end = "Философия"
    path = find_chain(start, end)

    if path:
        for link in path:
            print(link)
    else:
        print('Цепочка не найдена', file=sys.stderr)


if __name__ == '__main__':
    main()