from src.models import Post, db

class PostRepository:

    def get_all_posts(self):
        # TODO get all posts from the DB
        return Post.query.all()

    def get_movie_by_id(self, movie_id):
        # TODO get a single post from the DB using the ID
        return Post.query.get(movie_id)

    def create_post(self, title, content):
        # TODO create a new post in the DB
        new_post = Post(title, content)
        db.session.add(new_post)
        db.session.commit()
        return new_post

# Singleton to be used in other modules
post_repository_singleton = PostRepository()
