/*markdown
 # Database setup for DevContainer
 */

CREATE TABLE Articles (
    URLId text PRIMARY KEY,
    Headline text,
    Contents text,
    Authors text,
    UploadDate text,
    ReadTime text,
    ImageURL text,
    ImageDescription text
);
