import pandas as pd

# Load the reviews you just scraped
df = pd.read_csv('mygate_reviews_real.csv')

print("📊 MYGATE REVIEW ANALYSIS\n")

# 1. Rating breakdown
print("⭐ Rating Distribution:")
print(df['score'].value_counts().sort_index(ascending=False))

# 2. Find negative reviews
print("\n❌ Negative Reviews (1-2 stars):")
negative = df[df['score'] <= 2]
print(f"Found {len(negative)} negative reviews ({len(negative)/len(df)*100:.1f}%)")

# 3. Look for common complaints
print("\n🐛 Reviews mentioning 'bug' or 'crash':")
bugs = df[df['content'].str.contains('bug|crash|error', case=False, na=False)]
print(f"Found {len(bugs)} bug-related reviews")

# Show examples
for i, review in bugs.head(3).iterrows():
    print(f"\n{review['score']}⭐: {review['content'][:150]}...")

# 4. Feature requests
print("\n💡 Reviews asking for features:")
features = df[df['content'].str.contains('add|need|should', case=False, na=False)]
print(f"Found {len(features)} feature request mentions")

for i, review in features.head(3).iterrows():
    print(f"\n{review['score']}⭐: {review['content'][:150]}...")
