import { useState, useEffect } from 'react'
import { createClient } from '@blinkdotnew/sdk'
import { Search, Moon, Sun, Copy, Download, ExternalLink, Calendar, Clock, User, Code, Play, Loader2 } from 'lucide-react'
import { Button } from './components/ui/button'
import { Input } from './components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Badge } from './components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { Progress } from './components/ui/progress'
import { toast } from 'sonner'

// Initialize Blink client
const blink = createClient({
  projectId: 'linkedin-keyword-post-automation-tool-0vnpl8ec',
  authRequired: true
})

interface LinkedInPost {
  id: string
  title: string
  url: string
  date: string
  time: string
  description: string
  author: string
  engagement: {
    likes: number
    comments: number
    shares: number
  }
}

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [keyword, setKeyword] = useState('')
  const [posts, setPosts] = useState<LinkedInPost[]>([])
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [searchHistory, setSearchHistory] = useState<string[]>([])
  const [user, setUser] = useState(null)

  // Auth state management
  useEffect(() => {
    const unsubscribe = blink.auth.onAuthStateChanged((state) => {
      setUser(state.user)
    })
    return unsubscribe
  }, [])

  // Dark mode toggle
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  // Mock data generator for LinkedIn posts
  const generateMockPosts = (searchKeyword: string): LinkedInPost[] => {
    const mockPosts = [
      {
        id: '1',
        title: `How ${searchKeyword} is transforming the industry`,
        url: 'https://linkedin.com/posts/example-1',
        date: '2024-01-20',
        time: '14:30',
        description: `Exploring the latest trends in ${searchKeyword} and how it's reshaping business strategies. Key insights from industry leaders and practical applications.`,
        author: 'Sarah Johnson',
        engagement: { likes: 245, comments: 32, shares: 18 }
      },
      {
        id: '2',
        title: `5 Essential ${searchKeyword} Skills for 2024`,
        url: 'https://linkedin.com/posts/example-2',
        date: '2024-01-19',
        time: '09:15',
        description: `A comprehensive guide to mastering ${searchKeyword}. From fundamentals to advanced techniques, here's what you need to know.`,
        author: 'Michael Chen',
        engagement: { likes: 189, comments: 24, shares: 12 }
      },
      {
        id: '3',
        title: `The Future of ${searchKeyword}: Predictions and Insights`,
        url: 'https://linkedin.com/posts/example-3',
        date: '2024-01-18',
        time: '16:45',
        description: `Industry experts share their predictions about ${searchKeyword} trends. What to expect in the coming years and how to prepare.`,
        author: 'Emily Rodriguez',
        engagement: { likes: 312, comments: 45, shares: 28 }
      },
      {
        id: '4',
        title: `Case Study: Successful ${searchKeyword} Implementation`,
        url: 'https://linkedin.com/posts/example-4',
        date: '2024-01-17',
        time: '11:20',
        description: `Real-world example of ${searchKeyword} implementation that resulted in 40% efficiency improvement. Lessons learned and best practices.`,
        author: 'David Kim',
        engagement: { likes: 156, comments: 19, shares: 15 }
      },
      {
        id: '5',
        title: `Common ${searchKeyword} Mistakes to Avoid`,
        url: 'https://linkedin.com/posts/example-5',
        date: '2024-01-16',
        time: '13:10',
        description: `Learn from others' mistakes. Top 10 pitfalls in ${searchKeyword} and how to avoid them. Save time and resources with these insights.`,
        author: 'Lisa Thompson',
        engagement: { likes: 203, comments: 31, shares: 22 }
      }
    ]
    return mockPosts
  }

  const handleSearch = async () => {
    if (!keyword.trim()) {
      toast.error('Please enter a keyword to search')
      return
    }

    setLoading(true)
    setProgress(0)
    setPosts([])

    // Simulate search progress
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 200)

    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const mockPosts = generateMockPosts(keyword)
      setPosts(mockPosts)
      
      // Update search history
      if (!searchHistory.includes(keyword)) {
        setSearchHistory(prev => [keyword, ...prev.slice(0, 4)])
      }
      
      setProgress(100)
      toast.success(`Found ${mockPosts.length} posts for "${keyword}"`)
    } catch (error) {
      toast.error('Failed to fetch posts. Please try again.')
    } finally {
      setLoading(false)
      setTimeout(() => setProgress(0), 1000)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }

  const exportResults = () => {
    const dataStr = JSON.stringify(posts, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    const exportFileDefaultName = `linkedin-posts-${keyword}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
    
    toast.success('Results exported successfully!')
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold text-primary">LinkedIn Post Automation</CardTitle>
            <CardDescription>Please sign in to continue</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Button onClick={() => blink.auth.login()} className="w-full">
              Sign In
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Search className="w-4 h-4 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">LinkedIn Post Automation</h1>
                <p className="text-sm text-muted-foreground">Keyword-based post discovery tool</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setDarkMode(!darkMode)}
              >
                {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </Button>
              <Button variant="ghost" onClick={() => blink.auth.logout()}>
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Search Section */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Search className="w-5 h-5 text-primary" />
                  <span>Search LinkedIn Posts</span>
                </CardTitle>
                <CardDescription>
                  Enter a keyword to find relevant LinkedIn posts with metadata
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex space-x-2">
                  <Input
                    placeholder="Enter keyword (e.g., AI, Marketing, Leadership)"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    className="flex-1"
                  />
                  <Button onClick={handleSearch} disabled={loading}>
                    {loading ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Search className="w-4 h-4" />
                    )}
                    {loading ? 'Searching...' : 'Search'}
                  </Button>
                </div>
                
                {loading && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm text-muted-foreground">
                      <span>Fetching posts...</span>
                      <span>{progress}%</span>
                    </div>
                    <Progress value={progress} className="w-full" />
                  </div>
                )}

                {searchHistory.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Recent searches:</p>
                    <div className="flex flex-wrap gap-2">
                      {searchHistory.map((term, index) => (
                        <Badge
                          key={index}
                          variant="secondary"
                          className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
                          onClick={() => setKeyword(term)}
                        >
                          {term}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Results Section */}
            {posts.length > 0 && (
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>Search Results</CardTitle>
                    <CardDescription>
                      Found {posts.length} posts for "{keyword}"
                    </CardDescription>
                  </div>
                  <Button onClick={exportResults} variant="outline" size="sm">
                    <Download className="w-4 h-4 mr-2" />
                    Export JSON
                  </Button>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {posts.map((post) => (
                      <Card key={post.id} className="border-l-4 border-l-primary">
                        <CardContent className="pt-6">
                          <div className="space-y-3">
                            <div className="flex items-start justify-between">
                              <h3 className="font-semibold text-lg leading-tight">
                                {post.title}
                              </h3>
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => copyToClipboard(post.url)}
                                className="shrink-0"
                              >
                                <Copy className="w-4 h-4" />
                              </Button>
                            </div>
                            
                            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                              <div className="flex items-center space-x-1">
                                <User className="w-4 h-4" />
                                <span>{post.author}</span>
                              </div>
                              <div className="flex items-center space-x-1">
                                <Calendar className="w-4 h-4" />
                                <span>{post.date}</span>
                              </div>
                              <div className="flex items-center space-x-1">
                                <Clock className="w-4 h-4" />
                                <span>{post.time}</span>
                              </div>
                            </div>
                            
                            <p className="text-muted-foreground leading-relaxed">
                              {post.description}
                            </p>
                            
                            <div className="flex items-center justify-between pt-2">
                              <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                                <span>👍 {post.engagement.likes}</span>
                                <span>💬 {post.engagement.comments}</span>
                                <span>🔄 {post.engagement.shares}</span>
                              </div>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => window.open(post.url, '_blank')}
                              >
                                <ExternalLink className="w-4 h-4 mr-2" />
                                View Post
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Process Visualization */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Code className="w-5 h-5 text-primary" />
                  <span>Automation Process</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="workflow" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="workflow">Workflow</TabsTrigger>
                    <TabsTrigger value="code">Code</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="workflow" className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex items-center space-x-3 p-3 bg-muted/50 rounded-lg">
                        <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center text-xs text-primary-foreground font-bold">1</div>
                        <span className="text-sm">Initialize Selenium WebDriver</span>
                      </div>
                      <div className="flex items-center space-x-3 p-3 bg-muted/50 rounded-lg">
                        <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center text-xs text-primary-foreground font-bold">2</div>
                        <span className="text-sm">Navigate to LinkedIn search</span>
                      </div>
                      <div className="flex items-center space-x-3 p-3 bg-muted/50 rounded-lg">
                        <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center text-xs text-primary-foreground font-bold">3</div>
                        <span className="text-sm">Input search keyword</span>
                      </div>
                      <div className="flex items-center space-x-3 p-3 bg-muted/50 rounded-lg">
                        <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center text-xs text-primary-foreground font-bold">4</div>
                        <span className="text-sm">Extract post metadata</span>
                      </div>
                      <div className="flex items-center space-x-3 p-3 bg-muted/50 rounded-lg">
                        <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center text-xs text-primary-foreground font-bold">5</div>
                        <span className="text-sm">Format and display results</span>
                      </div>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="code" className="space-y-4">
                    <div className="bg-muted p-4 rounded-lg text-sm font-mono">
                      <div className="text-green-600 dark:text-green-400"># Python + Selenium</div>
                      <div className="mt-2">
                        <div className="text-blue-600 dark:text-blue-400">from</div> selenium <div className="text-blue-600 dark:text-blue-400">import</div> webdriver
                      </div>
                      <div>
                        <div className="text-blue-600 dark:text-blue-400">from</div> selenium.webdriver.common.by <div className="text-blue-600 dark:text-blue-400">import</div> By
                      </div>
                      <div className="mt-2">
                        driver = webdriver.Chrome()
                      </div>
                      <div>
                        driver.get(<div className="text-green-600 dark:text-green-400">"linkedin.com/search"</div>)
                      </div>
                      <div className="mt-2">
                        <div className="text-green-600 dark:text-green-400"># Extract post data</div>
                      </div>
                      <div>
                        posts = driver.find_elements(By.CLASS_NAME, <div className="text-green-600 dark:text-green-400">"post"</div>)
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>

            {/* Statistics */}
            <Card>
              <CardHeader>
                <CardTitle>Session Statistics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Searches performed:</span>
                  <span className="font-semibold">{searchHistory.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Posts found:</span>
                  <span className="font-semibold">{posts.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Current keyword:</span>
                  <span className="font-semibold">{keyword || 'None'}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App