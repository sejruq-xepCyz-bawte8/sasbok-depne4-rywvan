import anvil.image
import base64

def parse_cover_image(file, **event)->str:
     cover = anvil.image.generate_thumbnail(file, 300)
     content_type = file.content_type
     cover_bytes = cover.get_bytes()
     image_base64 = base64.b64encode(cover_bytes).decode('utf-8')
     image_url = f'data:{content_type};base64,{image_base64}'
     #url = image_url #f'url("{image_url}")'
     #bytes = image_base64
     #mime = content_type
     return image_url