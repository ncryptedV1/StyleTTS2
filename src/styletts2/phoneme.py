from gruut import sentences
from collections.abc import Iterable
from espeakng import ESpeakNG


class PhonemeConverter:
    def phonemize(self, text):
        pass


class GruutPhonemizer(PhonemeConverter):
    def phonemize(self, text, lang='en-us', ssml: bool = False, espeak: bool = False):
        phonemized = []
        for sent in sentences(text, lang=lang, ssml=ssml, espeak=espeak):
            for word in sent:
                if isinstance(word.phonemes, Iterable):
                    phonemized.append(''.join(word.phonemes))
                elif isinstance(word.phonemes, str):
                    phonemized.append(word.phonemes)
        phonemized_text = ' '.join(phonemized)
        return phonemized_text

class ESpeakPhonemizer(PhonemeConverter):
    def __init__(self, volume: int = 100, speed: int = 175):
        self.phonemizer = ESpeakNG(volume=volume, speed=speed)

    def phonemize(self, text, lang='english-us'):
        self.phonemizer._voice = lang
        phonemized_text = self.phonemizer.g2p(text, ipa=2)
        return phonemized_text

# class YourPhonemizer(Phonemizer):
#     def phonemize(self, text):
#         ...


class PhonemeConverterFactory:
    @staticmethod
    def load_phoneme_converter(name: str, **kwargs):
        if name == 'gruut':
            return GruutPhonemizer(**kwargs)
        elif name == 'espeak':
            return ESpeakPhonemizer(**kwargs)
        else:
            raise ValueError("Invalid phoneme converter.")