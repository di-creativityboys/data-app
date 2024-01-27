import pandas as pd


class Article:
    def __init__(
        self,
        urlId: str,
        headline: str | None,
        content: str | None,
        authors: list[str] | None,
        upload_timestamp: pd.Timestamp | None,
        image_url: str | None,
        image_description: str | None,
        scraping_timestamp: pd.Timestamp,
        source: str | None,
        topic: str | None,
    ):
        self.urlId: str = urlId
        self.headline: str | None = headline
        self.content: str | None = content
        self.authors: list[str] | None = authors
        self.upload_timestamp: pd.Timestamp | None = upload_timestamp
        self.image_url: str | None = image_url
        self.image_description: str | None = image_description
        self.scraping_timestamp: pd.Timestamp = scraping_timestamp
        self.source: str | None = source
        self.topic: str | None = topic

    def __str__(self):
        return f"{self.headline}"

    def to_dataFrame(self) -> pd.DataFrame:
        dataFrame = pd.DataFrame()

        dataFrame["urlId"] = self.urlId
        dataFrame["headline"] = self.headline
        dataFrame["content"] = self.content
        dataFrame["authors"] = self.authors
        dataFrame["upload_timestamp"] = self.upload_timestamp
        dataFrame["imageURL"] = self.image_url
        dataFrame["imageDescription"] = self.image_description
        dataFrame["scrapingTimestamp"] = self.scraping_timestamp
        dataFrame["source"] = self.source
        dataFrame["topic"] = self.topic

        return dataFrame
