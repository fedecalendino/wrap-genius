from genius.scrapper import get_followers


def lazy_property(prop):
    @property
    def wrapper(*args):
        self = args[0]
        if not self._fully_loaded_:
            self.__fetch_extra_data__()
            self._fully_loaded_ = True
        return prop(self)
    return wrapper


class SocialMedia:
    """
    Attributes
    ----------
    followers: int
        Amount of followers in the network.
    handle: str
        username in the network.
    network: str
        social media network (facebook, instagram, twitter, etc).
    url: str
        url in the network.
    """

    _fully_loaded_: bool = False

    def __init__(self, network, handle):
        self.handle = handle
        self.network = network
        self.__followers = 0

    def __fetch_extra_data__(self):
        self.__followers = get_followers(self.url, self.handle)

    @property
    def url(self):
        return f"https://{self.network}.com/{self.handle}"

    @lazy_property
    def followers(self) -> int:
        return self.__followers

    def __repr__(self):  # pragma: no cover
        return self.url
