drop table posts;

create table blog (
  id integer primary key autoincrement,
  first_name text,
  last_name text,
  photo text,
  blog_title text,
  about_blog text
);

create table posts (
  id integer primary key autoincrement,
  blog_id integer,
  post_date text,
  post_title text,
  post text
);
