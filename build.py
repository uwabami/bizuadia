#!/usr/bin/python3

import subprocess
from typing import Any, Tuple
import psMat
import fontforge

VERSION = "v0.0.1"
FONT_NAME = "BIZUDIA"

BUILD_TMP = "tmp"
DISTS     = "dists"
SOURCE_DIR = "source_fonts"
SOURCE_FONT_JP = "BIZUDGothic-{}.ttf"
SOURCE_FONT_EN = "CascadiaMono-{}.ttf"
SOURCE_FONT_EMOJI = "NotoEmoji-{}.ttf"
SOURCE_FONT_ICON = "isfit-plus.ttf"
SOURCE_SPACE_FONT = "ideographic_space.sfd"
SPACE_FONT = "ideographic_space.ttf"



EM_ASCENT = 1802
EM_DESCENT = 246

FONT_ASCENT = EM_ASCENT   # + 60
FONT_DESCENT = EM_DESCENT # + 170

EN_FONT_OLD_WIDTH=1200
EN_FONT_NEW_WIDTH=1024
EN_FONT_SCALE_DOWN = float(EN_FONT_NEW_WIDTH) / EN_FONT_OLD_WIDTH

EMOJI_OLD_WIDTH = 2600
EMOJI_NEW_WIDTH = 2048
EMOJI_SCALE_DOWN = float(EMOJI_NEW_WIDTH) / EMOJI_OLD_WIDTH

ICON_OLD_WIDTH = 1700
ICON_NEW_WIDTH = 2048
# ICON_SCALE_= float(ICON_NEW_WIDTH) / ICON_OLD_WIDTH
ICON_SCALE = 0.9  #?


COPYRIGHT = """[CascadiaMono]
Copyright (c) 2019 - Present, Microsoft Corporation, with Reserved Font Name Cascadia Code (https://github.com/microsoft/cascadia-code)

[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[Noto Emoji]
Copyright 2013-2017 Google Inc., Arjen Nienhuis <a.g.nienhuis@gmail.com> (https://github.com/googlefonts/noto-emoji)

[ideographic_space.sfd]
Copyright (c) 2022 Yuko OTAWARA. with Reserved Font Name "UDEV Gothic" (https://github.com/yuru7/udev-gothic/)

[bizudia]
Copyright 2023 Youhei SASAKI <uwabami@gfd-dennou.org>
"""


def open_font(weight) -> Tuple[Any, Any]:
    """フォントファイルを開く"""
    jp_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_FONT_JP.format(weight)}")
    en_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_FONT_EN.format(weight)}")
    emoji_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_FONT_EMOJI.format(weight)}")
    icon_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_FONT_ICON}")
    space_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_SPACE_FONT}")
    return jp_font, en_font, emoji_font, space_font, icon_font


def remove_duplicate_glyphs(jp_font, en_font):
    """重複しているグリフを削除する. ただし幾つかの全角記号は残す"""
    for g in en_font.glyphs():
        if not g.isWorthOutputting():
            continue
        unicode = int(g.unicode)
        if unicode >= 0:
            if unicode == 0x00A7:           # §
                continue
            if unicode == 0x00B1:           # ±
                continue
            if unicode == 0x00B6:           # ¶
                continue
            if unicode == 0x00F7:           # ÷
                continue
            if unicode == 0x00D7:           # ×
                continue
            if unicode == 0x21D2:           # ⇒
                continue
            if unicode == 0x21D4:           # ⇔
                continue
            if 0x25A0 <= unicode <= 0x25A1: # ■-□
                continue
            if 0x25B2 <= unicode <= 0x25B3: # ▲-△
                continue
            if 0x25B6 <= unicode <= 0x25B7: # ▲-△
                continue
            if 0x25BC <= unicode <= 0x25BD: # ▼-▽
                continue
            if 0x25C0 <= unicode <= 0x25C1: # ▼-▽
                continue
            if 0x25C6 <= unicode <= 0x25C7: # ◆-◇
                continue
            if unicode == 0x25CB:           # ○
                continue
            if 0x25CE <= unicode <= 0x25CF: # ◎-●
                continue
            if unicode == 0x25E5:           # ◥
                continue
            if unicode == 0x25EF:           # ◯
                continue
            if unicode == 0x221A:           # √
                continue
            if unicode == 0x221E:           # ∞
                continue
            if unicode == 0x2010:           # ‐
                continue
            if 0x2018 <= unicode <= 0x201A: # ‘-‚
                continue
            if 0x201C <= unicode <= 0x201E: # “-„
                continue
            if 0x2020 <= unicode <= 0x2021: # †-‡
                continue
            if unicode == 0x2026:           # …
                continue
            if unicode == 0x2030:           # ‰
                continue
            if 0x2190 <= unicode <= 0x2193:  # ←-↓
                continue
            if unicode == 0x2200:           # ∀
                continue
            if 0x2202 <= unicode <= 0x2203: # ∂-∃
                continue
            if unicode == 0x2208:           # ∈
                continue
            if unicode == 0x220B:           # ∋
                continue
            if unicode == 0x2211:           # ∑
                continue
            if unicode == 0x2225:           # ∥
                continue
            if 0x2227 <= unicode <= 0x222C: # ∧-∬
                continue
            if 0x2260 <= unicode <= 0x2261: # ≠-≡
                continue
            if 0x2282 <= unicode <= 0x2283: # ⊂-⊃
                continue
            if 0x2286 <= unicode <= 0x2287: # ⊆-⊇
                continue
            if 0x2500 <= unicode <= 0x257F: # ─-╿ (Box Drawing)
                continue
            else:
                for g_jp in jp_font.selection.select(unicode).byGlyphs:
                    g_jp.clear()


def merge_fonts(jp_font, en_font, emoji_font, space_font, icon_font, weight) -> Any:
    """英語フォント, 絵文字, 日本語フォントをマージする"""
    # マージするためにemを揃える
    em_size = EM_ASCENT + EM_DESCENT

    en_font.em = em_size
    mat = psMat.scale(EN_FONT_SCALE_DOWN)
    en_font.selection.all()
    for glyph in list(en_font.selection.byGlyphs):
        glyph.transform(mat)
        glyph.width = EN_FONT_NEW_WIDTH
    en_font.generate(f"{BUILD_TMP}/modified_{SOURCE_FONT_EN.format(weight)}")

    emoji_font.em = em_size
    mat = psMat.scale(EMOJI_SCALE_DOWN)
    emoji_font.selection.all()
    for glyph in list(emoji_font.selection.byGlyphs):
        glyph.transform(mat)
        glyph.width = EMOJI_NEW_WIDTH
    emoji_font.generate(f"{BUILD_TMP}/modified_{SOURCE_FONT_EMOJI.format(weight)}")

    icon_font.em = em_size
    mat = psMat.scale(ICON_SCALE)
    icon_font.selection.all()
    for glyph in list(icon_font.selection.byGlyphs):
        glyph.transform(mat)
        glyph.width = ICON_NEW_WIDTH
    icon_font.generate(f"{BUILD_TMP}/modified_{SOURCE_FONT_ICON.format(weight)}")

    space_font.em = em_size
    space_font.generate(f"{BUILD_TMP}/modified_{SPACE_FONT}")

    jp_font.em = em_size
    # 全角スペース削除
    jp_font.selection.none()
    jp_font.selection.select(0x3000)
    jp_font.clear()
    jp_font.selection.none()

    # merge
    jp_font.mergeFonts(f"{BUILD_TMP}/modified_{SOURCE_FONT_EN.format(weight)}")
    jp_font.mergeFonts(f"{BUILD_TMP}/modified_{SPACE_FONT}")
    jp_font.mergeFonts(f"{BUILD_TMP}/modified_{SOURCE_FONT_ICON}")
    jp_font.mergeFonts(f"{BUILD_TMP}/modified_{SOURCE_FONT_EMOJI.format(weight)}")
    return jp_font


def edit_meta_data(font, weight: str):
    """フォント内のメタデータを編集する"""
    font.ascent = EM_ASCENT
    font.descent = EM_DESCENT
    font.os2_typoascent = EM_ASCENT
    font.os2_typodescent = -EM_DESCENT

    font.hhea_ascent = FONT_ASCENT
    font.hhea_descent = -FONT_DESCENT
    font.os2_winascent = FONT_ASCENT
    font.os2_windescent = FONT_DESCENT
    font.hhea_linegap = 0
    font.os2_typolinegap = 0

    font.sfnt_names = (
        (
            "English (US)",
            "License",
            "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL",
        ),
        ("English (US)", "License URL", "http://scripts.sil.org/OFL"),
        ("English (US)", "Version", f"{FONT_NAME} {VERSION}"),
    )
    font.familyname = FONT_NAME
    font.os2_family_class = 2057  # SS Typewriter Gothic
    font.fontname = f"{FONT_NAME}-{weight}"
    font.fullname = f"{FONT_NAME} {weight}"
    font.os2_vendor = "YS"
#    font.encoding = "UnicodeFull"
    font.copyright = COPYRIGHT
    if weight == "Regular":
        font.weight = "Book"
        font.os2_weight = 400
        font.os2_panose = (
            2,  # Latin: Text and Display
            11, # Nomal Sans
            5,
            9,  # Monospaced
            2,  # None
            2,  # No Variation
            3,  # Straight Arms/Wedge
            2,
            2,  # Standard/Trimmed
            7,  # Ducking/Large
        )
        font.os2_stylemap = 0b0001000000
        font.macstyle = 0b00
    else:
        font.weight = "Bold"
        font.os2_weight = 700
        font.os2_panose = (
            2,  # Latin: Text and Display
            11, # Nomal Sans
            8,
            9,  # Monospaced
            2,  # None
            2,  # No Variation
            3,  # Straight Arms/Wedge
            2,
            2,  # Standard/Trimmed
            7,  # Ducking/Large
        )
        font.os2_stylemap = 0b0001000000
        font.macstyle = 0b01

def main():
    # TODO: tmpフォルダを作って final で削除する

    for weight in ("Regular", "Bold"):
        jp_font, en_font, emoji_font, space_font, icon_font = open_font(weight)

        remove_duplicate_glyphs(jp_font, en_font)

        font = merge_fonts(jp_font, en_font, emoji_font, space_font, icon_font, weight)

        edit_meta_data(font, weight)

        font.generate(f"{BUILD_TMP}/gen_{FONT_NAME}-{weight}.ttf")

        subprocess.run(
            (
                "ttfautohint",
                "--dehint",
                f"{BUILD_TMP}/gen_{FONT_NAME}-{weight}.ttf",
                f"{DISTS}/{FONT_NAME}-{weight}.ttf",
            )
        )


if __name__ == "__main__":
    main()
