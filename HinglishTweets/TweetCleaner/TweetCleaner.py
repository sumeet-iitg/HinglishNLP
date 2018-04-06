# -*- coding: utf-8 -*-

import string

import preprocessor as p
from transliteration import getInstance

text = "RT @Pritpal77777: @Gurmeetramrahim GURU JI!! 61210 peoples take pledge to leave their drug and bad deeds n to adopt path of righteousness i\xe2\x80\xa6"
parsed_tweet = p.parse(text)
print(parsed_tweet.hashtags, parsed_tweet.mentions, parsed_tweet.reserved_words)

text = "ke liye best kar rahe hain to apki talash yahan par khatm hoti hai kyonki is post me main apko top video downloader apps ke baare me bataunga jinhe bahut hi aasani se install or use kiya jaa sakta ha."
t = getInstance()
t_text = t.transliterate(text, "hi_IN")
print(t_text)
# urls = None
#     emojis = None
#     smileys = None
#     hashtags = None
#     mentions = None
#     reserved_words = None