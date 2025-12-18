// API Configuration
const API_BASE = localStorage.getItem('API_BASE') || 'http://localhost:8000/api';

// State Management
let state = {
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    currentView: localStorage.getItem('currentView') || 'posts',
    currentPostId: localStorage.getItem('currentPostId') || null,
    currentChatId: localStorage.getItem('currentChatId') || null,
    chatSocket: null
};

// Save state to localStorage
function saveState() {
    localStorage.setItem('currentView', state.currentView);
    localStorage.setItem('currentPostId', state.currentPostId || '');
    localStorage.setItem('currentChatId', state.currentChatId || '');
}

// DOM Elements - Initialize after DOM loads
let elements = {};

// Initialize app
document.addEventListener('DOMContentLoaded', init);

function init() {
    // Cache DOM elements
    elements = {
        authSection: document.getElementById('auth-section'),
        registerSection: document.getElementById('register-section'),
        mainSection: document.getElementById('main-section'),
        postDetailSection: document.getElementById('post-detail'),
        postsSection: document.getElementById('posts-section'),
        chatsSection: document.getElementById('chats-section'),
        postsList: document.getElementById('posts-list'),
        commentsList: document.getElementById('comments-list'),
        chatsList: document.getElementById('chats-list'),
        messagesList: document.getElementById('messages-list'),
        loginForm: document.getElementById('login-form'),
        registerForm: document.getElementById('register-form'),
        postForm: document.getElementById('post-form'),
        commentForm: document.getElementById('comment-form'),
        chatForm: document.getElementById('chat-form'),
        messageForm: document.getElementById('message-form'),
        showPostsBtn: document.getElementById('show-posts-btn'),
        showChatsBtn: document.getElementById('show-chats-btn')
    };

    setupEventListeners();

    // Check if user is logged in
    if (state.accessToken) {
        // Restore previous view on refresh
        restoreView();
    } else {
        showAuthView();
    }
}

function restoreView() {
    console.log('Restoring view:', state.currentView);

    if (state.currentView === 'chats') {
        hideAll();
        elements.mainSection.classList.remove('hidden');
        showChatsView();

        // If there was a chat open, restore it
        if (state.currentChatId) {
            showMessagesView(state.currentChatId);
        }
    } else if (state.currentView === 'post-detail' && state.currentPostId) {
        showPostDetailView(state.currentPostId);
    } else {
        // Default to posts view
        showMainView();
    }
}

function setupEventListeners() {
    // Auth forms
    elements.loginForm.addEventListener('submit', handleLogin);
    elements.registerForm.addEventListener('submit', handleRegister);

    // Navigation
    document.getElementById('show-register').addEventListener('click', (e) => {
        e.preventDefault();
        showRegisterView();
    });
    document.getElementById('show-login').addEventListener('click', (e) => {
        e.preventDefault();
        showAuthView();
    });
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    document.getElementById('back-to-posts').addEventListener('click', () => showMainView());
    document.getElementById('back-to-chats').addEventListener('click', () => showChatsView());
    elements.showPostsBtn.addEventListener('click', () => showPostsView());
    elements.showChatsBtn.addEventListener('click', () => showChatsView());

    // Post and comment forms
    elements.postForm.addEventListener('submit', handleCreatePost);
    elements.commentForm.addEventListener('submit', handleCreateComment);

    // Chat and message forms
    elements.chatForm.addEventListener('submit', handleCreateChat);
    elements.messageForm.addEventListener('submit', handleSendMessage);

    // Event delegation
    elements.postsList.addEventListener('click', handlePostClick);
    elements.chatsList.addEventListener('click', handleChatClick);
}

// ============================================
// VIEW MANAGEMENT
// ============================================

function showAuthView() {
    hideAll();
    elements.authSection.classList.remove('hidden');
}

function showRegisterView() {
    hideAll();
    elements.registerSection.classList.remove('hidden');
}

function showMainView() {
    hideAll();
    elements.mainSection.classList.remove('hidden');
    showPostsView();
}

function showPostsView() {
    state.currentView = 'posts';
    state.currentPostId = null;
    state.currentChatId = null;
    saveState();

    elements.postsSection.classList.remove('hidden');
    elements.chatsSection.classList.add('hidden');
    elements.showPostsBtn.classList.add('active');
    elements.showChatsBtn.classList.remove('active');
    loadPosts();
}

function showChatsView() {
    state.currentView = 'chats';
    state.currentPostId = null;
    saveState();

    elements.postsSection.classList.add('hidden');
    elements.chatsSection.classList.remove('hidden');
    elements.showPostsBtn.classList.remove('active');
    elements.showChatsBtn.classList.add('active');
    document.getElementById('chat-section').classList.remove('hidden');
    document.getElementById('messages-section').classList.add('hidden');
    
    loadChats();
    
    // Останавливаем polling
    stopMessagePolling();
    
    // Закрываем WebSocket если открыт
    if (state.chatSocket) {
        console.log('🔌 Closing WebSocket connection');
        state.chatSocket.close();
        state.chatSocket = null;
    }
}

function showPostDetailView(postId) {
    state.currentView = 'post-detail';
    state.currentPostId = postId;
    saveState();

    hideAll();
    elements.postDetailSection.classList.remove('hidden');
    viewPost(postId);
}

function showMessagesView(chatId) {
    state.currentView = 'chats';
    state.currentChatId = chatId;
    saveState();

    document.getElementById('chat-section').classList.add('hidden');
    document.getElementById('messages-section').classList.remove('hidden');
    viewChat(chatId);
}

function hideAll() {
    elements.authSection.classList.add('hidden');
    elements.registerSection.classList.add('hidden');
    elements.mainSection.classList.add('hidden');
    elements.postDetailSection.classList.add('hidden');
}

// ============================================
// AUTHENTICATION
// ============================================

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_BASE}/users/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            state.accessToken = data.tokens.access;
            state.refreshToken = data.tokens.refresh;
            localStorage.setItem('accessToken', state.accessToken);
            localStorage.setItem('refreshToken', state.refreshToken);
            showMainView();
        } else {
            const error = await response.json();
            alert('Login failed: ' + (error.detail || 'Invalid credentials'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login error: ' + error.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const password_confirm = document.getElementById('register-password-confirm').value;

    if (password !== password_confirm) {
        alert('Passwords do not match');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/users/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password, password_confirm })
        });

        if (response.ok) {
            alert('Registration successful! Please login.');
            showAuthView();
        } else {
            const error = await response.json();
            alert('Registration failed: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration error: ' + error.message);
    }
}

async function handleLogout() {
    try {
        await fetch(`${API_BASE}/users/auth/logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.accessToken}`
            },
            body: JSON.stringify({ refresh: state.refreshToken })
        });
    } catch (error) {
        console.error('Logout error:', error);
    }

    // Clear all state
    state.accessToken = null;
    state.refreshToken = null;
    state.currentView = 'posts';
    state.currentPostId = null;
    state.currentChatId = null;

    // Clear localStorage
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('currentView');
    localStorage.removeItem('currentPostId');
    localStorage.removeItem('currentChatId');

    showAuthView();
}

async function refreshAccessToken() {
    try {
        const response = await fetch(`${API_BASE}/users/auth/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: state.refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            state.accessToken = data.access;
            localStorage.setItem('accessToken', state.accessToken);
            return true;
        } else {
            handleLogout();
            return false;
        }
    } catch (error) {
        console.error('Refresh token error:', error);
        handleLogout();
        return false;
    }
}

// ============================================
// POSTS
// ============================================

async function loadPosts(page = 1) {
    console.log('Loading posts...');
    try {
        const response = await fetch(`${API_BASE}/posts/?page=${page}`, {
            headers: { 'Authorization': `Bearer ${state.accessToken}` }
        });

        console.log('Posts response status:', response.status);

        if (response.ok) {
            const data = await response.json();
            console.log('Posts data received:', data);
            // Handle both paginated and non-paginated responses
            const posts = data.results || data || [];
            console.log('Displaying', posts.length, 'posts');
            displayPosts(posts);
        } else if (response.status === 401) {
            console.log('Token expired, refreshing...');
            if (await refreshAccessToken()) {
                return loadPosts(page);
            }
        } else {
            const errorText = await response.text();
            console.error('Failed to load posts, status:', response.status, 'Error:', errorText);
            displayPosts([]);
        }
    } catch (error) {
        console.error('Load posts error:', error);
        displayPosts([]);
    }
}

function displayPosts(posts) {
    elements.postsList.innerHTML = '';

    if (!Array.isArray(posts) || posts.length === 0) {
        elements.postsList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">No posts yet. Create the first one!</p>';
        return;
    }

    posts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'post';
        postElement.innerHTML = `
            <h4>${escapeHtml(post.title)}</h4>
            <p>${escapeHtml(post.content)}</p>
            <div style="color: #6c757d; font-size: 14px; margin-bottom: 12px;">
                By: <strong>${escapeHtml(post.author_username)}</strong> |
                Likes: <strong>${post.liked_count || 0}</strong> |
                Comments: <strong>${post.comment_count || 0}</strong>
            </div>
            <button class="view-btn" data-post-id="${post.id}">View Details</button>
            <button class="like-btn" data-post-id="${post.id}" data-is-liked="${post.is_liked}">
                ${post.is_liked ? '❤️ Unlike' : '🤍 Like'}
            </button>
        `;
        elements.postsList.appendChild(postElement);
    });
}

async function handleCreatePost(e) {
    e.preventDefault();
    const title = document.getElementById('post-title').value;
    const content = document.getElementById('post-content-input').value;

    if (!title.trim() || !content.trim()) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/posts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.accessToken}`
            },
            body: JSON.stringify({ title, content })
        });

        if (response.ok) {
            document.getElementById('post-title').value = '';
            document.getElementById('post-content-input').value = '';
            loadPosts(); // Reload to show new post
            alert('Post created successfully!');
        } else {
            const error = await response.json();
            alert('Failed to create post: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Create post error:', error);
        alert('Create post error: ' + error.message);
    }
}

async function viewPost(postId) {
    try {
        const response = await fetch(`${API_BASE}/posts/${postId}/`, {
            headers: { 'Authorization': `Bearer ${state.accessToken}` }
        });

        if (response.ok) {
            const post = await response.json();
            displayPostDetail(post);
            loadComments(postId);
        }
    } catch (error) {
        console.error('View post error:', error);
    }
}

function displayPostDetail(post) {
    const postContent = document.getElementById('post-detail-content');
    postContent.innerHTML = `
        <div style="border: 1px solid #e9ecef; padding: 24px; border-radius: 12px; background: white;">
            <h3 style="margin-top: 0;">${escapeHtml(post.title)}</h3>
            <p style="line-height: 1.8; color: #333;">${escapeHtml(post.content)}</p>
            <div style="color: #6c757d; font-size: 14px; padding-top: 16px; border-top: 1px solid #e9ecef;">
                By: <strong>${escapeHtml(post.author_username)}</strong> |
                Created: ${new Date(post.created_at).toLocaleString()} |
                Likes: <strong>${post.liked_count || 0}</strong>
            </div>
        </div>
    `;
}

async function likePost(postId) {
    try {
        const response = await fetch(`${API_BASE}/posts/${postId}/like/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${state.accessToken}` }
        });

        if (response.ok) {
            loadPosts(); // Reload to update like count
        }
    } catch (error) {
        console.error('Like post error:', error);
    }
}

function handlePostClick(e) {
    const target = e.target;
    if (target.classList.contains('view-btn')) {
        const postId = target.getAttribute('data-post-id');
        showPostDetailView(postId);
    } else if (target.classList.contains('like-btn')) {
        const postId = target.getAttribute('data-post-id');
        likePost(postId);
    }
}

// ============================================
// COMMENTS
// ============================================

async function loadComments(postId) {
    try {
        const response = await fetch(`${API_BASE}/posts/${postId}/comments/`, {
            headers: { 'Authorization': `Bearer ${state.accessToken}` }
        });

        if (response.ok) {
            const comments = await response.json();
            displayComments(comments);
        }
    } catch (error) {
        console.error('Load comments error:', error);
    }
}

function displayComments(comments) {
    elements.commentsList.innerHTML = '';

    if (!Array.isArray(comments) || comments.length === 0) {
        elements.commentsList.innerHTML = '<p style="text-align: center; color: #6c757d;">No comments yet. Be the first to comment!</p>';
        return;
    }

    comments.forEach(comment => {
        const commentElement = document.createElement('div');
        commentElement.className = 'comment';
        commentElement.innerHTML = `
            <p><strong>${escapeHtml(comment.author_username)}:</strong> ${escapeHtml(comment.content)}</p>
            <small>${new Date(comment.created_at).toLocaleString()}</small>
        `;
        elements.commentsList.appendChild(commentElement);
    });
}

async function handleCreateComment(e) {
    e.preventDefault();
    const content = document.getElementById('comment-content').value;

    if (!content.trim()) {
        alert('Please enter a comment');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/posts/${state.currentPostId}/comment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.accessToken}`
            },
            body: JSON.stringify({ content })
        });

        if (response.ok) {
            document.getElementById('comment-content').value = '';
            loadComments(state.currentPostId);
        } else {
            alert('Failed to create comment');
        }
    } catch (error) {
        console.error('Create comment error:', error);
        alert('Create comment error: ' + error.message);
    }
}

// ============================================
// CHATS
// ============================================

async function loadChats() {
    try {
        const response = await fetch(`${API_BASE}/chats/`, {
            headers: { 'Authorization': `Bearer ${state.accessToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            const chats = Array.isArray(data) ? data : (data.results || []);
            displayChats(chats);
        } else if (response.status === 401) {
            if (await refreshAccessToken()) {
                loadChats();
            }
        } else {
            console.error('Failed to load chats');
            displayChats([]);
        }
    } catch (error) {
        console.error('Load chats error:', error);
        displayChats([]);
    }
}

function displayChats(chats) {
    elements.chatsList.innerHTML = '';

    if (!Array.isArray(chats) || chats.length === 0) {
        elements.chatsList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">No chats yet. Start a conversation!</p>';
        return;
    }

    chats.forEach(chat => {
        const chatElement = document.createElement('div');
        chatElement.className = 'chat';
        const members = chat.members_usernames || [];
        chatElement.innerHTML = `
            <p><strong>${members.map(m => escapeHtml(m)).join(', ')}</strong></p>
            <button class="view-chat-btn" data-chat-id="${chat.id}">Open Chat</button>
        `;
        elements.chatsList.appendChild(chatElement);
    });
}

async function handleCreateChat(e) {
    e.preventDefault();
    const memberUsername = document.getElementById('chat-member-username').value;

    if (!memberUsername.trim()) {
        alert('Please enter a username');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/chats/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.accessToken}`
            },
            body: JSON.stringify({ member_username: memberUsername })
        });

        if (response.ok) {
            document.getElementById('chat-member-username').value = '';
            loadChats();
            alert('Chat created successfully!');
        } else if (response.status === 404) {
            alert('User not found');
        } else {
            const error = await response.json();
            alert('Failed to create chat: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Create chat error:', error);
        alert('Create chat error: ' + error.message);
    }
}

async function viewChat(chatId) {
    try {
        const response = await fetch(`${API_BASE}/chats/${chatId}/`, {
            headers: { 'Authorization': `Bearer ${state.accessToken}` }
        });

        if (response.ok) {
            const chat = await response.json();
            document.getElementById('chat-title').textContent = `Chat with ${chat.members_usernames.join(', ')}`;
            
            // Сначала загружаем историю сообщений
            await loadMessages(chatId);
            
            // Потом подключаем WebSocket
            startChatWebSocket(chatId);
        }
    } catch (error) {
        console.error('View chat error:', error);
    }
}

function handleChatClick(e) {
    const target = e.target;
    if (target.classList.contains('view-chat-btn')) {
        const chatId = target.getAttribute('data-chat-id');
        showMessagesView(chatId);
    }
}

// ============================================
// MESSAGES
// ============================================

async function loadMessages(chatId) {
    try {
        let response = await fetch(`${API_BASE}/chats/${chatId}/messages/`, {
            headers: { 'Authorization': `Bearer ${state.accessToken}` }
        });

        // Если 401, обновляем токен и пробуем снова
        if (response.status === 401) {
            console.log('Token expired, refreshing...');
            if (await refreshAccessToken()) {
                response = await fetch(`${API_BASE}/chats/${chatId}/messages/`, {
                    headers: { 'Authorization': `Bearer ${state.accessToken}` }
                });
            } else {
                return;
            }
        }

        if (response.ok) {
            const messages = await response.json();
            displayMessages(messages);
        }
    } catch (error) {
        console.error('Load messages error:', error);
    }
    // НЕ ЗАПУСКАЕМ POLLING ЗДЕСЬ!
}

function displayMessages(messages) {
    elements.messagesList.innerHTML = '';

    if (!Array.isArray(messages) || messages.length === 0) {
        elements.messagesList.innerHTML = '<p style="text-align: center; color: #6c757d;">No messages yet. Start the conversation!</p>';
        return;
    }

    messages.forEach(message => {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        const timestamp = message.timestamp || message.created_at;
        messageElement.innerHTML = `
            <p><strong>${escapeHtml(message.sender_username)}:</strong> ${escapeHtml(message.content)}</p>
            <small>${new Date(timestamp).toLocaleString()}</small>
        `;
        elements.messagesList.appendChild(messageElement);
    });

    elements.messagesList.scrollTop = elements.messagesList.scrollHeight;
}

async function handleSendMessage(e) {
    e.preventDefault();
    const content = document.getElementById('message-content').value;

    if (!content.trim()) {
        alert('Please enter a message');
        return;
    }

    if (state.chatSocket && state.chatSocket.readyState === WebSocket.OPEN) {
        state.chatSocket.send(JSON.stringify({ content: content }));
        document.getElementById('message-content').value = '';
    } else {
        // Fallback to HTTP
        try {
            const response = await fetch(`${API_BASE}/chats/${state.currentChatId}/messages/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${state.accessToken}`
                },
                body: JSON.stringify({ content })
            });

            if (response.ok) {
                document.getElementById('message-content').value = '';
                loadMessages(state.currentChatId);
            } else {
                alert('Failed to send message');
            }
        } catch (error) {
            console.error('Send message error:', error);
            alert('Send message error: ' + error.message);
        }
    }
}

// ============================================
// WEBSOCKET
// ============================================

function startChatWebSocket(chatId) {
    console.log('🔌 Starting WebSocket connection for chat:', chatId);
    
    // ВАЖНО: Сначала останавливаем polling
    stopMessagePolling();
    
    // Закрываем старый socket если есть
    if (state.chatSocket) {
        state.chatSocket.close();
        state.chatSocket = null;
    }

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//localhost:8000/ws/chat/${chatId}/?token=${state.accessToken}`;
    
    console.log('🔌 Connecting to:', wsUrl);

    try {
        state.chatSocket = new WebSocket(wsUrl);

        state.chatSocket.onopen = function(e) {
            console.log('✅ WebSocket CONNECTED successfully');
        };

        state.chatSocket.onmessage = function(e) {
            console.log('📨 Message received:', e.data);
            const message = JSON.parse(e.data);
            const messageElement = document.createElement('div');
            messageElement.className = 'message';
            messageElement.innerHTML = `
                <p><strong>${escapeHtml(message.sender_username)}:</strong> ${escapeHtml(message.content)}</p>
                <small>${new Date(message.timestamp).toLocaleString()}</small>
            `;
            elements.messagesList.appendChild(messageElement);
            elements.messagesList.scrollTop = elements.messagesList.scrollHeight;
        };

        state.chatSocket.onclose = function(e) {
            console.error('❌ WebSocket CLOSED. Code:', e.code, 'Reason:', e.reason);
            console.log('⚠️ Falling back to polling...');
            state.chatSocket = null;
            startMessagePolling(chatId);
        };

        state.chatSocket.onerror = function(e) {
            console.error('❌ WebSocket ERROR:', e);
        };
    } catch (error) {
        console.error('❌ Failed to create WebSocket:', error);
        startMessagePolling(chatId);
    }
}
// Polling fallback
let messagePollingInterval;

function startMessagePolling(chatId) {
    clearInterval(messagePollingInterval);
    messagePollingInterval = setInterval(() => {
        loadMessages(chatId);
    }, 5000);
}

function stopMessagePolling() {
    clearInterval(messagePollingInterval);
}

// ============================================
// UTILITIES
// ============================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
