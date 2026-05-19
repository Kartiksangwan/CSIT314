// ============================================================
// api.js — shared helper for all frontend pages
// All API calls go through here so we only need to change
// the BASE_URL in one place if the server moves.
// ============================================================

const BASE_URL = 'http://127.0.0.1:5000/api';

// ---- low-level fetch helpers ----

async function apiGet(path) {
  const res = await fetch(BASE_URL + path, {
    credentials: 'include'
  });
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(BASE_URL + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body)
  });
  return res.json();
}

async function apiPut(path, body) {
  const res = await fetch(BASE_URL + path, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body)
  });
  return res.json();
}

async function apiDelete(path) {
  const res = await fetch(BASE_URL + path, {
    method: 'DELETE',
    credentials: 'include'
  });
  return res.json();
}

// ---- auth ----

async function login(email, password) {
  return apiPost('/auth/login', { email, password });
}

async function register(email, password, role) {
  return apiPost('/auth/register', { email, password, role });
}

async function logout() {
  return apiPost('/auth/logout', {});
}

async function getMe() {
  return apiGet('/auth/me');
}

// ---- candidate ----

async function getCandidateProfile() {
  return apiGet('/candidates/profile');
}

async function updateCandidateProfile(data) {
  return apiPut('/candidates/profile', data);
}

async function updateSubscription(plan) {
  return apiPut('/candidates/subscription', { plan });
}

// ---- employer ----

async function getEmployerProfile() {
  return apiGet('/employers/profile');
}

async function updateEmployerProfile(data) {
  return apiPut('/employers/profile', data);
}

async function getApplicants() {
  return apiGet('/employers/applicants');
}

// ---- jobs ----

async function getAllJobs() {
  return apiGet('/jobs/');
}

async function getJob(jobId) {
  return apiGet('/jobs/' + jobId);
}

async function createJob(data) {
  return apiPost('/jobs/', data);
}

async function applyToJob(jobId) {
  return apiPost('/jobs/' + jobId + '/apply', {});
}

async function getMyJobs() {
  return apiGet('/jobs/my-jobs');
}

// ---- search ----

async function searchJobs(keyword, location, workMode) {
  let url = '/search/jobs?';
  if (keyword) url += 'keyword=' + encodeURIComponent(keyword) + '&';
  if (location) url += 'location=' + encodeURIComponent(location) + '&';
  if (workMode) url += 'work_mode=' + encodeURIComponent(workMode);
  return apiGet(url);
}

async function searchCandidates(keyword) {
  return apiGet('/search/candidates?keyword=' + encodeURIComponent(keyword));
}

// ---- bookmarks ----

async function getBookmarks() {
  return apiGet('/bookmarks/');
}

async function addBookmark(jobId) {
  return apiPost('/bookmarks/add', { job_id: jobId });
}

async function removeBookmark(jobId) {
  return apiDelete('/bookmarks/remove/' + jobId);
}

// ---- messages ----

async function getMessages() {
  return apiGet('/messages/');
}

async function getThread(partnerUserId) {
  return apiGet('/messages/thread/' + partnerUserId);
}

async function sendMessage(receiverUserId, content) {
  return apiPost('/messages/send', { receiver_user_id: receiverUserId, content });
}

// ---- offers ----

async function getOffers() {
  return apiGet('/offers/');
}

async function getEmployerOffers() {
  return apiGet('/offers/employer');
}

async function sendOffer(data) {
  return apiPost('/offers/send', data);
}

async function respondToOffer(offerId, status) {
  return apiPut('/offers/' + offerId + '/respond', { status });
}

// ---- recommendations ----

async function getTodaysRecommendations() {
  return apiGet('/recommendations/today');
}

async function getTopCandidates(jobId) {
  return apiGet('/recommendations/top-candidates/' + jobId);
}

// ---- session helpers ----

// Save user info to sessionStorage after login
function saveSession(user) {
  sessionStorage.setItem('user', JSON.stringify(user));
}

function getSession() {
  const u = sessionStorage.getItem('user');
  return u ? JSON.parse(u) : null;
}

function clearSession() {
  sessionStorage.removeItem('user');
}

// redirect to login if not logged in
function requireLogin(role) {
  const user = getSession();
  if (!user) {
    if (role === 'employer') {
      window.location.href = '../employers/companylogin.html';
    } else {
      window.location.href = 'loginnC.html';
    }
    return false;
  }
  return true;
}
