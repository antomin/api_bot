from aiohttp import ClientSession

from tgbot_app.utils.enums import GenerationResult


class Translator:
    def __init__(self, token, proxy_url: str):
        self.proxy_url = proxy_url
        self.proxies_dict = {"http": proxy_url, "https": proxy_url}
        self.url = "https://nlp-translation.p.rapidapi.com/v1/translate"
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": token,
            "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com",
        }

    async def translate(self, text: str, to_: str = "en", from_: str = "ru") -> GenerationResult:
        payload = {"text": text, "to": to_, "from": from_}

        async with ClientSession(headers=self.headers) as session:
            async with session.post(url=self.url, data=payload, proxy=self.proxy_url) as response:
                if response.ok:
                    result = await response.json()
                    translation = result.get("translated_text").get(to_)
                    if not translation:
                        return GenerationResult(success=False)
                    return GenerationResult(result=translation)
                else:
                    return GenerationResult(success=False)
