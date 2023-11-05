CREATE TABLE Users(
    u_Username char(12) NOT NULL,
    u_Email varchar(320) NOT NULL,
    u_Password varchar(256) NOT NULL
);

CREATE TABLE Game(
    g_GameID decimal(32,0) NOT NULL,
    g_GameTitle varchar(256) NOT NULL,
    g_ReleaseDate char(8) NOT NULL,
    g_TagID char(4) NOT NULL,
    g_PubID char(4) NOT NULL
);

CREATE TABLE Publisher(
    p_PubID char(4) NOT NULL,
    p_Name varchar(256) NOT NULL
);

CREATE TABLE Tag(
    t_TagID char(4) NOT NULL,
    t_Name varchar(256) NOT NULL
);

CREATE TABLE Review(
    r_ID char(10) NOT NULL,
    r_Username char(12) NOT NULL,
    r_GameID decimal(32,0) NOT NULL,
    r_Rating char(8) NOT NULL,
    r_Comment varchar(8000) NOT NULL,
    r_Date char(8) NOT NULL
);

CREATE TABLE Sale(
    s_ID char(10) NOT NULL,
    s_StartDate char(8) NOT NULL,
    s_EndDate char(8) NOT NULL,
    s_GameID decimal(32,0) NOT NULL,
    s_DiscountPercent varchar(3) NOT NULL
);

CREATE TABLE Wishlist(
    w_ID char(10) NOT NULL,
    w_Username char(12) NOT NULL,
    w_GameID decimal(32,0) NOT NULL
);