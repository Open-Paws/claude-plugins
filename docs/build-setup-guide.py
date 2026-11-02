#!/usr/bin/env python3
"""Build the printable setup guide (open-paws-tools-setup-guide.pdf).

The guide is the README's setup steps written for people who don't work with
code, in a form you can email or print. The README stays the source of truth:
when the connector URL, the steps or the data notice change there, change them
here too and rebuild.

    python3 -m venv .venv
    .venv/bin/pip install reportlab pillow
    .venv/bin/python docs/build-setup-guide.py

Fonts come from macOS (Arial, Menlo). On another platform, point FONTS at
equivalents.
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "open-paws-tools-setup-guide.pdf")
LOGO = os.path.join(HERE, "assets", "openpaws-logo.png")

CONNECTOR_URL = "https://tools-api-production-71f4.up.railway.app/mcp"
MARKETPLACE_URL = "https://github.com/Open-Paws/claude-plugins"

# Brand palette, taken from the Open Paws website.
TEAL = colors.HexColor("#006C67")
TEAL_DARK = colors.HexColor("#00534F")
ORANGE = colors.HexColor("#FF8552")
PEACH = colors.HexColor("#FFE1D1")
INK = colors.HexColor("#17201F")
MUTED = colors.HexColor("#5C6B6A")
MIST = colors.HexColor("#F1F5F4")
LINE = colors.HexColor("#DCE5E3")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

FONTS = {
    "Body": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "Body-Bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "Body-Italic": "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
    "Mono": "/System/Library/Fonts/Menlo.ttc",
}


def register_fonts():
    for name, path in FONTS.items():
        if path.endswith(".ttc"):
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=0))
        else:
            pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(
        "Body", normal="Body", bold="Body-Bold", italic="Body-Italic"
    )


def styles():
    base = ParagraphStyle(
        "base",
        fontName="Body",
        fontSize=10.5,
        leading=15.5,
        textColor=INK,
        alignment=TA_LEFT,
    )
    return {
        "title": ParagraphStyle(
            "title", base, fontName="Body-Bold", fontSize=26, leading=30,
            textColor=TEAL_DARK, spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", base, fontSize=12.5, leading=18, textColor=MUTED,
        ),
        "eyebrow": ParagraphStyle(
            "eyebrow", base, fontName="Body-Bold", fontSize=8.5, leading=11,
            textColor=ORANGE,
        ),
        "section": ParagraphStyle(
            "section", base, fontName="Body-Bold", fontSize=15, leading=19,
            textColor=TEAL_DARK, spaceBefore=4, spaceAfter=2,
        ),
        "lede": ParagraphStyle("lede", base, textColor=MUTED, spaceAfter=2),
        "body": base,
        "card_title": ParagraphStyle(
            "card_title", base, fontName="Body-Bold", fontSize=11.5, leading=15,
            textColor=TEAL_DARK, spaceAfter=1,
        ),
        "card_body": ParagraphStyle(
            "card_body", base, fontSize=10, leading=14.5, textColor=INK,
        ),
        "meta": ParagraphStyle(
            "meta", base, fontSize=9, leading=12.5, textColor=MUTED,
        ),
        "step_title": ParagraphStyle(
            "step_title", base, fontName="Body-Bold", fontSize=12.5, leading=16,
            textColor=INK, spaceAfter=3,
        ),
        "callout_title": ParagraphStyle(
            "callout_title", base, fontName="Body-Bold", fontSize=10.5,
            leading=14.5, textColor=INK, spaceAfter=2,
        ),
        "mono": ParagraphStyle(
            "mono", base, fontName="Mono", fontSize=10, leading=14,
            textColor=TEAL_DARK,
        ),
        "mono_small": ParagraphStyle(
            "mono_small", base, fontName="Mono", fontSize=9.5, leading=15,
            textColor=TEAL_DARK,
        ),
        "strip": ParagraphStyle(
            "strip", base, fontName="Body-Bold", fontSize=10.5, leading=14,
            textColor=INK,
        ),
    }


S = None  # populated in main()


class Rule(Flowable):
    """A hairline the width of the frame."""

    def __init__(self, color=LINE, thickness=0.75, space_before=0, space_after=0):
        Flowable.__init__(self)
        self.color = color
        self.thickness = thickness
        self.space_before = space_before
        self.space_after = space_after
        self.width = 0

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.thickness + self.space_before + self.space_after

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self.space_after
        self.canv.line(0, y, self.width, y)


class StepNumber(Flowable):
    """A filled circle with the step number in it."""

    SIZE = 24

    def __init__(self, number):
        Flowable.__init__(self)
        self.number = str(number)
        self.width = self.SIZE
        self.height = self.SIZE

    def wrap(self, aw, ah):
        return self.SIZE, self.SIZE

    def draw(self):
        r = self.SIZE / 2.0
        self.canv.setFillColor(TEAL)
        self.canv.circle(r, r, r, stroke=0, fill=1)
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Body-Bold", 12.5)
        self.canv.drawCentredString(r, r - 4.4, self.number)


def arrow(*parts):
    """Menu path, e.g. Customize > Connectors."""
    sep = ' <font color="#8FA3A1">&#8250;</font> '
    return sep.join("<b>%s</b>" % p for p in parts)


def tool_cards(items):
    """Three columns of (title, body, meta), with the meta lines on one baseline."""
    rows = [
        [Paragraph(t, S["card_title"]) for t, _, _ in items],
        [Paragraph(b, S["card_body"]) for _, b, _ in items],
        [Paragraph(m, S["meta"]) for _, _, m in items],
    ]
    t = Table(rows, colWidths=[CONTENT_W / 3.0] * 3)
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, 1), "TOP"),
                ("VALIGN", (0, 2), (-1, 2), "BOTTOM"),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("LEFTPADDING", (1, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, 0), 10),
                ("TOPPADDING", (0, 1), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
                ("BOTTOMPADDING", (0, 2), (-1, 2), 2),
                ("LINEBEFORE", (1, 0), (-1, -1), 0.75, LINE),
            ]
        )
    )
    return t


def step_strip(items):
    """A compact preview of the steps: number, then label."""
    cells = []
    for i, label in enumerate(items, start=1):
        inner = Table(
            [[StepNumber(i), Paragraph(label, S["strip"])]], colWidths=[34, None]
        )
        inner.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        cells.append(inner)
    t = Table([cells], colWidths=[CONTENT_W / 3.0] * 3)
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("LEFTPADDING", (1, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    return t


def callout(title, body, bg=PEACH, bar=ORANGE):
    inner = Table(
        [[Paragraph(title, S["callout_title"])], [Paragraph(body, S["card_body"])]],
        colWidths=[CONTENT_W - 26],
    )
    inner.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    outer = Table([[inner]], colWidths=[CONTENT_W])
    outer.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    return outer


def closing_band(text):
    style = ParagraphStyle(
        "band", S["body"], fontName="Body-Bold", fontSize=11, leading=15.5,
        textColor=colors.white,
    )
    t = Table([[Paragraph(text, style)]], colWidths=[CONTENT_W])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
            ]
        )
    )
    return t


def code_box(text, style_key="mono", width=None):
    w = width or (CONTENT_W - 44)
    t = Table([[Paragraph(text, S[style_key])]], colWidths=[w])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MIST),
                ("BOX", (0, 0), (-1, -1), 0.75, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return t


def step(number, title, blocks):
    body = [Paragraph(title, S["step_title"])]
    for b in blocks:
        body.append(Paragraph(b, S["body"]) if isinstance(b, str) else b)
        body.append(Spacer(1, 5))
    body.pop()
    t = Table(
        [[StepNumber(number), body]],
        colWidths=[StepNumber.SIZE + 14, CONTENT_W - StepNumber.SIZE - 14],
    )
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return KeepTogether([t, Spacer(1, 16)])


def bullets(items, style_key="body"):
    rows = []
    for it in items:
        rows.append(
            [
                Paragraph('<font color="#FF8552">&#8226;</font>', S[style_key]),
                Paragraph(it, S[style_key]),
            ]
        )
    t = Table(rows, colWidths=[14, CONTENT_W - 14])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def page_furniture(canvas, doc):
    canvas.saveState()
    # Brand bar along the top edge.
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 7, PAGE_W, 7, stroke=0, fill=1)
    # Footer.
    canvas.setFillColor(MUTED)
    canvas.setFont("Body", 8.5)
    canvas.drawString(MARGIN, 13 * mm, "Open Paws  ·  openpaws.ai")
    canvas.drawRightString(
        PAGE_W - MARGIN, 13 * mm, "Page %d of 3" % canvas.getPageNumber()
    )
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.75)
    canvas.line(MARGIN, 16 * mm, PAGE_W - MARGIN, 16 * mm)
    canvas.restoreState()


def masthead():
    logo = Image(LOGO, width=46, height=46 * 584 / 560.0)
    words = [
        Paragraph("SETUP GUIDE", S["eyebrow"]),
        Spacer(1, 3),
        Paragraph("Open Paws Tools in Claude", S["title"]),
    ]
    t = Table([[logo, words]], colWidths=[62, CONTENT_W - 62])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (0, 0), 2),
                ("TOPPADDING", (1, 0), (1, 0), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return t


def build_story():
    s = []

    # ---------- Page 1 ----------
    s.append(masthead())
    s.append(Spacer(1, 10))
    s.append(
        Paragraph(
            "Open Paws builds AI research tools for animal advocates. This guide "
            "connects them to Claude, so you can ask for them in ordinary language. "
            "It takes about five minutes and needs no technical knowledge.",
            S["subtitle"],
        )
    )
    s.append(Spacer(1, 16))
    s.append(Rule())
    s.append(Spacer(1, 12))

    s.append(Paragraph("What you get", S["section"]))
    s.append(
        Paragraph(
            "Three tools, used from any Claude conversation.", S["lede"]
        )
    )
    s.append(
        tool_cards(
            [
                (
                    "Deep Research",
                    "An in-depth report with sources on an animal-related question "
                    "&mdash; farmed animal welfare, wildlife, animal law and policy, "
                    "or a company&rsquo;s commitments.",
                    "Takes 6&ndash;20 minutes",
                ),
                (
                    "Research Companies",
                    "A profile of one company built from public information: its key "
                    "people, supply chain and recent news.",
                    "Takes 5&ndash;20 minutes",
                ),
                (
                    "The knowledge base",
                    "Answers drawn from animal advocacy sources, and it keeps the "
                    "thread so you can ask follow-up questions.",
                    "Usually under a minute",
                ),
            ]
        )
    )
    s.append(Spacer(1, 20))

    s.append(
        callout(
            "Before you start: get your access token",
            "You need an Open Paws access token. It begins with <b>opk_</b> &mdash; ask "
            "Open Paws for one. Treat it like a password: it is tied to you, so don&rsquo;t "
            "share it, email it on, or paste it anywhere public.",
        )
    )
    s.append(Spacer(1, 16))
    s.append(
        callout(
            "Which Claude is this for?",
            "The steps on the next page cover <b>claude.ai</b> in a browser, the "
            "<b>Claude desktop app</b>, <b>Claude on mobile</b> and <b>Cowork</b>. You do "
            "this once; it then works everywhere you sign in to Claude. If you use "
            "<b>Claude Code</b> instead, there is a short note at the end.",
            bg=MIST,
            bar=TEAL,
        )
    )
    s.append(Spacer(1, 18))
    s.append(Rule())
    s.append(Paragraph("What happens next", S["section"]))
    s.append(
        step_strip(
            ["Add the connector", "Sign in with<br/>your token", "Add the skills<br/>(optional)"]
        )
    )
    s.append(
        Paragraph("Each step is spelled out on the next page.", S["meta"])
    )

    s.append(PageBreak())

    # ---------- Page 2 ----------
    s.append(Paragraph("Set it up", S["section"]))
    s.append(
        Paragraph(
            "Three steps. The third one is optional but worth doing.", S["lede"]
        )
    )
    s.append(Spacer(1, 14))

    s.append(
        step(
            1,
            "Add the connector",
            [
                "In Claude, open %s."
                % arrow("Customize", "Connectors", "Add custom connector"),
                "Give it a name you&rsquo;ll recognize, such as <b>Open Paws Tools</b>, and "
                "paste this address:",
                code_box(CONNECTOR_URL),
                "If Claude asks how it should identify itself, choose "
                "<b>Register automatically</b>. Then save.",
            ],
        )
    )

    s.append(
        step(
            2,
            "Sign in with your token",
            [
                "Claude opens the Open Paws sign-in page. Paste your <b>opk_</b> token "
                "there once, and you&rsquo;re connected.",
                "Claude never sees the token itself. It gets its own key for that one "
                "connection, renews that key on its own, and the key stops working the "
                "moment your token is revoked.",
            ],
        )
    )

    s.append(
        step(
            3,
            "Add the skills (optional)",
            [
                "The skills teach Claude when and how to use each tool, so you get "
                "better results without having to explain yourself.",
                "Open %s, enter:" % arrow("Customize", "Plugins", "Add", "Add marketplace"),
                code_box(MARKETPLACE_URL),
                "then install <b>Open Paws Tools</b>.",
            ],
        )
    )

    s.append(Spacer(1, 2))
    s.append(
        callout(
            "On a Team or Enterprise plan",
            "An Owner adds the connector once, under %s. Everyone else then connects "
            "with their own token &mdash; usage and history stay separate per person."
            % arrow("Organization settings", "Connectors"),
            bg=MIST,
            bar=TEAL,
        )
    )
    s.append(Spacer(1, 22))

    s.append(Paragraph("Try it", S["section"]))
    s.append(
        Paragraph(
            "Ask in plain language &mdash; Claude picks the right tool. For example:",
            S["lede"],
        )
    )
    s.append(Spacer(1, 8))
    s.append(
        bullets(
            [
                "&ldquo;Research cage-free egg commitments by UK supermarkets since 2020.&rdquo;",
                "&ldquo;Build me a profile of this company: who runs it, its supply chain, "
                "and anything in the news recently.&rdquo;",
                "&ldquo;What do advocacy sources say about ag-gag laws in the US?&rdquo;",
            ]
        )
    )
    s.append(
        Paragraph(
            "If you added the skills, you can also start one directly by typing "
            "<b>/open-paws-tools:deep-research</b>, <b>/open-paws-tools:company-research</b> "
            "or <b>/open-paws-tools:knowledge-base</b>.",
            S["body"],
        )
    )

    s.append(PageBreak())

    # ---------- Page 3 ----------
    s.append(Paragraph("What to expect", S["section"]))
    s.append(Spacer(1, 6))
    s.append(
        bullets(
            [
                "<b>Claude asks first.</b> It checks with you before it starts a research "
                "run or sends a message to the knowledge base.",
                "<b>Research takes a while.</b> A report takes 6&ndash;20 minutes. You can "
                "leave the conversation and come back &mdash; ask Claude for the result later.",
                "<b>Knowledge base answers are quick</b>, usually under a minute, and "
                "Claude remembers the thread for follow-up questions.",
            ]
        )
    )
    s.append(Spacer(1, 12))

    s.append(Paragraph("Where your questions go", S["section"]))
    s.append(Spacer(1, 4))
    s.append(
        Paragraph(
            "Your questions, the companies you research and any organization details you "
            "add go to the Open Paws Tools API, which runs them through Open Paws&rsquo; "
            "research workflows. Those workflows search the web and use AI models. Open "
            "Paws keeps your runs and conversations, linked to your token, until you ask "
            "for them to be deleted.",
            S["body"],
        )
    )
    s.append(Spacer(1, 18))

    s.append(Paragraph("If something doesn&rsquo;t work", S["section"]))
    s.append(Spacer(1, 6))
    s.append(
        bullets(
            [
                "Check the token was pasted whole and starts with <b>opk_</b>.",
                "Check the connector shows as connected under %s."
                % arrow("Customize", "Connectors"),
                "Still stuck, or need a token? Get in touch with Open Paws.",
            ]
        )
    )
    s.append(Spacer(1, 16))

    s.append(
        callout(
            "If you use Claude Code",
            "Run these two commands in a Claude Code session, and enter your token when "
            "asked &mdash; it is kept in your system keychain. Needs Claude Code 2.1.269 or "
            "later. To change the token later: <b>/plugin configure "
            "open-paws-tools@open-paws</b>. For updates: <b>/plugin marketplace update "
            "open-paws</b>. If you set up the connector as well, Claude Code gets a synced "
            "copy of the plugin &mdash; keep one copy switched on and turn the other off, so "
            "the tools don&rsquo;t appear twice.",
            bg=MIST,
            bar=TEAL,
        )
    )
    s.append(Spacer(1, 10))
    s.append(
        code_box(
            "/plugin marketplace add Open-Paws/claude-plugins<br/>"
            "/plugin install open-paws-tools@open-paws",
            style_key="mono_small",
            width=CONTENT_W,
        )
    )
    s.append(Spacer(1, 26))
    s.append(
        closing_band(
            "Need a token, or stuck on a step? Get in touch with Open Paws "
            "&mdash; openpaws.ai"
        )
    )

    return s


def main():
    global S
    register_fonts()
    S = styles()

    doc = BaseDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title="Open Paws Tools in Claude — Setup Guide",
        author="Open Paws",
        subject="How to connect Open Paws' research tools to Claude",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="body",
    )
    doc.addPageTemplates(
        [PageTemplate(id="page", frames=[frame], onPage=page_furniture)]
    )
    doc.build(build_story())
    print("wrote", OUT)


if __name__ == "__main__":
    main()
