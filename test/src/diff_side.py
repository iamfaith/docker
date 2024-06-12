
import difflib
import itertools
import textwrap
import typing

from typing import List, Tuple, Iterator


class Sdiffer:
    def __init__(self, max_width:int = 80):
        # Two columns with a gutter
        self._col_width = (max_width - 3) // 2
        assert self._col_width > 0
        self.diff_lines_cnt = 0
        
    def _fit(self, s: str) -> str:
        s = s.rstrip()[:self._col_width]
        return  f"{s: <{self._col_width}}"

    def sdiff(self, a: List[str], b: List[str]) -> Iterator[str]:
        diff_lines = difflib.Differ().compare(a, b)
        diff_table: List[Tuple[str, List[str], List[str]]] = []
        for diff_type, line_group in itertools.groupby(diff_lines, key=lambda ln: ln[:1]):
            lines = [ln[2:] for ln in line_group]
            if diff_type == " ":
                diff_table.append((" ", lines, lines))
            else:
                if not diff_table or diff_table[-1][0] != "|":
                    diff_table.append(("|", [], []))
                if diff_type == "-":
                    # Lines only in `a`
                    diff_table[-1][1].extend(lines)
                elif diff_type == "+":
                    # Lines only in `b`
                    diff_table[-1][2].extend(lines)
        idx = 1
        for diff_type, cell_a, cell_b in diff_table:
            for left, right in itertools.zip_longest(cell_a, cell_b, fillvalue=""):  
                if diff_type == "|":
                    self.diff_lines_cnt += 1
                yield f"{idx:<5}{self._fit(left)} {diff_type} {self._fit(right)}"
                idx += 1
    
    def print_sdiff(self, a: List[str], b: List[str]) -> Iterator[str]:
        print("\n".join(self.sdiff(a, b)))
        

def side_by_side(
    left: typing.List[str],
    right: typing.List[str],
    width: int = 78,
    as_string: bool = False,
    separator: typing.Optional[str] = " | ",
    left_title: typing.Optional[str] = None,
    right_title: typing.Optional[str] = None,
) -> typing.Union[str, typing.List[str]]:
    """Returns either the list of lines, or string of lines, that results from
    merging the two lists side-by-side.
    :param left: Lines of text to place on the left side
    :type left: typing.List[str]
    :param right: Lines of text to place on the right side
    :type right: typing.List[str]
    :param width: Character width of the overall output, defaults to 78
    :type width: int, optional
    :param as_string: Whether to return a string (as opposed to a list of strings), defaults to False
    :type as_string: bool, optional
    :param separator: String separating the left and right side, defaults to " | "
    :type separator: typing.Optional[str], optional
    :param left_title: Title to place on the left side, defaults to None
    :type left_title: typing.Optional[str], optional
    :param right_title: Title to place on the right side, defaults to None
    :type right_title: typing.Optional[str], optional
    :return: Lines or text of the merged side-by-side output.
    :rtype: typing.Union[str, typing.List[str]]
    """

    DEFAULT_SEPARATOR = " | "
    separator = separator or DEFAULT_SEPARATOR

    mid_width = (width - len(separator) - (1 - width % 2)) // 2

    tw = textwrap.TextWrapper(
        width=mid_width,
        break_long_words=False,
        replace_whitespace=False
    )

    def reflow(lines):
        wrapped_lines = list(map(tw.wrap, lines))
        wrapped_lines_with_linebreaks = [
            [""] if len(wls) == 0 else wls
            for wls in wrapped_lines
        ]
        return list(itertools.chain.from_iterable(wrapped_lines_with_linebreaks))

    left = reflow(left)
    right = reflow(right)

    zip_pairs = itertools.zip_longest(left, right)
    if left_title is not None or right_title is not None:
        left_title = left_title or ""
        right_title = right_title or ""
        zip_pairs = [
            (left_title, right_title),
            (mid_width * "-", mid_width * "-")
        ] + list(zip_pairs)

    lines = []
    for l, r in zip_pairs:
        l = l or ""
        r = r or ""
        line = "{}{}{}{}".format(
            l,
            (" " * max(0, mid_width - len(l))),
            separator,
            r
        )
        lines.append(line)

    if as_string:
        return "\n".join(lines)

    return lines


def better_diff(
    left: typing.List[str],
    right: typing.List[str],
    width: int = 78,
    as_string: bool = False,
    separator: typing.Optional[str] = None,
    left_title: typing.Optional[str] = None,
    right_title: typing.Optional[str] = None,
) -> typing.Union[str, typing.List[str]]:
    """Returns a side-by-side comparison of the two provided inputs, showing
    common lines between both inputs, and the lines that are unique to each.
    :param left: Lines of text to place on the left side
    :type left: typing.List[str]
    :param right: Lines of text to place on the right side
    :type right: typing.List[str]
    :param width: Character width of the overall output, defaults to 78
    :type width: int, optional
    :param as_string: Whether to return a string (as opposed to a list of strings), defaults to False
    :type as_string: bool, optional
    :param separator: String separating the left and right side, defaults to " | "
    :type separator: typing.Optional[str], optional
    :param left_title: Title to place on the left side, defaults to None
    :type left_title: typing.Optional[str], optional
    :param right_title: Title to place on the right side, defaults to None
    :type right_title: typing.Optional[str], optional
    :return: Lines or text of the merged side-by-side diff comparison output.
    :rtype: typing.Union[str, typing.List[str]]
    """

    differ = difflib.Differ()

    left_side = []
    right_side = []

    # adapted from
    # LINK: https://stackoverflow.com/a/66091742/408734
    difflines = list(differ.compare(left, right))

    for line in difflines:
        op = line[0]
        tail = line[2:]
        if op == " ":
            # line is same in both
            left_side.append(tail)
            right_side.append(tail)

        elif op == "-":
            # line is only on the left
            left_side.append(tail)
            right_side.append("")

        elif op == "+":
            # line is only on the right
            left_side.append("")
            right_side.append(tail)

    return side_by_side(
        left=left_side,
        right=right_side,
        width=width,
        as_string=as_string,
        separator=separator,
        left_title=left_title,
        right_title=right_title,
    )