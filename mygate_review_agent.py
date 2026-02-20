"""
MYGATE REVIEW ANALYSIS AGENT

What this does:
- Scrapes MyGate app reviews from Google Play Store / Apple App Store
- Categorizes reviews by theme (security, visitor management, bugs, etc.)
- Answers questions about reviews using AI
- Creates dashboard with insights

This is PERFECT for PMs because:
- Understand user pain points
- Track sentiment over time
- Identify feature requests
- Monitor competitor feedback
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import random
from collections import Counter
import re

class MyGateReviewAnalysisAgent:
    """
    Intelligent agent to analyze MyGate app reviews
    """
    
    def __init__(self):
        print("🏢 MyGate Review Analysis Agent initialized!")
        print("📱 Data sources: Google Play Store, Apple App Store")
        
        # In production, you'd scrape real reviews
        # For now, we'll simulate realistic MyGate reviews
        self.reviews = self._load_reviews()
        
        # Pre-defined categories for MyGate
        self.categories = {
            'visitor_management': ['visitor', 'guest', 'delivery', 'approve', 'qr'],
            'security': ['security', 'guard', 'safe', 'surveillance', 'camera'],
            'bugs': ['crash', 'bug', 'error', 'not working', 'freeze', 'slow'],
            'ui_ux': ['interface', 'design', 'confusing', 'easy', 'navigate'],
            'notifications': ['notification', 'alert', 'push', 'remind'],
            'payment': ['payment', 'billing', 'charge', 'subscription'],
            'staff_helpdesk': ['staff', 'support', 'help', 'response', 'customer service'],
            'community': ['neighbors', 'community', 'society', 'apartment'],
            'feature_request': ['add', 'need', 'should have', 'missing', 'wish']
        }
        
        print(f"✅ Loaded {len(self.reviews)} reviews")
        print(f"📊 Tracking {len(self.categories)} categories")
    
    def _load_reviews(self):
        """
        In production, this would scrape real reviews using:
        
        Option 1: google-play-scraper library
        from google_play_scraper import app, reviews
        result = reviews(
            'com.nextgendevlabs.mygate',
            lang='en',
            country='in',
            count=1000
        )
        
        Option 2: app-store-scraper for iOS
        from app_store_scraper import AppStore
        mygate = AppStore(country='in', app_name='mygate')
        mygate.review(how_many=1000)
        
        For demo, we'll simulate realistic MyGate reviews
        """
        
        # Realistic review templates based on actual MyGate issues
        review_templates = [
            # Positive reviews
            {"text": "Great app for visitor management! QR code feature works smoothly.", "rating": 5, "category": "visitor_management"},
            {"text": "Very useful for tracking deliveries and guests. Security is improved.", "rating": 5, "category": "security"},
            {"text": "Easy to approve visitors from anywhere. Love the notifications!", "rating": 4, "category": "visitor_management"},
            {"text": "Good app for community living. Staff coordination is better now.", "rating": 4, "category": "community"},
            
            # Negative reviews
            {"text": "App crashes frequently. Can't approve visitors when needed urgently!", "rating": 1, "category": "bugs"},
            {"text": "Notifications don't work properly. Missed important visitor approvals.", "rating": 2, "category": "notifications"},
            {"text": "Too many bugs after latest update. Very slow performance.", "rating": 1, "category": "bugs"},
            {"text": "UI is confusing. Hard to find visitor history.", "rating": 2, "category": "ui_ux"},
            {"text": "Payment issues! Getting charged twice for subscription.", "rating": 1, "category": "payment"},
            {"text": "Customer support is terrible. No response for days.", "rating": 1, "category": "staff_helpdesk"},
            
            # Feature requests
            {"text": "Need video calling feature for visitor verification!", "rating": 3, "category": "feature_request"},
            {"text": "Should add delivery tracking with photos. Very needed!", "rating": 3, "category": "feature_request"},
            {"text": "Missing guest pre-approval feature. Please add!", "rating": 3, "category": "feature_request"},
            
            # Mixed reviews
            {"text": "App is good but crashes sometimes. Fix the bugs please.", "rating": 3, "category": "bugs"},
            {"text": "Visitor management works but notifications are delayed.", "rating": 3, "category": "notifications"},
        ]
        
        # Generate 500 simulated reviews
        reviews = []
        for i in range(500):
            template = random.choice(review_templates)
            review = {
                'id': i + 1,
                'text': template['text'],
                'rating': template['rating'],
                'date': (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d'),
                'version': random.choice(['5.2.1', '5.2.0', '5.1.8', '5.1.5']),
                'helpful_count': random.randint(0, 50),
                'source': random.choice(['Google Play', 'App Store']),
                'primary_category': template['category']
            }
            reviews.append(review)
        
        return pd.DataFrame(reviews)
    
    # ========================================================================
    # CORE ANALYSIS FUNCTIONS
    # ========================================================================
    
    def get_overview(self):
        """Get high-level metrics"""
        print("\n📊 MyGate App Reviews - Overview")
        print("=" * 80)
        
        total_reviews = len(self.reviews)
        avg_rating = self.reviews['rating'].mean()
        recent_reviews = len(self.reviews[pd.to_datetime(self.reviews['date']) > datetime.now() - timedelta(days=30)])
        
        print(f"\n📈 Key Metrics:")
        print(f"  Total Reviews: {total_reviews}")
        print(f"  Average Rating: {avg_rating:.2f} / 5.0")
        print(f"  Reviews (Last 30 days): {recent_reviews}")
        
        # Rating distribution
        print(f"\n⭐ Rating Distribution:")
        rating_dist = self.reviews['rating'].value_counts().sort_index(ascending=False)
        for rating, count in rating_dist.items():
            pct = (count / total_reviews) * 100
            bar = '█' * int(pct / 2)
            print(f"  {rating}⭐: {bar} {count} ({pct:.1f}%)")
        
        return {
            'total_reviews': total_reviews,
            'avg_rating': avg_rating,
            'recent_reviews': recent_reviews,
            'rating_distribution': rating_dist.to_dict()
        }
    
    def categorize_reviews(self):
        """Automatically categorize reviews by theme"""
        print("\n🏷️  Review Categories")
        print("=" * 80)
        
        # Count reviews by category
        category_counts = self.reviews['primary_category'].value_counts()
        
        print("\n📂 Top Issues/Topics:")
        for category, count in category_counts.items():
            pct = (count / len(self.reviews)) * 100
            emoji = self._get_category_emoji(category)
            print(f"  {emoji} {category.replace('_', ' ').title()}: {count} ({pct:.1f}%)")
        
        return category_counts
    
    def get_sentiment_by_category(self):
        """Analyze sentiment for each category"""
        print("\n😊 Sentiment by Category")
        print("=" * 80)
        
        for category in self.reviews['primary_category'].unique():
            cat_reviews = self.reviews[self.reviews['primary_category'] == category]
            avg_rating = cat_reviews['rating'].mean()
            
            sentiment = "Positive" if avg_rating >= 4 else "Negative" if avg_rating < 3 else "Mixed"
            emoji = "✅" if sentiment == "Positive" else "❌" if sentiment == "Negative" else "⚠️"
            
            print(f"\n{emoji} {category.replace('_', ' ').title()}:")
            print(f"  Average Rating: {avg_rating:.2f}/5.0")
            print(f"  Sentiment: {sentiment}")
            print(f"  Review Count: {len(cat_reviews)}")
    
    def find_common_complaints(self):
        """Extract most common complaints"""
        print("\n⚠️  Top User Complaints")
        print("=" * 80)
        
        # Get negative reviews (1-2 stars)
        negative_reviews = self.reviews[self.reviews['rating'] <= 2]
        
        print(f"\n📉 Found {len(negative_reviews)} negative reviews (1-2 stars)")
        print(f"\nMost Common Issues:")
        
        complaints = negative_reviews['primary_category'].value_counts().head(5)
        for i, (category, count) in enumerate(complaints.items(), 1):
            pct = (count / len(negative_reviews)) * 100
            print(f"  {i}. {category.replace('_', ' ').title()}: {count} complaints ({pct:.1f}%)")
            
            # Show example
            example = negative_reviews[negative_reviews['primary_category'] == category].iloc[0]
            print(f"     Example: \"{example['text'][:80]}...\"")
            print()
    
    def find_feature_requests(self):
        """Extract feature requests from reviews"""
        print("\n💡 Feature Requests from Users")
        print("=" * 80)
        
        feature_requests = self.reviews[self.reviews['primary_category'] == 'feature_request']
        
        print(f"\n🎯 Found {len(feature_requests)} feature request mentions")
        print(f"\nTop Requested Features:")
        
        # In production, use NLP to extract actual features
        # For demo, show examples
        for i, review in feature_requests.head(5).iterrows():
            print(f"  • {review['text']}")
            print(f"    Rating: {review['rating']}⭐ | Date: {review['date']}")
            print()
    
    def analyze_version_feedback(self):
        """Track issues by app version"""
        print("\n📱 Feedback by App Version")
        print("=" * 80)
        
        version_stats = self.reviews.groupby('version').agg({
            'rating': ['mean', 'count']
        }).round(2)
        
        print("\n🔄 Version Performance:")
        for version in version_stats.index:
            avg_rating = version_stats.loc[version, ('rating', 'mean')]
            count = version_stats.loc[version, ('rating', 'count')]
            
            status = "✅" if avg_rating >= 4 else "⚠️" if avg_rating >= 3 else "❌"
            print(f"  {status} v{version}: {avg_rating}/5.0 ({int(count)} reviews)")
    
    def track_trends_over_time(self):
        """Track rating trends over time"""
        print("\n📈 Rating Trends Over Time")
        print("=" * 80)
        
        # Group by month
        self.reviews['month'] = pd.to_datetime(self.reviews['date']).dt.to_period('M')
        monthly = self.reviews.groupby('month')['rating'].agg(['mean', 'count'])
        
        print("\n📅 Monthly Trends (Last 6 months):")
        for month in monthly.tail(6).index:
            avg_rating = monthly.loc[month, 'mean']
            count = monthly.loc[month, 'count']
            
            trend = "📈" if avg_rating >= 4 else "📉" if avg_rating < 3 else "➡️"
            print(f"  {trend} {month}: {avg_rating:.2f}/5.0 ({int(count)} reviews)")
    
    # ========================================================================
    # INTELLIGENT Q&A (This is where agents shine!)
    # ========================================================================
    
    def answer_question(self, question):
        """
        Natural language Q&A about reviews
        
        In production, this would use Claude API to analyze reviews:
        
        import anthropic
        client = anthropic.Anthropic(api_key="...")
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"Based on these reviews: {reviews_text}\n\nQuestion: {question}"
            }]
        )
        """
        
        question = question.lower()
        
        print(f"\n💬 Question: {question}")
        print("=" * 80)
        
        # Simple keyword-based responses (in production, use LLM)
        if 'bug' in question or 'crash' in question or 'issue' in question:
            print("\n🤖 Agent Answer:")
            bugs = self.reviews[self.reviews['primary_category'] == 'bugs']
            print(f"There are {len(bugs)} reviews mentioning bugs or crashes.")
            print(f"Average rating for bug-related reviews: {bugs['rating'].mean():.2f}/5.0")
            print(f"\nMost common bug complaints:")
            for i, review in bugs.head(3).iterrows():
                print(f"  • \"{review['text']}\" ({review['rating']}⭐)")
        
        elif 'visitor' in question or 'guest' in question:
            print("\n🤖 Agent Answer:")
            visitor = self.reviews[self.reviews['primary_category'] == 'visitor_management']
            print(f"Visitor management is mentioned in {len(visitor)} reviews.")
            print(f"Average rating: {visitor['rating'].mean():.2f}/5.0")
            positive = len(visitor[visitor['rating'] >= 4])
            print(f"{positive} positive reviews ({positive/len(visitor)*100:.1f}%)")
        
        elif 'feature' in question or 'request' in question or 'add' in question:
            print("\n🤖 Agent Answer:")
            self.find_feature_requests()
        
        elif 'rating' in question or 'score' in question:
            print("\n🤖 Agent Answer:")
            print(f"Average rating: {self.reviews['rating'].mean():.2f}/5.0")
            print(f"Based on {len(self.reviews)} total reviews")
            
        elif 'recent' in question or 'latest' in question:
            print("\n🤖 Agent Answer:")
            recent = self.reviews[pd.to_datetime(self.reviews['date']) > datetime.now() - timedelta(days=30)]
            print(f"In the last 30 days:")
            print(f"  Reviews: {len(recent)}")
            print(f"  Average Rating: {recent['rating'].mean():.2f}/5.0")
            print(f"  Trend: {'Improving' if recent['rating'].mean() > self.reviews['rating'].mean() else 'Declining'}")
        
        else:
            print("\n🤖 Agent Answer:")
            print("I can help you analyze MyGate reviews! Try asking:")
            print("  • What are the main bugs users report?")
            print("  • How is visitor management performing?")
            print("  • What features are users requesting?")
            print("  • What's the recent rating trend?")
    
    # ========================================================================
    # DASHBOARD CREATION
    # ========================================================================
    
    def create_dashboard(self):
        """Generate a comprehensive dashboard"""
        print("\n" + "="*80)
        print("📊 MYGATE APP REVIEW DASHBOARD")
        print("="*80)
        
        self.get_overview()
        self.categorize_reviews()
        self.get_sentiment_by_category()
        self.find_common_complaints()
        self.track_trends_over_time()
        
        print("\n" + "="*80)
        print("✅ Dashboard Complete!")
        print("="*80)
    
    # ========================================================================
    # HELPER FUNCTIONS
    # ========================================================================
    
    def _get_category_emoji(self, category):
        """Get emoji for category"""
        emojis = {
            'visitor_management': '🚪',
            'security': '🔒',
            'bugs': '🐛',
            'ui_ux': '🎨',
            'notifications': '🔔',
            'payment': '💳',
            'staff_helpdesk': '🤝',
            'community': '🏘️',
            'feature_request': '💡'
        }
        return emojis.get(category, '📝')
    
    def export_insights(self):
        """Export insights to files for sharing"""
        print("\n📤 Exporting Insights...")
        
        # Save to CSV
        self.reviews.to_csv('/home/claude/mygate_reviews.csv', index=False)
        print("  ✅ Reviews saved to: mygate_reviews.csv")
        
        # Save summary
        summary = {
            'total_reviews': len(self.reviews),
            'avg_rating': float(self.reviews['rating'].mean()),
            'top_categories': self.reviews['primary_category'].value_counts().head(5).to_dict(),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('/home/claude/mygate_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        print("  ✅ Summary saved to: mygate_summary.json")


# ============================================================================
# DEMO & INTERACTIVE MODE
# ============================================================================

def interactive_mode():
    """Interactive Q&A mode"""
    agent = MyGateReviewAnalysisAgent()
    
    print("\n" + "="*80)
    print("🤖 INTERACTIVE MODE - Ask questions about MyGate reviews!")
    print("="*80)
    print("\nExample questions:")
    print("  • What are the main bugs?")
    print("  • How is visitor management performing?")
    print("  • What features do users want?")
    print("  • Show me the dashboard")
    print("\nType 'exit' to quit\n")
    
    while True:
        question = input("💬 Your question: ").strip()
        
        if question.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Thanks for using MyGate Review Agent!")
            break
        
        if 'dashboard' in question.lower():
            agent.create_dashboard()
        else:
            agent.answer_question(question)
        
        print("\n" + "-"*80 + "\n")


if __name__ == "__main__":
    print("="*80)
    print("🏢 MYGATE REVIEW ANALYSIS AGENT - DEMO")
    print("="*80)
    print("\nThis agent analyzes app reviews to help PMs understand:")
    print("  • User sentiment and satisfaction")
    print("  • Common bugs and issues")
    print("  • Feature requests")
    print("  • Category-wise feedback")
    print()
    
    # Initialize agent
    agent = MyGateReviewAnalysisAgent()
    
    # Run automated analysis
    print("\n🔍 Running Automated Analysis...")
    agent.create_dashboard()
    
    # Demo Q&A
    print("\n\n🎯 Demo: Intelligent Q&A")
    print("="*80)
    
    questions = [
        "What are the main bugs users are reporting?",
        "How is visitor management performing?",
        "What features are users requesting?"
    ]
    
    for q in questions:
        agent.answer_question(q)
        print()
    
    # Export
    agent.export_insights()
    
    print("\n" + "="*80)
    print("✅ Demo Complete!")
    print("="*80)
    print("\nIn production, this would:")
    print("  • Scrape REAL reviews from Play Store / App Store")
    print("  • Use Claude API for intelligent Q&A")
    print("  • Update daily automatically")
    print("  • Send alerts when ratings drop")
    print("  • Create visual dashboards with charts")
