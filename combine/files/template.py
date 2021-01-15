from jinja2 import meta


from .ignored import IgnoredFile


class TemplateFile(IgnoredFile):
    def render_to_output(self, *args, **kwargs):
        self.load_references(jinja_env=kwargs["jinja_environment"])
        import ipdb

        ipdb.set_trace()

    def load_references(self, jinja_env):
        with open(self.path, "r") as f:
            ast = jinja_env.parse(f.read())
            self.references = list(meta.find_referenced_templates(ast))
