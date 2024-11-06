from app import db
from app.models import SoftwareTool

tool1 = SoftwareTool(
    name="ToolA",
    vendor="VendorA",
    official_website="https://toola.com",
    update_source="rss",
    update_url="https://tool-a.com/updates/rss",
)
tool2 = SoftwareTool(
    name="ToolB",
    vendor="VendorB",
    official_website="https://toolb.com",
    update_source="rss",
    update_url="https://tool-b.com/updates/rss",
)
db.session.add(tool1)
db.session.add(tool2)
db.session.commit()
