import asyncio
import aiohttp


async def main():
    urls = [
        'http://httpbin.org/cookies/set?test=ok',
        'http://127.0.0.1:9999/ui/student/264',
    ]
    for url in urls:
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as s:
            async with s.get(url) as r:
                print('JSON', await r.json())
                cookies = s.cookie_jar.filter_cookies('http://httpbin.org')
                for key, cookie in cookies.items():
                    print('Key: "%s", Value: "%s"' % (cookie.key, cookie.value))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())