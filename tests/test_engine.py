"""Integration checks exercise real native shaping and exported artifacts."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import warnings
from xml.etree import ElementTree as ET

from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader
from arabic_calligraphy.cli import main
from arabic_calligraphy.engine import Canvas, Layout, backend, family_for, render, styles
from arabic_calligraphy.fonts import coverage, manifest, validate_coverage
from arabic_calligraphy.layouts import certificate, document, poster

ROOT = Path(__file__).resolve().parents[1]
CORPUS = json.loads((ROOT/'tests/fixtures/unicode.json').read_text())


class Artifacts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_registry(self):
        self.assertEqual(len(styles()), 20)
        self.assertEqual(sum(s['implemented'] for s in styles()), 5)
        self.assertFalse(any(s['expert_authenticity_reviewed'] for s in styles()))
        self.assertEqual(json.loads((ROOT/'capabilities.json').read_text())['styles'], styles())

    def test_font_licenses_hashes_and_coverage(self):
        self.assertEqual(len(coverage()), 6)
        for record in manifest():
            self.assertEqual(record['license'], 'OFL-1.1')
            self.assertEqual(record['fs_type'], {'LaylaDiwani': 2, 'LaylaThuluth': 8}.get(record['family'], 0))
            self.assertEqual(record['embedding_permission'], record['family'] != 'LaylaDiwani')

    def test_reference_only_fails(self):
        for entry in styles():
            if not entry['implemented']:
                with self.subTest(style=entry['id']), self.assertRaisesRegex(ValueError, 'Reference Only'):
                    render('العلم', self.root/'x.png', style=entry['id'])

    def test_unknown_style(self):
        with self.assertRaisesRegex(ValueError, 'Unknown style'):
            family_for('invented')

    def test_uncovered_glyph(self):
        with self.assertRaisesRegex(ValueError, 'lacks coverage'):
            render('العربية 🦄', self.root/'x.png')

    def test_explicit_fallback_warning(self):
        with warnings.catch_warnings(record=True) as out:
            warnings.simplefilter('always')
            validate_coverage('العربية English', family_for('naskh'))
        self.assertTrue(any('fallback' in str(w.message) for w in out))

    def test_png_alpha_and_dimensions(self):
        p=self.root/'x.png'
        render('العلم نور',p,width=640,height=360,font_size=50,margin=30)
        with Image.open(p) as image:
            self.assertEqual(image.size,(640,360))
            alpha=image.getchannel('A')
            self.assertEqual(alpha.getextrema(),(0,255))
            box=alpha.getbbox()
            self.assertGreater(box[0],25)
            self.assertLess(box[2],615)

    def test_overflow_is_atomic(self):
        p=self.root/'x.png';p.write_bytes(b'original')
        with self.assertRaisesRegex(ValueError,'overflow'):
            render('العلم نور '*50,p,width=200,height=100,margin=20)
        self.assertEqual(p.read_bytes(),b'original')
        self.assertEqual(list(self.root.iterdir()),[p])

    def test_symlink_refused(self):
        p=self.root/'x.png'; p.symlink_to(self.root/'target.png')
        with self.assertRaisesRegex(ValueError,'symlink'):
            render('العلم',p)

    def test_svg_has_paths_and_exact_metadata(self):
        p=self.root/'x.svg';render('بِسْمِ الله',p)
        root=ET.parse(p).getroot()
        self.assertEqual(root.find('{http://www.w3.org/2000/svg}desc').text,'بِسْمِ الله')
        self.assertGreater(len(root.findall('.//{http://www.w3.org/2000/svg}path')),0)

    def test_pdf_semantic_text_and_embedded_fonts(self):
        text='العِلْمُ نور — Arabic 123'
        p=self.root/'x.pdf'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore');render(text,p,background='#FFFFFF')
        page=PdfReader(p).pages[0]
        stream=page.get_contents().get_data()
        self.assertIn((b'\xfe\xff'+text.encode('utf-16-be')).hex().encode(),stream)
        fonts=page['/Resources']['/Font']
        self.assertTrue(fonts)
        for font in fonts.values():
            f=font.get_object()
            descriptor=f.get('/FontDescriptor')
            if descriptor is None:
                descriptor=f['/DescendantFonts'][0].get_object()['/FontDescriptor']
            d=descriptor.get_object()
            self.assertTrue('/FontFile2' in d or '/FontFile3' in d)
        # Raw extractor behavior is reported separately; it is not asserted to be lossless.
        self.assertIn('Arabic',page.extract_text())

    def test_multipage_document(self):
        p=self.root/'doc.pdf'
        document('# عنوان\n'+('العلم نور والمعرفة قوة.\n'*70),p)
        pages=PdfReader(p).pages
        self.assertGreater(len(pages),1)
        for page in pages:
            self.assertIn(b'/ActualText',page.get_contents().get_data())

    def test_plain_document_never_executes(self):
        p=self.root/'doc.pdf'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore');document('$(touch injected) <script>alert(1)</script>',p)
        self.assertTrue(p.exists());self.assertFalse((self.root/'injected').exists())

    def test_poster_all_exports(self):
        for ext in ('png','svg','pdf'):
            p=self.root/f'poster.{ext}';poster('اللغة العربية',p,subtitle='العلم نور')
            self.assertGreater(p.stat().st_size,100)

    def test_certificate(self):
        p=self.root/'certificate.pdf';certificate('أحمد محمد','تقديراً للجهود المتميزة',p)
        self.assertEqual(len(PdfReader(p).pages),1)

    def test_certificate_rejects_empty_required_fields(self):
        for recipient, body in [('', 'نص'), ('اسم', '   ')]:
            with self.assertRaises(ValueError):
                certificate(recipient, body, self.root/'blank.pdf')

    def test_certificate_scales_canvas(self):
        p=self.root/'small.png'
        certificate('أحمد', 'شكراً', p, width=595, height=421)
        with Image.open(p) as image:
            self.assertEqual(image.size, (595,421))

    def test_poster_respects_large_margin(self):
        p=self.root/'poster.png'
        poster('نور',p,width=640,height=640,font_size=28,margin=200,
               background='transparent',foreground='#FFFFFF')
        with Image.open(p) as image:
            # The decorative frame is intentionally at half the margin.
            box=image.getchannel('A').getbbox()
            self.assertGreaterEqual(box[0],99)
            self.assertLessEqual(box[2],541)

    def test_diwani_pdf_refused_without_replacement(self):
        p=self.root/'diwani.pdf';p.write_bytes(b'original')
        with self.assertRaisesRegex(ValueError,'embedding flag'):
            render('العلم نور',p,style='diwani')
        self.assertEqual(p.read_bytes(),b'original')

    def test_diwani_poster_pdf_refused(self):
        with self.assertRaisesRegex(ValueError,'embedding flag'):
            poster('العلم نور',self.root/'poster.pdf',style='diwani')

    def test_diwani_document_body_refused(self):
        with self.assertRaisesRegex(ValueError,'embedding flag'):
            document('العلم نور',self.root/'document.pdf',body_style='diwani')

    def test_diwani_marks_refused(self):
        for text in ['بَ','بّ','مُحَمَّد','ب\u0653']:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError,'combining marks'):
                render(text,self.root/'marks.svg',style='diwani')

    def test_diwani_no_silent_arabic_fallback(self):
        with self.assertRaisesRegex(ValueError,'lacks coverage'):
            render('العربية \u08b0',self.root/'missing.svg',style='diwani')

    def test_diwani_png_and_svg(self):
        for ext in ['png','svg']:
            p=self.root/f'diwani.{ext}'
            render('اللغة العربية',p,style='diwani',width=1000,height=450,font_size=95)
            self.assertGreater(p.stat().st_size,100)
        root=ET.parse(self.root/'diwani.svg').getroot()
        self.assertEqual(root.find('{http://www.w3.org/2000/svg}desc').text,'اللغة العربية')
        self.assertFalse(root.findall('.//{http://www.w3.org/2000/svg}text'))

    def test_diwani_visual_regression(self):
        p=self.root/'diwani.png'
        render('العلم نور',p,style='diwani',width=640,height=360,font_size=70,
               margin=30,background='#FFFFFF',align='center')
        with Image.open(p) as current, Image.open(ROOT/'tests/visual/diwani.png') as ref:
            a,b=current.convert('RGB'),ref.convert('RGB')
            box=ImageChops.difference(b,Image.new('RGB',b.size,'white')).getbbox()
            delta=ImageStat.Stat(ImageChops.difference(a.crop(box),b.crop(box)))
            self.assertLess(sum(delta.mean)/3,10)

    def test_thuluth_exports_exact_svg(self):
        for ext in ['png','svg','pdf']:
            p=self.root/f'thuluth.{ext}'
            render('العلم نور',p,style='thuluth',width=1000,height=450,font_size=100)
            self.assertGreater(p.stat().st_size,100)
        root=ET.parse(self.root/'thuluth.svg').getroot()
        self.assertEqual(root.find('{http://www.w3.org/2000/svg}desc').text,'العلم نور')
        self.assertFalse(root.findall('.//{http://www.w3.org/2000/svg}text'))

    def test_thuluth_pdf_embeds_selected_font(self):
        p=self.root/'thuluth.pdf';text='الجزيرة'
        render(text,p,style='thuluth',width=900,height=450,font_size=100)
        page=PdfReader(p).pages[0]
        fonts=page['/Resources']['/Font']
        self.assertTrue(fonts)
        for font in fonts.values():
            f=font.get_object()
            self.assertIn('LaylaThuluth',str(f['/BaseFont']))
            descriptor=f.get('/FontDescriptor')
            if descriptor is None:
                descriptor=f['/DescendantFonts'][0].get_object()['/FontDescriptor']
            self.assertIn('/FontFile2',descriptor.get_object())
        self.assertIn((b'\xfe\xff'+text.encode('utf-16-be')).hex().encode(),
                      page.get_contents().get_data())

    def test_thuluth_marks_refused_atomically(self):
        p=self.root/'marked.svg';p.write_text('original')
        for text in ['بَ','بّ','مُحَمَّد','ب\u0653']:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError,'combining marks'):
                render(text,p,style='thuluth')
        self.assertEqual(p.read_text(),'original')

    def test_thuluth_missing_coverage_refused(self):
        with self.assertRaisesRegex(ValueError,'lacks coverage'):
            render('العربية \u08b0',self.root/'missing.svg',style='thuluth')

    def test_thuluth_poster_exports(self):
        for ext in ['png','svg','pdf']:
            p=self.root/f'poster.{ext}'
            poster('الخط العربي',p,style='thuluth',subtitle='جمال الحرف والمعنى')
            self.assertGreater(p.stat().st_size,100)

    def test_thuluth_cli(self):
        with contextlib.redirect_stdout(io.StringIO()):
            code=main(['render','--text','الجزيرة','--style','thuluth',
                       '--output',str(self.root/'cli.svg')])
        self.assertEqual(code,0)

    def test_thuluth_visual_regression(self):
        p=self.root/'thuluth.png'
        render('العلم نور',p,style='thuluth',width=640,height=360,font_size=70,
               margin=30,background='#FFFFFF',align='center')
        with Image.open(p) as current, Image.open(ROOT/'tests/visual/thuluth.png') as ref:
            a,b=current.convert('RGB'),ref.convert('RGB')
            box=ImageChops.difference(b,Image.new('RGB',b.size,'white')).getbbox()
            delta=ImageStat.Stat(ImageChops.difference(a.crop(box),b.crop(box)))
            self.assertLess(sum(delta.mean)/3,10)

    def test_cli_success(self):
        with contextlib.redirect_stdout(io.StringIO()):
            code=main(['render','--text','العلم نور','--size','640x360','--font-size','48',
                       '--margin','30','--output',str(self.root/'cli.png')])
        self.assertEqual(code,0)

    def test_cli_unsupported(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(['render','--text','العلم','--style','tughra',
                                   '--output',str(self.root/'x.svg')]),2)

    def test_deterministic_raster(self):
        for name in ('a','b'):
            render('بِسْمِ الله',self.root/f'{name}.png',background='#FFFFFF')
        self.assertEqual(hashlib.sha256((self.root/'a.png').read_bytes()).digest(),
                         hashlib.sha256((self.root/'b.png').read_bytes()).digest())

    def test_visual_regressions(self):
        for style in ('naskh','kufic','nastaliq'):
            p=self.root/f'{style}.png'
            render('العِلْمُ نور',p,style=style,width=640,height=360,font_size=50,
                   margin=30,background='#FFFFFF',align='center')
            baseline=ROOT/f'tests/visual/{style}.png'
            with Image.open(p) as current, Image.open(baseline) as ref:
                a,b=current.convert('RGB'),ref.convert('RGB')
                self.assertEqual(a.size,b.size)
                # Compare the union of ink bounds to avoid diluting differences in empty margins.
                box=ImageChops.difference(b,Image.new('RGB',b.size,'white')).getbbox()
                delta=ImageStat.Stat(ImageChops.difference(a.crop(box),b.crop(box)))
                self.assertLess(sum(delta.mean)/3,10,style)


# Every corpus case exercises real Pango coverage/shaping and exact SVG source preservation.
# Distinct joins, marks, bidi punctuation and wrapping are tested across all implemented styles.
def unicode_test(text,style):
    def test(self):
        p=self.root/'text.svg'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            render(text,p,style=style,width=1200,height=1200,font_size=28,margin=40)
        self.assertEqual(ET.parse(p).getroot().find('{http://www.w3.org/2000/svg}desc').text,text)
    return test


for index,text in enumerate(CORPUS):
    for style in ('naskh','kufic','nastaliq'):
        setattr(Artifacts,f'test_unicode_{index:03d}_{style}',unicode_test(text,style))


def invalid_test(kwargs):
    def test(self):
        with self.assertRaises((ValueError,TypeError)):
            render('العلم',self.root/'bad.png',**kwargs)
    return test


for i,kwargs in enumerate([
    {'width':0},{'height':-1},{'font_size':0},{'font_size':float('nan')},
    {'margin':-1},{'margin':600},{'width':8193},{'width':1.5},
    {'width':8192,'height':8192},{'align':'diagonal'},
    {'foreground':'red'},{'background':'#ZZZZZZ'},{'height':float('inf')},
]):
    setattr(Artifacts,f'test_invalid_configuration_{i:02d}',invalid_test(kwargs))

# Diwani intentionally refuses vocalized input: test every unmarked corpus string
# through native shaping and exact SVG metadata, while explicit rejection tests
# above cover the unsupported inputs and exports.
import unicodedata
for index,text in enumerate(CORPUS):
    if not any(unicodedata.category(c) in ('Mn','Me') for c in text):
        setattr(Artifacts,f'test_diwani_unicode_{index:03d}',unicode_test(text,'diwani'))

# The Thuluth font has no GPOS: exact-source integration checks cover all 89
# unmarked corpus inputs; explicit tests above cover refusal of vocalization.
for index,text in enumerate(CORPUS):
    if not any(unicodedata.category(c) in ('Mn','Me') for c in text):
        setattr(Artifacts,f'test_thuluth_unicode_{index:03d}',unicode_test(text,'thuluth'))
