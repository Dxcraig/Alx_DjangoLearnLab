# Follow System and Feed Documentation

## Overview
This document describes the follow system and feed functionality implemented in the Social Media API. Users can follow other users and view an aggregated feed of posts from users they follow.

## Model Changes

### CustomUser Model
The `CustomUser` model has been updated with a `following` field:

```python
following = models.ManyToManyField(
    'self',
    symmetrical=False,
    related_name='followers',
    blank=True,
    help_text="Users that this user follows"
)
```

**Key Relationships:**
- `user.following.all()` - Returns all users that this user follows
- `user.followers.all()` - Returns all users who follow this user (reverse relationship)
- `user.get_following_count()` - Returns the count of users being followed
- `user.get_followers_count()` - Returns the count of followers

## API Endpoints

### 1. Follow a User
**Endpoint:** `POST /api/accounts/follow/<int:user_id>/`

**Authentication:** Required (Token Authentication)

**Description:** Follow another user. Users cannot follow themselves or follow the same user twice.

**Request:**
```bash
POST /api/accounts/follow/2/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
{
    "message": "You are now following john_doe",
    "user": {
        "id": 2,
        "username": "john_doe",
        "bio": "Software developer",
        "profile_picture": "http://example.com/media/profile_pictures/john.jpg"
    }
}
```

**Error Responses:**
- **400 Bad Request** - Trying to follow yourself:
```json
{
    "error": "You cannot follow yourself"
}
```

- **400 Bad Request** - Already following:
```json
{
    "error": "You are already following john_doe"
}
```

- **404 Not Found** - User does not exist:
```json
{
    "detail": "Not found."
}
```

### 2. Unfollow a User
**Endpoint:** `POST /api/accounts/unfollow/<int:user_id>/`

**Authentication:** Required (Token Authentication)

**Description:** Unfollow a user you are currently following.

**Request:**
```bash
POST /api/accounts/unfollow/2/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
{
    "message": "You have unfollowed john_doe"
}
```

**Error Responses:**
- **400 Bad Request** - Not following the user:
```json
{
    "error": "You are not following john_doe"
}
```

- **404 Not Found** - User does not exist:
```json
{
    "detail": "Not found."
}
```

### 3. List Following
**Endpoint:** `GET /api/accounts/following/`

**Authentication:** Required (Token Authentication)

**Description:** Get a list of users that the authenticated user follows.

**Request:**
```bash
GET /api/accounts/following/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
[
    {
        "id": 2,
        "username": "john_doe",
        "bio": "Software developer",
        "profile_picture": "http://example.com/media/profile_pictures/john.jpg"
    },
    {
        "id": 3,
        "username": "jane_smith",
        "bio": "Designer",
        "profile_picture": "http://example.com/media/profile_pictures/jane.jpg"
    }
]
```

### 4. List Followers
**Endpoint:** `GET /api/accounts/followers/`

**Authentication:** Required (Token Authentication)

**Description:** Get a list of users who follow the authenticated user.

**Request:**
```bash
GET /api/accounts/followers/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
[
    {
        "id": 4,
        "username": "mike_wilson",
        "bio": "Content creator",
        "profile_picture": "http://example.com/media/profile_pictures/mike.jpg"
    }
]
```

### 5. User Feed
**Endpoint:** `GET /api/posts/feed/`

**Authentication:** Required (Token Authentication)

**Description:** Get a personalized feed of posts from users that the authenticated user follows, ordered by creation date (most recent first).

**Request:**
```bash
GET /api/posts/feed/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
{
    "count": 15,
    "next": "http://example.com/api/posts/feed/?page=2",
    "previous": null,
    "results": [
        {
            "id": 10,
            "author": {
                "id": 2,
                "username": "john_doe"
            },
            "title": "My Latest Project",
            "content": "Just finished working on an amazing new feature...",
            "created_at": "2025-12-14T10:30:00Z",
            "updated_at": "2025-12-14T10:30:00Z",
            "comments_count": 5
        },
        {
            "id": 8,
            "author": {
                "id": 3,
                "username": "jane_smith"
            },
            "title": "Design Trends 2025",
            "content": "Here are the top design trends I'm seeing...",
            "created_at": "2025-12-13T15:20:00Z",
            "updated_at": "2025-12-13T15:20:00Z",
            "comments_count": 12
        }
    ]
}
```

**Features:**
- **Pagination:** Results are paginated (default page size configured in settings)
- **Ordering:** Posts are ordered by creation date (most recent first)
- **Filtering:** Only shows posts from users you follow
- **Empty Feed:** If you don't follow anyone, the feed will be empty

**Empty Response (200 OK):**
```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

## Usage Examples

### Using cURL

#### Follow a User
```bash
curl -X POST http://localhost:8000/api/accounts/follow/2/ \
  -H "Authorization: Token your-token-here"
```

#### Unfollow a User
```bash
curl -X POST http://localhost:8000/api/accounts/unfollow/2/ \
  -H "Authorization: Token your-token-here"
```

#### Get Following List
```bash
curl -X GET http://localhost:8000/api/accounts/following/ \
  -H "Authorization: Token your-token-here"
```

#### Get Followers List
```bash
curl -X GET http://localhost:8000/api/accounts/followers/ \
  -H "Authorization: Token your-token-here"
```

#### Get Feed
```bash
curl -X GET http://localhost:8000/api/posts/feed/ \
  -H "Authorization: Token your-token-here"
```

### Using Python Requests

```python
import requests

# Your authentication token
TOKEN = "your-token-here"
BASE_URL = "http://localhost:8000/api"
headers = {"Authorization": f"Token {TOKEN}"}

# Follow a user
response = requests.post(f"{BASE_URL}/accounts/follow/2/", headers=headers)
print(response.json())

# Get following list
response = requests.get(f"{BASE_URL}/accounts/following/", headers=headers)
print(response.json())

# Get feed
response = requests.get(f"{BASE_URL}/posts/feed/", headers=headers)
print(response.json())

# Unfollow a user
response = requests.post(f"{BASE_URL}/accounts/unfollow/2/", headers=headers)
print(response.json())
```

### Using Postman

1. **Set up Authentication:**
   - Add a header: `Authorization: Token your-token-here`

2. **Follow a User:**
   - Method: POST
   - URL: `http://localhost:8000/api/accounts/follow/2/`
   - Headers: Authorization token

3. **Get Feed:**
   - Method: GET
   - URL: `http://localhost:8000/api/posts/feed/`
   - Headers: Authorization token

## Testing Workflow

### 1. Create Test Users
```bash
# Register user 1
POST /api/accounts/register/
{
    "username": "user1",
    "email": "user1@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
}

# Register user 2
POST /api/accounts/register/
{
    "username": "user2",
    "email": "user2@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
}
```

### 2. Create Posts (as user2)
```bash
POST /api/posts/posts/
Authorization: Token <user2-token>
{
    "title": "User 2's First Post",
    "content": "This is a test post from user 2"
}
```

### 3. Follow User (as user1)
```bash
POST /api/accounts/follow/2/
Authorization: Token <user1-token>
```

### 4. Check Feed (as user1)
```bash
GET /api/posts/feed/
Authorization: Token <user1-token>
# Should show posts from user2
```

### 5. Verify Following/Followers
```bash
# As user1, check who you're following
GET /api/accounts/following/
Authorization: Token <user1-token>

# As user2, check who's following you
GET /api/accounts/followers/
Authorization: Token <user2-token>
```

### 6. Unfollow User (as user1)
```bash
POST /api/accounts/unfollow/2/
Authorization: Token <user1-token>
```

### 7. Verify Empty Feed
```bash
GET /api/posts/feed/
Authorization: Token <user1-token>
# Should return empty results
```

## Permission Summary

| Endpoint | Permission | Notes |
|----------|-----------|-------|
| `POST /follow/<id>/` | Authenticated | Cannot follow yourself |
| `POST /unfollow/<id>/` | Authenticated | Must be following the user |
| `GET /following/` | Authenticated | Shows your following list |
| `GET /followers/` | Authenticated | Shows your followers |
| `GET /feed/` | Authenticated | Personalized feed |

## Database Queries

The feed is optimized with the following query:
```python
Post.objects.filter(author__in=following_users).order_by('-created_at')
```

This efficiently retrieves posts from followed users in a single database query.

## Error Handling

All endpoints return appropriate HTTP status codes:
- **200 OK** - Successful operation
- **400 Bad Request** - Invalid request (e.g., following yourself)
- **401 Unauthorized** - Missing or invalid authentication token
- **404 Not Found** - User or resource does not exist

## Notes

1. **Following Relationship:** The relationship is asymmetric (if A follows B, B doesn't automatically follow A)
2. **Feed Updates:** The feed updates in real-time as posts are created by followed users
3. **Performance:** Consider implementing pagination for large following/followers lists
4. **Privacy:** Currently, all users can view all profiles; consider adding privacy settings in future updates

## Migration Information

The follow system required the following migration:
```
accounts/migrations/0002_remove_customuser_followers_customuser_following.py
```

This migration:
- Removes the old `followers` field
- Adds the new `following` field with `related_name='followers'`

## Next Steps

Consider implementing:
1. Follow requests (for private accounts)
2. Block functionality
3. Follow recommendations based on mutual connections
4. Notifications for new followers
5. Activity feed (likes, comments, follows)
