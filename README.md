### Setup

#### 1. Config file

Place a **setting.py** under root and fill in the blanks.

```
DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = ["db"]
```

#### 2. Sync database schema

Use [Django migration](https://docs.djangoproject.com/en/3.2/topics/migrations/)

#### 3. Set your [YouTube API Key](https://developers.google.com/youtube/registering_an_application)

Set it as environment variable **YOUTUBE_API_KEY** or through init_youtube_client(key)

---

### Entry point

Run [**main.py**](main.py)