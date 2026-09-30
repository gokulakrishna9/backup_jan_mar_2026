import client from './client';

/**
 * List public repositories for a GitHub user or organization.
 * GET /api/github/:user/repos
 */
export async function listRepos(user) {
  const res = await client.get(`/github/${encodeURIComponent(user)}/repos`);
  return res.data;
}

/**
 * Get detailed metadata for a single repository.
 * GET /api/github/:owner/:repo
 */
export async function repoInfo(owner, repo) {
  const res = await client.get(`/github/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}`);
  return res.data;
}

/**
 * Get the file tree for a repository.
 * GET /api/github/:owner/:repo/tree
 */
export async function repoTree(owner, repo) {
  const res = await client.get(`/github/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/tree`);
  return res.data;
}

/**
 * Read a single file from a repository.
 * GET /api/github/:owner/:repo/file?path=...
 */
export async function readFile(owner, repo, path) {
  const res = await client.get(`/github/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/file`, {
    params: { path },
  });
  return res.data;
}

/**
 * Generate a markdown summary of a user's repositories.
 * GET /api/github/:user/summary
 */
export async function summarize(user) {
  const res = await client.get(`/github/${encodeURIComponent(user)}/summary`);
  return res.data;
}
