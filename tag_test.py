# from keybert import KeyBERT
#
# doc = """
#          У меня аллергия на понос и на очко, ищу друга с такими же проблемами
#       """
# kw_model = KeyBERT()
# keywords = kw_model.extract_keywords(doc)
# print(keywords)


from multi_rake import Rake

train_text = (
    'У меня аллергия на молочку. Люблю играть в футбол. Ищу собесдника.'
    'Ненавижу футбольчик, но люблю играть в волейбол. Есть аллергия на сыр.'
)

text_en = (
    'У меня аллергия на молочку. Люблю играть в футбол. Ищу собесдника.'
)

rake = Rake(
    max_words=1,
    language_code='ru',
    generated_stopwords_max_len=11,
)

keywords = rake.apply(text_en, text_for_stopwords=train_text)

print(keywords[:10])
