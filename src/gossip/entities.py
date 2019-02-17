from collections import deque
from dataclasses import dataclass
import enum
from typing import Union

from bs4 import element, BeautifulSoup


class TermType(enum.Enum):
    bold = enum.auto()
    plain = enum.auto()


@dataclass
class Source:
    outlet: str
    link: str


class Paragraph:
    def __init__(self, paragraph: Union[str, element.Tag]):
        if isinstance(paragraph, str):
            paragraph = BeautifulSoup(paragraph)

        self.paragraph = paragraph

        self.bold_terms = []
        self.plain_terms = []
        self.term_ordering = []

        self.parse_terms()

        self.source = get_source(self.paragraph)

    def parse_terms(self):
        """
        Populate `self.bold_terms`, `self.plain_terms` and `self.term_ordering`.

        Terms may be words but also phrases, e.g. "Manchester United", "Everton", or "is about to join".

        `self.bold_terms` is a list of the bold terms in self.paragraph.

        `self.plain_terms` is a list of all plain terms in self.paragraph.

        `self.term_ordering` is a list denoting the ordering of the terms in the paragraph as a whole.
        For example, [TermType.bold, TermType.plain, TermType.bold] indicates that the paragraph
        consists of the first element of `self.bold_terms` then the first element of `self.plain_terms`
        and finally the second element of `self.bold_terms`.
        """
        first_element = self.paragraph.next_element
        self.parse_element(first_element)

        for sibling in first_element.next_siblings:
            if self.is_plaintext(sibling) or self.is_bold(sibling):
                self.parse_element(sibling)

    def parse_element(self, paragraph_element: Union[element.NavigableString, element.Tag]):
        term = None

        if self.is_plaintext(paragraph_element):
            self.plain_terms.append(str(paragraph_element))
            term = TermType.plain
        elif self.is_bold(paragraph_element):
            bold_string = str(paragraph_element.string)
            self.bold_terms.append(bold_string)
            term = TermType.bold
        else:
            pass  # TODO: log do nothing

        if term is not None:
            self.term_ordering.append(term)

    def is_bold(self, paragraph_element: Union[element.NavigableString, element.Tag]):
        return isinstance(paragraph_element, element.Tag) and paragraph_element.name == 'b'

    def is_plaintext(self, paragraph_element: Union[element.NavigableString, element.Tag]):
        return isinstance(paragraph_element, element.NavigableString)

    def build_paragraph_words(self, show_bold=False):
        bold_terms = deque(self.bold_terms)
        plain_terms = deque(self.plain_terms)

        all_terms = []

        for term_type in self.term_ordering:
            if term_type is TermType.bold:
                if show_bold:
                    term = f'*{bold_terms.popleft()}*'
                else:
                    term = bold_terms.popleft()
            else:
                term = plain_terms.popleft()

            all_terms.append(term)

        return all_terms

    def build_paragraph(self, show_bold=False):
        paragraph_words = self.build_paragraph_words(show_bold)
        return ''.join(paragraph_words)

    def __bool__(self):
        return bool(self.term_ordering)


def get_source(paragraph: element.Tag):
    source_anchor = paragraph.find('a')

    link = source_anchor['href']
    outlet = None

    # element.Tag.string only works if the tag has a single child,
    # however, source_anchor typically contains a <i/> tag.
    for content in source_anchor.contents:
        if isinstance(content, element.NavigableString):
            outlet = str(content).strip('()')
            break

    return Source(outlet=outlet, link=link)
