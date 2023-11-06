-- Create the User table
CREATE TABLE User (
    Username TEXT PRIMARY KEY,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL
);

-- Create the Game table
CREATE TABLE Game (
    GameID INTEGER PRIMARY KEY,
    GameTitle TEXT NOT NULL,
    ReleaseDate DATE NOT NULL,
    PublisherID INTEGER,
    FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID)
);

-- Create the Tag table
CREATE TABLE Tag (
    TagID INTEGER PRIMARY KEY,
    TagName TEXT NOT NULL
);

-- Create the GameTag table to manage the many-to-many relationship between Games and Tags
CREATE TABLE GameTag (
    GameID INTEGER,
    TagID INTEGER,
    PRIMARY KEY (GameID, TagID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID),
    FOREIGN KEY (TagID) REFERENCES Tag(TagID)
);

-- Create the Publisher table
CREATE TABLE Publisher (
    PublisherID INTEGER PRIMARY KEY,
    PublisherName TEXT NOT NULL
);

-- Create the Wishlist table
CREATE TABLE Wishlist (
    WishlistID INTEGER PRIMARY KEY,
    Username TEXT,
    GameID INTEGER,
    FOREIGN KEY (Username) REFERENCES User(Username),
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
);

-- Create the Review table
CREATE TABLE Review (
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
CREATE TABLE Sale (
    SaleID INTEGER PRIMARY KEY,
    Start_Date DATE,
    End_Date DATE,
    GameID INTEGER,
    DiscountPercent REAL,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
);