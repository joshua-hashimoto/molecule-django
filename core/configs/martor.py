MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',        # to enable/disable emoji icons.
    'imgur': 'true',        # to enable/disable imgur/custom uploader.
    'mention': 'false',     # to enable/disable mention
    # to include/revoke jquery (require for admin default django)
    'jquery': 'true',
    'living': 'false',      # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',         # to enable/disable hljs highlighting in preview
}
# Upload to locale storage
MARTOR_UPLOAD_URL = '/api/uploader/'  # change to local uploader
# Maximum Upload Image
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_IMAGE_UPLOAD_SIZE = 10485760
MARTOR_MARKDOWN_EXTENSIONS = [
    # default extensions.
    'markdown.extensions.extra',  # code
    'markdown.extensions.nl2br',  # new line
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',
    # Custom markdown extensions for martor.
    'martor.extensions.urlize',
    'martor.extensions.del_ins',      # ~~strikethrough~~ and ++underscores++
    'martor.extensions.mention',      # to parse markdown mention
    'martor.extensions.emoji',        # to parse markdown emoji
    'martor.extensions.mdx_video',    # to parse embed/iframe video
    'martor.extensions.escape_html',  # to handle the XSS vulnerabilities
    # added extensions.
    'markdown.extensions.toc',  # TOC
    'markdown.extensions.tables',  # table
    'markdown.extensions.codehilite',  # code line highlight
]
MARTOR_THEME = 'bootstrap'
