const BASE_URL = 'http://localhost/api/v1'

async function parseResponse(response) {
  const text = await response.text()
  try {
    return text ? JSON.parse(text) : {}
  } catch {
    return { message: text || response.statusText }
  }
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options)
  if (!response.ok) {
    const body = await parseResponse(response)
    const message = body?.message || body?.error || response.statusText || 'Request failed'
    throw new Error(message)
  }
  return await parseResponse(response)
}

export function login(username, password) {
  return fetchJson(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
}

export function register(username, password) {
  return fetchJson(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
}

export function getRuns(token) {
  return fetchJson(`${BASE_URL}/runs/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function submitRun(token, prompt, modelOutput) {
  return fetchJson(`${BASE_URL}/runs/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      experiment_id: 1,
      prompt,
      model_output: modelOutput,
      model_name: 'gemini-pro',
    }),
  })
}

export function triggerEval(token, runId) {
  return fetchJson(`${BASE_URL}/runs/${runId}/evaluate`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function getRunById(token, runId) {
  return fetchJson(`${BASE_URL}/runs/${runId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function deleteRun(token, runId) {
  return fetchJson(`${BASE_URL}/runs/${runId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function logout(token) {
  return fetchJson(`${BASE_URL}/auth/logout`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function getMe(token) {
  return fetchJson(`${BASE_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}
