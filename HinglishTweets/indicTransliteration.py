# -*- coding: utf-8 -*-
# The path to the local git repo for Indic NLP library
INDIC_NLP_LIB_HOME="C:/Users/Sumeet Singh/PycharmProjects/IndicNlp/indic_nlp_library"

# The path to the local git repo for Indic NLP Resources
INDIC_NLP_RESOURCES="C:/Users/Sumeet Singh/PycharmProjects/IndicNlp/indic_nlp_resources"

import sys
sys.path.append('{}/src'.format(INDIC_NLP_LIB_HOME))

from indicnlp import common
common.set_resources_path(INDIC_NLP_RESOURCES)

import unicodedata
import sys
from indicnlp.transliterate.unicode_transliterate import ItransTransliterator

from indicnlp.normalize.indic_normalize import IndicNormalizerFactory


# input_text=u"एक्सेर्साइसर सर्वाधिकार © 2006 , 2007 आईबीएम निगम ( बीएसडी )"
# remove_nuktas = True
# factory = IndicNormalizerFactory()
# normalizer = factory.get_normalizer("hi", remove_nuktas)
# norm_text = normalizer.normalize(input_text)
# lang = 'hi'
# print sys.stdout.encoding
# print ItransTransliterator.to_itrans(norm_text, lang).encode(sys.stdout.encoding, errors='replace')

# def transliterate_file()
# with open("C:/Users/Sumeet Singh/Documents/Code-Mixed/DataSets/IITBparallel/parallel/IITB.en-hi.hi") as fp:
#     input_text = fp.readline().decode("utf-8")
#     lang = "hi"
#     while input_text:
#         remove_nuktas = True
#         factory = IndicNormalizerFactory()
#         normalizer = factory.get_normalizer("hi", remove_nuktas)
#         norm_text = normalizer.normalize(input_text)
#         translit_text = ItransTransliterator.to_itrans(norm_text, lang)
#         with open("C:/Users/Sumeet Singh/Documents/Code-Mixed/DataSets/IITBparallel/parallel/IITB.en-hi.tl", 'a') as w:
#             w.write(translit_text.encode("utf-8"))
#         input_text = fp.readline().decode("utf-8")

input_text=u"ke liye best kar rahe hain to apki talash yahan par khatm hoti hai kyonki is post me main apko top video downloader apps ke baare me bataunga jinhe bahut hi aasani se install or use kiya jaa sakta ha"
remove_nuktas = True
lang = 'hi'

translit_text = ItransTransliterator.from_itrans(input_text, lang) #.encode(sys.stdout.encoding, errors='replace')
factory = IndicNormalizerFactory()
normalizer = factory.get_normalizer("hi", remove_nuktas)
norm_text = normalizer.normalize(translit_text)

print norm_text.encode('utf-8')
