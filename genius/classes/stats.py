from .commons import Base


class Stats(Base):
    def __init__(self, genius, data):
        super().__init__(genius)

        self.concurrents: int = data.get("concurrents", 0)
        self.hot: bool = data.get("hot", False)
        self.pageviews: int = data.get("pageviews", 0)
        self.unreviewed_annotations: int = data.get("unreviewed_annotations", 0)
