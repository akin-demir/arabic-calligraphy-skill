"""Generate actual samples with the bundled renderer; no external image service."""
from pathlib import Path
from arabic_calligraphy.engine import render
from arabic_calligraphy.layouts import certificate, document, poster

ROOT = Path(__file__).resolve().parents[1]


def main():
    dest = ROOT / 'examples/gallery'
    dest.mkdir(parents=True, exist_ok=True)
    for style in ('naskh', 'kufic', 'nastaliq'):
        for ext in ('png', 'svg', 'pdf'):
            render('بسم الله الرحمن الرحيم\nالعِلْمُ نور', dest / f'{style}.{ext}',
                   style=style, width=1000, height=600, font_size=72, margin=60,
                   background='#FAF6EC', align='center')
    for ext in ('png', 'svg', 'pdf'):
        poster('اللغة العربية', dest / f'poster.{ext}', subtitle='حروف تحمل المعنى')
        certificate('أحمد محمد', 'تقديراً للجهود المتميزة في خدمة اللغة العربية',
                    dest / f'certificate.{ext}', signature='فريق اللغة العربية')
    for ext in ('png','svg'):
        render('العلم نور\nاللغة العربية',dest/f'diwani.{ext}',style='diwani',
               width=1200,height=640,font_size=110,margin=70,
               background='#FAF6EC',align='center')
        poster('اللغة العربية',dest/f'diwani-poster.{ext}',style='diwani',
               subtitle='حروف تحمل المعنى',font_size=110)
    for ext in ('png','svg','pdf'):
        render('العلم نور\nالخط العربي',dest/f'thuluth.{ext}',style='thuluth',
               width=1200,height=640,font_size=110,margin=70,
               background='#FAF6EC',align='center')
        poster('الخط العربي',dest/f'thuluth-poster.{ext}',style='thuluth',
               subtitle='جمال الحرف والمعنى',font_size=125)
    render('أهلاً وسهلاً', dest / 'wordmark.svg', width=900, height=360, font_size=90,
           align='center')
    render('أ إ آ ء ؤ ئ لا لَا\nبَ بِ بُ بّ بْ بً بٍ بٌ\nالعربية — Arabic 123 / ١٢٣',
           dest / 'typography.png', width=1000, height=640, font_size=48,
           background='#FFFFFF', align='right')
    document((ROOT / 'examples/documents/report.md').read_text(), dest / 'report.pdf')


if __name__ == '__main__':
    main()
