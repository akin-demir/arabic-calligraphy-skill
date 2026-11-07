# Architecture

CLI → validated Unicode/style/layout → Pango paragraph layout → HarfBuzz shaping and bidi stack → Cairo PNG/SVG/PDF → atomic output. The Python ctypes layer binds only the required stable C interfaces, declares argument/result types and releases native resources on errors. Mature native libraries handle Arabic shaping; no Python reshaper or string reversal is used.

Fontconfig uses a private in-process configuration of five bundled font files (four Noto and Layla Diwani). fontTools checks hashes, embedding/export permissions and Unicode coverage before registration. Noto Sans is an explicitly warned fallback for Latin and a small Common punctuation allowlist. Arabic coverage never silently falls through to another tradition. Do not call rendering concurrently in one process: Fontconfig state is process-global.

Artwork uses measured ink/logical bounds and explicit overflow errors. Paginated documents use Pango UTF-8 line boundaries, preserving codepoints rather than byte-splitting Arabic. Headings and page numbers are structured by the layout code. PDF postprocessing with pypdf associates semantic ActualText with drawn content and retains embedded font subsets; it does not establish universal extractor correctness. SVG outlines preserve appearance and include source text as metadata.

We considered manual reshaping with raster-only drawing and rejected it for bidi, Unicode mapping and PDF limitations. A browser/HTML engine would add a larger runtime and resource-loading surface than these plain-text layouts require. Advanced publishing, arbitrary PDF editing and manual composition are outside this small engine.

The style registry lives in package data; the root copy serves agent discovery. Tests require equality. No style can be classified Verified without technical tests and recorded human authenticity review evidence. Technical checks cover a defined corpus, never every possible string.

The Diwani registry entry narrows support to unvocalized PNG/SVG. The font policy validates its original fsType=2 against the manifest, registers it for those outline/raster exports and refuses PDF. Missing GPOS is an explicit legacy positioning profile, with combining marks rejected. Other fonts still require GSUB/GPOS and unrestricted embedding.
