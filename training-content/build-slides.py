"""
Build slides.html from a Module .md file.
Usage: python build-slides.py <path-to-md-file>
       or place in a module's PPT/ folder and run (auto-detects .md)
"""

import re, os, sys, glob

def find_md():
    """Find the .md file -- from arg or auto-detect in current dir."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    # Auto-detect: look for Module-*.md in same directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mds = glob.glob(os.path.join(script_dir, 'Module-*.md'))
    if mds:
        return mds[0]
    # Try parent PPT dir
    mds = glob.glob(os.path.join(script_dir, 'PPT', 'Module-*.md'))
    if mds:
        return mds[0]
    print("No Module-*.md file found. Pass path as argument.")
    sys.exit(1)

def extract_module_info(first_slide):
    """Extract module number and name from the title slide markdown."""
    lines = first_slide.split('\n')
    title = ''
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    # Try to find module number from ## line
    num = '01'
    name = title
    for line in lines:
        if 'Module' in line:
            m = re.search(r'Module\s+(\d+)', line)
            if m:
                num = m.group(1).zfill(2)
    return num, name, title

def read_slides(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    raw = re.split(r'\n---\n', content)
    return [s.strip() for s in raw if s.strip()]

def inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Escape HTML inside backtick code spans before wrapping in <code>
    def escape_code(m):
        inner = m.group(1).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<code>{inner}</code>'
    text = re.sub(r'`([^`]+)`', escape_code, text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    return text

VISUALS = {
'box-model': '''
<div style="display:flex;gap:30px;align-items:center;margin:16px 0">
  <div style="background:#FFE0E0;border:3px dashed #D85B5B;border-radius:8px;padding:20px;text-align:center;flex:0 0 340px">
    <div style="font-size:11px;font-weight:700;color:#D85B5B;margin-bottom:8px">MARGIN</div>
    <div style="background:#DDEEFF;border:3px solid #3D8DFF;border-radius:6px;padding:16px">
      <div style="font-size:11px;font-weight:700;color:#3D8DFF;margin-bottom:6px">BORDER</div>
      <div style="background:#E8F5E9;border:2px dashed #2BAA76;border-radius:4px;padding:14px">
        <div style="font-size:11px;font-weight:700;color:#2BAA76;margin-bottom:6px">PADDING</div>
        <div style="background:#fff;border:1px solid #ccc;border-radius:4px;padding:16px 24px;font-size:15px;font-weight:700;color:var(--ink)">CONTENT</div>
      </div>
    </div>
  </div>
  <div style="flex:1">
    <div style="font-size:15px;color:var(--body);line-height:1.8">
      <div><span style="display:inline-block;width:12px;height:12px;background:#FFE0E0;border:2px solid #D85B5B;border-radius:2px;margin-right:8px;vertical-align:middle"></span><strong>Margin</strong> &mdash; space outside the border</div>
      <div><span style="display:inline-block;width:12px;height:12px;background:#DDEEFF;border:2px solid #3D8DFF;border-radius:2px;margin-right:8px;vertical-align:middle"></span><strong>Border</strong> &mdash; the visible edge</div>
      <div><span style="display:inline-block;width:12px;height:12px;background:#E8F5E9;border:2px solid #2BAA76;border-radius:2px;margin-right:8px;vertical-align:middle"></span><strong>Padding</strong> &mdash; space inside the border</div>
      <div><span style="display:inline-block;width:12px;height:12px;background:#fff;border:2px solid #ccc;border-radius:2px;margin-right:8px;vertical-align:middle"></span><strong>Content</strong> &mdash; text, image, etc.</div>
    </div>
  </div>
</div>''',

'page-layout': '''
<div style="display:flex;gap:24px;margin:12px 0;align-items:flex-start">
  <div style="flex:0 0 380px;border:2px solid #E0E4E8;border-radius:10px;overflow:hidden;font-size:13px;font-weight:700">
    <div style="background:#DDEEFF;padding:10px 16px;color:#3D8DFF;border-bottom:1px solid #E0E4E8">&lt;header&gt;<span style="float:right;font-weight:400;color:#5D6874">logo, title</span></div>
    <div style="background:#EAF4FF;padding:8px 16px;color:#3D8DFF;border-bottom:1px solid #E0E4E8">&lt;nav&gt;<span style="float:right;font-weight:400;color:#5D6874">links</span></div>
    <div style="display:flex;border-bottom:1px solid #E0E4E8">
      <div style="flex:3;background:#F2F5F7;padding:14px 16px;color:#101820;border-right:1px solid #E0E4E8">&lt;main&gt;<br><div style="background:#fff;border:1px dashed #2BAA76;border-radius:4px;padding:8px;margin:8px 0;color:#2BAA76;font-size:12px">&lt;section&gt;<br><div style="background:#EAF6F1;border-radius:3px;padding:4px 8px;margin:4px 0;font-size:11px">article / card</div><div style="background:#EAF6F1;border-radius:3px;padding:4px 8px;margin:4px 0;font-size:11px">article / card</div></div></div>
      <div style="flex:1;background:#FFF4DE;padding:14px 12px;color:#A0660B">&lt;aside&gt;<div style="font-weight:400;font-size:11px;margin-top:4px">cart, filters</div></div>
    </div>
    <div style="background:#E9EDF0;padding:10px 16px;color:#5D6874">&lt;footer&gt;<span style="float:right;font-weight:400">contact, links</span></div>
  </div>
  <div style="flex:1">
    <div style="font-size:15px;color:var(--body);line-height:2">
      <div><span style="color:#3D8DFF;font-weight:700">header</span> &mdash; site identity</div>
      <div><span style="color:#3D8DFF;font-weight:700">nav</span> &mdash; navigation links</div>
      <div><span style="color:#101820;font-weight:700">main</span> &mdash; primary content</div>
      <div><span style="color:#2BAA76;font-weight:700">section</span> &mdash; thematic group</div>
      <div><span style="color:#A0660B;font-weight:700">aside</span> &mdash; secondary content</div>
      <div><span style="color:#5D6874;font-weight:700">footer</span> &mdash; metadata, contact</div>
    </div>
  </div>
</div>''',

'browser-pipeline': '''
<div style="display:flex;align-items:center;gap:6px;margin:20px 0">
  <div style="flex:1;background:var(--panel);border-radius:10px;padding:16px;text-align:center">
    <div style="width:36px;height:36px;background:var(--blue);color:#fff;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;margin-bottom:8px">1</div>
    <div style="font-size:17px;font-weight:700;color:var(--ink)">Request</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">HTML, CSS,<br>assets fetched</div>
  </div>
  <div style="font-size:24px;color:var(--cyan)">&#9654;</div>
  <div style="flex:1;background:var(--panel);border-radius:10px;padding:16px;text-align:center">
    <div style="width:36px;height:36px;background:var(--blue);color:#fff;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;margin-bottom:8px">2</div>
    <div style="font-size:17px;font-weight:700;color:var(--ink)">Parse</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">DOM tree<br>+ CSSOM tree</div>
  </div>
  <div style="font-size:24px;color:var(--cyan)">&#9654;</div>
  <div style="flex:1;background:var(--panel);border-radius:10px;padding:16px;text-align:center">
    <div style="width:36px;height:36px;background:var(--blue);color:#fff;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;margin-bottom:8px">3</div>
    <div style="font-size:17px;font-weight:700;color:var(--ink)">Layout</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">Sizes and<br>positions</div>
  </div>
  <div style="font-size:24px;color:var(--cyan)">&#9654;</div>
  <div style="flex:1;background:var(--panel);border-radius:10px;padding:16px;text-align:center">
    <div style="width:36px;height:36px;background:var(--blue);color:#fff;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;margin-bottom:8px">4</div>
    <div style="font-size:17px;font-weight:700;color:var(--ink)">Paint</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">Pixels<br>and layers</div>
  </div>
  <div style="font-size:24px;color:var(--cyan)">&#9654;</div>
  <div style="flex:1;background:var(--green-tint);border-radius:10px;padding:16px;text-align:center">
    <div style="width:36px;height:36px;background:var(--green);color:#fff;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;margin-bottom:8px">5</div>
    <div style="font-size:17px;font-weight:700;color:var(--ink)">Interact</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">Events<br>and state</div>
  </div>
</div>''',

'cascade-flow': '''
<div style="display:flex;flex-direction:column;gap:6px;margin:12px 0;max-width:700px">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:32px;height:32px;background:#D85B5B;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0">1</div>
    <div style="flex:1;background:#FFEDED;border-radius:6px;padding:10px 16px;font-size:16px"><strong style="color:#D85B5B">!important</strong> &mdash; overrides everything (avoid!)</div>
  </div>
  <div style="margin-left:16px;font-size:18px;color:var(--cyan)">&#9660;</div>
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:32px;height:32px;background:#E97132;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0">2</div>
    <div style="flex:1;background:#FFF4DE;border-radius:6px;padding:10px 16px;font-size:16px"><strong style="color:#A0660B">Inline styles</strong> &mdash; style="..." attribute</div>
  </div>
  <div style="margin-left:16px;font-size:18px;color:var(--cyan)">&#9660;</div>
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:32px;height:32px;background:var(--blue);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0">3</div>
    <div style="flex:1;background:var(--blue-tint);border-radius:6px;padding:10px 16px;font-size:16px"><strong style="color:var(--blue)">ID selectors</strong> &mdash; #header (1,0,0)</div>
  </div>
  <div style="margin-left:16px;font-size:18px;color:var(--cyan)">&#9660;</div>
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:32px;height:32px;background:var(--green);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0">4</div>
    <div style="flex:1;background:var(--green-tint);border-radius:6px;padding:10px 16px;font-size:16px"><strong style="color:var(--green)">Class selectors</strong> &mdash; .card, .btn (0,1,0)</div>
  </div>
  <div style="margin-left:16px;font-size:18px;color:var(--cyan)">&#9660;</div>
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:32px;height:32px;background:var(--body);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0">5</div>
    <div style="flex:1;background:var(--panel);border-radius:6px;padding:10px 16px;font-size:16px"><strong style="color:var(--body)">Element selectors</strong> &mdash; p, div, h1 (0,0,1)</div>
  </div>
</div>''',

'flexbox-axes': '''
<div style="margin:12px 0;display:flex;gap:30px">
  <div style="flex:1;border:2px solid var(--blue);border-radius:10px;padding:20px;position:relative">
    <div style="font-size:12px;font-weight:700;color:var(--blue);position:absolute;top:-10px;left:16px;background:#fff;padding:0 6px">flex-direction: row</div>
    <div style="display:flex;gap:8px;align-items:center">
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:4px;padding:12px 20px;font-size:13px;font-weight:700;color:var(--blue)">Item 1</div>
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:4px;padding:12px 20px;font-size:13px;font-weight:700;color:var(--blue)">Item 2</div>
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:4px;padding:12px 20px;font-size:13px;font-weight:700;color:var(--blue)">Item 3</div>
    </div>
    <div style="font-size:11px;color:var(--blue);margin-top:8px;text-align:center">&#x2194; main axis (horizontal) &nbsp; &#x2195; cross axis</div>
  </div>
  <div style="flex:1;border:2px solid var(--green);border-radius:10px;padding:20px;position:relative">
    <div style="font-size:12px;font-weight:700;color:var(--green);position:absolute;top:-10px;left:16px;background:#fff;padding:0 6px">flex-direction: column</div>
    <div style="display:flex;flex-direction:column;gap:8px">
      <div style="background:var(--green-tint);border:1px solid var(--green);border-radius:4px;padding:10px 20px;font-size:13px;font-weight:700;color:var(--green)">Item 1</div>
      <div style="background:var(--green-tint);border:1px solid var(--green);border-radius:4px;padding:10px 20px;font-size:13px;font-weight:700;color:var(--green)">Item 2</div>
      <div style="background:var(--green-tint);border:1px solid var(--green);border-radius:4px;padding:10px 20px;font-size:13px;font-weight:700;color:var(--green)">Item 3</div>
    </div>
    <div style="font-size:11px;color:var(--green);margin-top:8px;text-align:center">&#x2195; main axis (vertical) &nbsp; &#x2194; cross axis</div>
  </div>
</div>''',

'grid-visual': '''
<div style="margin:12px 0;display:flex;gap:30px">
  <div style="flex:1">
    <div style="font-size:13px;font-weight:700;color:var(--body);margin-bottom:6px">repeat(3, 1fr) &mdash; fixed 3 columns</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--blue)">1fr</div>
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--blue)">1fr</div>
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--blue)">1fr</div>
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--blue)">1fr</div>
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--blue)">1fr</div>
      <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--blue)">1fr</div>
    </div>
  </div>
  <div style="flex:1">
    <div style="font-size:13px;font-weight:700;color:var(--body);margin-bottom:6px">auto-fit, minmax(120px, 1fr) &mdash; responsive</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px">
      <div style="background:var(--green-tint);border:1px solid var(--green);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--green)">auto</div>
      <div style="background:var(--green-tint);border:1px solid var(--green);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--green)">auto</div>
      <div style="background:var(--green-tint);border:1px solid var(--green);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--green)">auto</div>
      <div style="background:var(--green-tint);border:1px solid var(--green);border-radius:6px;padding:20px;text-align:center;font-size:13px;font-weight:700;color:var(--green)">auto</div>
    </div>
  </div>
</div>''',

'sticky-footer': '''
<div style="display:flex;gap:24px;margin:12px 0;align-items:stretch">
  <div style="flex:1;border:2px solid #D85B5B;border-radius:10px;overflow:hidden">
    <div style="font-size:12px;font-weight:700;color:#D85B5B;padding:8px 12px;background:#FFEDED;text-align:center">WITHOUT flex</div>
    <div style="padding:12px">
      <div style="background:#DDEEFF;border-radius:4px;padding:6px 10px;font-size:11px;color:#3D8DFF;font-weight:700;margin-bottom:6px">header</div>
      <div style="background:var(--panel);border-radius:4px;padding:16px 10px;font-size:11px;color:var(--ink);font-weight:700;margin-bottom:6px">main (short content)</div>
      <div style="background:#E9EDF0;border-radius:4px;padding:6px 10px;font-size:11px;color:#5D6874;font-weight:700">footer &#x2191; floats here</div>
      <div style="height:40px"></div>
      <div style="font-size:10px;color:#D85B5B;text-align:center;border-top:1px dashed #D85B5B;padding-top:4px">empty space below</div>
    </div>
  </div>
  <div style="flex:1;border:2px solid var(--green);border-radius:10px;overflow:hidden">
    <div style="font-size:12px;font-weight:700;color:var(--green);padding:8px 12px;background:var(--green-tint);text-align:center">WITH flex column + mt-auto</div>
    <div style="padding:12px;display:flex;flex-direction:column;min-height:200px">
      <div style="background:#DDEEFF;border-radius:4px;padding:6px 10px;font-size:11px;color:#3D8DFF;font-weight:700;margin-bottom:6px">header</div>
      <div style="background:var(--panel);border-radius:4px;padding:16px 10px;font-size:11px;color:var(--ink);font-weight:700;margin-bottom:6px">main (short content)</div>
      <div style="background:#E9EDF0;border-radius:4px;padding:6px 10px;font-size:11px;color:#5D6874;font-weight:700;margin-top:auto">footer &#x2193; pushed to bottom</div>
    </div>
  </div>
</div>''',

'responsive-breakpoints': '''
<div style="display:flex;gap:12px;margin:12px 0;align-items:flex-end">
  <div style="flex:0 0 60px;text-align:center">
    <div style="background:var(--ink);border-radius:4px 4px 0 0;width:30px;height:60px;margin:0 auto"></div>
    <div style="background:var(--ink);border-radius:0 0 4px 4px;width:40px;height:4px;margin:0 auto"></div>
    <div style="font-size:11px;font-weight:700;color:var(--body);margin-top:6px">xs<br>&lt;576</div>
  </div>
  <div style="flex:0 0 70px;text-align:center">
    <div style="background:var(--ink);border-radius:4px 4px 0 0;width:40px;height:55px;margin:0 auto"></div>
    <div style="background:var(--ink);border-radius:0 0 4px 4px;width:50px;height:4px;margin:0 auto"></div>
    <div style="font-size:11px;font-weight:700;color:var(--blue);margin-top:6px">sm<br>576+</div>
  </div>
  <div style="flex:0 0 80px;text-align:center">
    <div style="background:var(--blue);border-radius:6px;width:60px;height:45px;margin:0 auto;display:flex;align-items:center;justify-content:center"><div style="background:#fff;width:50px;height:35px;border-radius:3px"></div></div>
    <div style="background:var(--ink);width:20px;height:3px;margin:2px auto"></div>
    <div style="font-size:11px;font-weight:700;color:var(--blue);margin-top:6px">md<br>768+</div>
  </div>
  <div style="flex:0 0 100px;text-align:center">
    <div style="background:var(--blue);border-radius:4px;width:80px;height:50px;margin:0 auto;display:flex;align-items:center;justify-content:center"><div style="background:#fff;width:70px;height:40px;border-radius:2px"></div></div>
    <div style="background:var(--ink);width:40px;height:5px;margin:2px auto;border-radius:2px"></div>
    <div style="font-size:11px;font-weight:700;color:var(--blue);margin-top:6px">lg<br>992+</div>
  </div>
  <div style="flex:0 0 120px;text-align:center">
    <div style="background:var(--green);border-radius:4px;width:100px;height:55px;margin:0 auto;display:flex;align-items:center;justify-content:center"><div style="background:#fff;width:90px;height:45px;border-radius:2px"></div></div>
    <div style="background:var(--ink);width:50px;height:5px;margin:2px auto;border-radius:2px"></div>
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-top:6px">xl<br>1200+</div>
  </div>
</div>''',

'display-types': '''
<div style="margin:12px 0;display:flex;flex-direction:column;gap:10px">
  <div style="font-size:13px;font-weight:700;color:var(--body)">display: block</div>
  <div style="display:flex;flex-direction:column;gap:4px">
    <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:4px;padding:8px 16px;font-size:13px;color:var(--blue);font-weight:700">div &mdash; takes full width</div>
    <div style="background:var(--blue-tint);border:1px solid var(--blue);border-radius:4px;padding:8px 16px;font-size:13px;color:var(--blue);font-weight:700;width:60%">p &mdash; takes full width</div>
  </div>
  <div style="font-size:13px;font-weight:700;color:var(--body);margin-top:8px">display: inline</div>
  <div>
    <span style="background:var(--green-tint);border:1px solid var(--green);border-radius:4px;padding:4px 12px;font-size:13px;color:var(--green);font-weight:700">span</span>
    <span style="background:var(--green-tint);border:1px solid var(--green);border-radius:4px;padding:4px 12px;font-size:13px;color:var(--green);font-weight:700">a</span>
    <span style="background:var(--green-tint);border:1px solid var(--green);border-radius:4px;padding:4px 12px;font-size:13px;color:var(--green);font-weight:700">strong</span>
    <span style="font-size:13px;color:var(--body);margin-left:8px">&larr; flow side by side, width = content</span>
  </div>
  <div style="font-size:13px;font-weight:700;color:var(--body);margin-top:8px">display: inline-block</div>
  <div>
    <span style="background:#FFF4DE;border:1px solid #E97132;border-radius:4px;padding:8px 20px;font-size:13px;color:#E97132;font-weight:700;display:inline-block">Button</span>
    <span style="background:#FFF4DE;border:1px solid #E97132;border-radius:4px;padding:8px 20px;font-size:13px;color:#E97132;font-weight:700;display:inline-block">Badge</span>
    <span style="font-size:13px;color:var(--body);margin-left:8px">&larr; inline flow + block padding/margin</span>
  </div>
</div>''',

'form-anatomy': '''
<div style="display:flex;gap:20px;margin:12px 0;align-items:flex-start">
  <div style="flex:1;border:2px solid #E0E4E8;border-radius:10px;padding:20px;background:var(--panel)">
    <div style="font-size:13px;font-weight:700;color:var(--blue);margin-bottom:12px">FORM ANATOMY</div>
    <div style="margin-bottom:14px">
      <div style="font-size:14px;font-weight:700;color:var(--green);margin-bottom:4px">&lt;label for="name"&gt;</div>
      <div style="background:#fff;border:2px solid var(--blue);border-radius:6px;padding:10px 14px;font-size:15px;color:var(--body)">
        <span style="color:#aaa">John Doe</span>
        <span style="float:right;font-size:11px;font-weight:700;color:var(--blue)">type="text"</span>
      </div>
      <div style="font-size:11px;color:var(--body);margin-top:2px">id="name" &nbsp; name="name" &nbsp; required</div>
    </div>
    <div style="margin-bottom:14px">
      <div style="font-size:14px;font-weight:700;color:var(--green);margin-bottom:4px">&lt;label for="email"&gt;</div>
      <div style="background:#fff;border:2px solid var(--blue);border-radius:6px;padding:10px 14px;font-size:15px;color:var(--body)">
        <span style="color:#aaa">user@example.com</span>
        <span style="float:right;font-size:11px;font-weight:700;color:var(--blue)">type="email"</span>
      </div>
    </div>
    <div style="background:var(--blue);color:#fff;border-radius:6px;padding:10px;text-align:center;font-weight:700;font-size:15px">
      &lt;button type="submit"&gt; Place Order
    </div>
  </div>
  <div style="flex:0 0 220px;font-size:14px;color:var(--body);line-height:2">
    <div><span style="color:var(--green);font-weight:700">label</span> &rarr; visible text</div>
    <div><span style="color:var(--blue);font-weight:700">for/id</span> &rarr; connects them</div>
    <div><span style="color:var(--ink);font-weight:700">name</span> &rarr; sent to server</div>
    <div><span style="color:var(--ink);font-weight:700">type</span> &rarr; keyboard + validation</div>
    <div><span style="color:#D85B5B;font-weight:700">required</span> &rarr; cannot be blank</div>
  </div>
</div>''',

'heading-hierarchy': '''
<div style="margin:12px 0;display:flex;gap:20px;align-items:flex-start">
  <div style="flex:0 0 320px;background:var(--panel);border-radius:10px;padding:18px 20px">
    <div style="font-size:30px;font-weight:700;color:var(--ink);margin-bottom:4px;border-left:4px solid var(--blue);padding-left:12px">h1 Page Title</div>
    <div style="font-size:24px;font-weight:700;color:var(--ink);margin:10px 0 4px;border-left:4px solid var(--blue);padding-left:12px;margin-left:16px">h2 Section</div>
    <div style="font-size:1.28em;font-weight:700;color:var(--body);margin:8px 0 4px;border-left:4px solid var(--cyan);padding-left:12px;margin-left:32px">h3 Subsection</div>
    <div style="font-size:1.28em;font-weight:700;color:var(--body);margin:8px 0 4px;border-left:4px solid var(--cyan);padding-left:12px;margin-left:32px">h3 Subsection</div>
    <div style="font-size:24px;font-weight:700;color:var(--ink);margin:10px 0 4px;border-left:4px solid var(--blue);padding-left:12px;margin-left:16px">h2 Section</div>
    <div style="font-size:1.28em;font-weight:700;color:var(--body);margin:8px 0 4px;border-left:4px solid var(--cyan);padding-left:12px;margin-left:32px">h3 Subsection</div>
  </div>
  <div style="flex:1;font-size:15px;color:var(--body);line-height:1.8">
    <div><span style="font-weight:700;color:var(--blue)">h1</span> &mdash; one per page, the main title</div>
    <div><span style="font-weight:700;color:var(--blue)">h2</span> &mdash; major sections</div>
    <div><span style="font-weight:700;color:var(--cyan)">h3</span> &mdash; subsections within h2</div>
    <div style="margin-top:10px;padding:8px 12px;background:var(--red-tint);border-radius:4px;font-size:14px;color:#D85B5B;font-weight:700">Never skip levels: h1 &rarr; h3 (wrong!)</div>
    <div style="margin-top:6px;padding:8px 12px;background:var(--green-tint);border-radius:4px;font-size:14px;color:var(--green);font-weight:700">Screen readers use this as a nav outline</div>
  </div>
</div>''',

'html-vs-css': '''
<div style="display:flex;gap:16px;margin:12px 0">
  <div style="flex:1;background:var(--blue-tint);border:2px solid var(--blue);border-radius:10px;padding:20px;text-align:center">
    <div style="font-size:36px;margin-bottom:8px">&#x1F4C4;</div>
    <div style="font-size:22px;font-weight:700;color:var(--blue);margin-bottom:8px">HTML</div>
    <div style="font-size:16px;color:var(--ink);font-weight:700;margin-bottom:4px">Structure &amp; Meaning</div>
    <div style="font-size:14px;color:var(--body);line-height:1.5">Headings, paragraphs, links,<br>images, forms, tables,<br>semantic landmarks</div>
  </div>
  <div style="display:flex;align-items:center;font-size:28px;color:var(--body)">+</div>
  <div style="flex:1;background:var(--green-tint);border:2px solid var(--green);border-radius:10px;padding:20px;text-align:center">
    <div style="font-size:36px;margin-bottom:8px">&#x1F3A8;</div>
    <div style="font-size:22px;font-weight:700;color:var(--green);margin-bottom:8px">CSS</div>
    <div style="font-size:16px;color:var(--ink);font-weight:700;margin-bottom:4px">Presentation &amp; Layout</div>
    <div style="font-size:14px;color:var(--body);line-height:1.5">Colors, fonts, spacing,<br>positioning, responsive,<br>animations</div>
  </div>
  <div style="display:flex;align-items:center;font-size:28px;color:var(--body)">=</div>
  <div style="flex:1;background:#FFF4DE;border:2px solid #E97132;border-radius:10px;padding:20px;text-align:center">
    <div style="font-size:36px;margin-bottom:8px">&#x1F310;</div>
    <div style="font-size:22px;font-weight:700;color:#E97132;margin-bottom:8px">Web Page</div>
    <div style="font-size:16px;color:var(--ink);font-weight:700;margin-bottom:4px">What users see</div>
    <div style="font-size:14px;color:var(--body);line-height:1.5">Structured content<br>presented visually<br>in the browser</div>
  </div>
</div>''',

'devtools-panels': '''
<div style="display:flex;gap:12px;margin:12px 0">
  <div style="flex:1;background:var(--panel);border-radius:8px;padding:14px;text-align:center">
    <div style="font-size:24px;margin-bottom:6px">&#x1F50D;</div>
    <div style="font-size:15px;font-weight:700;color:var(--ink)">Elements</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">DOM tree<br>+ CSS rules</div>
  </div>
  <div style="flex:1;background:var(--panel);border-radius:8px;padding:14px;text-align:center">
    <div style="font-size:24px;margin-bottom:6px">&#x1F4CA;</div>
    <div style="font-size:15px;font-weight:700;color:var(--ink)">Computed</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">Final values<br>+ box model</div>
  </div>
  <div style="flex:1;background:var(--panel);border-radius:8px;padding:14px;text-align:center">
    <div style="font-size:24px;margin-bottom:6px">&#x1F4E1;</div>
    <div style="font-size:15px;font-weight:700;color:var(--ink)">Network</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">Resources<br>+ load timing</div>
  </div>
  <div style="flex:1;background:var(--panel);border-radius:8px;padding:14px;text-align:center">
    <div style="font-size:24px;margin-bottom:6px">&#x26A0;&#xFE0F;</div>
    <div style="font-size:15px;font-weight:700;color:var(--ink)">Console</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">Errors<br>+ warnings</div>
  </div>
  <div style="flex:1;background:var(--green-tint);border-radius:8px;padding:14px;text-align:center">
    <div style="font-size:24px;margin-bottom:6px">&#x2705;</div>
    <div style="font-size:15px;font-weight:700;color:var(--ink)">Lighthouse</div>
    <div style="font-size:13px;color:var(--body);margin-top:4px">Performance<br>+ accessibility</div>
  </div>
</div>''',
}

def md_to_html(md):
    lines = md.split('\n')
    html_parts = []
    in_code = False
    code_lang = ''
    code_lines = []
    in_table = False
    table_rows = []
    in_list = False
    list_items = []

    def flush_list():
        nonlocal in_list, list_items
        if in_list and list_items:
            html_parts.append('<ul class="bl">' + ''.join(list_items) + '</ul>')
            list_items = []
            in_list = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            headers = table_rows[0]
            body = [r for r in table_rows[1:] if r is not None]
            h = ''.join(f'<th>{inline(c.strip())}</th>' for c in headers)
            rows = ''
            for row in body:
                cells = ''.join(f'<td>{inline(c.strip())}</td>' for c in row)
                rows += f'<tr>{cells}</tr>'
            html_parts.append(f'<table class="tbl"><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table>')
            table_rows = []
            in_table = False

    for line in lines:
        if line.startswith('```'):
            if in_code:
                code_text = '\n'.join(code_lines)
                code_text_esc = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                nums = '<br>'.join(str(i+1) for i in range(len(code_lines)))
                fn = 'example.' + (code_lang[:3] if code_lang else 'txt')
                lang = code_lang.upper() if code_lang else 'CODE'
                html_parts.append(
                    f'<div class="cb"><div class="cb-bar">'
                    f'<div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>'
                    f'<span class="cb-fn">{fn}</span><span class="cb-lg">{lang}</span></div>'
                    f'<div class="cb-body"><div class="cb-ln">{nums}</div>'
                    f'<div class="cb-cd">{code_text_esc}</div></div></div>'
                )
                code_lines = []
                in_code = False
            else:
                flush_list()
                flush_table()
                code_lang = line[3:].strip()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if '|' in line and line.strip().startswith('|'):
            flush_list()
            cols = [c for c in line.split('|')[1:-1]]
            if all(c.strip().replace('-', '').replace(':', '') == '' for c in cols):
                table_rows.append(None)
            else:
                if not in_table:
                    in_table = True
                    table_rows = []
                table_rows.append(cols)
            continue
        else:
            flush_table()

        if line.startswith('### '):
            flush_list()
            html_parts.append(f'<div style="font-size:1.5em;font-weight:700;color:var(--ink);margin:1em 0 .5em">{inline(line[4:])}</div>')
            continue
        if line.startswith('## ') or line.startswith('# '):
            flush_list()
            continue

        if line.startswith('> '):
            flush_list()
            text = inline(line[2:])
            if text.startswith('<strong>Next:') or text.startswith('**Next:'):
                html_parts.append(f'<div class="db" style="margin-top:16px"><span class="db-l">NEXT</span><span class="db-t" style="font-size:22px">{text}</span></div>')
            else:
                html_parts.append(f'<div class="ib"><div class="ib-t" style="font-size:1.28em">{text}</div></div>')
            continue

        if line.startswith('- '):
            if not in_list:
                flush_table()
                in_list = True
            text = inline(line[2:])
            list_items.append(f'<li>{text}</li>')
            continue
        if re.match(r'^  +- ', line):
            text = inline(line.strip()[2:])
            list_items.append(f'<li class="s">{text}</li>')
            continue

        m = re.match(r'^(\d+)\.\s+(.+)', line)
        if m:
            if not in_list:
                flush_table()
                in_list = True
            text = inline(m.group(2))
            list_items.append(f'<li>{m.group(1)}. {text}</li>')
            continue

        flush_list()

        if not line.strip():
            continue

        # Visual markers: <!--VISUAL:name-->
        vm = re.match(r'<!--VISUAL:(\S+)-->', line.strip())
        if vm:
            vname = vm.group(1)
            if vname in VISUALS:
                html_parts.append(VISUALS[vname])
            continue

        html_parts.append(f'<p style="font-size:1.35em;color:var(--ink);line-height:1.5;margin:.4em 0">{inline(line)}</p>')

    flush_list()
    flush_table()
    return '\n'.join(html_parts)

def extract_title(md):
    for line in md.split('\n'):
        if line.startswith('## '):
            return inline(line[3:])
    return ''

def guess_tag(md, module_name):
    title = extract_title(md).lower()
    mn = module_name.lower()

    tag_map = [
        ('agenda', 'AGENDA'), ('session', 'AGENDA'), ('by the end', 'OUTCOME'),
        ('takeaway', 'SUMMARY'), ('key takeaway', 'SUMMARY'),
        ('lab', 'LAB'), ('acceptance', 'LAB'), ('capsule', 'LAB'), ('mcq', 'MCQ'),
        ('checkpoint', 'CHECKPOINT'), ('devtools', 'DEVTOOLS'), ('inspect', 'DEVTOOLS'),
        ('troubleshoot', 'TROUBLESHOOTING'),
        ('form', 'FORMS'), ('input type', 'FORMS'), ('select', 'FORMS'), ('validation', 'FORMS'),
        ('html', 'HTML'), ('semantic', 'HTML'), ('heading', 'HTML'), ('link', 'HTML'),
        ('image', 'HTML'), ('list', 'HTML'), ('table', 'HTML'), ('meta', 'HTML'), ('tag', 'HTML'),
        ('responsive', 'RESPONSIVE'), ('media quer', 'RESPONSIVE'), ('breakpoint', 'RESPONSIVE'),
        ('viewport', 'RESPONSIVE'), ('flexbox', 'LAYOUT'), ('grid', 'LAYOUT'), ('position', 'CSS'),
        ('typograph', 'TYPOGRAPHY'), ('font', 'TYPOGRAPHY'), ('web font', 'TYPOGRAPHY'),
        ('color', 'VISUAL'), ('background', 'VISUAL'), ('gradient', 'VISUAL'),
        ('transition', 'ANIMATION'), ('animation', 'ANIMATION'), ('@keyframes', 'ANIMATION'),
        ('reduced-motion', 'ACCESSIBILITY'), ('motion', 'ACCESSIBILITY'),
        ('bootstrap', 'BOOTSTRAP'), ('semantic ui', 'SEMANTIC UI'),
        ('framework', 'FRAMEWORKS'), ('comparison', 'FRAMEWORKS'), ('choosing', 'FRAMEWORKS'),
        ('cascade', 'CSS'), ('specificity', 'CSS'), ('box model', 'CSS'),
        ('display', 'CSS'), ('unit', 'CSS'), ('pseudo', 'CSS'),
        ('selector', 'CSS'), ('css syntax', 'CSS'), ('common css', 'CSS'),
        ('performance', 'PERFORMANCE'), ('bundle', 'PERFORMANCE'),
        ('migration', 'MIGRATION'),
    ]
    for keyword, tag in tag_map:
        if keyword in title:
            return tag
    return ''

# ─── CSS ───
# Uses clamp() for fluid font sizes and % padding so slides scale at any zoom.
# Base: 1vw ≈ 13.3px at 1333px viewport. All sizes scale proportionally.
CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;background:#1a1a2e;color:#101820;overflow:hidden}
.deck{position:relative;width:100vw;height:100vh}
.slide{position:absolute;inset:0;width:100%;height:100%;display:none;flex-direction:column;background:#fff;overflow-y:auto;overflow-x:hidden;
  font-size:clamp(10px,1.15vw,18px)}
/* Scale all inline-styled visuals proportionally */
.bd>*{max-width:100%}
.slide.active{display:flex}
code{font-family:Consolas,'Courier New',monospace;background:#F2F5F7;padding:.05em .35em;border-radius:3px;font-size:0.92em}
:root{--blue:#3D8DFF;--ink:#101820;--body:#5D6874;--green:#2BAA76;--cyan:#6DCBF4;--panel:#F2F5F7;--blue-tint:#EAF4FF;--green-tint:#EAF6F1;--red-tint:#FFEDED;--dark:#101820;--dark-badge:#1D2A35;--code-bg:#0B1220;--code-tab:#172235;--code-text:#EAF6FF;--code-line:#587087;--dot-red:#FF6B6B;--dot-yellow:#F5C451;--dot-green:#38C987;--subtitle-light:#C9D6E0;--footer-light:#91A2B0;--high-red:#D85B5B}

/* Chrome */
.sc{padding:0;display:flex;flex-direction:column;height:100%}
.ch{display:flex;justify-content:space-between;align-items:center;padding:1.8% 3.6% 0}
.cm{font-size:clamp(10px,.95em,15px);font-weight:700;color:var(--blue);letter-spacing:.5px}
.ct{font-size:clamp(10px,.95em,15px);font-weight:700;color:var(--body);letter-spacing:.5px}
.tt{font-size:clamp(22px,2.9em,48px);font-weight:700;color:var(--ink);padding:.6% 3.6% 0;line-height:1.2}
.dv{height:1px;background:#E0E4E8;margin:.9% 3.6% 0}
.bd{flex:1;padding:1.2% 3.6% 3%;overflow-y:auto;overflow-x:hidden}
.ft{display:flex;justify-content:space-between;align-items:center;padding:0 3.6% .8%;min-height:2.5%}
.fl{font-size:clamp(8px,.8em,13px);font-weight:700;color:var(--body)}
.fr{font-size:clamp(9px,.85em,14px);font-weight:700;color:var(--body)}

/* Title slide */
.s-title{background:var(--dark);position:relative}
.t-rpanel{position:absolute;right:0;top:0;bottom:0;width:37%;background:var(--blue)}
.t-rcard{position:absolute;right:5%;top:11%;width:26%;background:#fff;border-radius:.6em;padding:1.4em 1.6em}
.t-rcard .rl{margin-bottom:.4em}
.t-rcard .r1{font-size:clamp(14px,1.4em,22px);font-weight:700;color:var(--blue)}
.t-rcard .r2{font-size:clamp(11px,1.05em,17px);font-weight:700;color:var(--ink)}
.t-rcard .r3{font-size:clamp(10px,.9em,15px);font-weight:700;color:var(--green)}
.t-badges{position:absolute;right:5.2%;top:44%;display:flex;gap:.5em;align-items:center}
.t-badges span{font-size:clamp(16px,1.7em,28px);font-weight:700;color:#fff;padding:.5em 1em}
.t-badges .plus{color:var(--dark-badge)}
.t-cnt{position:relative;z-index:2;padding:3.5% 4% 4%;height:100%;display:flex;flex-direction:column}
.t-mod{font-size:clamp(11px,1em,16px);font-weight:700;color:var(--cyan);margin-top:1.5%}
.t-main{font-size:clamp(28px,4.5em,72px);font-weight:700;color:#fff;line-height:1.15;margin-top:2%}
.t-sub{font-size:clamp(14px,1.85em,30px);color:var(--subtitle-light);margin-top:2%;max-width:55%;line-height:1.4}
.t-dur{background:var(--dark-badge);border-radius:.4em;padding:.9em 1.3em;margin-top:auto;margin-bottom:6%;display:inline-block;max-width:45%}
.t-dur span{font-size:clamp(14px,1.5em,24px);font-weight:700;color:#fff}
.t-ft{position:absolute;bottom:1.2%;left:4%;font-size:clamp(10px,.95em,15px);font-weight:700;color:var(--footer-light)}

/* End slide */
.s-end{background:var(--dark)}
.s-end .tbl th{color:#8899AA;border-bottom-color:#2A3A4E}
.s-end .tbl td{color:#C9D6E0;border-bottom-color:#1D2A35}
.s-end .tbl tr:nth-child(even) td{background:#141E2A}
.s-end .tbl td:first-child{color:var(--cyan);font-weight:700}
.s-end .bl li{color:#C9D6E0}
.s-end .bl li::before{background:var(--cyan)}
.s-end p{color:#C9D6E0 !important}
.s-end strong{color:#fff}
.s-end code{background:#1D2A35;color:var(--cyan)}
.e-cnt{padding:3.5% 4% 4%;height:100%;display:flex;flex-direction:column}
.e-mod{font-size:clamp(11px,1em,16px);font-weight:700;color:var(--cyan)}
.e-ttl{font-size:clamp(24px,3.9em,62px);font-weight:700;color:#fff;line-height:1.2;margin-top:3%}
.e-dv{height:1px;background:#303C4A;margin-top:4%}
.e-pls{display:flex;margin-top:2%}
.e-pl{flex:1}
.e-pl-l{font-size:clamp(10px,.95em,15px);font-weight:700;color:var(--cyan);letter-spacing:.5px}
.e-pl-l.g{color:var(--green)}
.e-pl-v{font-size:clamp(14px,1.6em,26px);font-weight:700;color:#fff;margin-top:.5em}
.e-ban{background:var(--blue);border-radius:.5em;padding:1.2em 1.6em;margin-top:auto;margin-bottom:1.5%}
.e-ban span{font-size:clamp(13px,1.55em,25px);font-weight:700;color:#fff}

/* Bullets */
.bl{list-style:none;padding:0}
.bl li{font-size:clamp(13px,1.4em,22px);color:var(--ink);line-height:1.55;padding:.25em 0 .25em 1.6em;position:relative}
.bl li::before{content:'';position:absolute;left:0;top:.65em;width:.5em;height:.5em;border-radius:50%;background:var(--blue)}
.bl li.s{font-size:clamp(12px,1.28em,20px);color:var(--body);padding-left:3.2em}
.bl li.s::before{left:1.6em;width:.4em;height:.4em}
.bl li.e{padding:.1em 0}.bl li.e::before{display:none}

/* Callout boxes */
.ib{background:var(--blue-tint);border-radius:.5em;padding:.9em 1.3em;margin-top:1em}
.ib-l{font-size:clamp(10px,1em,16px);font-weight:700;color:var(--blue)}
.ib-t{font-size:clamp(14px,1.5em,24px);font-weight:700;color:var(--ink);margin-top:.25em}
.eb{background:var(--green-tint);border-radius:.5em;padding:.9em 1.3em;margin-top:1em}
.eb-t{font-size:clamp(12px,1.2em,19px);font-weight:700;color:var(--green)}
.db{background:var(--ink);border-radius:.5em;padding:1em 1.3em;margin-top:1em;display:flex;align-items:center;gap:1em}
.db-l{font-size:clamp(10px,.95em,15px);font-weight:700;color:var(--cyan)}
.db-t{font-size:clamp(14px,1.8em,29px);font-weight:700;color:#fff}

/* Tables */
.tbl{width:100%;border-collapse:separate;border-spacing:0;font-size:clamp(11px,1.15em,18px);margin-top:.6em}
.tbl th{text-align:left;font-size:clamp(9px,.88em,14px);font-weight:700;color:var(--body);padding:.5em .8em;border-bottom:2px solid #E0E4E8}
.tbl td{padding:.5em .8em;border-bottom:1px solid #F0F0F0;color:var(--ink);vertical-align:top}
.tbl tr:nth-child(even) td{background:var(--panel)}
.tbl td:first-child{font-weight:700}

/* Code blocks */
.cb{background:var(--code-bg);border-radius:.65em;overflow:hidden;font-family:Consolas,'Courier New',monospace;margin:.5em 0}
.cb-bar{background:var(--code-tab);padding:.65em 1em;display:flex;align-items:center;gap:.5em;border-bottom:.2em solid var(--code-tab)}
.dot{width:.8em;height:.8em;border-radius:50%}.dot.r{background:var(--dot-red)}.dot.y{background:var(--dot-yellow)}.dot.g{background:var(--dot-green)}
.cb-fn{font-size:clamp(9px,.88em,14px);font-weight:700;color:#B9C8D8;margin-left:.65em}
.cb-lg{font-size:clamp(8px,.8em,13px);font-weight:700;color:var(--cyan);margin-left:auto}
.cb-body{display:flex;padding:.9em 0}
.cb-ln{color:var(--code-line);font-size:clamp(11px,1.08em,17px);line-height:1.55;padding:0 .4em 0 .9em;text-align:right;user-select:none;border-right:1px solid #2A3A4E;min-width:2.2em}
.cb-cd{color:var(--code-text);font-size:clamp(11px,1.08em,17px);line-height:1.55;padding:0 1.3em;white-space:pre;flex:1;overflow-x:auto}

/* Slide counter (top-right, non-intrusive) */
.slide-counter{position:fixed;top:8px;right:12px;background:rgba(16,24,32,.7);color:#aaa;font-size:12px;font-weight:700;padding:4px 10px;border-radius:4px;z-index:100;pointer-events:none;font-family:Arial,sans-serif}
"""

def build(md_path):
    slides_md = read_slides(md_path)
    num, name, title = extract_module_info(slides_md[0])
    module_label = f"MODULE {num} - {name.upper()}".replace('&', '&amp;')
    out_file = os.path.join(os.path.dirname(md_path), 'slides.html')

    # Title slide parts from first slide
    first = slides_md[0]
    duration = '1 day'
    subtitle = ''
    for line in first.split('\n'):
        if line.startswith('**') and 'day' in line.lower():
            duration = line.strip('* ')
        if not line.startswith('#') and not line.startswith('**') and not line.startswith('##') and line.strip():
            if not subtitle:
                subtitle = line.strip()

    # Build HTML
    out = [f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}</title>
<style>{CSS}</style>
</head>
<body>
<div class="deck" id="deck">

<div class="slide s-title active" data-n="1">
  <div class="t-rpanel"></div>
  <div class="t-cnt">
    <div class="t-mod">MODULE {num}</div>
    <div class="t-main">{title.replace("&","&amp;")}</div>
    <div class="t-sub">{subtitle}</div>
    <div class="t-dur"><span>{duration}</span></div>
    <div class="t-ft">Sustain Engineering Training | July 2026</div>
  </div>
</div>''']

    for idx, slide_md in enumerate(slides_md[1:], 2):
        stitle = extract_title(slide_md)
        tag = guess_tag(slide_md, name)
        body = md_to_html(slide_md)
        is_last = idx == len(slides_md)

        if is_last:
            # End slide: render content in a dark theme
            # Extract the "Next:" line if present for the banner
            next_line = ''
            for mdline in slide_md.split('\n'):
                if mdline.strip().startswith('> **Next:') or mdline.strip().startswith('>**Next:'):
                    next_line = inline(mdline.strip()[2:])
                    break
            if not next_line:
                next_line = 'Review your evidence and prepare for the next module.'
            out.append(f'''
<div class="slide s-end" data-n="{idx}">
  <div class="e-cnt">
    <div class="e-mod">MODULE {num} - COMPLETE</div>
    <div class="e-ttl">{stitle}</div>
    <div class="e-dv"></div>
    <div style="flex:1;overflow:auto;margin-top:20px">{body}</div>
    <div class="e-ban"><span>{next_line}</span></div>
  </div>
</div>''')
        else:
            sn = f'{idx:02d}'
            out.append(f'''
<div class="slide" data-n="{idx}">
  <div class="sc">
    <div class="ch"><span class="cm">{module_label}</span><span class="ct">{tag}</span></div>
    <div class="tt">{stitle}</div>
    <div class="dv"></div>
    <div class="bd">{body}</div>
    <div class="ft"><span class="fr">{sn}</span></div>
  </div>
</div>''')

    total = len(slides_md)
    out.append(f'''
</div>
<div class="slide-counter" id="sc">1 / {total}</div>
<script>
const S=document.querySelectorAll('.slide');let c=0;
function show(n){{S[c].classList.remove('active');c=Math.max(0,Math.min(n,S.length-1));S[c].classList.add('active');document.getElementById('sc').textContent=(c+1)+' / '+S.length;S[c].scrollTop=0}}
function go(d){{show(c+d)}}
document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key===' '){{e.preventDefault();go(1)}}if(e.key==='ArrowLeft'){{e.preventDefault();go(-1)}}if(e.key==='Home'){{e.preventDefault();show(0)}}if(e.key==='End'){{e.preventDefault();show(S.length-1)}}}});
show(0);
</script>
</body></html>''')

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'Built {out_file} with {total} slides')

if __name__ == '__main__':
    md = find_md()
    print(f'Building from: {md}')
    build(md)
