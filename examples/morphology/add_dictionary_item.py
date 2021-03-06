"""
Zemberek: Adding Dictionary Item Example
Java Code Example: https://bit.ly/2qTlmXb
"""
from typing import List

from jpype import JClass, JString

__all__: List[str] = ['run']

TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
DictionaryItem: JClass = JClass('zemberek.morphology.lexicon.DictionaryItem')
RootAttribute: JClass = JClass('zemberek.core.turkish.RootAttribute')
PrimaryPos: JClass = JClass('zemberek.core.turkish.PrimaryPos')
SecondaryPos: JClass = JClass('zemberek.core.turkish.SecondaryPos')
WordAnalysis: JClass = JClass('zemberek.morphology.analysis.WordAnalysis')


def print_results(results: WordAnalysis) -> None:
    """
    Prints analysis results.

    Args:
        results (WordAnalysis): Analysis results.
    """
    if results.analysisCount() == 0:
        print('No Analysis')
    for i, result in enumerate(results, 1):
        rstr: str = str(result.formatLong())
        if result.getDictionaryItem().attributes.contains(
            RootAttribute.Runtime
        ):
            rstr += ' (Generated by UnidentifiedTokenParser)\n'
        print(f'{i} - {rstr}')


def _test(
    morphology: TurkishMorphology, inp: str, new_item: DictionaryItem
) -> None:
    """
    Testing analysis before and after adding dictionary item.

    Args:
        morphology (TurkishMorphology): Turkish morphology analyzer.
        inp (str): Input to analyze.
        new_item (DictionaryItem): Item to add to the dictionary.
    """
    print(f'Parses for {inp} before adding {new_item}')
    before: WordAnalysis = morphology.analyze(JString(inp))
    print_results(before)
    morphology.invalidateCache()
    morphology.getMorphotactics().getStemTransitions().addDictionaryItem(
        new_item
    )
    after: WordAnalysis = morphology.analyze(inp)
    print(f'Parses for {inp} after adding {new_item}')
    print_results(after)


def run() -> None:
    """
    Dictionary item addition tests.
    """

    morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()

    print('\nProper Noun Test - 1:\n')
    _test(
        morphology,
        'Meydan\'a',
        DictionaryItem(
            JString('Meydan'),
            JString('meydan'),
            JString('meydan'),
            PrimaryPos.Noun,
            SecondaryPos.ProperNoun,
        ),
    )

    print('\nProper Noun Test - 2:\n')
    _test(
        morphology,
        'Meeeydan\'a',
        DictionaryItem(
            JString('Meeeydan'),
            JString('meeeydan'),
            JString('meeeydan'),
            PrimaryPos.Noun,
            SecondaryPos.ProperNoun,
        ),
    )

    print('\nVerb Test:\n')
    _test(
        morphology,
        'tweetleyeyazd??m',
        DictionaryItem(
            JString('tweetlemek'),
            JString('tweetle'),
            JString('tivitle'),
            PrimaryPos.Verb,
            SecondaryPos.None_,
        ),
    )
