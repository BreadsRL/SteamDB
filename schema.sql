-- Create the User table
CREATE TABLE IF NOT EXISTS User (
    Username TEXT PRIMARY KEY,
    Email TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL
);

-- Create the Game table
CREATE TABLE IF NOT EXISTS Game (
    GameID INTEGER PRIMARY KEY,
    GameTitle TEXT UNIQUE NOT NULL,
    ReleaseDate DATE NOT NULL,
    PublisherID INTEGER,
    FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID)
);

-- Create the Tag table
CREATE TABLE IF NOT EXISTS Tag (
    TagID INTEGER PRIMARY KEY,
    TagName TEXT UNIQUE NOT NULL
);

-- Create the GameTag table to manage the many-to-many relationship between Games and Tags
CREATE TABLE IF NOT EXISTS GameTag (
    GameID INTEGER,
    TagID INTEGER,
    PRIMARY KEY (GameID, TagID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID),
    FOREIGN KEY (TagID) REFERENCES Tag(TagID)
);

-- Create the Publisher table
CREATE TABLE IF NOT EXISTS Publisher (
    PublisherID INTEGER PRIMARY KEY,
    PublisherName TEXT UNIQUE NOT NULL
);

-- Create the Wishlist table
CREATE TABLE IF NOT EXISTS Wishlist (
    WishlistID INTEGER PRIMARY KEY,
    Username TEXT,
    GameID INTEGER,
    FOREIGN KEY (Username) REFERENCES User(Username),
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
    UNIQUE (Username, GameID)
);

-- Create the Review table
CREATE TABLE IF NOT EXISTS Review (
    ReviewID INTEGER PRIMARY KEY,
    Username TEXT,
    GameID INTEGER,
    Rating INTEGER,
    Comment TEXT,
    ReviewDate DATE,
    FOREIGN KEY (Username) REFERENCES User(Username),
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
);

-- Create the Sale table
CREATE TABLE IF NOT EXISTS Sale (
    SaleID INTEGER PRIMARY KEY,
    Start_Date DATE,
    End_Date DATE,
    GameID INTEGER,
    DiscountPercent REAL,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
);