class Author:
    enable = True
    name = "John Smith"
    description = (
        "This is some description text about the author. "
        "You can change the value in the config file."
    )
    image_url = "https://placeimg.com/180/180/animals"
    url = "/post/1/about"


class Facebook:
    enable = True
    app_id = "[your_app_id]"

    class CommentAndLike:
        enable = True


class GoogleTagManager:
    enable = True
    app_id = "[your_app_id]"
