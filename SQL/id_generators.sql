-- article_data INSERT Trigger
CREATE OR ALTER TRIGGER data_gen_id
ON dbo.article_data
INSTEAD OF INSERT
AS BEGIN

IF NOT EXISTS(SELECT * FROM dbo.article_data WHERE id=1000)
INSERT INTO dbo.article_data
SELECT 1000 AS id, title, author, category, [description], [data]
FROM inserted;

ELSE INSERT INTO dbo.article_data 
SELECT 
(SELECT MIN(id+1) 
FROM dbo.article_data
WHERE id+1 NOT IN
(SELECT DISTINCT id FROM dbo.article_data)) AS id, 
title, author, category, [description], [data]
FROM inserted;

END;
GO

-- article_categories INSERT Trigger
CREATE OR ALTER TRIGGER category_gen_id
ON dbo.article_categories
INSTEAD OF INSERT
AS BEGIN

IF NOT EXISTS(SELECT * FROM dbo.article_categories WHERE id=10)
INSERT INTO dbo.article_categories
SELECT 10 AS id, title, [description]
FROM inserted;

ELSE INSERT INTO dbo.article_categories 
SELECT 
(SELECT MIN(id+1) 
FROM dbo.article_categories
WHERE id+1 NOT IN
(SELECT DISTINCT id FROM dbo.article_categories)) AS id, 
title, [description]
FROM inserted;

END;
GO

-- data_gen_id Testing
DISABLE TRIGGER data_gen_id ON dbo.article_data;
INSERT INTO dbo.article_data(id, title) VALUES (1001, 'Test 1');
INSERT INTO dbo.article_data(id, title) VALUES (1003, 'Test 2');
INSERT INTO dbo.article_data(id, title) VALUES (1006, 'Test 3');

ENABLE TRIGGER data_gen_id ON dbo.article_data;
INSERT INTO dbo.article_data (title) VALUES ('Filled 1');
INSERT INTO dbo.article_data (title) VALUES ('Filled 2');
INSERT INTO dbo.article_data (title) VALUES ('Filled 3');
INSERT INTO dbo.article_data (title) VALUES ('Filled 4');
INSERT INTO dbo.article_data (title) VALUES ('Filled 5');

SELECT * FROM dbo.article_data;
DELETE FROM dbo.article_data;


-- category_gen_id Testing
DISABLE TRIGGER category_gen_id ON dbo.article_categories;
INSERT INTO dbo.article_categories(id, title) VALUES (11, 'Test 1');
INSERT INTO dbo.article_categories(id, title) VALUES (13, 'Test 2');
INSERT INTO dbo.article_categories(id, title) VALUES (16, 'Test 3');

ENABLE TRIGGER category_gen_id ON dbo.article_categories;
INSERT INTO dbo.article_categories (title) VALUES ('Filled 1');
INSERT INTO dbo.article_categories (title) VALUES ('Filled 2');
INSERT INTO dbo.article_categories (title) VALUES ('Filled 3');
INSERT INTO dbo.article_categories (title) VALUES ('Filled 4');
INSERT INTO dbo.article_categories (title) VALUES ('Filled 5');

SELECT * FROM dbo.article_categories;
DELETE FROM dbo.article_categories;