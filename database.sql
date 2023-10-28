/*markdown
# Database setup for DevContainer
*/

CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);

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