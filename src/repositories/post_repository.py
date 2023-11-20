from src.models import Post, db, users

class PostRepository:

    # get a single post from the DB using the ID
    def get_post_by_id(self, post_id):
        return Post.query.get(post_id)
    
    # get all posts from the DB with their creators
    def get_all_posts_with_users(self):
        #filter by date
        return db.session.query(Post, users).join(users, users.user_id == Post.user_id).order_by(Post.date_posted.desc()).all()

    # create a new post in the DB
    def create_post(self, title, content, user_id):
        new_post = Post(user_id, title, content)
        db.session.add(new_post)
        db.session.commit()
        return new_post
    
    # add a like to a post
    def add_like(self, post_id, user_id):
        post = Post.query.get(post_id)
        user = users.query.get(user_id)
        if user in post.liked_by:
            post.liked_by.remove(user)
            post.likes -= 1
            db.session.commit()
        elif user not in post.liked_by:
            post.liked_by.append(user)
            post.likes += 1
            db.session.commit()

    # get the user who created the post
    def get_post_creator_id(self, post_id):
        return Post.query.get(post_id).user_id

# Singleton to be used in other modules
post_repository_singleton = PostRepository()
