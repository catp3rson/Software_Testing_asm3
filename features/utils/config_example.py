# -*- coding: utf-8 -*-
# supported browsers: ["CHROME", "FIREFOX", "EDGE", "IE"]
CONFIG = {
    "DRIVERS": {
        "DOMAINS": {
            "BKEL": {"name": "e-learning.hcmut.edu.vn"},
            "SSO": {"name": "sso.hcmut.edu.vn", "username": "", "password": ""},
        },
        "BROWSERS": {
            "CHROME": {
                # configuration options for browser specified here will override DEFAULT_CONFIG
                # try uncomment the option below and observe the difference :)
                # "HEADLESS": False
            },
            "FIREFOX": {},
            "EDGE": {},
        },
        "DEFAULT_CONFIG": {
            "HEADLESS": True,
            "WINDOW_SIZE": (1920, 1080),
            "MAXIMIZE_WINDOW": True,
        },
        "DEFAULT_BROWSER": "FIREFOX",
    },
    "DATA": {"DATA_DIR": ""},
}
