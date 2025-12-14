# Likes and Notifications System Documentation

## Overview
This document describes the likes and notifications functionality implemented in the Social Media API. Users can like posts and receive notifications for various interactions such as new followers, likes on their posts, and comments.

## Table of Contents
- [Models](#models)
- [API Endpoints](#api-endpoints)
  - [Likes Endpoints](#likes-endpoints)
  - [Notifications Endpoints](#notifications-endpoints)
- [Usage Examples](#usage-examples)
- [Testing Guide](#testing-guide)

---

## Models

### Like Model
The `Like` model tracks which users have liked which posts.

**Fields:**
- `user` (ForeignKey to User) - The user who liked the post
- `post` (ForeignKey to Post) - The post being liked
- `created_at` (DateTimeField) - When the like was created

**Constraints:**
- `unique_together` on `(user, post)` - A user can only like a post once

**Methods:**
- `__str__()` - Returns formatted string representation

### Notification Model
The `Notification` model tracks user interactions and events using GenericForeignKey for flexibility.

**Fields:**
- `recipient` (ForeignKey to User) - User receiving the notification
- `actor` (ForeignKey to User) - User who performed the action
- `verb` (CharField) - Description of the action
- `target_content_type` (ForeignKey to ContentType) - Type of target object
- `target_object_id` (PositiveIntegerField) - ID of target object
- `target` (GenericForeignKey) - The target object
- `timestamp` (DateTimeField) - When notification was created
- `read` (BooleanField) - Whether notification has been read

**Methods:**
- `mark_as_read()` - Marks the notification as read
- `__str__()` - Returns formatted string representation

**Notification Types:**
1. **Follow** - When someone follows you
2. **Like** - When someone likes your post
3. **Comment** - When someone comments on your post

---

## API Endpoints

### Likes Endpoints

#### 1. Like a Post
**Endpoint:** `POST /api/posts/<int:pk>/like/`

**Authentication:** Required (Token Authentication)

**Description:** Like a specific post. Users cannot like the same post twice or like their own posts.

**Request:**
```bash
POST /api/posts/1/like/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
{
    "message": "Post liked successfully",
    "likes_count": 5
}
```

**Error Responses:**

- **400 Bad Request** - Already liked:
```json
{
    "error": "You have already liked this post"
}
```

- **401 Unauthorized** - Not authenticated:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

- **404 Not Found** - Post does not exist:
```json
{
    "detail": "Not found."
}
```

**Behavior:**
- Creates a `Like` object
- Increments the post's like count
- Creates a notification for the post author (if not liking own post)

---

#### 2. Unlike a Post
**Endpoint:** `POST /api/posts/<int:pk>/unlike/`

**Authentication:** Required (Token Authentication)

**Description:** Remove a like from a post that you previously liked.

**Request:**
```bash
POST /api/posts/1/unlike/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
{
    "message": "Post unliked successfully",
    "likes_count": 4
}
```

**Error Responses:**

- **400 Bad Request** - Haven't liked the post:
```json
{
    "error": "You have not liked this post"
}
```

- **404 Not Found** - Post does not exist

**Behavior:**
- Deletes the `Like` object
- Decrements the post's like count
- Does not remove the notification (for historical tracking)

---

### Notifications Endpoints

#### 3. List All Notifications
**Endpoint:** `GET /api/notifications/`

**Authentication:** Required (Token Authentication)

**Description:** Get all notifications for the authenticated user, with unread notifications shown first.

**Request:**
```bash
GET /api/notifications/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
[
    {
        "id": 15,
        "recipient": 1,
        "actor": {
            "id": 2,
            "username": "john_doe",
            "profile_picture": "http://example.com/media/profile_pictures/john.jpg"
        },
        "verb": "liked your post",
        "target_type": "post",
        "target_object_id": 5,
        "timestamp": "2025-12-14T10:30:00Z",
        "read": false
    },
    {
        "id": 14,
        "recipient": 1,
        "actor": {
            "id": 3,
            "username": "jane_smith",
            "profile_picture": null
        },
        "verb": "started following you",
        "target_type": "customuser",
        "target_object_id": 1,
        "timestamp": "2025-12-14T09:15:00Z",
        "read": false
    },
    {
        "id": 13,
        "recipient": 1,
        "actor": {
            "id": 4,
            "username": "mike_wilson",
            "profile_picture": null
        },
        "verb": "commented on your post",
        "target_type": "post",
        "target_object_id": 3,
        "timestamp": "2025-12-13T18:45:00Z",
        "read": true
    }
]
```

**Features:**
- Unread notifications appear first
- Ordered by timestamp (most recent first)
- Includes actor details (username, profile picture)
- Shows target type and ID for reference

---

#### 4. List Unread Notifications
**Endpoint:** `GET /api/notifications/unread/`

**Authentication:** Required (Token Authentication)

**Description:** Get only unread notifications for the authenticated user.

**Request:**
```bash
GET /api/notifications/unread/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
[
    {
        "id": 15,
        "recipient": 1,
        "actor": {
            "id": 2,
            "username": "john_doe",
            "profile_picture": null
        },
        "verb": "liked your post",
        "target_type": "post",
        "target_object_id": 5,
        "timestamp": "2025-12-14T10:30:00Z",
        "read": false
    },
    {
        "id": 14,
        "recipient": 1,
        "actor": {
            "id": 3,
            "username": "jane_smith",
            "profile_picture": null
        },
        "verb": "started following you",
        "target_type": "customuser",
        "target_object_id": 1,
        "timestamp": "2025-12-14T09:15:00Z",
        "read": false
    }
]
```

**Use Case:**
- Display unread notification count badge
- Show unread notifications prominently in UI
- Filter out already-read notifications

---

#### 5. Mark Notification as Read
**Endpoint:** `POST /api/notifications/<int:notification_id>/read/`

**Authentication:** Required (Token Authentication)

**Description:** Mark a specific notification as read.

**Request:**
```bash
POST /api/notifications/15/read/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
{
    "message": "Notification marked as read"
}
```

**Error Responses:**

- **404 Not Found** - Notification doesn't exist or doesn't belong to you:
```json
{
    "error": "Notification not found"
}
```

**Behavior:**
- Updates `read` field to `True`
- Only affects notifications owned by the requesting user

---

#### 6. Mark All Notifications as Read
**Endpoint:** `POST /api/notifications/read-all/`

**Authentication:** Required (Token Authentication)

**Description:** Mark all unread notifications as read for the authenticated user.

**Request:**
```bash
POST /api/notifications/read-all/
Authorization: Token <your-token>
```

**Success Response (200 OK):**
```json
{
    "message": "5 notifications marked as read"
}
```

**Behavior:**
- Bulk updates all unread notifications
- Returns count of affected notifications
- Useful for "clear all" functionality

---

## Usage Examples

### Using cURL

#### Like a Post
```bash
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Token your-token-here"
```

#### Unlike a Post
```bash
curl -X POST http://localhost:8000/api/posts/1/unlike/ \
  -H "Authorization: Token your-token-here"
```

#### Get All Notifications
```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token your-token-here"
```

#### Get Unread Notifications
```bash
curl -X GET http://localhost:8000/api/notifications/unread/ \
  -H "Authorization: Token your-token-here"
```

#### Mark Notification as Read
```bash
curl -X POST http://localhost:8000/api/notifications/15/read/ \
  -H "Authorization: Token your-token-here"
```

#### Mark All Notifications as Read
```bash
curl -X POST http://localhost:8000/api/notifications/read-all/ \
  -H "Authorization: Token your-token-here"
```

---

### Using Python Requests

```python
import requests

# Configuration
TOKEN = "your-token-here"
BASE_URL = "http://localhost:8000/api"
headers = {"Authorization": f"Token {TOKEN}"}

# Like a post
response = requests.post(f"{BASE_URL}/posts/1/like/", headers=headers)
print(response.json())
# Output: {"message": "Post liked successfully", "likes_count": 5}

# Unlike a post
response = requests.post(f"{BASE_URL}/posts/1/unlike/", headers=headers)
print(response.json())
# Output: {"message": "Post unliked successfully", "likes_count": 4}

# Get all notifications
response = requests.get(f"{BASE_URL}/notifications/", headers=headers)
notifications = response.json()
print(f"Total notifications: {len(notifications)}")

# Get unread notifications
response = requests.get(f"{BASE_URL}/notifications/unread/", headers=headers)
unread = response.json()
print(f"Unread notifications: {len(unread)}")

# Mark notification as read
notification_id = unread[0]['id']
response = requests.post(
    f"{BASE_URL}/notifications/{notification_id}/read/",
    headers=headers
)
print(response.json())
# Output: {"message": "Notification marked as read"}

# Mark all as read
response = requests.post(f"{BASE_URL}/notifications/read-all/", headers=headers)
print(response.json())
# Output: {"message": "5 notifications marked as read"}
```

---

### Using JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://localhost:8000/api';
const TOKEN = 'your-token-here';
const headers = {
    'Authorization': `Token ${TOKEN}`,
    'Content-Type': 'application/json'
};

// Like a post
async function likePost(postId) {
    const response = await fetch(`${BASE_URL}/posts/${postId}/like/`, {
        method: 'POST',
        headers: headers
    });
    const data = await response.json();
    console.log(data);
}

// Get unread notifications
async function getUnreadNotifications() {
    const response = await fetch(`${BASE_URL}/notifications/unread/`, {
        headers: headers
    });
    const notifications = await response.json();
    console.log(`Unread: ${notifications.length}`);
    return notifications;
}

// Mark all as read
async function markAllAsRead() {
    const response = await fetch(`${BASE_URL}/notifications/read-all/`, {
        method: 'POST',
        headers: headers
    });
    const data = await response.json();
    console.log(data);
}

// Usage
likePost(1);
getUnreadNotifications();
markAllAsRead();
```

---

## Testing Guide

### Manual Testing Workflow

#### Test 1: Like System
1. **Create test users and posts:**
   ```bash
   # Login as user1
   POST /api/accounts/login/
   {
       "username": "user1",
       "password": "testpass123"
   }
   # Save the token
   
   # Login as user2
   POST /api/accounts/login/
   {
       "username": "user2",
       "password": "testpass123"
   }
   # Save the token
   
   # User2 creates a post
   POST /api/posts/posts/
   Authorization: Token <user2-token>
   {
       "title": "Test Post",
       "content": "This is a test post for likes"
   }
   # Note the post ID
   ```

2. **Test like functionality:**
   ```bash
   # User1 likes user2's post
   POST /api/posts/1/like/
   Authorization: Token <user1-token>
   
   # Expected: Success message and likes_count
   
   # Try to like again (should fail)
   POST /api/posts/1/like/
   Authorization: Token <user1-token>
   
   # Expected: Error "You have already liked this post"
   ```

3. **Check post details:**
   ```bash
   # Get post details
   GET /api/posts/posts/1/
   Authorization: Token <user1-token>
   
   # Expected: likes_count: 1, is_liked_by_user: true
   ```

4. **Test unlike functionality:**
   ```bash
   # User1 unlikes the post
   POST /api/posts/1/unlike/
   Authorization: Token <user1-token>
   
   # Expected: Success message and updated likes_count
   
   # Try to unlike again (should fail)
   POST /api/posts/1/unlike/
   Authorization: Token <user1-token>
   
   # Expected: Error "You have not liked this post"
   ```

#### Test 2: Notifications
1. **Check user2's notifications:**
   ```bash
   # User2 checks notifications (should see like notification)
   GET /api/notifications/
   Authorization: Token <user2-token>
   
   # Expected: Notification with verb "liked your post"
   ```

2. **Test unread notifications:**
   ```bash
   # Get unread notifications
   GET /api/notifications/unread/
   Authorization: Token <user2-token>
   
   # Expected: List of unread notifications
   ```

3. **Mark notification as read:**
   ```bash
   # Mark specific notification as read
   POST /api/notifications/1/read/
   Authorization: Token <user2-token>
   
   # Expected: Success message
   
   # Check unread again
   GET /api/notifications/unread/
   Authorization: Token <user2-token>
   
   # Expected: Notification should be gone from unread list
   ```

#### Test 3: Comment Notifications
```bash
# User1 comments on user2's post
POST /api/comments/
Authorization: Token <user1-token>
{
    "post": 1,
    "content": "Great post!"
}

# User2 checks notifications
GET /api/notifications/unread/
Authorization: Token <user2-token>

# Expected: Notification with verb "commented on your post"
```

#### Test 4: Follow Notifications
```bash
# User1 follows user2
POST /api/accounts/follow/2/
Authorization: Token <user1-token>

# User2 checks notifications
GET /api/notifications/unread/
Authorization: Token <user2-token>

# Expected: Notification with verb "started following you"
```

#### Test 5: Mark All as Read
```bash
# User2 marks all notifications as read
POST /api/notifications/read-all/
Authorization: Token <user2-token>

# Expected: Message with count of marked notifications

# Check unread notifications
GET /api/notifications/unread/
Authorization: Token <user2-token>

# Expected: Empty list
```

---

### Postman Collection Testing

Create a Postman collection with the following requests:

**Collection: Likes and Notifications**

1. **Setup**
   - Login User1 → Save token to environment
   - Login User2 → Save token to environment
   - Create Post (User2) → Save post_id

2. **Like Tests**
   - Like Post (User1)
   - Verify Like (check post details)
   - Try Duplicate Like (should fail)
   - Unlike Post
   - Try Unlike Again (should fail)

3. **Notification Tests**
   - Get All Notifications (User2)
   - Get Unread Notifications (User2)
   - Mark One as Read
   - Verify Read Status
   - Mark All as Read
   - Verify All Read

4. **Integration Tests**
   - User1 likes post → User2 gets notification
   - User1 comments → User2 gets notification
   - User1 follows User2 → User2 gets notification
   - Check notification counts

---

## Permission Summary

| Endpoint | Permission | Can Perform |
|----------|-----------|-------------|
| `POST /posts/<id>/like/` | Authenticated | Any user except post author |
| `POST /posts/<id>/unlike/` | Authenticated | Users who liked the post |
| `GET /notifications/` | Authenticated | View own notifications |
| `GET /notifications/unread/` | Authenticated | View own unread |
| `POST /notifications/<id>/read/` | Authenticated | Mark own as read |
| `POST /notifications/read-all/` | Authenticated | Mark all own as read |

---

## Database Schema

### Like Table
```sql
CREATE TABLE posts_like (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    post_id INTEGER NOT NULL REFERENCES posts_post(id),
    created_at DATETIME NOT NULL,
    UNIQUE(user_id, post_id)
);
```

### Notification Table
```sql
CREATE TABLE notifications_notification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    actor_id INTEGER NOT NULL REFERENCES accounts_customuser(id),
    verb VARCHAR(255) NOT NULL,
    target_content_type_id INTEGER REFERENCES django_content_type(id),
    target_object_id INTEGER,
    timestamp DATETIME NOT NULL,
    read BOOLEAN NOT NULL DEFAULT 0
);
```

---

## Best Practices

### For Frontend Developers

1. **Polling for Notifications:**
   ```javascript
   // Poll unread notifications every 30 seconds
   setInterval(async () => {
       const unread = await getUnreadNotifications();
       updateNotificationBadge(unread.length);
   }, 30000);
   ```

2. **Optimistic UI Updates:**
   ```javascript
   // Immediately update UI, then sync with server
   function likePost(postId) {
       // Update UI immediately
       incrementLikeCount(postId);
       setLiked(postId, true);
       
       // Send request
       fetch(`/api/posts/${postId}/like/`, {...})
           .catch(error => {
               // Revert on error
               decrementLikeCount(postId);
               setLiked(postId, false);
           });
   }
   ```

3. **Notification Display:**
   - Show unread notifications prominently
   - Mark as read when user views them
   - Provide "clear all" functionality
   - Link notifications to their targets

### For Backend Developers

1. **Performance Optimization:**
   - Use `select_related()` and `prefetch_related()` for notifications
   - Add database indexes for frequent queries
   - Consider caching notification counts

2. **Notification Management:**
   - Clean up old read notifications periodically
   - Prevent duplicate notifications
   - Batch notification creation when possible

3. **Security:**
   - Always verify ownership before marking as read
   - Validate post existence before liking
   - Rate limit notification endpoints

---

## Troubleshooting

### Common Issues

**Issue: "You have already liked this post"**
- **Cause:** Trying to like a post twice
- **Solution:** Check if user has already liked before sending request

**Issue: "Notification not found"**
- **Cause:** Trying to access another user's notification
- **Solution:** Ensure notification belongs to authenticated user

**Issue: Notifications not appearing**
- **Cause:** Content type not set correctly
- **Solution:** Verify GenericForeignKey setup and content type imports

**Issue: High database load**
- **Cause:** Too many notification queries
- **Solution:** Implement pagination and caching

---

## Future Enhancements

1. **Real-time Notifications:**
   - Implement WebSocket support
   - Use Django Channels for live updates
   - Push notifications to mobile devices

2. **Notification Preferences:**
   - Allow users to customize notification types
   - Email notifications for important events
   - Notification grouping and summarization

3. **Advanced Like Features:**
   - Multiple reaction types (love, laugh, etc.)
   - Like analytics for post authors
   - Trending posts based on likes

4. **Notification Analytics:**
   - Track notification open rates
   - User engagement metrics
   - Notification delivery timing optimization

---

## Conclusion

The likes and notifications system provides essential social features for user engagement. It enables users to interact with content through likes and stay informed about platform activities through real-time notifications. The system is built with scalability, security, and user experience in mind.

For additional support or questions, refer to the main API documentation or contact the development team.
