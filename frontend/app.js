// App State
let profileData = {};
let videosData = [];
let coursesData = [];
let bundlesData = [];
let podcastsData = [];
let currentCategory = "All";

// DOM Elements
const navName = document.getElementById('nav-name');
const navAvatar = document.getElementById('nav-avatar');
const heroName = document.getElementById('hero-name');
const heroAvatar = document.getElementById('hero-avatar');
const heroTagline = document.getElementById('hero-tagline');
const heroBio = document.getElementById('hero-bio');
const footerName = document.getElementById('footer-name');

const linkInstagram = document.getElementById('link-instagram');
const linkYoutube = document.getElementById('link-youtube');
const contactDisplayEmail = document.getElementById('contact-display-email');

const statSubs = document.getElementById('stat-subs');
const statFollowers = document.getElementById('stat-followers');
const statStudents = document.getElementById('stat-students');
const statProducts = document.getElementById('stat-products');

const videoGrid = document.getElementById('video-grid');
const productsGrid = document.getElementById('products-grid');
const podcastList = document.getElementById('podcast-list');

const videoModal = document.getElementById('video-modal');
const modalIframe = document.getElementById('modal-iframe');
const modalVideoTitle = document.getElementById('modal-video-title');
const modalVideoDesc = document.getElementById('modal-video-desc');

const courseModal = document.getElementById('course-modal');
const modalCourseTitle = document.getElementById('modal-course-title');
const modalCourseDesc = document.getElementById('modal-course-desc');
const modalCourseCurriculum = document.getElementById('modal-course-curriculum');
const modalCoursePrice = document.getElementById('modal-course-price');

const adminModal = document.getElementById('admin-modal');
const toast = document.getElementById('toast');
const globalSearch = document.getElementById('global-search');
const themeSelect = document.getElementById('theme-select');

const API_BASE = '/api';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  fetchProfile();
  fetchVideos();
  fetchCoursesAndBundles();
  fetchPodcasts();
  setupEventListeners();
});

// Toast Helper
function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// Fetch Profile
async function fetchProfile() {
  try {
    const res = await fetch(`${API_BASE}/profile`);
    profileData = await res.json();
    renderProfile();
  } catch (err) {
    console.error('Error loading profile:', err);
  }
}

function renderProfile() {
  if (!profileData || !profileData.name) return;

  navName.textContent = profileData.name;
  heroName.textContent = profileData.name;
  footerName.textContent = profileData.name;

  if (profileData.avatar_url) {
    navAvatar.src = profileData.avatar_url;
    heroAvatar.src = profileData.avatar_url;
    document.getElementById('admin-avatar-url').value = profileData.avatar_url;
  }

  heroTagline.textContent = profileData.tagline || '';
  heroBio.textContent = profileData.bio || '';

  if (profileData.instagram) linkInstagram.href = profileData.instagram;
  if (profileData.youtube) linkYoutube.href = profileData.youtube;
  if (profileData.business_email) {
    contactDisplayEmail.textContent = profileData.business_email;
  }

  statSubs.textContent = profileData.subscribers_count || '125K+';
  statFollowers.textContent = profileData.followers_count || '45K+';
  statStudents.textContent = profileData.students_count || '8.2K+';
  statProducts.textContent = profileData.products_count || '14+';

  document.getElementById('admin-name').value = profileData.name || '';
  document.getElementById('admin-tagline').value = profileData.tagline || '';
  document.getElementById('admin-bio').value = profileData.bio || '';
  document.getElementById('admin-instagram').value = profileData.instagram || '';
  document.getElementById('admin-youtube').value = profileData.youtube || '';
  document.getElementById('admin-email').value = profileData.business_email || '';
}

// Fetch Videos
async function fetchVideos() {
  try {
    const res = await fetch(`${API_BASE}/videos`);
    videosData = await res.json();
    renderVideos();
  } catch (err) {
    console.error('Error loading videos:', err);
  }
}

function renderVideos() {
  videoGrid.innerHTML = '';
  const searchQ = globalSearch.value.toLowerCase().trim();

  const filtered = videosData.filter(v => {
    const matchesCategory = currentCategory === 'All' || v.category === currentCategory;
    const matchesSearch = !searchQ || v.title.toLowerCase().includes(searchQ) || (v.description && v.description.toLowerCase().includes(searchQ));
    return matchesCategory && matchesSearch;
  });

  if (filtered.length === 0) {
    videoGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No videos match your search or filter.</div>`;
    return;
  }

  filtered.forEach(video => {
    const card = document.createElement('div');
    card.className = 'video-card';
    const isGaming = video.category === 'Gaming';
    const categoryBadgeClass = isGaming ? 'badge-pink' : 'badge-violet';

    card.innerHTML = `
      <div class="video-thumb-wrap">
        <img src="${video.thumbnail_url}" alt="${video.title}" class="video-thumb">
        <div class="play-badge">▶</div>
        <span class="video-duration">${video.duration}</span>
      </div>
      <div class="video-info">
        <div class="video-meta">
          <span class="badge ${categoryBadgeClass}">${isGaming ? '🎮 Gaming' : video.category}</span>
          <span>👁️ ${video.views || '1K'} views</span>
        </div>
        <h3 class="video-title">${video.title}</h3>
        <p class="video-desc">${video.description || ''}</p>
        <div style="margin-top: 0.75rem; text-align: right;">
          <button class="delete-vid-btn" style="background: transparent; border: none; color: #ef4444; font-size: 0.75rem; cursor: pointer;">🗑️ Remove Video</button>
        </div>
      </div>
    `;
    card.querySelector('.video-thumb-wrap').addEventListener('click', () => openVideoModal(video));
    card.querySelector('.video-title').addEventListener('click', () => openVideoModal(video));
    card.querySelector('.delete-vid-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      if (confirm(`Remove video "${video.title}" from SQLite database?`)) {
        deleteVideo(video.id);
      }
    });
    videoGrid.appendChild(card);
  });
}

async function deleteVideo(id) {
  try {
    const res = await fetch(`${API_BASE}/videos/${id}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Video removed from database!');
      fetchVideos();
    }
  } catch (err) {
    alert('Error deleting video.');
  }
}

function openVideoModal(video) {
  modalIframe.src = `https://www.youtube.com/embed/${video.youtube_id}?autoplay=1`;
  modalVideoTitle.textContent = video.title;
  modalVideoDesc.textContent = video.description || '';
  videoModal.classList.add('active');
}

// Fetch Courses & Bundles
async function fetchCoursesAndBundles() {
  try {
    const [cRes, bRes] = await Promise.all([
      fetch(`${API_BASE}/courses`),
      fetch(`${API_BASE}/bundles`)
    ]);
    coursesData = await cRes.json();
    bundlesData = await bRes.json();
    renderProducts();
  } catch (err) {
    console.error('Error loading products:', err);
  }
}

function renderProducts() {
  productsGrid.innerHTML = '';
  const searchQ = globalSearch.value.toLowerCase().trim();

  coursesData.forEach(course => {
    if (searchQ && !course.title.toLowerCase().includes(searchQ) && !course.description.toLowerCase().includes(searchQ)) {
      return;
    }
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${course.image_url}" alt="${course.title}" class="product-image">
      <div class="product-body">
        <div class="product-header">
          <span class="badge badge-emerald">${course.badge}</span>
          <span class="product-price">${course.price}</span>
        </div>
        <h3 class="product-title">${course.title}</h3>
        <p class="product-desc">${course.description}</p>
        <div class="product-footer">
          <button class="btn btn-outline view-curriculum-btn" style="flex: 1;">Curriculum</button>
          <button class="btn btn-primary" onclick="alert('Enrolling in ${course.title}!')" style="flex: 1;">Enroll</button>
        </div>
      </div>
    `;
    card.querySelector('.view-curriculum-btn').addEventListener('click', () => openCourseModal(course));
    productsGrid.appendChild(card);
  });

  bundlesData.forEach(bundle => {
    if (searchQ && !bundle.title.toLowerCase().includes(searchQ)) return;
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${bundle.image_url}" alt="${bundle.title}" class="product-image">
      <div class="product-body">
        <div class="product-header">
          <span class="badge badge-cyan">${bundle.badge}</span>
          <span class="product-price">${bundle.price}</span>
        </div>
        <h3 class="product-title">${bundle.title}</h3>
        <p class="product-desc">${bundle.description}</p>
        <div style="font-size: 0.8rem; color: var(--accent-cyan); margin-bottom: 1rem; font-weight: 600;">
          ${bundle.items_included}
        </div>
        <div class="product-footer">
          <button class="btn btn-primary" onclick="alert('Purchasing bundle ${bundle.title}!')" style="width: 100%;">Get Bundle Now</button>
        </div>
      </div>
    `;
    productsGrid.appendChild(card);
  });
}

function openCourseModal(course) {
  modalCourseTitle.textContent = course.title;
  modalCourseDesc.textContent = course.description;
  modalCourseCurriculum.textContent = course.curriculum || 'Curriculum details coming soon.';
  modalCoursePrice.textContent = course.price;
  courseModal.classList.add('active');
}

// Fetch Podcasts
async function fetchPodcasts() {
  try {
    const res = await fetch(`${API_BASE}/podcasts`);
    podcastsData = await res.json();
    renderPodcasts();
  } catch (err) {
    console.error('Error loading podcasts:', err);
  }
}

function renderPodcasts() {
  podcastList.innerHTML = '';
  podcastsData.forEach(p => {
    const card = document.createElement('div');
    card.className = 'podcast-card';
    card.innerHTML = `
      <img src="${p.cover_url}" alt="${p.title}" class="podcast-cover">
      <div class="podcast-details">
        <h4 class="podcast-title">${p.title}</h4>
        <p class="podcast-meta">Duration: ${p.duration}</p>
        <audio controls style="margin-top: 0.5rem; width: 100%; height: 32px;" src="${p.audio_url}"></audio>
      </div>
    `;
    podcastList.appendChild(card);
  });
}

// Setup Event Listeners
function setupEventListeners() {
  themeSelect.addEventListener('change', (e) => {
    document.body.className = '';
    if (e.target.value === 'neon') document.body.classList.add('theme-neon');
    if (e.target.value === 'midnight') document.body.classList.add('theme-midnight');
    showToast(`Switched theme to ${e.target.options[e.target.selectedIndex].text}`);
  });

  globalSearch.addEventListener('input', () => {
    renderVideos();
    renderProducts();
  });

  const filterBtns = document.querySelectorAll('#video-filters .filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.dataset.category;
      renderVideos();
    });
  });

  const copyEmail = () => {
    const email = profileData.business_email || 'alex.rivera.biz@example.com';
    navigator.clipboard.writeText(email);
    showToast(`Copied ${email} to clipboard!`);
  };

  document.getElementById('copy-email-btn').addEventListener('click', copyEmail);
  document.getElementById('copy-email-btn-2').addEventListener('click', copyEmail);

  document.getElementById('close-video-modal').addEventListener('click', () => {
    videoModal.classList.remove('active');
    modalIframe.src = '';
  });

  document.getElementById('close-course-modal').addEventListener('click', () => {
    courseModal.classList.remove('active');
  });

  document.getElementById('open-admin-btn').addEventListener('click', () => {
    adminModal.classList.add('active');
  });

  document.getElementById('close-admin-modal').addEventListener('click', () => {
    adminModal.classList.remove('active');
  });

  // Admin Tab Switcher
  const adminTabs = document.querySelectorAll('.admin-tab-btn');
  adminTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      adminTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.tab;

      document.getElementById('tab-profile').style.display = target === 'tab-profile' ? 'block' : 'none';
      document.getElementById('tab-add-video').style.display = target === 'tab-add-video' ? 'block' : 'none';
      document.getElementById('tab-inquiries').style.display = target === 'tab-inquiries' ? 'block' : 'none';

      if (target === 'tab-inquiries') fetchAdminInquiries();
    });
  });

  // Add Video Form with custom thumbnail URL support
  document.getElementById('add-video-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('add-video-title').value;
    const url = document.getElementById('add-video-url').value;
    const category = document.getElementById('add-video-category').value;
    const thumbnail_url = document.getElementById('add-video-thumb').value;
    const duration = document.getElementById('add-video-duration').value || '12:00';
    const description = document.getElementById('add-video-desc').value;

    try {
      const res = await fetch(`${API_BASE}/videos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          youtube_url: url,
          category,
          thumbnail_url,
          duration,
          description
        })
      });

      const data = await res.json();
      if (res.ok && data.success) {
        showToast('🚀 Video & Thumbnail published to web!');
        document.getElementById('add-video-form').reset();
        adminModal.classList.remove('active');
        fetchVideos();
      } else {
        alert(data.error || 'Failed to add video.');
      }
    } catch (err) {
      alert('Error adding video.');
    }
  });

  // Newsletter Form
  document.getElementById('newsletter-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('newsletter-email').value;
    try {
      const res = await fetch(`${API_BASE}/subscribers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const data = await res.json();
      showToast(data.message || 'Subscribed successfully!');
      document.getElementById('newsletter-email').value = '';
    } catch (err) {
      alert('Error subscribing.');
    }
  });

  // Inquiry Form
  document.getElementById('inquiry-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('form-name').value,
      email: document.getElementById('form-email').value,
      subject: document.getElementById('form-subject').value,
      message: document.getElementById('form-message').value
    };

    try {
      const res = await fetch(`${API_BASE}/inquiries`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok && data.success) {
        showToast('Inquiry sent! Saved to SQLite database.');
        document.getElementById('inquiry-form').reset();
      } else {
        alert(data.error || 'Failed to submit inquiry.');
      }
    } catch (err) {
      alert('Error submitting inquiry.');
    }
  });

  // Admin Profile & Avatar Image Form Submission
  document.getElementById('admin-profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('admin-name').value,
      avatar_url: document.getElementById('admin-avatar-url').value,
      tagline: document.getElementById('admin-tagline').value,
      bio: document.getElementById('admin-bio').value,
      instagram: document.getElementById('admin-instagram').value,
      youtube: document.getElementById('admin-youtube').value,
      business_email: document.getElementById('admin-email').value,
      subscribers_count: profileData.subscribers_count,
      followers_count: profileData.followers_count,
      students_count: profileData.students_count,
      products_count: profileData.products_count
    };

    try {
      const res = await fetch(`${API_BASE}/profile`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        showToast('Profile & Avatar Image updated in SQLite DB!');
        adminModal.classList.remove('active');
        fetchProfile();
      }
    } catch (err) {
      alert('Error updating profile.');
    }
  });
}

// Fetch Admin Inquiries Inbox
async function fetchAdminInquiries() {
  const container = document.getElementById('inquiries-inbox');
  container.innerHTML = '<div style="color: var(--text-muted);">Loading inquiries from database...</div>';
  try {
    const res = await fetch(`${API_BASE}/inquiries`);
    const inquiries = await res.json();
    if (inquiries.length === 0) {
      container.innerHTML = '<div style="color: var(--text-muted);">No inquiries submitted yet.</div>';
      return;
    }
    container.innerHTML = '';
    inquiries.forEach(inq => {
      const item = document.createElement('div');
      item.style.cssText = 'background: rgba(0,0,0,0.4); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);';
      item.innerHTML = `
        <div style="display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 0.25rem;">
          <span>${inq.name} (<a href="mailto:${inq.email}" style="color: var(--accent-cyan);">${inq.email}</a>)</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${inq.created_at || ''}</span>
        </div>
        <div style="font-size: 0.85rem; color: var(--accent-violet); font-weight: 600; margin-bottom: 0.5rem;">Subject: ${inq.subject}</div>
        <p style="font-size: 0.9rem; color: var(--text-muted);">${inq.message}</p>
      `;
      container.appendChild(item);
    });
  } catch (err) {
    container.innerHTML = '<div style="color: red;">Failed to load inquiries.</div>';
  }
}
