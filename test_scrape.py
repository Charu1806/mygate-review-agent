from google_play_scraper import app, reviews_all
import pandas as pd

print("🔍 Scraping MyGate reviews...")

# Get app info
app_id = "com.mygate.user"
mygate_info = app('com.mygate.user')
print(f"\nApp: {mygate_info['title']}")
print(f"Rating: {mygate_info['score']}/5.0")
print(f"Total Reviews: {mygate_info['ratings']}")

# Get recent reviews
print("\n Fetching 100 recent reviews...")
reviews = reviews_all(
    app_id,
    lang='en',
    country='in',
    count=100  # Start with 100 for speed
)

# Convert to DataFrame
df = pd.DataFrame(reviews)

# Show basic stats
print(f"\n Successfully scraped {len(df)} reviews!")
print(f"Average rating: {df['score'].mean():.2f}/5.0")
print(f"Date range: {df['at'].min()} to {df['at'].max()}")

# Show a few examples
print("\n Sample reviews:")
for i in range(3):
    review = df.iloc[i]
    print(f"\n{review['score']}⭐ - {review['at'].strftime('%Y-%m-%d')}")
    print(f"{review['content'][:100]}...")

# Save to CSV
df.to_csv('mygate_reviews_real.csv', index=False)
print("\n💾 Saved to: mygate_reviews_real.csv")
