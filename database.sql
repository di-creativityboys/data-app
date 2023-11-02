/*markdown
# Database setup for DevContainer
*/

CREATE TABLE Articles (
    URLId text Constraint primary_key Primary Key,
    Headline text,
    Contents text,
    Authors text,
    UploadDate text,
    ReadTime text,
    ImageURL text,
    ImageDescription text,
    ScrapingTimeStamp text
);