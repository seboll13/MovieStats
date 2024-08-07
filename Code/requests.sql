-- Top actors with at least 5 movies and average rating over 7.5
SELECT actors.name, COUNT(ratings.id), AVG(ratings.your_rating)
FROM `title_ratings`.`imdb_ratings` AS ratings
JOIN `title_ratings`.`movie_actors` AS ma ON ma.movie_id = ratings.id
JOIN `title_ratings`.`actors` ON actors.actor_id = ma.actor_id
GROUP BY actors.name HAVING COUNT(ratings.id) >= 5 AND AVG(ratings.your_rating) > 7.5
ORDER BY COUNT(ratings.id) DESC;


-- List of movies for a given actor
SELECT ratings.title, ratings.your_rating FROM `title_ratings`.`imdb_ratings` AS ratings
JOIN `title_ratings`.`movie_actors` AS ma ON ma.movie_id = ratings.id
JOIN `title_ratings`.`actors` ON actors.actor_id = ma.actor_id
WHERE actors.name = 'Tom Hanks'
ORDER BY ratings.your_rating DESC;


-- Top 10 rated directors with at least 5 movies
SELECT directors.name, COUNT(directors.name), AVG(ratings.your_rating)
FROM `title_ratings`.`directors`
JOIN `title_ratings`.`movie_directors` AS md ON md.director_id = directors.director_id
JOIN `title_ratings`.`imdb_ratings` AS ratings ON ratings.id = md.movie_id
GROUP BY directors.name HAVING COUNT(directors.name) > 4
ORDER BY AVG(ratings.your_rating) DESC LIMIT 10;


-- Best actor pairings with at least 3 movies
SELECT
    a1.name, a2.name,
    COUNT(*) AS movie_count,
    AVG(ratings.your_rating) AS average_rating
FROM `title_ratings`.`movie_actors` ma1
JOIN `title_ratings`.`movie_actors` ma2 ON ma1.movie_id = ma2.movie_id AND ma1.actor_id < ma2.actor_id
JOIN `title_ratings`.`actors` a1 ON ma1.actor_id = a1.actor_id
JOIN `title_ratings`.`actors` a2 ON ma2.actor_id = a2.actor_id
JOIN `title_ratings`.`imdb_ratings` AS ratings ON ma1.movie_id = ratings.id
GROUP BY ma1.actor_id, ma2.actor_id HAVING movie_count > 2
ORDER BY average_rating DESC LIMIT 20;


-- Top genres for each highest rated actor
SELECT actors.name, genres.name, COUNT(*), AVG(ratings.your_rating) FROM `title_ratings`.`actors`
JOIN `title_ratings`.`movie_actors` ma ON actors.actor_id = ma.actor_id
JOIN `title_ratings`.`imdb_ratings` AS ratings ON ma.movie_id = ratings.id
JOIN `title_ratings`.`movie_genres` mg ON ratings.id = mg.movie_id
JOIN `title_ratings`.`genres` ON mg.genre_id = genres.genre_id
GROUP BY actors.name, genres.name HAVING AVG(ratings.your_rating) > 7.5
ORDER BY COUNT(*) DESC LIMIT 20;


-- Top rated musicians with at least 5 movies
SELECT musicians.name, COUNT(*), AVG(ratings.your_rating)
FROM `title_ratings`.`musicians`
JOIN `title_ratings`.`movie_musicians` AS md ON md.musician_id = musicians.musician_id
JOIN `title_ratings`.`imdb_ratings` AS ratings ON ratings.id = md.movie_id
GROUP BY musicians.name HAVING COUNT(*) > 4
ORDER BY COUNT(*) DESC LIMIT 15;