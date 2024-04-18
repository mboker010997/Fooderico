from nltk.corpus import wordnet
from transformers import pipeline


class SynonymFinder:
    def __init__(self):
        self.translator = pipeline(
            "translation", model="Helsinki-NLP/opus-mt-ru-en"
        )

    def to_english(self, text):
        return self.translator(text, max_length=40)[0]["translation_text"]

    def are_synonyms(self, word1, word2):
        synonyms = []
        word1 = self.to_english(word1)
        word2 = self.to_english(word2)

        for syn in wordnet.synsets(word1):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())

        return word2 in synonyms
