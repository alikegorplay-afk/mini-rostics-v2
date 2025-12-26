from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

ROBOTS = """
User-agent: *
Allow: /

# Поисковые системы
User-agent: Googlebot
Allow: /static/
Allow: /images/
Crawl-delay: 1

User-agent: YandexBot
Allow: /static/
Allow: /images/
Crawl-delay: 2

# Боты соцсетей
User-agent: FacebookBot
Allow: /
Crawl-delay: 3

User-agent: TwitterBot
Allow: /
Crawl-delay: 3

# Плохие боты
User-agent: MJ12bot
Disallow: /

User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /
"""

router = APIRouter(tags= ["robots"])

@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return ROBOTS