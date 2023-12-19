import pandas as pd

 # upload_timestamp changed to uploadtimestamp
class Article():
    def __init__(self,
                 urlId: str,
                 headline: str | None,
                 content: str | None,
                 authors: list[str] | None,
                 upload_timestamp: pd.Timestamp | None,
                 imageURL: str | None,
                 imageDescription: str | None,
                 scrapingTimestamp: pd.Timestamp,
                 source: str | None,
                 topic: str | None):
        self.urlId: str = urlId
        self.headline: str | None = headline
        self.content: str | None = content
        self.authors: list[str] | None = authors
        self.uploadtimestamp: pd.Timestamp | None = upload_timestamp
        self.imageURL: str | None = imageURL
        self.imageDescription: str | None = imageDescription
        self.scrapingTimestamp: pd.Timestamp = scrapingTimestamp
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
        dataFrame["uploadtimestamp"] = self.upload_timestamp
        dataFrame["imageURL"] = self.imageURL
        dataFrame["imageDescription"] = self.imageDescription
        dataFrame["scrapingTimestamp"] = self.scrapingTimestamp
        dataFrame["source"] = self.source
        dataFrame["topic"] = self.topic

        return dataFrame
