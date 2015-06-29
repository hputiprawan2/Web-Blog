
-- Create a database -- 
create database WebDB;
show databases;
use WebDB;
show tables;

-- Create Tables -- 
DROP TABLE Users;

CREATE TABLE Users(
	user_id INT NOT NULL AUTO_INCREMENT,
	user_name TEXT NOT NULL,
	user_password TEXT NOT NULL,
    user_email TEXT NOT NULL,
	PRIMARY KEY (user_id)
);

select * from Users;

CREATE TABLE Posts(
	post_id INT NOT NULL AUTO_INCREMENT,
    post_type TEXT NOT NULL, 
	post_title TEXT NOT NULL,
    post_time TIMESTAMP NOT NULL,
	post_content LONGTEXT NOT NULL,
	post_authorID INT NOT NULL,
	PRIMARY KEY (post_id),
    FOREIGN KEY (post_authorID) REFERENCES Users(user_id)
);

select * from Posts;

DROP TABLE IF EXISTS PostsRecord;
CREATE TABLE PostsRecord (
    trigger_id INT(11) NOT NULL AUTO_INCREMENT,
    p_user_id INT(11) NOT NULL,
    post_on DATETIME DEFAULT NULL,
    post_action VARCHAR(50) NOT NULL,
    PRIMARY KEY (trigger_id)
);
select * from PostsRecord;


DROP table IF exists Comments;
CREATE TABLE Comments(
	comment_id INT NOT NULL AUTO_INCREMENT,
    comment_content TEXT NOT NULL, 
	comment_time TIMESTAMP NOT NULL,
    comment_owner INT NOT NULL,
	comment_postID INT NOT NULL,
	PRIMARY KEY (comment_id),
    FOREIGN KEY (comment_owner) REFERENCES Users(user_id),
    FOREIGN KEY (comment_postID) REFERENCES Posts(post_id)
);























-- Create Triggers -- 
drop trigger if exists posts_trigger;
delimiter |
CREATE TRIGGER posts_trigger
	AFTER INSERT ON Posts
    FOR EACH ROW 
	BEGIN
    
	-- Insert record into audit table --
    INSERT INTO PostsRecord
    (	p_user_id, 
		post_on,
        post_action
	)
    values
    (	new.post_authorID,
		now(),
        'ADD'
    );
end |
delimiter ;

drop trigger if exists posts_update_trigger;
delimiter |
CREATE TRIGGER posts_update_trigger
	AFTER UPDATE ON Posts
    FOR EACH ROW 
	BEGIN
    
	-- Insert record into audit table --
    INSERT INTO PostsRecord
    (	p_user_id, 
		post_on,
        post_action
	)
    values
    (	new.post_authorID,
		now(),
        'EDIT'
    );
end |
delimiter ;

drop trigger if exists posts_delete_trigger;
delimiter |
CREATE TRIGGER posts_delete_trigger
	BEFORE DELETE ON Posts
    FOR EACH ROW 
	BEGIN
    
	-- Insert record into audit table --
    INSERT INTO PostsRecord
    (	p_user_id, 
		post_on,
        post_action
	)
    values
    (	OLD.post_authorID,
		now(),
        'DELETE'
    );
end |
delimiter ;

select * from Users;
select * from Posts;
select * from Comments;
select * from PostsRecord;
select * from UsersRecord;
insert into Posts (post_type, post_title, post_content, post_authorID)values('Recipe - Desserts', 'M & M Cookies', 'aa','24');

select * from ActivityLog;

SELECT * FROM Users, Posts, PostsRecord WHERE Posts.post_id = PostsRecord.trigger_p_postID 
AND Users.user_id = PostsRecord.trigger_p_fromID;

drop table if exists ActivityLog;
create table ActivityLog(
	log_id int not null auto_increment,
    primary key(log_id)
);

show tables;
select * from Users;
select * from Posts;
select * from Comments;
select * from ActivityLog;
select * from HashLog;

drop table if exists HashLog;







insert into Users values('', 'admin', 'admin');
insert into Users values('', 'hanna', 'hanna');
insert into Users (user_name, user_password) values('test','test');

select * from Users;
select * from PostsEncrypted;

CREATE TABLE Posts(
	post_id INT NOT NULL AUTO_INCREMENT,
	post_title TEXT NOT NULL,
	post_description LONGTEXT NOT NULL,
	post_authorID INT NOT NULL,
	PRIMARY KEY (post_id),
    FOREIGN KEY (post_authorID) REFERENCES Users(user_id)
);

insert into Posts values('', 'Recipe - Desserts', 'M & M Cookies', '24');
insert into Posts values('', 'Recipe - Food', 'Spaghetti', '24');
insert into Posts values('', 'Recipe - Desserts', 'Macaroons', '24');
insert into Posts values('', 'Dream Catcher', 'History of Dream Catcher', '24');
insert into Posts values('', 'NewPost', 'NewPost', '', '', '26');

select * from Posts, Users where Users.user_id = Posts.post_authorID;

select * from Posts;


alter table Posts
change post_title post_type text;

alter table Posts
change post_description post_title text;

alter table Posts
add post_time timestamp after post_title;

alter table Posts
add post_content longtext after post_time;