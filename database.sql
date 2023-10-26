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

INSERT INTO Persons VALUES (3, 'hi', 'moiun', 'hu', 'sad');

select * from persons