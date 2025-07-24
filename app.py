import streamlit as st
import pandas as pd
import json
from datetime import datetime
import time
import os
from linkedin_scraper import LinkedInScraper
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="LinkedIn Post Automation Tool",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for LinkedIn-inspired styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0A66C2 0%, #00A0DC 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .post-card {
        background: white;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .author-info {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .engagement-stats {
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        color: #666;
    }
    
    .process-step {
        background: #f3f2ef;
        border-left: 4px solid #0A66C2;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0A66C2 0%, #00A0DC 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .stButton > button {
        background: #0A66C2;
        color: white;
        border: none;
        border-radius: 24px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: #004182;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'scraped_posts' not in st.session_state:
    st.session_state.scraped_posts = []
if 'scraper' not in st.session_state:
    st.session_state.scraper = None
if 'total_searches' not in st.session_state:
    st.session_state.total_searches = 0

def initialize_scraper(headless_mode, use_login, email, password):
    """Initialize the LinkedIn scraper with user settings"""
    try:
        if st.session_state.scraper:
            st.session_state.scraper.close()
        
        st.session_state.scraper = LinkedInScraper(headless=headless_mode)
        
        if use_login and email and password:
            with st.spinner("🔐 Logging into LinkedIn..."):
                login_success = st.session_state.scraper.login_to_linkedin(email, password)
                if login_success:
                    st.success("✅ Successfully logged into LinkedIn!")
                    return True
                else:
                    st.error("❌ LinkedIn login failed. Will proceed without login.")
                    return False
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize scraper: {str(e)}")
        return False

def scrape_linkedin_posts(keyword, max_posts, use_login):
    """Scrape LinkedIn posts for the given keyword"""
    if not st.session_state.scraper:
        st.error("❌ Scraper not initialized. Please configure settings first.")
        return []
    
    try:
        with st.spinner(f"🔍 Searching LinkedIn for '{keyword}'..."):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Update progress
            progress_bar.progress(25)
            status_text.text("🌐 Navigating to LinkedIn...")
            time.sleep(1)
            
            progress_bar.progress(50)
            status_text.text("🔍 Searching for posts...")
            
            if use_login:
                posts = st.session_state.scraper.search_posts(keyword, max_posts)
            else:
                posts = st.session_state.scraper.scrape_without_login(keyword, max_posts)
            
            progress_bar.progress(75)
            status_text.text("📊 Processing results...")
            time.sleep(1)
            
            progress_bar.progress(100)
            status_text.text("✅ Scraping completed!")
            time.sleep(1)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            return posts
            
    except Exception as e:
        st.error(f"❌ Error during scraping: {str(e)}")
        return []

def display_post_card(post, index):
    """Display a single post in a card format"""
    with st.container():
        st.markdown(f"""
        <div class="post-card">
            <div class="author-info">
                <div>
                    <strong>{post['author']}</strong><br>
                    <small style="color: #666;">{post['author_title']}</small>
                </div>
            </div>
            
            <h4 style="margin: 0.5rem 0; color: #333;">{post['title']}</h4>
            
            <p style="color: #666; margin: 0.5rem 0;">{post['description'][:200]}{'...' if len(post['description']) > 200 else ''}</p>
            
            <div class="engagement-stats">
                <span>👍 {post['likes']:,} likes</span>
                <span>💬 {post['comments']:,} comments</span>
                <span>🔄 {post['shares']:,} shares</span>
                <span>📅 {post['date']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.text_input("Post URL:", value=post['url'], key=f"url_{index}", disabled=True)
        with col2:
            if st.button("📋 Copy URL", key=f"copy_{index}"):
                st.success("URL copied to clipboard!")
        with col3:
            if st.button("🔗 Open Post", key=f"open_{index}"):
                st.markdown(f"[Open in LinkedIn]({post['url']})")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔗 LinkedIn Post Automation Tool</h1>
        <p>Dynamic web scraping with Python + Selenium</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Scraper settings
        st.subheader("🤖 Scraper Settings")
        headless_mode = st.checkbox("Headless Mode", value=True, help="Run browser in background")
        max_posts = st.slider("Max Posts to Scrape", min_value=5, max_value=50, value=10)
        
        # Login settings
        st.subheader("🔐 LinkedIn Login (Optional)")
        use_login = st.checkbox("Use LinkedIn Login", help="Login for better access (requires valid credentials)")
        
        email = ""
        password = ""
        if use_login:
            email = st.text_input("LinkedIn Email:", type="default")
            password = st.text_input("LinkedIn Password:", type="password")
            st.warning("⚠️ Your credentials are only used for this session and not stored.")
        
        # Initialize scraper button
        if st.button("🚀 Initialize Scraper"):
            if initialize_scraper(headless_mode, use_login, email, password):
                st.success("✅ Scraper initialized successfully!")
            else:
                st.error("❌ Failed to initialize scraper")
        
        # Process visualization
        st.subheader("🔄 Automation Process")
        st.markdown("""
        <div class="process-step">
            <strong>1. Initialize WebDriver</strong><br>
            Setup Chrome with anti-detection
        </div>
        <div class="process-step">
            <strong>2. Navigate to LinkedIn</strong><br>
            Access LinkedIn search page
        </div>
        <div class="process-step">
            <strong>3. Perform Search</strong><br>
            Search for keyword-based posts
        </div>
        <div class="process-step">
            <strong>4. Extract Data</strong><br>
            Scrape post details and metadata
        </div>
        <div class="process-step">
            <strong>5. Process Results</strong><br>
            Clean and structure the data
        </div>
        """, unsafe_allow_html=True)
        
        # Session statistics
        st.subheader("📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{st.session_state.total_searches}</h3>
                <p>Total Searches</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(st.session_state.scraped_posts)}</h3>
                <p>Posts Scraped</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Search LinkedIn Posts")
        
        # Search form
        with st.form("search_form"):
            keyword = st.text_input("Enter keyword to search:", placeholder="e.g., AI, Marketing, Leadership")
            
            col_search, col_clear = st.columns([3, 1])
            with col_search:
                search_button = st.form_submit_button("🚀 Start Scraping", use_container_width=True)
            with col_clear:
                if st.form_submit_button("🗑️ Clear Results"):
                    st.session_state.scraped_posts = []
                    st.rerun()
        
        # Perform search
        if search_button and keyword:
            if not st.session_state.scraper:
                st.error("❌ Please initialize the scraper first using the sidebar.")
            else:
                # Add to search history
                if keyword not in st.session_state.search_history:
                    st.session_state.search_history.append(keyword)
                    if len(st.session_state.search_history) > 10:
                        st.session_state.search_history.pop(0)
                
                # Perform scraping
                posts = scrape_linkedin_posts(keyword, max_posts, use_login)
                
                if posts:
                    st.session_state.scraped_posts = posts
                    st.session_state.total_searches += 1
                    st.success(f"✅ Successfully scraped {len(posts)} posts for '{keyword}'!")
                else:
                    st.error("❌ No posts found or scraping failed.")
        
        # Display results
        if st.session_state.scraped_posts:
            st.header(f"📄 Scraped Posts ({len(st.session_state.scraped_posts)})")
            
            # Export options
            col_json, col_csv = st.columns(2)
            with col_json:
                if st.button("📥 Export as JSON"):
                    json_data = json.dumps(st.session_state.scraped_posts, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"linkedin_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col_csv:
                if st.button("📊 Export as CSV"):
                    df = pd.DataFrame(st.session_state.scraped_posts)
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"linkedin_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            # Display posts
            for i, post in enumerate(st.session_state.scraped_posts):
                display_post_card(post, i)
                st.divider()
    
    with col2:
        st.header("📈 Analytics")
        
        if st.session_state.scraped_posts:
            # Engagement analytics
            df = pd.DataFrame(st.session_state.scraped_posts)
            
            # Top posts by engagement
            st.subheader("🔥 Top Posts by Likes")
            top_posts = df.nlargest(5, 'likes')[['author', 'likes', 'comments', 'shares']]
            st.dataframe(top_posts, use_container_width=True)
            
            # Engagement distribution
            st.subheader("📊 Engagement Distribution")
            fig = px.scatter(df, x='likes', y='comments', size='shares', 
                           hover_data=['author'], title="Likes vs Comments")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Date distribution
            if 'date' in df.columns:
                st.subheader("📅 Posts by Date")
                date_counts = df['date'].value_counts().head(10)
                fig_bar = px.bar(x=date_counts.index, y=date_counts.values, 
                               title="Posts Distribution by Date")
                fig_bar.update_layout(height=300)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Search history
        st.subheader("🕒 Recent Searches")
        if st.session_state.search_history:
            for i, search_term in enumerate(reversed(st.session_state.search_history[-5:])):
                if st.button(f"🔍 {search_term}", key=f"history_{i}"):
                    st.text_input("Keyword", value=search_term, key="history_input")
        else:
            st.info("No search history yet")
        
        # Code preview
        st.subheader("💻 Python Code Preview")
        with st.expander("View Selenium Code"):
            st.code("""
# LinkedIn Scraper Implementation
from selenium import webdriver
from selenium.webdriver.common.by import By

class LinkedInScraper:
    def __init__(self, headless=True):
        self.setup_driver()
    
    def search_posts(self, keyword, max_posts=10):
        search_url = f"https://www.linkedin.com/search/results/content/?keywords={keyword}"
        self.driver.get(search_url)
        
        posts = []
        post_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-chameleon-result-urn]")
        
        for post_element in post_elements:
            post_data = self.extract_post_data(post_element)
            posts.append(post_data)
        
        return posts
            """, language="python")

if __name__ == "__main__":
    main()
    
    # Cleanup on app close
    if st.session_state.scraper:
        try:
            st.session_state.scraper.close()
        except:
            pass