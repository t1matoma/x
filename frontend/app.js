// API base can be overridden by setting localStorage.setItem('API_BASE', 'http://host:port/api')
const API_BASE = localStorage.getItem('API_BASE') || 'http://localhost:8000/api';
let accessToken = localStorage.getItem('accessToken');
let refreshToken = localStorage.getItem('refreshToken');

// DOM elements
const authSection = document.getElementById('auth-section');
const registerSection = document.getElementById('register-section');
const mainSection = document.getElementById('main-section');
const postDetailSection = document.getElementById('post-detail');

// Forms
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const postForm = document.getElementById('post-form');
const commentForm = document.getElementById('comment-form');

// Buttons
const showRegister = document.getElementById('show-register');
const showLogin = document.getElementById('show-login');
const logoutBtn = document.getElementById('logout-btn');
const backToPosts = document.getElementById('back-to-posts');

// Lists
const postsList = document.getElementById('posts-list');
const commentsList = document.getElementById('comments-list');

// Initialize app
document.addEventListener('DOMContentLoaded', init);

function init() {
    if (accessToken) {
        showMain();
        loadPosts();
    } else {
        showAuth();
    }

    // Event listeners
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    postForm.addEventListener('submit', handleCreatePost);
    commentForm.addEventListener('submit', handleCreateComment);
    showRegister.addEventListener('click', (e) => {
        e.preventDefault();
        showRegisterForm();
    });
    showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        showLoginForm();
    });
    logoutBtn.addEventListener('click', handleLogout);
    backToPosts.addEventListener('click', showMain);

    // Event delegation for post actions
    postsList.addEventListener('click', handlePostAction);
}

function showAuth() {
    authSection.classList.remove('hidden');
    registerSection.classList.add('hidden');
    mainSection.classList.add('hidden');
    postDetailSection.classList.add('hidden');
}

function showRegisterForm() {
    authSection.classList.add('hidden');
    registerSection.classList.remove('hidden');
    mainSection.classList.add('hidden');
    postDetailSection.classList.add('hidden');
}

function showLoginForm() {
    authSection.classList.remove('hidden');
    registerSection.classList.add('hidden');
    mainSection.classList.add('hidden');
    postDetailSection.classList.add('hidden');
}

function showMain() {
    authSection.classList.add('hidden');
    registerSection.classList.add('hidden');
    mainSection.classList.remove('hidden');
    postDetailSection.classList.add('hidden');
}

function showPostDetail() {
    authSection.classList.add('hidden');
    registerSection.classList.add('hidden');
    mainSection.classList.add('hidden');
    postDetailSection.classList.remove('hidden');
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_BASE}/users/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const data = await response.json();
            accessToken = data.tokens.access;
            refreshToken = data.tokens.refresh;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', refreshToken);
            showMain();
            loadPosts();
        } else {
            alert('Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login error');
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
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password, password_confirm }),
        });

        if (response.ok) {
            alert('Registration successful! Please login.');
            showLoginForm();
        } else {
            const error = await response.json();
            alert('Registration failed: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration error');
    }
}

async function handleLogout() {
    try {
        await fetch(`${API_BASE}/users/auth/logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });
    } catch (error) {
        console.error('Logout error:', error);
    }

    accessToken = null;
    refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    showAuth();
}

async function loadPosts() {
    try {
        const response = await fetch(`${API_BASE}/posts/`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            },
        });

        if (response.ok) {
            const posts = await response.json();
            displayPosts(posts);
        } else if (response.status === 401) {
            // Token expired, try refresh
            await refreshAccessToken();
            loadPosts();
        }
    } catch (error) {
        console.error('Load posts error:', error);
    }
}

function displayPosts(posts) {
    postsList.innerHTML = '';
    posts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'post';
        postElement.innerHTML = `
            <h4>${post.title}</h4>
            <p>${post.content}</p>
            <p>By: ${post.author_username} | Likes: ${post.liked_count} | Comments: ${post.comment_count}</p>
            <button class="view-post-btn" data-post-id="${post.id}">View Details</button>
            <button class="like-post-btn" data-post-id="${post.id}">Like</button>
        `;
        postsList.appendChild(postElement);
    });
}

async function handleCreatePost(e) {
    e.preventDefault();
    const title = document.getElementById('post-title').value;
    // Use the renamed textarea id
    const content = document.getElementById('post-content-input').value;

    try {
        const response = await fetch(`${API_BASE}/posts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ title, content }),
        });

        if (response.ok) {
            document.getElementById('post-title').value = '';
            document.getElementById('post-content-input').value = '';
            loadPosts();
        } else {
            alert('Failed to create post');
        }
    } catch (error) {
        console.error('Create post error:', error);
        alert('Create post error');
    }
}

async function viewPost(postId) {
    try {
        const response = await fetch(`${API_BASE}/posts/${postId}/`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            },
        });

        if (response.ok) {
            const post = await response.json();
            displayPostDetail(post);
            loadComments(postId);
            showPostDetail();
        }
    } catch (error) {
        console.error('View post error:', error);
    }
}

function displayPostDetail(post) {
    // Use renamed detail container id
    const postContent = document.getElementById('post-detail-content');
    postContent.innerHTML = `
        <h3>${post.title}</h3>
        <p>${post.content}</p>
        <p>By: ${post.author_username} | Created: ${new Date(post.created_at).toLocaleString()}</p>
    `;
}

async function loadComments(postId) {
    try {
        const response = await fetch(`${API_BASE}/posts/${postId}/comments/`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            },
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
    commentsList.innerHTML = '';
    comments.forEach(comment => {
        const commentElement = document.createElement('div');
        commentElement.className = 'comment';
        commentElement.innerHTML = `
            <p><strong>${comment.author_username}:</strong> ${comment.content}</p>
            <small>${new Date(comment.created_at).toLocaleString()}</small>
        `;
        commentsList.appendChild(commentElement);
    });
}

async function handleCreateComment(e) {
    e.preventDefault();
    const content = document.getElementById('comment-content').value;
    const postId = getCurrentPostId(); // Need to store current post ID

    try {
        const response = await fetch(`${API_BASE}/posts/${postId}/comment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ content }),
        });

        if (response.ok) {
            document.getElementById('comment-content').value = '';
            loadComments(postId);
            loadPosts(); // Refresh posts list to update comment counts
        } else {
            alert('Failed to create comment');
        }
    } catch (error) {
        console.error('Create comment error:', error);
        alert('Create comment error');
    }
}

async function likePost(postId) {
    try {
        const response = await fetch(`${API_BASE}/posts/${postId}/like/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            },
        });

        if (response.ok) {
            loadPosts();
        }
    } catch (error) {
        console.error('Like post error:', error);
    }
}

async function refreshAccessToken() {
    try {
        const response = await fetch(`${API_BASE}/users/auth/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (response.ok) {
            const data = await response.json();
            accessToken = data.access;
            localStorage.setItem('accessToken', accessToken);
        } else {
            // Refresh failed, logout
            handleLogout();
        }
    } catch (error) {
        console.error('Refresh token error:', error);
        handleLogout();
    }
}

function getCurrentPostId() {
    // Extract post ID from URL or store in a variable
    // For simplicity, assume we store it when viewing post
    return window.currentPostId;
}

// Set current post ID when viewing
function setCurrentPostId(postId) {
    window.currentPostId = postId;
}

// Modify viewPost to set current post ID
const originalViewPost = viewPost;
viewPost = function(postId) {
    setCurrentPostId(postId);
    originalViewPost(postId);
};

// Handle post actions (view, like) through event delegation
function handlePostAction(e) {
    const target = e.target;
    if (target.classList.contains('view-post-btn')) {
        const postId = target.getAttribute('data-post-id');
        viewPost(postId);
    } else if (target.classList.contains('like-post-btn')) {
        const postId = target.getAttribute('data-post-id');
        likePost(postId);
    }
}
