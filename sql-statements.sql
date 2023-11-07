-- 1. Adding Users
INSERT INTO User (Username, Email, Password) VALUES
    ('user7', 'user7@email.com', 'password7');
    -- ('user2', 'user2@email.com', 'password2'),
    -- ('user3', 'user3@email.com', 'password3'),
    -- ('user4', 'user4@email.com', 'password4'),
    -- ('user5', 'user5@email.com', 'password5'),
    -- ('user6', 'user6@email.com', 'password6');

-- 2. Adding Tags
INSERT INTO Tag (TagName) VALUES
    -- ('Combat'),
    -- ('VR'),
    -- ('Story Rich'),
    -- ('Adventure');

-- 3. Adding Publishers
INSERT INTO Publisher (PublisherName) VALUES
    -- ('Gaijin Distribution KFT');

-- 4. Adding Games
INSERT INTO Game (GameTitle, ReleaseDate, PublisherID) VALUES
    -- ('War Thunder', '2013-08-15', 8);

-- 5. Adding Game-Tag relations
INSERT INTO GameTag (GameID, TagID) VALUES
    -- (5, 10),
    -- (5, 2),
    -- (5, 12),
    -- (5, 9);
    -- (6, 15); 


-- 6. Adding Wishlists
INSERT INTO Wishlist (Username, GameID) VALUES
    ('user7', 10);
    -- ('user6', 6),
    -- ('user6', 7),
    -- ('user6', 8),
    -- ('user6', 9);

-- 7. Adding reviews, 0 for positive rating, 1 for negative rating
INSERT INTO Review (Username, GameID, Rating, Comment, ReviewDate) VALUES
    ('user7', 10, 1, 'Test', '2016-02-15');

-- 8. Adding Games for sale
INSERT INTO Sale (Start_Date, End_Date, GameID, DiscountPercent) VALUES
    -- ('2023-10-05', '2023-11-01', 6, 51.1),
    -- ('2023-11-10', '2023-11-18', 9, 15);
    
-- 9. Search for a game by one tag
SELECT DISTINCT Game.GameTitle
FROM Game
JOIN GameTag ON Game.GameID = GameTag.GameID
JOIN Tag ON GameTag.TagID = Tag.TagID
WHERE Tag.TagName = 'Action' OR Tag.TagName = 'FPS';

-- 10. Search for a game by multiple tags
SELECT DISTINCT Game.GameTitle
FROM Game
JOIN GameTag ON Game.GameID = GameTag.GameID
JOIN Tag ON GameTag.TagID = Tag.TagID
WHERE Tag.TagName IN ('MOBA', 'Multiplayer')
GROUP BY Game.GameID
HAVING COUNT(DISTINCT Tag.TagID) = 2;

-- 11. Edit a review for a certain user and game
UPDATE Review
SET Rating = 1, Comment = 'Update test', ReviewDate = '2023-11-05'
WHERE Username = 'user6' AND GameID = 10;

-- 12. Delete reviews for a certain user and game
DELETE FROM Review
WHERE Username = 'user6' AND GameID = 10;

-- 13. Remove a game from a user's wishlist
DELETE FROM Wishlist
WHERE Username = 'user6' AND GameID = 10;

-- 14. Search for a game by title and see its details
SELECT Game.GameTitle, Game.ReleaseDate, Publisher.PublisherName, GROUP_CONCAT(DISTINCT Tag.TagName) AS Tags
FROM Game
LEFT JOIN Publisher ON Game.PublisherID = Publisher.PublisherID
LEFT JOIN GameTag ON Game.GameID = GameTag.GameID
LEFT JOIN Tag ON GameTag.TagID = Tag.TagID
WHERE Game.GameTitle = 'Counter-Strike 2';

-- 15. View current ongoing game sales
SELECT Game.GameTitle, Sale.Start_Date, Sale.End_Date, Sale.DiscountPercent
FROM Game
INNER JOIN Sale ON Game.GameID = Sale.GameID
WHERE date('now') BETWEEN Sale.Start_Date AND Sale.End_Date;

-- 16. View current and future game sales
SELECT Game.GameTitle, Sale.Start_Date, Sale.End_Date, Sale.DiscountPercent
FROM Game
INNER JOIN Sale ON Game.GameID = Sale.GameID
WHERE date('now') <= Sale.End_Date;

-- 17. Delete a user's account and related records
DELETE FROM Wishlist WHERE Username = 'user7';
DELETE FROM Review WHERE Username = 'user7';
DELETE FROM User WHERE Username = 'user7';

-- 18. Update the user's username
UPDATE User
SET Username = 'new_username'
WHERE Username = 'current_username';

-- 19. Update the user's email
UPDATE User
SET Email = 'new_email'
WHERE Username = 'current_username';

-- 20. Update the user's password
UPDATE User
SET Password = 'new_password'
WHERE Username = 'current_username'

-- Delete Table values
DELETE from Game;
DELETE from Publisher;
DELETE from Review;
DELETE from Sale;
DELETE from Tag;
DELETE from User;
DELETE from Wishlist;
DELETE from GameTag;