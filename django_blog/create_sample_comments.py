# Script to create sample blog posts and comments for testing
# Run this in Django shell: python manage.py shell < create_sample_comments.py

from django.contrib.auth.models import User
from blog.models import Post, Comment

# Get or create a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f'Created user: {user.username}')
else:
    print(f'Using existing user: {user.username}')

# Get or create another test user
user2, created = User.objects.get_or_create(
    username='commenter',
    defaults={'email': 'commenter@example.com'}
)
if created:
    user2.set_password('testpass123')
    user2.save()
    print(f'Created user: {user2.username}')
else:
    print(f'Using existing user: {user2.username}')

# Create sample posts if they don't exist
if Post.objects.count() == 0:
    post1 = Post.objects.create(
        title='Welcome to Django Blog',
        content='This is my first blog post about learning Django. Django is an amazing web framework that makes it easy to build robust web applications.',
        author=user
    )
    print(f'Created post: {post1.title}')
    
    post2 = Post.objects.create(
        title='Understanding Django Models',
        content='Django models are Python classes that define the structure of your database. Each model maps to a single database table.',
        author=user
    )
    print(f'Created post: {post2.title}')
    
    post3 = Post.objects.create(
        title='Working with Django Views',
        content='Views in Django are Python functions or classes that receive web requests and return web responses. They contain the logic for handling requests.',
        author=user2
    )
    print(f'Created post: {post3.title}')
else:
    print(f'Found {Post.objects.count()} existing posts')

# Get the first post for adding comments
first_post = Post.objects.first()

if first_post:
    # Create sample comments
    comments_data = [
        {
            'author': user2,
            'content': 'Great post! I really enjoyed reading about Django. Looking forward to more content like this.'
        },
        {
            'author': user,
            'content': 'Thank you for the feedback! I\'ll be posting more tutorials soon.'
        },
        {
            'author': user2,
            'content': 'I have a question about implementing authentication. Could you cover that in a future post?'
        },
        {
            'author': user,
            'content': 'Absolutely! Authentication will be covered in my next post. Stay tuned!'
        },
    ]
    
    # Check if comments already exist for this post
    existing_comments = Comment.objects.filter(post=first_post).count()
    
    if existing_comments == 0:
        for comment_data in comments_data:
            comment = Comment.objects.create(
                post=first_post,
                author=comment_data['author'],
                content=comment_data['content']
            )
            print(f'Created comment by {comment.author.username} on {comment.post.title}')
        
        print(f'\nSuccessfully created {len(comments_data)} comments!')
    else:
        print(f'\n{existing_comments} comments already exist for "{first_post.title}"')

# Add comments to the second post if it exists
posts = Post.objects.all()
if len(posts) >= 2:
    second_post = posts[1]
    if Comment.objects.filter(post=second_post).count() == 0:
        Comment.objects.create(
            post=second_post,
            author=user2,
            content='This explanation of Django models is very clear. Thanks for sharing!'
        )
        Comment.objects.create(
            post=second_post,
            author=user,
            content='Glad you found it helpful! Models are fundamental to Django development.'
        )
        print(f'\nAdded comments to "{second_post.title}"')

print('\n=== Summary ===')
print(f'Total Users: {User.objects.count()}')
print(f'Total Posts: {Post.objects.count()}')
print(f'Total Comments: {Comment.objects.count()}')
print('\nYou can now test the comment system!')
print('Login with:')
print('  Username: testuser, Password: testpass123')
print('  Username: commenter, Password: testpass123')
