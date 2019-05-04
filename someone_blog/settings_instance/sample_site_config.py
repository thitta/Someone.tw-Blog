SITE_TITLE = "Someone Blog"

SITE_SUBTITLE = "For Lightweight & Productive Blogging"

NAV_BUTTONS = [
    {
        "text": "Home",
        "url": "/",
        "target": "_self",
    },
]

PLUGINS = {
    "fb_base": {
        "on": False,
        "app_id": "[your app id]",
    },
    "fb_social": {
        "fb_comment": {
            "on": False
        },
        "fb_meta": {
            "on": False
        },
        "fb_like": {
            "on": False
        },
    },
    "gg_tagmanager": {
        "on": False,
        "app_id": "[your app id]",
    }
}
