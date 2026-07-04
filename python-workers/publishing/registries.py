class RendererRegistry:
    def __init__(self):
        # We store metadata for rendering engines without coupling them to our process
        self._renderers = {
            "PDFRenderer": {"version": "1.0", "description": "Native PDF output generator"},
            "PPTXRenderer": {"version": "1.0", "description": "Native PPTX output generator"},
            "HTMLRenderer": {"version": "1.0", "description": "HTML export utility"},
            "MarkdownRenderer": {"version": "1.0", "description": "Markdown text formatter"},
            "ReactRenderer": {"version": "1.0", "description": "Frontend UI generator"},
            "NextJSRenderer": {"version": "1.0", "description": "React Server Component UI generator"},
            "MobileRenderer": {"version": "1.0", "description": "React Native mapping output"},
            "APIRenderer": {"version": "1.0", "description": "Headless JSON payload formatter"}
        }

    def is_supported(self, renderer_name: str) -> bool:
        return renderer_name in self._renderers

    def get_metadata(self, renderer_name: str) -> dict:
        return self._renderers.get(renderer_name, {})

class TemplateRegistry:
    def __init__(self):
        # We store templates as metadata-driven configurations
        self._templates = {
            "Executive": {"version": "1.0", "layout": "Summary-heavy"},
            "Corporate": {"version": "1.0", "layout": "Standard"},
            "Investor": {"version": "1.0", "layout": "Financial-heavy"},
            "Board": {"version": "1.0", "layout": "Strategic"},
            "Minimal": {"version": "1.0", "layout": "Clean"},
            "Dark": {"version": "1.0", "layout": "Dark-mode default"},
            "Light": {"version": "1.0", "layout": "Light-mode default"},
            "WhiteLabel": {"version": "1.0", "layout": "Custom-branded"}
        }

    def is_supported(self, template_name: str) -> bool:
        return template_name in self._templates

    def get_metadata(self, template_name: str) -> dict:
        return self._templates.get(template_name, {})
