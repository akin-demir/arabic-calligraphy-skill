"""Generate actual samples with the bundled renderer; no external image service."""
from pathlib import Path
from arabic_calligraphy.engine import render, Canvas, backend, color
from arabic_calligraphy.layouts import draw_block, border
from arabic_calligraphy.layouts import certificate, document, poster

ROOT = Path(__file__).resolve().parents[1]


def readme_hero(dest):
    """Actual Diwani title with Cairo framing, exported as raster and outlined vector."""
    title = 'فن الخط العربي'
    subtitle = 'حروف تحمل المعنى'
    header = 'ARABIC CALLIGRAPHY / AGENT SKILL'
    footer = '20 DOCUMENTED TRADITIONS   /   4 FONT WORKFLOWS   /   LOCAL RENDERING'
    metadata = '\n'.join((header,title,subtitle,footer))
    for ext in ('png','svg'):
        with Canvas(dest/f'readme-hero.{ext}',1600,800,'#102D2A',metadata) as canvas:
            n = backend()
            border(canvas,28,'#806E4B')
            border(canvas,40,'#324D43')
            # Quiet inset framing and small manuscript-inspired corner rules.
            n.color(canvas.context,*color('#BFA373'))
            n.line_width(canvas.context,2)
            for x in (65,1495):
                for y in (65,695):
                    n.rectangle(canvas.context,x,y,40,40)
                    n.stroke(canvas.context)
            draw_block(canvas,header,'Noto Sans',23,120,90,1360,60,
                       ink='#CBB88F')
            draw_block(canvas,title,'LaylaDiwani',230,100,160,1400,430,
                       ink='#F6E8C8')
            draw_block(canvas,subtitle,'Noto Naskh Arabic',44,160,590,1280,90,
                       ink='#D2D8C9')
            n.color(canvas.context,*color('#806E4B'))
            n.line_width(canvas.context,1)
            n.rectangle(canvas.context,480,690,640,1)
            n.stroke(canvas.context)
            draw_block(canvas,'\u2066'+footer+'\u2069','Noto Sans',18,120,725,1360,40,
                       ink='#BCAA85')


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
    render('أهلاً وسهلاً', dest / 'wordmark.svg', width=900, height=360, font_size=90,
           align='center')
    render('أ إ آ ء ؤ ئ لا لَا\nبَ بِ بُ بّ بْ بً بٍ بٌ\nالعربية — Arabic 123 / ١٢٣',
           dest / 'typography.png', width=1000, height=640, font_size=48,
           background='#FFFFFF', align='right')
    document((ROOT / 'examples/documents/report.md').read_text(), dest / 'report.pdf')
    readme_hero(dest)


if __name__ == '__main__':
    main()
