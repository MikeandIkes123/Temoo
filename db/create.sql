CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    balance DECIMAL(10, 2)
);

CREATE TABLE Sellers (
    id INT NOT NULL PRIMARY KEY REFERENCES Users(id)
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    -- available BOOLEAN DEFAULT TRUE,
    quantity INT NOT NULL,
    description VARCHAR(255),
    main_category VARCHAR(255),
    sub_category VARCHAR(255),
    ratings DECIMAL(2,1) DEFAULT 0,
    no_of_ratings INT DEFAULT 0,
    image_url VARCHAR(2083)
);

-- TODO: create an actual purchases table
CREATE TABLE Purchases (
    -- can have id not as primary key, but just as as distinct indicator
    id INT UNIQUE NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    sid INT NOT NULL REFERENCES Sellers(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    quantity INT NOT NULL,
    fulfillment BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (uid, pid, sid, time_purchased)
);
-- creating feedbacks table 
CREATE TABLE Feedbacks (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id), 
    pid INT NOT NULL REFERENCES Products(id),
    comment TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Sells(
    uid INT NOT NULL REFERENCES Sellers(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (uid, pid)
);

CREATE TABLE Cart(
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (uid, pid)
);

CREATE TABLE sFeedbacks (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    sid INT NOT NULL REFERENCES Sellers(id),
    uid INT NOT NULL REFERENCES Users(id),
    comment TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

-- CREATE TABLE OrderItems (
--     id INT NOT NULL PRIMARY KEY,
--     order_id INT REFERENCES Orders(id),
--     product_id INT REFERENCES Products(id),
--     quantity INT,
--     unit_price DECIMAL(10, 2)
-- );
