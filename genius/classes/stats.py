class Stats:
    def __init__(self, api, data):
        self.api = api

        self.accepted_annotations: int = data.get("accepted_annotations", 0)
        self.concurrents: int = data.get("concurrents", 0)
        self.contributors: int = data.get("contributors", 0)
        self.hot: bool = data.get("hot", False)
        self.iq_earners: int = data.get("iq_earners", 0)
        self.pageviews: int = data.get("pageviews", 0)
        self.transcribers: int = data.get("transcribers", 0)
        self.unreviewed_annotations: int = data.get("unreviewed_annotations", 0)
        self.verified_annotations: int = data.get("verified_annotations", 0)
