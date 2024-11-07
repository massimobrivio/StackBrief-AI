import feedparser

# Function to get GitHub Changelog (RSS Feed)
def get_github_updates():
    url = "https://github.blog/changelog/feed/"
    feed = feedparser.parse(url)
    latest_entry = feed.entries[0]
    return f"Latest GitHub update: {latest_entry.title} - {latest_entry.link}"

# Main function to run all updates
def main():
    print(get_github_updates())

if __name__ == "__main__":
    main()
