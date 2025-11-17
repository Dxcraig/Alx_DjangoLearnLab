"""
accounts.models: custom user model moved to `bookshelf.models.CustomUser`.

The project previously defined `CustomUser` here. It was relocated to
`bookshelf.models` per the user's request. Keep this file to avoid import
errors from references to the `accounts` app; remove or rework migrations if
you need a clean app model migration history.
"""
