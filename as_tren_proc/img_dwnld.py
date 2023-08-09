import requests
import threading
from multiprocessing import Process, Pool
import os
import sys
import time
import asyncio
import aiofiles
from aiohttp import ClientSession


images_list = [
    'https://www.team-bhp.com/sites/default/files/styles/check_extra_large_for_review/public/shelby-mustang-hertz-rental-1.jpg',
    'https://autotuning-bmw.ru/uploads/carousel/66/38bf34c1c92b8f4420e81b9259f35097.jpg',
    'https://www.allcarz.ru/wp-content/uploads/2020/01/foto-mansory-carbonado-price_01.jpg',
    'https://a.d-cd.net/e80f78es-960.jpg',
    'https://p.turbosquid.com/ts-thumb/CM/I3VlaX/uY9EMZmk/hotrod9/jpg/1275815089/1920x1080/fit_q99/1a7b617a385c846d917a0a3cdcf9dbc554e583cf/hotrod9.jpg'
]

# --------------------------------------------------------------------------------------

def download(url, dir_name):
    start = time.time()
    response = requests.get(url)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    _, file_name = url.rsplit('/', 1)
    full_name = dir_name + '/' + file_name
    with open(full_name, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {file_name} in {time.time()-start:.2f} seconds")

def main_code_tr(urls=images_list):
    threads = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=download, args=[url, 'img_thrd'])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f'Общее время: {time.time() - start_time:.2f} seconds\n')

# -------------------------------------------------------------------

def main_code_pr(urls=images_list):
    processes = []
    start_time = time.time()
    for url in urls:
        process = Process(target=download, args=[url, 'img_proc'])
        processes.append(process)
        process.start()
    for proc in processes:
        proc.join()
    print(f'Общее время: {time.time() - start_time:.2f} seconds\n')

# -------------------------------------------------------------------

async def as_download(session, url, dir_name):
    start = time.time()
    resp = await session.request(method="GET", url=url)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    _, file_name = url.rsplit('/', 1)
    full_name = dir_name + '/' + file_name
    async with aiofiles.open(full_name, "wb") as f:
        await f.write(await resp.read())
    print(f"Downloaded {file_name} in {time.time()-start:.2f} seconds")

async def main_code_as(urls=images_list):
    start_time = time.time()
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                as_download(session, url, 'img_asy')
            )
        await asyncio.gather(*tasks)
    print(f'Общее время: {time.time() - start_time:.2f} seconds\n')

# -------------------------------------------------------------------

if __name__ == '__main__':
    _, *args = sys.argv
    if args:
        main_code_tr(args)
        main_code_pr(args)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main_code_as(args))
    else:
        main_code_tr()
        main_code_pr()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main_code_as())
