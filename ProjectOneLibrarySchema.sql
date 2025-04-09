-- Create the database
CREATE DATABASE IF NOT EXISTS ProjectOneLibrary;
USE ProjectOneLibrary;

-- Create Genre table
CREATE TABLE Genre (
    genreID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create Book table
CREATE TABLE Book (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year_published INT,
    genreID INT,
    FOREIGN KEY (genreID) REFERENCES Genre(genreID)
);

-- Insert genres
INSERT INTO Genre (name) VALUES 
('Fantasy'),
('Sci-Fi'),
('Romance'),
('Historical Fiction');

-- Insert books
INSERT INTO Book (title, author, year_published, genreID) VALUES
-- Fantasy (genreID = 1)
('The Hobbit', 'J.R.R. Tolkien', 1937, 1),
('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 1997, 1),
('The Name of the Wind', 'Patrick Rothfuss', 2007, 1),
('Mistborn: The Final Empire', 'Brandon Sanderson', 2006, 1),

-- Sci-Fi (genreID = 2)
('Dune', 'Frank Herbert', 1965, 2),
('Ender\'s Game', 'Orson Scott Card', 1985, 2),
('Neuromancer', 'William Gibson', 1984, 2),
('The Martian', 'Andy Weir', 2011, 2),

-- Romance (genreID = 3)
('Pride and Prejudice', 'Jane Austen', 1813, 3),
('Outlander', 'Diana Gabaldon', 1991, 3),
('The Notebook', 'Nicholas Sparks', 1996, 3),
('Me Before You', 'Jojo Moyes', 2012, 3),

-- Historical Fiction (genreID = 4)
('All the Light We Cannot See', 'Anthony Doerr', 2014, 4),
('The Book Thief', 'Markus Zusak', 2005, 4),
('A Tale of Two Cities', 'Charles Dickens', 1859, 4);
