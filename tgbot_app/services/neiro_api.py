class Midjourney:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.url = "https://api.нейросети.com/midjourney/"


class OpenAI:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.url = "https://api.нейросети.com/openai/"


class StableDiffusion:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.url = "https://api.нейросети.com/stablediffusion/"


class Gemini:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.url = "https://api.нейросети.com/bard/"


class Claude:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.url = "https://api.нейросети.com/claude/"


class Yandex:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.url = "https://api.нейросети.com/yandex/"



