import falcon

class Docs:
    def __init__(self):
        self.content = self.read_html("docs/template.html")
        

    def read_html(self, filename):
        with open(filename, 'r') as f:
            return f.read()

        return None

    async def on_get_docs(self, req, resp): #get_template
        resp.content_type = falcon.MEDIA_HTML

        resp.text = self.content
        resp.status = falcon.HTTP_200

    async def on_get_template(self, req, resp): #get_docs
        resp.content_type = falcon.MEDIA_HTML

        self.def_yaml = self.read_html("docs/openapi.yaml")

        resp.text = self.def_yaml
        resp.status = falcon.HTTP_200
