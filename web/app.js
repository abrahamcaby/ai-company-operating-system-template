'use strict';

// The only HTML strings in this application are these static, authored SVGs.
// All API data is inserted with textContent or other DOM properties.
const ICONS = {
  overview: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  knowledge: '<path d="M4 4h6l2 2 2-2h6v15h-6l-2 2-2-2H4z"/><path d="M12 6v15M7 8h2M7 12h2M15 8h2M15 12h2"/>',
  workflows: '<rect x="3" y="3" width="6" height="6" rx="1.5"/><rect x="15" y="15" width="6" height="6" rx="1.5"/><path d="M6 9v9h9M9 6h9v9"/>',
  connections: '<path d="m8 9 7-7m-5 9 7-7M7 8l9 9m-8-7-4 4a4 4 0 0 0 6 6l4-4M11 5l2-2a4 4 0 0 1 6 6l-2 2"/>',
  shield: '<path d="m12 3 8 3v5c0 5-4 8-8 10-4-2-8-5-8-10V6z"/><path d="m8 12 3 3 5-6"/>',
  arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>',
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
  file: '<path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6M9 16h5"/>',
  spark: '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5z"/>',
  check: '<path d="m5 12 4 4L19 6"/>',
  close: '<path d="m6 6 12 12M18 6 6 18"/>',
  lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7v.1"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'
};

const state = { users: [], userId: '', workspace: null, actions: [], page: 'overview', generation: 0, query: '', kind: 'all', connectionQuery: '', documentGeneration: 0 };
const pageNames = { overview: 'Overview', knowledge: 'Knowledge', workflows: 'Workflows', connections: 'Connections', access: 'My access' };
const content = document.querySelector('#page-content');
const persona = document.querySelector('#persona');
const dialog = document.querySelector('#document-dialog');

function el(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined && text !== null) element.textContent = String(text);
  return element;
}

function icon(name) {
  const holder = el('span');
  holder.setAttribute('aria-hidden', 'true');
  holder.innerHTML = '<svg viewBox="0 0 24 24">' + (ICONS[name] || ICONS.file) + '</svg>';
  return holder;
}

function button(text, className, handler, iconName) {
  const control = el('button', className, text);
  control.type = 'button';
  if (iconName) control.append(icon(iconName));
  if (handler) control.addEventListener('click', handler);
  return control;
}

function human(value) { return String(value || '').replaceAll('_', ' ').replaceAll('-', ' '); }
function dateLabel(value) {
  if (!value) return 'Demo record';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}
function personName(id) { return state.users.find(user => user.id === id)?.name || id || 'Unassigned'; }
function currentUser() { return state.workspace?.user || {}; }
function documents() { return state.workspace?.documents || []; }
function permissions() { return state.workspace?.permissions || {}; }

async function api(path, options = {}) {
  const headers = { 'X-Demo-User': state.userId, ...options.headers };
  if (options.body !== undefined) headers['Content-Type'] = 'application/json';
  const response = await fetch(path, { ...options, headers });
  let data;
  try { data = await response.json(); } catch { throw new Error('The workspace returned an unreadable response. Please try again.'); }
  if (!response.ok) throw new Error(data.error || 'The request could not be completed.');
  return data;
}

function clearMessage() { document.querySelector('#global-message').replaceChildren(); }
function message(text, error = false, target = document.querySelector('#global-message')) {
  const note = el('div', 'inline-message' + (error ? ' error' : ''), text);
  note.setAttribute('role', error ? 'alert' : 'status');
  target.replaceChildren(note);
}

function loading(title = 'Opening your workspace', detail = 'Loading the evidence this demo person can access.') {
  const box = el('div', 'loading-state');
  box.append(el('span', 'loading-dot'), el('h1', '', title), el('p', '', detail));
  box.setAttribute('role', 'status');
  return box;
}

function empty(title, detail, iconName = 'knowledge') {
  const box = el('div', 'empty-state');
  box.append(icon(iconName), el('h2', '', title), el('p', '', detail));
  return box;
}

function heading(eyebrow, title, description) {
  const box = el('div', 'page-heading');
  const copy = el('div');
  copy.append(el('span', 'eyebrow', eyebrow), el('h1', '', title), el('p', 'page-description', description));
  const badge = el('div', 'role-pill');
  badge.append(icon('shield'), el('span', '', currentUser().department + ' view'));
  box.append(copy, badge);
  return box;
}

function sectionIntro(title, text) {
  const box = el('div', 'section-intro');
  const copy = el('p');
  copy.append(el('strong', '', title + ' '), document.createTextNode(text));
  box.append(icon('shield'), copy);
  return box;
}

function panelHeader(title, subtitle, action) {
  const box = el('div', 'panel-header');
  const text = el('div');
  text.append(el('h2', '', title));
  if (subtitle) text.append(el('p', '', subtitle));
  box.append(text);
  if (action) box.append(action);
  return box;
}

function sourceButton(doc, short = false) {
  return button(short ? doc.system : doc.title, '', () => openDocument(doc.id));
}

function stat(value, label, iconName) {
  const box = el('div', 'stat-card');
  const mark = el('span', 'stat-icon');
  mark.append(icon(iconName));
  const copy = el('div');
  copy.append(el('strong', 'stat-value', value), el('span', 'stat-label', label));
  box.append(mark, copy);
  return box;
}

function renderOverview() {
  const user = currentUser();
  const firstName = String(user.name || 'there').split(' ')[0];
  content.append(heading('YOUR WORKSPACE, CONNECTED', 'A clearer view of your company.', 'Welcome, ' + firstName + '. Explore company knowledge, follow the evidence, and move work forward with the right permissions.'));
  const stats = el('div', 'stat-row');
  stats.append(stat(documents().length, 'Records in your scope', 'knowledge'), stat(state.actions.length, 'Visible workflow proposals', 'workflows'), stat((state.workspace.connections || []).length, 'Planned connections', 'connections'));
  content.append(stats);
  const grid = el('div', 'overview-grid');
  const primary = el('section', 'panel');
  primary.append(panelHeader('Your evidence brief', 'A few records available in your current view.', button('Browse knowledge', 'text-button', () => navigate('knowledge'), 'arrow')));
  const latest = [...documents()].sort((a, b) => String(b.updated_at).localeCompare(String(a.updated_at))).slice(0, 4);
  if (!latest.length) primary.append(empty('No records in this view', 'This demo person has no source documents available. Switch persona to explore another team’s workspace.'));
  latest.forEach((doc, index) => {
    const row = el('article', 'brief-doc');
    const copy = el('div', 'brief-doc-content');
    copy.append(el('h3', '', doc.title), el('p', '', doc.summary || 'Open this record to inspect its evidence.'));
    const source = el('div', 'source-line');
    source.append(sourceButton(doc, true), el('span', '', human(doc.kind)), el('span', '', dateLabel(doc.updated_at)));
    copy.append(source);
    row.append(el('span', 'brief-index', String(index + 1).padStart(2, '0')), copy);
    primary.append(row);
  });
  const secondary = el('div', 'overview-secondary');
  secondary.append(askPanel(), activityPanel());
  grid.append(primary, secondary);
  content.append(grid);
}

function askPanel() {
  const box = el('section', 'panel ask-panel');
  const mark = el('div', 'ask-mark');
  mark.append(icon('spark'));
  box.append(mark, el('h2', '', 'Start with a question.'), el('p', '', 'Search the company evidence you can access. Every result keeps a path back to its source.'));
  const form = el('form');
  const label = el('label', '', 'What would you like to understand?');
  label.htmlFor = 'ask-question';
  const input = el('textarea');
  input.id = 'ask-question';
  input.placeholder = 'What should our team focus on this quarter?';
  input.required = true;
  input.maxLength = 2000;
  input.rows = 3;
  const footer = el('div', 'ask-form-footer');
  const submit = button('Find evidence', 'button', null, 'arrow');
  submit.type = 'submit';
  footer.append(el('span', '', 'Evidence preview · Keyword search · No model connected'), submit);
  form.append(label, input, footer);
  const result = el('div');
  result.setAttribute('aria-live', 'polite');
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question) return;
    const generation = state.generation;
    submit.disabled = true;
    submit.textContent = 'Searching…';
    result.replaceChildren(el('p', 'field-message', 'Searching records available to ' + currentUser().name + '…'));
    try {
      const data = await api('/api/ask', { method: 'POST', body: JSON.stringify({ question }) });
      if (generation !== state.generation) return;
      const answer = el('div', 'ask-result');
      answer.append(el('span', 'answer-tag', 'EXTRACTIVE EVIDENCE PREVIEW'), el('p', '', data.answer || 'No matching evidence was found.'));
      if (data.citations?.length) {
        const citations = el('div', 'citation-list');
        data.citations.forEach(citation => citations.append(sourceButton(citation)));
        answer.append(citations);
      }
      result.replaceChildren(answer);
    } catch (error) {
      if (generation === state.generation) result.replaceChildren(el('p', 'field-message error', error.message));
    } finally {
      submit.disabled = false;
      submit.replaceChildren(document.createTextNode('Find evidence'), icon('arrow'));
    }
  });
  const samples = el('div', 'sample-questions');
  ['Quarterly priorities', 'Customer renewal risks', 'Budget and hiring'].forEach(question => samples.append(button(question, '', () => { input.value = question; input.focus(); })));
  box.append(form, samples, result);
  return box;
}

function activityPanel() {
  const panel = el('section', 'panel activity-panel');
  panel.append(panelHeader('Workspace activity', 'Events visible to your demo person.'));
  const list = el('div', 'activity-list');
  const activities = (state.workspace.activities || []).slice(0, 4);
  if (!activities.length) list.append(el('p', 'form-note', 'No workspace events are visible in this view yet.'));
  activities.forEach(activity => {
    const row = el('div', 'activity-item');
    const copy = el('div');
    copy.append(el('p', '', human(activity.event)), el('small', '', activity.detail));
    const time = el('time', '', dateLabel(activity.created_at));
    if (activity.created_at) time.dateTime = activity.created_at;
    row.append(el('span', 'activity-point'), copy, time);
    list.append(row);
  });
  panel.append(list);
  return panel;
}

function renderKnowledge() {
  content.append(heading('SHARED CONTEXT', 'Knowledge, with a source.', 'Company files, meeting notes, customer conversations, and operational records — each visible within your access.'));
  const toolbar = el('div', 'toolbar');
  const search = el('label', 'search-box');
  const input = el('input');
  input.type = 'search';
  input.placeholder = 'Search your accessible knowledge…';
  input.value = state.query;
  input.setAttribute('aria-label', 'Search accessible knowledge');
  search.append(icon('search'), input);
  const select = el('select', 'filter-select');
  select.setAttribute('aria-label', 'Filter knowledge by record type');
  const all = el('option', '', 'All record types');
  all.value = 'all';
  select.append(all);
  [...new Set(documents().map(doc => doc.kind))].sort().forEach(kind => {
    const option = el('option', '', human(kind));
    option.value = kind;
    select.append(option);
  });
  if (![...select.options].some(option => option.value === state.kind)) state.kind = 'all';
  select.value = state.kind;
  toolbar.append(search, select);
  const results = el('div');
  const caption = el('p', 'results-caption');
  caption.setAttribute('aria-live', 'polite');
  function filter() {
    const query = state.query.toLowerCase().trim();
    const matches = documents().filter(doc => (state.kind === 'all' || doc.kind === state.kind) && [doc.title, doc.summary, doc.system, doc.owner, ...(doc.tags || [])].join(' ').toLowerCase().includes(query));
    caption.textContent = matches.length + ' ' + (matches.length === 1 ? 'record' : 'records') + ' available in your current view';
    results.replaceChildren();
    if (!matches.length) { results.append(empty('No matching records', 'Try another search or record type. Records outside your access are not included in this view.')); return; }
    const grid = el('div', 'document-grid');
    matches.forEach(doc => grid.append(documentCard(doc)));
    results.append(grid);
  }
  input.addEventListener('input', () => { state.query = input.value; filter(); });
  select.addEventListener('change', () => { state.kind = select.value; filter(); });
  content.append(toolbar, caption, results);
  filter();
}

function documentCard(doc) {
  const card = button('', 'document-card', () => openDocument(doc.id));
  const top = el('div', 'document-card-top');
  const kind = el('span', 'document-kind');
  kind.append(icon(doc.kind === 'meeting' ? 'clock' : 'file'), document.createTextNode(human(doc.kind)));
  top.append(kind, el('span', 'classification', human(doc.classification)));
  const bottom = el('div', 'document-card-bottom');
  bottom.append(el('span', '', doc.system + ' · ' + dateLabel(doc.updated_at)), icon('arrow'));
  card.append(top, el('h2', '', doc.title), el('p', '', doc.summary || 'Open to inspect this source record.'), bottom);
  return card;
}

async function openDocument(id) {
  const target = document.querySelector('#document-content');
  const request = ++state.documentGeneration;
  target.replaceChildren(loading('Opening source', 'Checking access to this record.'));
  if (!dialog.open) dialog.showModal();
  try {
    const data = await api('/api/documents/' + encodeURIComponent(id));
    if (request !== state.documentGeneration || !dialog.open) return;
    const doc = data.document;
    const title = el('h2', '', doc.title);
    title.id = 'document-title';
    const metadata = el('dl', 'document-metadata');
    [['Source system', doc.system], ['Owner', doc.owner], ['Classification', human(doc.classification)], ['Updated', dateLabel(doc.updated_at)]].forEach(([label, value]) => {
      const item = el('div', 'metadata-item');
      item.append(el('dt', '', label), el('dd', '', value));
      metadata.append(item);
    });
    const tags = el('div', 'document-tags');
    (doc.tags || []).forEach(tag => tags.append(el('span', '', human(tag))));
    target.replaceChildren(el('span', 'document-kind', human(doc.kind)), title, metadata, el('p', 'document-summary', doc.summary), el('div', 'document-body', doc.content), tags);
    const derived = (doc.source_ids || []).map(sourceId => documents().find(source => source.id === sourceId)).filter(Boolean);
    if (derived.length) {
      const related = el('div', 'citation-list related-sources');
      derived.forEach(source => related.append(sourceButton(source)));
      target.append(el('p', 'form-note', 'Supporting source records'), related);
    }
    target.append(el('p', 'source-disclaimer', 'Fictional demonstration record. In a deployed system, this view would retain source attribution, freshness, and permission checks against the connected tool.'));
  } catch (error) {
    if (request !== state.documentGeneration) return;
    const title = el('h2', '', 'This record is unavailable');
    title.id = 'document-title';
    target.replaceChildren(title, el('p', 'document-summary', error.message));
  }
}

function renderWorkflows() {
  content.append(heading('HUMANS IN CONTROL', 'Move from context to action.', 'Propose a task from source evidence, have another authorized person review it, then simulate the approved action.'));
  content.append(sectionIntro('Every action has a checkpoint.', 'This demo records proposals and approvals locally. Execution is simulated; no task is sent to an external tool.'));
  const layout = el('div', 'workflow-layout');
  const list = el('section', 'panel');
  list.append(panelHeader('Action queue', 'Only proposals available within your access.'));
  if (!state.actions.length) list.append(empty('A clear queue', 'Propose a task from an accessible source to explore the approval flow.', 'workflows'));
  state.actions.forEach(action => list.append(workflowCard(action)));
  const create = el('section', 'panel');
  create.append(panelHeader('Propose a task', 'Start with a record you can access.'));
  if (permissions().can_propose && documents().length) create.append(proposalForm());
  else {
    const box = el('div', 'workflow-form');
    box.append(el('p', 'form-note', permissions().can_propose ? 'No source records are currently available for a proposal.' : 'This demo person can review the workspace but cannot propose tasks. Switch persona to try this workflow.'));
    create.append(box);
  }
  layout.append(list, create);
  content.append(layout);
}

function workflowCard(action) {
  const card = el('article', 'workflow-item');
  const head = el('div', 'workflow-item-heading');
  const status = ['proposed', 'approved', 'simulated'].includes(action.status) ? action.status : 'other';
  const label = status === 'simulated' ? 'Simulated' : human(action.status);
  head.append(el('h3', '', action.title), el('span', 'status-pill ' + status, label));
  const source = el('div', 'source-line');
  const doc = documents().find(record => record.id === action.document_id);
  if (doc) source.append(icon('file'), sourceButton(doc));
  const meta = el('p', 'workflow-meta', 'Proposed by ' + personName(action.requested_by) + ' · ' + dateLabel(action.created_at));
  if (action.approved_by) meta.append(el('br'), document.createTextNode('Approved by ' + personName(action.approved_by)));
  card.append(head, source, meta);
  const controls = el('div', 'workflow-controls');
  const owner = action.requested_by === currentUser().id;
  if (status === 'proposed' && permissions().can_approve && !owner) controls.append(button('Approve proposal', 'button secondary', event => transitionAction(action, 'approve', event.currentTarget), 'check'));
  if (status === 'approved' && permissions().can_approve && action.approved_by === currentUser().id) controls.append(button('Simulate execution', 'button secondary', event => transitionAction(action, 'execute', event.currentTarget), 'arrow'));
  if (controls.childNodes.length) card.append(controls);
  let hint = '';
  if (status === 'proposed') hint = owner ? 'A different authorized person must approve your proposal.' : permissions().can_approve ? 'Review the source evidence before approving this task.' : 'Waiting for an authorized reviewer to approve.';
  if (status === 'approved' && action.approved_by !== currentUser().id) hint = 'The recorded approver can simulate this action after source access is rechecked.';
  if (status === 'simulated') hint = 'Simulation complete. No change was made in an external system.';
  if (hint) card.append(el('p', 'workflow-hint', hint));
  return card;
}

function proposalForm() {
  const form = el('form', 'workflow-form');
  const steps = el('div', 'step-list');
  ['Propose', 'Review', 'Simulate'].forEach((label, index) => { const step = el('div', 'step'); step.append(el('b', '', index + 1), document.createTextNode(label)); steps.append(step); });
  const sourceField = el('div', 'form-field');
  const sourceLabel = el('label', '', 'Source evidence');
  sourceLabel.htmlFor = 'proposal-source';
  const select = el('select');
  select.id = 'proposal-source';
  select.required = true;
  documents().forEach(doc => { const option = el('option', '', doc.title); option.value = doc.id; select.append(option); });
  sourceField.append(sourceLabel, select);
  const titleField = el('div', 'form-field');
  const titleLabel = el('label', '', 'Proposed task');
  titleLabel.htmlFor = 'proposal-title';
  const input = el('input');
  input.id = 'proposal-title';
  input.placeholder = 'e.g. Review the renewal plan with the account team';
  input.required = true;
  input.maxLength = 200;
  titleField.append(titleLabel, input);
  const submit = button('Create proposal', 'button', null, 'arrow');
  submit.type = 'submit';
  const result = el('p', 'field-message');
  result.setAttribute('aria-live', 'polite');
  form.append(steps, sourceField, titleField, submit, el('p', 'form-note', 'Your proposal stays within the source’s permissions. A separate reviewer must approve it before a simulated execution.'), result);
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const title = input.value.trim();
    if (!title) { input.focus(); return; }
    const generation = state.generation;
    submit.disabled = true;
    result.textContent = 'Creating your proposal…';
    try {
      await api('/api/actions', { method: 'POST', body: JSON.stringify({ document_id: select.value, kind: 'create_task', title }) });
      if (generation !== state.generation) return;
      await refreshActions();
      if (generation === state.generation) message('Proposal created. Switch to another authorized reviewer to explore the approval step.');
    } catch (error) {
      if (generation === state.generation) { result.className = 'field-message error'; result.textContent = error.message; }
    } finally { submit.disabled = false; }
  });
  return form;
}

async function transitionAction(action, operation, control) {
  const generation = state.generation;
  control.disabled = true;
  clearMessage();
  try {
    await api('/api/actions/' + encodeURIComponent(action.id) + '/' + operation, { method: 'POST', body: '{}' });
    if (generation !== state.generation) return;
    await refreshActions();
    if (generation === state.generation) message(operation === 'approve' ? 'Proposal approved. You can now simulate its execution.' : 'Execution simulated. No external system was changed.');
  } catch (error) { if (generation === state.generation) message(error.message, true); }
  finally { control.disabled = false; }
}

async function refreshActions() {
  const generation = state.generation;
  const [actionData, workspace] = await Promise.all([api('/api/actions'), api('/api/workspace')]);
  if (generation !== state.generation) return;
  state.actions = actionData.actions || [];
  state.workspace = workspace;
  updateChrome();
  renderPage();
}

function renderConnections() {
  content.append(heading('BRING YOUR COMPANY TOOLS', 'One workspace. Your stack.', 'Connect the systems your teams already use through a shared adapter contract. Choose the tools that fit your company.'));
  content.append(sectionIntro('A catalog of planned adapters.', 'These are integration targets, not active connectors. Production adapters need authorization, ongoing sync, source permissions, and health monitoring.'));
  const toolbar = el('div', 'toolbar');
  const search = el('label', 'search-box');
  const input = el('input');
  input.type = 'search';
  input.placeholder = 'Find a tool or connection category…';
  input.value = state.connectionQuery;
  input.setAttribute('aria-label', 'Search planned connections');
  search.append(icon('search'), input);
  toolbar.append(search, el('span', 'small-label', permissions().can_admin ? 'CONNECTION ADMIN VIEW' : 'CATALOG VIEW'));
  const results = el('div');
  const caption = el('p', 'results-caption');
  caption.setAttribute('aria-live', 'polite');
  function filter() {
    const query = state.connectionQuery.trim().toLowerCase();
    const matches = (state.workspace.connections || []).filter(connection => [connection.name, connection.category, connection.description].join(' ').toLowerCase().includes(query));
    caption.textContent = matches.length + ' planned ' + (matches.length === 1 ? 'adapter' : 'adapters') + ' · 0 live connections';
    results.replaceChildren();
    if (!matches.length) { results.append(empty('No matching connections', 'Try a tool category such as CRM, meetings, or finance.', 'connections')); return; }
    const grid = el('div', 'connections-grid');
    matches.forEach(connection => {
      const card = el('article', 'connection-card');
      card.append(el('span', 'connection-icon', String(connection.name || '?').charAt(0).toUpperCase()), el('h2', '', connection.name), el('span', 'connection-category', human(connection.category)), el('p', '', connection.description), el('span', 'status-pill', 'Planned adapter'));
      grid.append(card);
    });
    results.append(grid);
  }
  input.addEventListener('input', () => { state.connectionQuery = input.value; filter(); });
  content.append(toolbar, caption, results);
  filter();
}

function renderAccess() {
  content.append(heading('THE RIGHT CONTEXT, THE RIGHT PEOPLE', 'Your access travels with you.', 'A shared operating system should respect individual boundaries across search, evidence, summaries, and actions.'));
  content.append(sectionIntro('Demo identity only.', 'The persona selector is intentionally open for exploration. Production needs verified company identity, SSO, source authorization, and independently enforced access policies.'));
  const grid = el('div', 'access-grid');
  const scope = el('section', 'panel access-card');
  scope.append(el('h2', '', currentUser().name), el('p', '', currentUser().title + ' · ' + currentUser().department));
  const list = el('ul', 'permission-list');
  [['View accessible knowledge', true], ['Propose source-backed tasks', permissions().can_propose], ['Approve another person’s tasks', permissions().can_approve], ['Manage connection configuration', permissions().can_admin]].forEach(([label, allowed]) => {
    const item = el('li');
    const value = el('span', 'permission-value' + (allowed ? '' : ' disabled'));
    value.append(icon(allowed ? 'check' : 'lock'), document.createTextNode(allowed ? 'Allowed' : 'Restricted'));
    item.append(el('span', '', label), value);
    list.append(item);
  });
  scope.append(list, el('p', 'form-note', documents().length + ' records and ' + state.actions.length + ' workflow proposals are visible in this demo view. Connection management is a policy flag; live configuration is not implemented.'));
  const rules = el('section', 'panel access-card');
  rules.append(el('h2', '', 'Boundaries by design'), el('p', '', 'The principles a company-wide system must preserve.'));
  const ruleList = el('ol', 'rule-list');
  [['Leadership is not blanket access', 'A CEO can see company and executive context without access to private HR or every personal record.'], ['Administration is a separate power', 'IT can manage the connection layer without automatically gaining permission to read the connected content.'], ['An answer inherits its sources', 'Search and generated context must enforce the underlying source access. Derived records cannot widen it.'], ['Approval remains accountable', 'People cannot approve their own proposals. Source access and evidence versions are checked again before simulation.']].forEach(([title, text], index) => {
    const item = el('li');
    const copy = el('p');
    copy.append(el('strong', '', title), document.createTextNode(text));
    item.append(el('span', '', String(index + 1).padStart(2, '0')), copy);
    ruleList.append(item);
  });
  rules.append(ruleList);
  grid.append(scope, rules);
  content.append(grid);
}

function updateChrome() {
  document.querySelector('#knowledge-count').textContent = documents().length;
  document.querySelector('#workflow-count').textContent = state.actions.length;
  document.querySelector('#user-avatar').textContent = String(currentUser().name || 'MW').split(' ').map(part => part[0]).slice(0, 2).join('');
  document.querySelector('#user-avatar').title = currentUser().name || '';
}

function renderPage() {
  if (!state.workspace) return;
  content.replaceChildren();
  document.querySelector('#breadcrumb-page').textContent = pageNames[state.page];
  document.title = pageNames[state.page] + ' · AI Company Operating System Template';
  document.querySelectorAll('[data-page]').forEach(link => {
    if (link.dataset.page === state.page) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  const renderers = { overview: renderOverview, knowledge: renderKnowledge, workflows: renderWorkflows, connections: renderConnections, access: renderAccess };
  renderers[state.page]();
}

function navigate(page) {
  if (!pageNames[page]) page = 'overview';
  if (location.hash !== '#' + page) { location.hash = page; return; }
  state.page = page;
  clearMessage();
  renderPage();
}

async function loadWorkspace() {
  const generation = ++state.generation;
  ++state.documentGeneration;
  if (dialog.open) dialog.close();
  document.querySelector('#document-content').replaceChildren();
  clearMessage();
  state.workspace = null;
  state.actions = [];
  state.query = '';
  state.kind = 'all';
  content.replaceChildren(loading());
  document.querySelector('#knowledge-count').textContent = '—';
  document.querySelector('#workflow-count').textContent = '—';
  document.querySelector('#user-avatar').textContent = '…';
  document.querySelector('#user-avatar').removeAttribute('title');
  try {
    const [workspace, actionData] = await Promise.all([api('/api/workspace'), api('/api/actions')]);
    if (generation !== state.generation) return;
    state.workspace = workspace;
    state.actions = actionData.actions || [];
    updateChrome();
    renderPage();
  } catch (error) {
    if (generation !== state.generation) return;
    const box = empty('The workspace could not load', error.message, 'connections');
    const retry = button('Try again', 'button secondary retry-button', loadWorkspace);
    box.append(retry);
    content.replaceChildren(box);
  }
}

async function boot() {
  document.querySelectorAll('[data-icon]').forEach(node => node.replaceChildren(icon(node.dataset.icon)));
  state.page = pageNames[location.hash.slice(1)] ? location.hash.slice(1) : 'overview';
  window.addEventListener('hashchange', () => navigate(location.hash.slice(1)));
  document.querySelector('#close-document').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const bounds = dialog.getBoundingClientRect(); if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close(); } });
  dialog.addEventListener('close', () => { ++state.documentGeneration; });
  persona.addEventListener('change', () => {
    state.userId = persona.value;
    try { localStorage.setItem('ai-company-os-demo-persona', state.userId); } catch { /* Storage is optional in restricted browsers. */ }
    loadWorkspace();
  });
  try {
    const data = await api('/api/demo/users');
    state.users = data.users || [];
    if (!state.users.length) throw new Error('No demo people are available.');
    let saved = '';
    try { saved = localStorage.getItem('ai-company-os-demo-persona') || ''; } catch { /* Storage is optional. */ }
    state.userId = state.users.some(user => user.id === saved) ? saved : state.users.some(user => user.id === 'ceo') ? 'ceo' : state.users[0].id;
    persona.replaceChildren();
    state.users.forEach(user => {
      const option = el('option', '', user.name + ' · ' + user.title);
      option.value = user.id;
      persona.append(option);
    });
    persona.value = state.userId;
    await loadWorkspace();
    const documentId = new URLSearchParams(location.search).get('document');
    if (documentId && state.workspace) openDocument(documentId);
  } catch (error) {
    persona.replaceChildren(el('option', '', 'Demo unavailable'));
    persona.disabled = true;
    const box = empty('Unable to open the demo', error.message + ' Start the local server and reload this page.', 'connections');
    content.replaceChildren(box);
  }
}

boot();
