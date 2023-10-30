/*markdown
# Database setup for DevContainer
*/

CREATE TABLE Articles (
    URLId text,
    Headline text,
    Contents text,
    Authors text,
    UploadDate text,
    ReadTime text,
    ImageURL text,
    ImageDescription text
);

DELETE FROM Articles;
