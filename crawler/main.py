# -*- coding: utf-8 -*-
import sys
import time
import urllib.request
import concurrent.futures


def fetch_url(url):
    t1 = time.time()
    with urllib.request.urlopen(url) as f:
        tt = time.time() - t1
        data = f.read(320).decode('utf-8')[:80]
        msg = """\n url: {url}\n time taken: {tt:3g}s url\n first 80 characters: {data}
              """.format(url=url,
                         tt=tt, data=data)
        return msg


def fetch_urls(urls, threads):
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=threads) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                msg = future.result()
                print(msg)
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))


def get_max_threads(max, threshold=50):
    # To get better perfomance scaling up
    # no of threads with no of url wont help
    if max < threshold:
        return max
    else:
        return threshold


# fetch urls by sending in batches.
start = time.time()
batch = []
max_batch = 30
threads = get_max_threads(max_batch)

with open(sys.argv[1], 'r', encoding='utf8') as file:
    for url in file:
        url = url.strip()
        batch.append(url)
        if len(batch) == max_batch:
            fetch_urls(batch, threads)
            batch = []
    if batch:
        fetch_urls(batch, threads)

print('total time taken:{0:5g}'.format(time.time() - start))
