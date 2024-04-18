from multi_rake import Rake

train_text = (
    "У меня аллергия на молоко. Люблю играть в футбол. Ищу собесдника."
    "Ненавижу футбольчик, но люблю играть в волейбол. Есть аллергия на сыр."
)


def extract_tags_from_text(text, lang_code):
    rake = Rake(
        max_words=1,
        language_code=lang_code,
    )
    keywords = rake.apply(text, text_for_stopwords=train_text)[:10]
    tags = [tag[0] for tag in keywords]
    return tags
