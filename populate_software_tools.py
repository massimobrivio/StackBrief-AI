from app import app, db
from app.models import SoftwareTool

def populate_software_tools():
    with app.app_context():
        # Define dummy data
        dummy_software_tools = [
            SoftwareTool(
                name='Tool Alpha',
                vendor='Alpha Corp',
                official_website='https://alpha.example.com',
                update_source='rss',
                update_url='https://alpha.example.com/updates/rss'
            ),
            SoftwareTool(
                name='Tool Beta',
                vendor='Beta LLC',
                official_website='https://beta.example.com',
                update_source='api',
                update_url='https://api.beta.example.com/updates'
            ),
            SoftwareTool(
                name='Tool Gamma',
                vendor='Gamma Inc',
                official_website='https://gamma.example.com',
                update_source='scrape',
                update_url='https://gamma.example.com/updates'
            ),
            SoftwareTool(
                name='Tool Delta',
                vendor='Delta Solutions',
                official_website='https://delta.example.com',
                update_source='rss',
                update_url='https://delta.example.com/feed'
            ),
            SoftwareTool(
                name='Tool Epsilon',
                vendor='Epsilon Tech',
                official_website='https://epsilon.example.com',
                update_source='api',
                update_url='https://api.epsilon.example.com/v1/updates'
            ),
        ]

        # Add the tools to the database
        db.session.bulk_save_objects(dummy_software_tools)
        db.session.commit()
        print("Dummy software tools have been added to the database.")

if __name__ == '__main__':
    populate_software_tools()
