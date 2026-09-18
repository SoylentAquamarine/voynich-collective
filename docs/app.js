const REPO = 'SoylentAquamarine/voynich-collective';
const RAW = `https://raw.githubusercontent.com/${REPO}/main/`;
const API = `https://api.github.com/repos/${REPO}/contents/`;

const cache = new Map();

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[char]));
}

function inlineMarkdown(value) {
  let text = escapeHtml(value);
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  text = text.replace(/\[([^\]]+)\]\(([^\s)]+)\)/g, (match, label, href) => {
    // Repository content is written by two AI agents from largely
    // uncontrolled research material; only allow http(s) links or
    // scheme-less relative paths through to a clickable href, so a
    // markdown link can't smuggle a javascript:/data: URI onto this
    // public page.
    const safe = /^https?:\/\//i.test(href) || !/^[a-z][a-z0-9+.-]*:/i.test(href);
    return safe ? `<a href="${href}">${label}</a>` : label;
  });
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/__([^_]+)__/g, '<strong>$1</strong>');
  text = text.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
  return text;
}

function markdown(source) {
  const lines = source.replace(/\r/g, '').split('\n');
  const out = [];
  let paragraph = [];
  let listType = null;
  let inCode = false;
  let code = [];

  const closeParagraph = () => {
    if (paragraph.length) out.push(`<p>${inlineMarkdown(paragraph.join(' '))}</p>`);
    paragraph = [];
  };
  const closeList = () => {
    if (listType) out.push(`</${listType}>`);
    listType = null;
  };

  for (const line of lines) {
    if (line.startsWith('```')) {
      closeParagraph(); closeList();
      if (inCode) { out.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`); code = []; }
      inCode = !inCode;
      continue;
    }
    if (inCode) { code.push(line); continue; }
    if (!line.trim()) { closeParagraph(); closeList(); continue; }
    if (/^---+$/.test(line.trim())) { closeParagraph(); closeList(); out.push('<hr>'); continue; }
    const heading = line.match(/^(#{1,4})\s+(.+)$/);
    if (heading) { closeParagraph(); closeList(); const level = heading[1].length; out.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`); continue; }
    const bullet = line.match(/^\s*[-*]\s+(.+)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
    if (bullet || ordered) {
      closeParagraph();
      const wanted = ordered ? 'ol' : 'ul';
      if (listType !== wanted) { closeList(); listType = wanted; out.push(`<${wanted}>`); }
      out.push(`<li>${inlineMarkdown((bullet || ordered)[1])}</li>`);
      continue;
    }
    if (line.startsWith('> ')) { closeParagraph(); closeList(); out.push(`<blockquote>${inlineMarkdown(line.slice(2))}</blockquote>`); continue; }
    paragraph.push(line.trim());
  }
  closeParagraph(); closeList();
  if (inCode) out.push(`<pre><code>${escapeHtml(code.join('\n'))}</code></pre>`);
  return out.join('\n');
}

async function getText(path) {
  if (cache.has(path)) return cache.get(path);
  const response = await fetch(RAW + path, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`Could not load ${path}`);
  const value = await response.text();
  cache.set(path, value);
  return value;
}

async function renderFile(path, element) {
  element.classList.add('loading');
  element.textContent = 'Loading the latest repository version…';
  try {
    element.innerHTML = markdown(await getText(path));
    element.classList.remove('loading', 'error');
  } catch (error) {
    element.textContent = `${error.message}. Open the repository directly to read this record.`;
    element.classList.add('error');
  }
}

const routes = [...document.querySelectorAll('.route')];
const links = [...document.querySelectorAll('[data-route]')];
function showRoute() {
  const requested = location.hash.slice(1) || 'overview';
  const route = routes.some(item => item.id === requested) ? requested : 'overview';
  routes.forEach(item => item.classList.toggle('active', item.id === route));
  links.forEach(item => item.classList.toggle('active', item.dataset.route === route));
  if (route === 'theories') renderFile('knowledge-base/state.md', document.querySelector('#state-content'));
  if (route === 'logs') loadLogs();
  if (route === 'dialogue') loadDialogue(document.querySelector('[data-dialogue].active')?.dataset.dialogue || 'claude');
  document.querySelector('#primary-nav').classList.remove('open');
  document.querySelector('.nav-toggle').setAttribute('aria-expanded', 'false');
  window.scrollTo({ top: 0, behavior: 'instant' });
}

let logsLoaded = false;
async function loadLogs() {
  if (logsLoaded) return;
  const list = document.querySelector('#log-list');
  const content = document.querySelector('#log-content');
  try {
    const response = await fetch(API + 'logs', { headers: { Accept: 'application/vnd.github+json' }, cache: 'no-cache' });
    if (!response.ok) throw new Error('Could not list logs');
    const files = (await response.json()).filter(item => item.type === 'file' && item.name.endsWith('.md') && item.name !== 'README.md').sort((a, b) => b.name.localeCompare(a.name));
    document.querySelector('#log-count').textContent = files.length;
    list.innerHTML = '';
    for (const [index, file] of files.entries()) {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = file.name.replace(/\.md$/, '').replaceAll('-', ' ');
      button.addEventListener('click', () => {
        list.querySelectorAll('button').forEach(item => item.classList.remove('active'));
        button.classList.add('active');
        renderFile(`logs/${file.name}`, content);
      });
      list.appendChild(button);
      if (index === 0) button.click();
    }
    if (!files.length) content.textContent = 'No research logs have been published yet.';
    logsLoaded = true;
  } catch (error) {
    content.textContent = `${error.message}. View the logs folder on GitHub instead.`;
    content.classList.add('error');
  }
}

const dialogueFiles = {
  claude: 'comms/FromClaudeToChatGPT.md',
  chatgpt: 'comms/FromChatGPTToClaude.md'
};
function loadDialogue(direction) {
  renderFile(dialogueFiles[direction], document.querySelector('#dialogue-content'));
}

document.querySelector('.nav-toggle').addEventListener('click', event => {
  const open = document.querySelector('#primary-nav').classList.toggle('open');
  event.currentTarget.setAttribute('aria-expanded', String(open));
});
document.querySelectorAll('[data-dialogue]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-dialogue]').forEach(item => { item.classList.remove('active'); item.setAttribute('aria-selected', 'false'); });
  button.classList.add('active'); button.setAttribute('aria-selected', 'true'); loadDialogue(button.dataset.dialogue);
}));
window.addEventListener('hashchange', showRoute);
showRoute();
