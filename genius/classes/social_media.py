class SocialMedia:
    """
    Attributes
    ----------
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

    @property
    def url(self):
        return f"https://{self.network}.com/{self.handle}"

    def __repr__(self):  # pragma: no cover
        return self.url
