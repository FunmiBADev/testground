class Config:
    def __init__(self):
        self.platform_tags = [
            {"tag": "AA42557", "tag_name": "PLATFORM", "url": "https://www.platform.com"},
            {"tag": "AA34475", "tag_name": "PLATFORM_ONE", "url": "https://www.platformone.com"},
            {"tag": "AA45492", "tag_name": "PLATFORM_TWO", "url": "https://www.platformtwo.com"}
        ]
        self.apis = {
            "PLATFORM_API_LOGIN": "/api/login",
            "PLATFORM_API_PROCESS_DEFINITIONS": "/api/proc/definitions",
            "PLATFORM_API_JRE": "/api/jre/display"
        }

    def get_platform_tags(self):
        return self.platform_tags

    def get_apis(self):
        return self.apis
config = Config()
platform_tags = config.get_platform_tags()
apis = config.get_apis()

print(platform_tags)
print(apis)
