"""
Frontend HTML and UI Generator for Gacha Character & Team Builder REST API.
Menyediakan antarmuka web interaktif (Single Page Application vanilla HTML5, CSS3, ES6 JavaScript)
yang modern, aesthetic, responsif, dan ringan tanpa dependensi eksternal.
"""

def get_frontend_html():
    """
    Mengembalikan string HTML dokumen lengkap untuk antarmuka pengguna web.
    """
    return """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gacha Character & Team Builder - REST API & Explorer</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>✦</text></svg>">
  <style>
    :root {
      --bg-body: #0a0e17;
      --bg-surface: #111827;
      --bg-card: #162032;
      --bg-card-hover: #1c2a42;
      --border-subtle: #223249;
      --border-strong: #334969;
      --text-main: #f8fafc;
      --text-dim: #94a3b8;
      --text-muted: #64748b;
      --primary: #38bdf8;
      --primary-hover: #0284c7;
      --star-5: #fbbf24;
      --star-5-glow: rgba(251, 191, 36, 0.25);
      --star-4: #c084fc;
      --star-4-glow: rgba(192, 132, 252, 0.25);
      --pyro: #f87171;
      --hydro: #38bdf8;
      --anemo: #2dd4bf;
      --electro: #c084fc;
      --dendro: #4ade80;
      --cryo: #bae6fd;
      --geo: #fbbf24;
      --danger: #ef4444;
      --success: #10b981;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --font-stack: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-body);
      color: var(--text-main);
      font-family: var(--font-stack);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 15% 20%, rgba(56, 189, 248, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(192, 132, 252, 0.05) 0%, transparent 40%);
    }

    /* Container */
    .container {
      width: 100%;
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 1.25rem;
    }

    /* Navbar */
    .navbar {
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .nav-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 68px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      text-decoration: none;
      color: var(--text-main);
    }

    .brand-icon {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.25rem;
      color: #0f172a;
      box-shadow: 0 0 14px rgba(251, 191, 36, 0.4);
    }

    .brand-title {
      font-weight: 700;
      font-size: 1.125rem;
      letter-spacing: -0.02em;
      display: flex;
      flex-direction: column;
    }

    .brand-sub {
      font-size: 0.725rem;
      font-weight: 500;
      color: var(--text-dim);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    /* Health pill */
    .health-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      font-size: 0.775rem;
      font-weight: 600;
      padding: 0.35rem 0.75rem;
      border-radius: 9999px;
      text-decoration: none;
      transition: all 0.2s ease;
    }

    .health-pill.degraded {
      background: rgba(239, 68, 68, 0.1);
      border-color: rgba(239, 68, 68, 0.3);
      color: #f87171;
    }

    .health-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s infinite;
    }

    .health-pill.degraded .health-dot {
      background-color: #ef4444;
      box-shadow: 0 0 8px #ef4444;
    }

    @keyframes pulse {
      0% { opacity: 0.6; transform: scale(0.95); }
      50% { opacity: 1; transform: scale(1.1); }
      100% { opacity: 0.6; transform: scale(0.95); }
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      font-size: 0.875rem;
      font-weight: 600;
      padding: 0.5rem 1rem;
      border-radius: var(--radius-sm);
      border: 1px solid transparent;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .btn-primary {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
    }

    .btn-primary:hover {
      background: #0369a1;
      transform: translateY(-1px);
    }

    .btn-secondary {
      background: var(--bg-surface);
      border-color: var(--border-subtle);
      color: var(--text-dim);
    }

    .btn-secondary:hover {
      background: var(--border-subtle);
      color: var(--text-main);
      border-color: var(--border-strong);
    }

    .btn-gold {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      color: #ffffff;
      box-shadow: 0 2px 10px rgba(245, 158, 11, 0.3);
    }

    .btn-gold:hover {
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      transform: translateY(-1px);
    }

    .btn-danger {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.4);
      color: #f87171;
    }

    .btn-danger:hover {
      background: #ef4444;
      color: #fff;
    }

    .btn-sm {
      padding: 0.3rem 0.65rem;
      font-size: 0.775rem;
    }

    /* Navigation Tabs */
    .tabs-bar {
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      padding: 0.5rem 0 0;
    }

    .tabs-list {
      display: flex;
      gap: 1.5rem;
      list-style: none;
      overflow-x: auto;
      scrollbar-width: none;
    }

    .tabs-list::-webkit-scrollbar {
      display: none;
    }

    .tab-item {
      padding: 0.65rem 0.25rem 0.75rem;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-dim);
      border-bottom: 2px solid transparent;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .tab-item:hover {
      color: var(--text-main);
    }

    .tab-item.active {
      color: var(--primary);
      border-bottom-color: var(--primary);
    }

    .tab-badge {
      background: var(--border-subtle);
      color: var(--text-dim);
      font-size: 0.725rem;
      padding: 0.1rem 0.45rem;
      border-radius: 9999px;
    }

    .tab-item.active .tab-badge {
      background: rgba(56, 189, 248, 0.2);
      color: var(--primary);
    }

    /* Main Content */
    main {
      flex: 1;
      padding: 1.75rem 0 3rem;
    }

    /* Hero Banner */
    .hero {
      background: linear-gradient(180deg, rgba(22, 32, 50, 0.6) 0%, rgba(17, 24, 39, 0.4) 100%);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 1.5rem;
      margin-bottom: 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1.25rem;
    }

    .hero-info h1 {
      font-size: 1.45rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 0.35rem;
    }

    .hero-info p {
      color: var(--text-dim);
      font-size: 0.875rem;
      max-width: 640px;
    }

    .hero-stats {
      display: flex;
      gap: 1.5rem;
    }

    .hero-stat-card {
      background: rgba(10, 14, 23, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 0.75rem 1.25rem;
      text-align: center;
      min-width: 105px;
    }

    .hero-stat-value {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--text-main);
      font-variant-numeric: tabular-nums;
    }

    .hero-stat-label {
      font-size: 0.725rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-top: 0.15rem;
    }

    /* Controls Bar: Search & Filters */
    .controls-wrapper {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 1rem;
      margin-bottom: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }

    .controls-row-top {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
    }

    .search-box {
      flex: 1;
      min-width: 260px;
      position: relative;
    }

    .search-input {
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 0.55rem 1rem 0.55rem 2.25rem;
      border-radius: var(--radius-sm);
      font-size: 0.875rem;
      outline: none;
      transition: border-color 0.2s ease;
    }

    .search-input:focus {
      border-color: var(--primary);
    }

    .search-icon {
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
      font-size: 0.9rem;
    }

    .filter-select {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 0.55rem 0.75rem;
      border-radius: var(--radius-sm);
      font-size: 0.825rem;
      outline: none;
      cursor: pointer;
    }

    .filter-select:focus {
      border-color: var(--primary);
    }

    /* Element Filter Buttons */
    .element-filters {
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
      align-items: center;
    }

    .element-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-dim);
      padding: 0.35rem 0.75rem;
      border-radius: var(--radius-sm);
      font-size: 0.775rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
    }

    .element-btn:hover {
      background: var(--border-subtle);
      color: var(--text-main);
    }

    .element-btn.active {
      color: #fff;
      border-color: currentColor;
      box-shadow: 0 0 10px rgba(255, 255, 255, 0.15);
    }

    .element-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      display: inline-block;
    }

    /* Character Cards Grid */
    .grid-characters {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.25rem;
    }

    /* Card */
    .char-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .char-card:hover {
      transform: translateY(-3px);
      border-color: var(--border-strong);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }

    .char-card.rarity-5 {
      border-top: 3px solid var(--star-5);
    }

    .char-card.rarity-5:hover {
      box-shadow: 0 8px 24px var(--star-5-glow);
    }

    .char-card.rarity-4 {
      border-top: 3px solid var(--star-4);
    }

    .char-card.rarity-4:hover {
      box-shadow: 0 8px 24px var(--star-4-glow);
    }

    .char-header {
      padding: 1.15rem 1.15rem 0.5rem;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .char-name-group {
      flex: 1;
    }

    .char-name {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    .char-stars {
      color: var(--star-5);
      font-size: 0.85rem;
      letter-spacing: 0.1em;
      margin-top: 0.15rem;
    }

    .rarity-4 .char-stars {
      color: var(--star-4);
    }

    .element-badge {
      font-size: 0.725rem;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
      border-radius: var(--radius-sm);
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .char-tags {
      padding: 0 1.15rem 0.75rem;
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
    }

    .tag-pill {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: var(--text-dim);
      font-size: 0.725rem;
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-sm);
    }

    .char-stats-table {
      background: rgba(10, 14, 23, 0.4);
      border-top: 1px solid var(--border-subtle);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.85rem 1.15rem;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.65rem;
      font-size: 0.775rem;
    }

    .stat-item {
      display: flex;
      flex-direction: column;
    }

    .stat-label {
      color: var(--text-muted);
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .stat-val {
      color: var(--text-main);
      font-weight: 700;
      font-variant-numeric: tabular-nums;
      margin-top: 0.1rem;
    }

    .stat-val.ascension {
      color: var(--primary);
    }

    .char-footer {
      padding: 0.85rem 1.15rem;
      display: flex;
      gap: 0.5rem;
      margin-top: auto;
    }

    /* Teams View */
    .teams-list {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    .team-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      overflow: hidden;
    }

    .team-header {
      background: rgba(17, 24, 39, 0.6);
      border-bottom: 1px solid var(--border-subtle);
      padding: 1rem 1.25rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    .team-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .team-owner {
      font-size: 0.8rem;
      color: var(--text-dim);
    }

    .team-members-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1rem;
      padding: 1.25rem;
    }

    .member-slot {
      background: rgba(10, 14, 23, 0.5);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 1rem;
      position: relative;
    }

    .slot-num {
      position: absolute;
      top: 0.6rem;
      right: 0.6rem;
      background: var(--border-subtle);
      color: var(--text-muted);
      width: 22px;
      height: 22px;
      border-radius: 50%;
      font-size: 0.7rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .member-name {
      font-weight: 700;
      font-size: 0.95rem;
      margin-bottom: 0.35rem;
    }

    .member-meta {
      font-size: 0.775rem;
      color: var(--text-dim);
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }

    /* Weapons View */
    .weapons-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.25rem;
    }

    .weapon-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 1.15rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }

    .weapon-card.rarity-5 {
      border-top: 3px solid var(--star-5);
    }

    .weapon-card.rarity-4 {
      border-top: 3px solid var(--star-4);
    }

    .weapon-name {
      font-weight: 700;
      font-size: 1.05rem;
    }

    .weapon-desc {
      font-size: 0.775rem;
      color: var(--text-dim);
      font-style: italic;
      line-height: 1.4;
      background: rgba(10, 14, 23, 0.4);
      padding: 0.65rem;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-subtle);
    }

    /* API Explorer Tab */
    .api-explorer-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 1.5rem;
    }

    .endpoint-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.75rem 0;
      border-bottom: 1px solid var(--border-subtle);
      gap: 1rem;
      flex-wrap: wrap;
    }

    .endpoint-row:last-child {
      border-bottom: none;
    }

    .method-badge {
      font-family: monospace;
      font-weight: 700;
      font-size: 0.75rem;
      padding: 0.2rem 0.5rem;
      border-radius: var(--radius-sm);
      min-width: 60px;
      text-align: center;
    }

    .method-get { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
    .method-post { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
    .method-put { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
    .method-delete { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

    .endpoint-path {
      font-family: monospace;
      font-size: 0.85rem;
      color: var(--text-main);
    }

    .endpoint-desc {
      font-size: 0.8rem;
      color: var(--text-dim);
      flex: 1;
    }

    /* Modals */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(10, 14, 23, 0.8);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 200;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }

    .modal-overlay.open {
      display: flex;
    }

    .modal-window {
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 560px;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
      display: flex;
      flex-direction: column;
    }

    .modal-header {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .modal-title {
      font-size: 1.2rem;
      font-weight: 700;
    }

    .modal-close {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.25rem;
      cursor: pointer;
      line-height: 1;
      padding: 0.25rem;
    }

    .modal-close:hover {
      color: var(--text-main);
    }

    .modal-body {
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }

    .form-row {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.85rem;
    }

    .form-row-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.85rem;
    }

    .form-label {
      font-size: 0.775rem;
      font-weight: 600;
      color: var(--text-dim);
    }

    .form-input, .form-select {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 0.55rem 0.75rem;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      outline: none;
    }

    .form-input:focus, .form-select:focus {
      border-color: var(--primary);
    }

    .modal-footer {
      padding: 1.25rem 1.5rem;
      border-top: 1px solid var(--border-subtle);
      display: flex;
      justify-content: flex-end;
      gap: 0.75rem;
    }

    /* Toast Notification */
    .toast-container {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      z-index: 300;
      pointer-events: none;
    }

    .toast {
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      color: var(--text-main);
      padding: 0.85rem 1.25rem;
      border-radius: var(--radius-md);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 0.65rem;
      pointer-events: auto;
      animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      max-width: 380px;
    }

    .toast.success {
      border-left: 4px solid var(--success);
    }

    .toast.error {
      border-left: 4px solid var(--danger);
    }

    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    /* Empty state & Loading */
    .state-message {
      text-align: center;
      padding: 4rem 1rem;
      color: var(--text-dim);
    }

    .spinner {
      width: 32px;
      height: 32px;
      border: 3px solid var(--border-subtle);
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 0 auto 1rem;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      padding: 1.5rem 0;
      margin-top: auto;
      font-size: 0.825rem;
      color: var(--text-muted);
    }

    .footer-inner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .footer-links {
      display: flex;
      gap: 1.25rem;
    }

    .footer-links a {
      color: var(--text-dim);
      text-decoration: none;
      transition: color 0.2s ease;
    }

    .footer-links a:hover {
      color: var(--primary);
    }

    @media (max-width: 768px) {
      .hero-stats {
        width: 100%;
        justify-content: space-between;
      }
      .hero-stat-card {
        flex: 1;
        min-width: 0;
        padding: 0.5rem;
      }
      .form-row, .form-row-3 {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <nav class="navbar">
    <div class="container nav-inner">
      <a href="/" class="brand">
        <div class="brand-icon">✦</div>
        <div class="brand-title">
          <span>Gacha Builder</span>
          <span class="brand-sub">RESTful API Engine</span>
        </div>
      </a>

      <div class="nav-actions">
        <a id="health-status" href="/api/health" target="_blank" class="health-pill" title="Periksa status live database">
          <span class="health-dot"></span>
          <span id="health-text">Checking API...</span>
        </a>

        <button class="btn btn-gold btn-sm" onclick="openAddModal()">
          <span>+ Add Character</span>
        </button>

        <a href="/?format=json" class="btn btn-secondary btn-sm" title="Lihat output metadata JSON asli">
          <span>JSON API</span>
        </a>
      </div>
    </div>
  </nav>

  <!-- Navigation Tabs -->
  <div class="tabs-bar">
    <div class="container">
      <ul class="tabs-list">
        <li class="tab-item active" onclick="switchTab('characters', this)">
          <span>✦ Characters</span>
          <span class="tab-badge" id="badge-characters">...</span>
        </li>
        <li class="tab-item" onclick="switchTab('teams', this)">
          <span>⚔ Party Teams</span>
          <span class="tab-badge" id="badge-teams">...</span>
        </li>
        <li class="tab-item" onclick="switchTab('weapons', this)">
          <span>🗡 Weapons Catalog</span>
          <span class="tab-badge" id="badge-weapons">...</span>
        </li>
        <li class="tab-item" onclick="switchTab('explorer', this)">
          <span>⚡ API Explorer & Docs</span>
        </li>
      </ul>
    </div>
  </div>

  <!-- Main Body Content -->
  <main class="container">
    
    <!-- Hero Banner -->
    <section class="hero">
      <div class="hero-info">
        <h1>Gacha Character & Team Builder Dashboard</h1>
        <p>
          Platform RESTful API berkinerja tinggi untuk manajemen karakter gacha, master data elemen & senjata,
          serta formasi party tim pemain. Terhubung langsung ke live database PostgreSQL Supabase & Vercel WSGI.
        </p>
      </div>
      <div class="hero-stats">
        <div class="hero-stat-card">
          <div class="hero-stat-value" id="stat-total-chars">-</div>
          <div class="hero-stat-label">Characters</div>
        </div>
        <div class="hero-stat-card">
          <div class="hero-stat-value" id="stat-5star-chars">-</div>
          <div class="hero-stat-label">5★ Legend</div>
        </div>
        <div class="hero-stat-card">
          <div class="hero-stat-value" id="stat-total-teams">-</div>
          <div class="hero-stat-label">Active Teams</div>
        </div>
      </div>
    </section>

    <!-- TAB 1: CHARACTERS -->
    <div id="tab-characters" class="tab-content">
      <!-- Search & Controls -->
      <div class="controls-wrapper">
        <div class="controls-row-top">
          <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="search-input" class="search-input" placeholder="Search character by name (e.g. Hu Tao, Furina)..." oninput="debounceFetchCharacters()">
          </div>

          <select id="filter-rarity" class="filter-select" onchange="fetchCharacters()">
            <option value="">All Rarities</option>
            <option value="5">5★ Legendary</option>
            <option value="4">4★ Epic</option>
          </select>

          <select id="filter-role" class="filter-select" onchange="fetchCharacters()">
            <option value="">All Roles</option>
            <option value="Main DPS">Main DPS</option>
            <option value="Sub DPS">Sub DPS</option>
            <option value="Support">Support</option>
            <option value="Healer">Healer</option>
            <option value="Shielder">Shielder</option>
          </select>

          <select id="filter-weapon" class="filter-select" onchange="fetchCharacters()">
            <option value="">All Weapons</option>
            <option value="Sword">Sword</option>
            <option value="Claymore">Claymore</option>
            <option value="Polearm">Polearm</option>
            <option value="Bow">Bow</option>
            <option value="Catalyst">Catalyst</option>
          </select>

          <select id="sort-by" class="filter-select" onchange="fetchCharacters()">
            <option value="id-asc">Sort: ID (Asc)</option>
            <option value="nama_karakter-asc">Sort: Name (A-Z)</option>
            <option value="rarity-desc">Sort: Rarity (High-Low)</option>
            <option value="base_atk-desc">Sort: Highest Base ATK</option>
            <option value="base_hp-desc">Sort: Highest Base HP</option>
            <option value="base_def-desc">Sort: Highest Base DEF</option>
          </select>
        </div>

        <!-- Elements Row -->
        <div class="element-filters" id="element-filters">
          <button class="element-btn active" data-element="" onclick="filterByElement('', this)">
            All Elements
          </button>
          <!-- Dynamic element buttons injected here -->
        </div>
      </div>

      <!-- Character Card Grid -->
      <div id="characters-grid" class="grid-characters">
        <div class="state-message">
          <div class="spinner"></div>
          <p>Memuat katalog karakter dari API...</p>
        </div>
      </div>
    </div>

    <!-- TAB 2: TEAMS -->
    <div id="tab-teams" class="tab-content" style="display: none;">
      <div id="teams-container" class="teams-list">
        <div class="state-message">
          <div class="spinner"></div>
          <p>Memuat formasi party tim dari API...</p>
        </div>
      </div>
    </div>

    <!-- TAB 3: WEAPONS -->
    <div id="tab-weapons" class="tab-content" style="display: none;">
      <div id="weapons-container" class="weapons-grid">
        <div class="state-message">
          <div class="spinner"></div>
          <p>Memuat katalog senjata master...</p>
        </div>
      </div>
    </div>

    <!-- TAB 4: API EXPLORER -->
    <div id="tab-explorer" class="tab-content" style="display: none;">
      <div class="api-explorer-card">
        <h2 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem;">REST API Endpoints Specification</h2>
        <p style="color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1.5rem;">
          Semua endpoint mengembalikan respon JSON terstruktur dengan standar status code HTTP (200, 201, 400, 404, 405, 409, 500).
        </p>

        <div class="endpoint-row">
          <span class="method-badge method-get">GET</span>
          <span class="endpoint-path">/</span>
          <span class="endpoint-desc">Katalog informasi REST API & navigasi metadata JSON / HTML Web UI.</span>
          <a href="/?format=json" target="_blank" class="btn btn-secondary btn-sm">Test JSON</a>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-get">GET</span>
          <span class="endpoint-path">/api/health</span>
          <span class="endpoint-desc">Pemeriksaan uptime server & ping konektivitas live database Supabase.</span>
          <a href="/api/health" target="_blank" class="btn btn-secondary btn-sm">Test</a>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-get">GET</span>
          <span class="endpoint-path">/api/characters</span>
          <span class="endpoint-desc">List karakter dengan query filter (?element, ?rarity, ?weapon_type, ?role, ?sort_by).</span>
          <a href="/api/characters" target="_blank" class="btn btn-secondary btn-sm">Test</a>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-get">GET</span>
          <span class="endpoint-path">/api/characters/&lt;id&gt;</span>
          <span class="endpoint-desc">Detail spesifik satu karakter beserta relasi elemental & skill/talents.</span>
          <a href="/api/characters/1" target="_blank" class="btn btn-secondary btn-sm">Test #1</a>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-post">POST</span>
          <span class="endpoint-path">/api/characters</span>
          <span class="endpoint-desc">Menambahkan karakter baru dengan validasi ketat constraint skema database.</span>
          <button class="btn btn-gold btn-sm" onclick="openAddModal()">Buka Form</button>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-put">PUT</span>
          <span class="endpoint-path">/api/characters/&lt;id&gt;</span>
          <span class="endpoint-desc">Memperbarui satu atau beberapa field atribut karakter (nama, stat, role, dll).</span>
          <span class="tag-pill">Gunakan Tombol Edit di Card</span>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-delete">DELETE</span>
          <span class="endpoint-path">/api/characters/&lt;id&gt;</span>
          <span class="endpoint-desc">Menghapus karakter (dilindungi proteksi Foreign Key Integrity 409 Conflict).</span>
          <span class="tag-pill">Protected FK</span>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-get">GET</span>
          <span class="endpoint-path">/api/teams</span>
          <span class="endpoint-desc">Formasi tim pemain dari view database v_party_team_details.</span>
          <a href="/api/teams" target="_blank" class="btn btn-secondary btn-sm">Test</a>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-get">GET</span>
          <span class="endpoint-path">/api/elements</span>
          <span class="endpoint-desc">Daftar 7 master element (Pyro, Hydro, Anemo, Electro, Dendro, Cryo, Geo).</span>
          <a href="/api/elements" target="_blank" class="btn btn-secondary btn-sm">Test</a>
        </div>

        <div class="endpoint-row">
          <span class="method-badge method-get">GET</span>
          <span class="endpoint-path">/api/weapons</span>
          <span class="endpoint-desc">Master katalog senjata dengan filter tipe, rarity, dan search.</span>
          <a href="/api/weapons" target="_blank" class="btn btn-secondary btn-sm">Test</a>
        </div>
      </div>
    </div>

  </main>

  <!-- MODAL: ADD / EDIT CHARACTER -->
  <div id="character-modal" class="modal-overlay">
    <div class="modal-window">
      <div class="modal-header">
        <div class="modal-title" id="modal-title">Tambah Karakter Baru</div>
        <button class="modal-close" onclick="closeModal('character-modal')">&times;</button>
      </div>
      <form id="character-form" onsubmit="handleCharacterSubmit(event)">
        <input type="hidden" id="char-id">
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label" for="char-name">Nama Karakter *</label>
            <input type="text" id="char-name" class="form-input" placeholder="e.g. Mavuika, Arlecchino" required maxlength="100">
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="char-element">Elemen Master *</label>
              <select id="char-element" class="form-select" required>
                <!-- Populated via API elements -->
              </select>
            </div>
            <div class="form-group">
              <label class="form-label" for="char-rarity">Rarity *</label>
              <select id="char-rarity" class="form-select" required>
                <option value="5">5★ Legendary</option>
                <option value="4">4★ Epic</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="char-weapon">Tipe Senjata *</label>
              <select id="char-weapon" class="form-select" required>
                <option value="Sword">Sword</option>
                <option value="Claymore">Claymore</option>
                <option value="Polearm">Polearm</option>
                <option value="Bow">Bow</option>
                <option value="Catalyst">Catalyst</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label" for="char-role">Role Utama *</label>
              <select id="char-role" class="form-select" required>
                <option value="Main DPS">Main DPS</option>
                <option value="Sub DPS">Sub DPS</option>
                <option value="Support">Support</option>
                <option value="Healer">Healer</option>
                <option value="Shielder">Shielder</option>
              </select>
            </div>
          </div>

          <div class="form-row-3">
            <div class="form-group">
              <label class="form-label" for="char-hp">Base HP *</label>
              <input type="number" id="char-hp" class="form-input" placeholder="15000" min="1" required>
            </div>
            <div class="form-group">
              <label class="form-label" for="char-atk">Base ATK *</label>
              <input type="number" id="char-atk" class="form-input" placeholder="250" min="1" required>
            </div>
            <div class="form-group">
              <label class="form-label" for="char-def">Base DEF *</label>
              <input type="number" id="char-def" class="form-input" placeholder="750" min="1" required>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="char-ascension">Ascension Stat *</label>
            <input type="text" id="char-ascension" class="form-input" placeholder="e.g. CRIT DMG, Energy Recharge" required maxlength="50">
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="closeModal('character-modal')">Batal</button>
          <button type="submit" id="submit-btn" class="btn btn-primary">Simpan Karakter</button>
        </div>
      </form>
    </div>
  </div>

  <!-- MODAL: CHARACTER DETAIL & SKILLS -->
  <div id="detail-modal" class="modal-overlay">
    <div class="modal-window">
      <div class="modal-header">
        <div class="modal-title" id="detail-title">Detail Karakter</div>
        <button class="modal-close" onclick="closeModal('detail-modal')">&times;</button>
      </div>
      <div class="modal-body" id="detail-body">
        <div class="state-message">
          <div class="spinner"></div>
          <p>Mengambil detail talenta karakter...</p>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" onclick="closeModal('detail-modal')">Tutup</button>
      </div>
    </div>
  </div>

  <!-- Toast Notification Hub -->
  <div class="toast-container" id="toast-container"></div>

  <!-- Footer -->
  <footer>
    <div class="container footer-inner">
      <div>
        <span>Gacha Character & Team Builder REST API &bull; Muhammad Izzul Islam (lunizura)</span>
      </div>
      <div class="footer-links">
        <a href="https://github.com/lunizura/gacha-builder-api-learninglabs" target="_blank" rel="noopener">GitHub</a>
        <a href="/api/health" target="_blank">Health Check</a>
        <a href="/?format=json" target="_blank">REST API Catalog</a>
        <a href="https://github.com/lunizura/gacha-builder-api-learninglabs/blob/main/postman_collection.json" target="_blank" rel="noopener">Postman Collection</a>
      </div>
    </div>
  </footer>

  <!-- Single Page Application Logic -->
  <script>
    // State Aplikasi
    let elementsList = [];
    let charactersCache = new Map();
    let currentSelectedElement = "";
    let debounceTimer = null;
    let healthInterval = null;

    // Element Color Map Fallback
    const ELEMENT_COLORS = {
      'Pyro': '#ef4444',
      'Hydro': '#38bdf8',
      'Anemo': '#2dd4bf',
      'Electro': '#c084fc',
      'Dendro': '#4ade80',
      'Cryo': '#bae6fd',
      'Geo': '#fbbf24'
    };

    // Helper: Escape HTML string to prevent XSS
    function escapeHtml(str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    // Helper: Toast Notifications
    function showToast(message, type = 'success') {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      toast.className = `toast ${type}`;
      toast.innerHTML = `<span>${type === 'success' ? '✓' : '⚠'}</span> <span>${escapeHtml(message)}</span>`;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }

    // Modal Handlers
    function openModal(id) {
      const modal = document.getElementById(id);
      if (modal) {
        modal.classList.add('open');
        const firstInput = modal.querySelector('input:not([type=hidden]), select');
        if (firstInput) setTimeout(() => firstInput.focus(), 50);
      }
    }

    function closeModal(id) {
      const modal = document.getElementById(id);
      if (modal) modal.classList.remove('open');
    }

    // Close modal on background click
    window.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('open');
      }
    });

    // Close modal on ESC key
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
      }
    });

    // Switch Tabs
    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-item').forEach(item => item.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.style.display = 'none');

      if (el) el.classList.add('active');
      const target = document.getElementById(`tab-${tabId}`);
      if (target) target.style.display = 'block';

      if (tabId === 'teams') fetchTeams();
      if (tabId === 'weapons') fetchWeapons();
    }

    // 1. Fetch Health Status
    async function checkHealth() {
      const pill = document.getElementById('health-status');
      const text = document.getElementById('health-text');
      try {
        const res = await fetch('/api/health');
        const data = await res.json();
        if (data.status === 'healthy') {
          pill.className = 'health-pill';
          const lat = data.database?.latency_ms ? `${data.database.latency_ms}ms` : 'active';
          text.textContent = `Online • ${data.database?.provider || 'PostgreSQL'} (${lat})`;
        } else {
          pill.className = 'health-pill degraded';
          text.textContent = `Degraded • ${data.database?.error || 'Database Offline'}`;
        }
      } catch (err) {
        pill.className = 'health-pill degraded';
        text.textContent = 'Offline';
      }
    }

    // 2. Fetch Master Elements
    async function fetchElements() {
      try {
        const res = await fetch('/api/elements');
        const json = await res.json();
        if (json.status === 'success') {
          elementsList = json.data;
          renderElementFilters();
          renderElementDropdown();
        }
      } catch (err) {
        console.error('Error fetching elements:', err);
      }
    }

    function renderElementFilters() {
      const container = document.getElementById('element-filters');
      container.innerHTML = `
        <button class="element-btn ${currentSelectedElement === '' ? 'active' : ''}" onclick="filterByElement('', this)">
          All Elements
        </button>
      `;

      elementsList.forEach(el => {
        const btn = document.createElement('button');
        btn.className = `element-btn ${currentSelectedElement === el.nama_elemen ? 'active' : ''}`;
        const color = el.warna_hex || ELEMENT_COLORS[el.nama_elemen] || '#94a3b8';
        btn.innerHTML = `<span class="element-dot" style="background-color: ${color};"></span> ${escapeHtml(el.nama_elemen)}`;
        btn.onclick = () => filterByElement(el.nama_elemen, btn);
        container.appendChild(btn);
      });
    }

    function renderElementDropdown() {
      const select = document.getElementById('char-element');
      select.innerHTML = '<option value="">-- Pilih Elemen --</option>';
      elementsList.forEach(el => {
        const opt = document.createElement('option');
        opt.value = el.id;
        opt.textContent = `${el.nama_elemen} (${el.reaksi_efek || 'Elemental'})`;
        select.appendChild(opt);
      });
    }

    function filterByElement(elementName, btn) {
      currentSelectedElement = elementName;
      document.querySelectorAll('.element-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      fetchCharacters();
    }

    function debounceFetchCharacters() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(fetchCharacters, 250);
    }

    // 3. Fetch Characters with query parameters
    async function fetchCharacters() {
      const grid = document.getElementById('characters-grid');
      const search = document.getElementById('search-input').value.trim();
      const rarity = document.getElementById('filter-rarity').value;
      const role = document.getElementById('filter-role').value;
      const weapon = document.getElementById('filter-weapon').value;
      const sortVal = document.getElementById('sort-by').value.split('-');
      const sortBy = sortVal[0] || 'id';
      const order = sortVal[1] || 'asc';

      const params = new URLSearchParams();
      if (currentSelectedElement) params.append('element', currentSelectedElement);
      if (rarity) params.append('rarity', rarity);
      if (role) params.append('role', role);
      if (weapon) params.append('weapon_type', weapon);
      if (search) params.append('search', search);
      params.append('sort_by', sortBy);
      params.append('order', order);

      try {
        const res = await fetch(`/api/characters?${params.toString()}`);
        const json = await res.json();

        if (json.status !== 'success') {
          grid.innerHTML = `<div class="state-message"><p style="color:var(--danger)">${escapeHtml(json.message)}</p></div>`;
          return;
        }

        const characters = json.data || [];
        charactersCache.clear();
        characters.forEach(char => charactersCache.set(char.id, char));

        document.getElementById('badge-characters').textContent = json.total;
        document.getElementById('stat-total-chars').textContent = json.total;

        // Count 5-stars
        const fiveStars = characters.filter(c => c.rarity === 5).length;
        document.getElementById('stat-5star-chars').textContent = fiveStars;

        if (characters.length === 0) {
          grid.innerHTML = `
            <div class="state-message" style="grid-column: 1 / -1;">
              <p>Tidak ada karakter yang cocok dengan kriteria filter.</p>
              <button class="btn btn-secondary btn-sm" style="margin-top: 0.75rem;" onclick="resetFilters()">Reset Filter</button>
            </div>
          `;
          return;
        }

        grid.innerHTML = characters.map(char => {
          const elColor = char.warna_hex || ELEMENT_COLORS[char.nama_elemen] || '#94a3b8';
          const stars = '★'.repeat(char.rarity);
          return `
            <div class="char-card rarity-${char.rarity}">
              <div class="char-header">
                <div class="char-name-group">
                  <div class="char-name">
                    <span>${escapeHtml(char.nama_karakter)}</span>
                  </div>
                  <div class="char-stars">${stars}</div>
                </div>
                <span class="element-badge" style="background: ${elColor}22; color: ${elColor}; border: 1px solid ${elColor}55;">
                  <span class="element-dot" style="background-color: ${elColor};"></span>
                  ${escapeHtml(char.nama_elemen)}
                </span>
              </div>

              <div class="char-tags">
                <span class="tag-pill">🗡 ${escapeHtml(char.tipe_senjata)}</span>
                <span class="tag-pill">🎯 ${escapeHtml(char.role_utama)}</span>
              </div>

              <div class="char-stats-table">
                <div class="stat-item">
                  <span class="stat-label">Base HP</span>
                  <span class="stat-val">${(Number(char.base_hp) || 0).toLocaleString()}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Base ATK</span>
                  <span class="stat-val">${(Number(char.base_atk) || 0).toLocaleString()}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Base DEF</span>
                  <span class="stat-val">${(Number(char.base_def) || 0).toLocaleString()}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Ascension</span>
                  <span class="stat-val ascension">${escapeHtml(char.ascension_stat)}</span>
                </div>
              </div>

              <div class="char-footer">
                <button class="btn btn-secondary btn-sm" style="flex:1" onclick="viewCharacterDetail(${char.id})">
                  ✦ Skills & Detail
                </button>
                <button class="btn btn-secondary btn-sm" title="Edit Karakter" onclick="openEditModal(${char.id})">
                  ✏
                </button>
                <button class="btn btn-danger btn-sm" title="Hapus Karakter" onclick="deleteCharacter(${char.id})">
                  🗑
                </button>
              </div>
            </div>
          `;
        }).join('');

      } catch (err) {
        grid.innerHTML = `<div class="state-message"><p style="color:var(--danger)">Gagal terhubung ke API: ${escapeHtml(err.message)}</p></div>`;
      }
    }

    function resetFilters() {
      document.getElementById('search-input').value = '';
      document.getElementById('filter-rarity').value = '';
      document.getElementById('filter-role').value = '';
      document.getElementById('filter-weapon').value = '';
      document.getElementById('sort-by').value = 'id-asc';
      filterByElement('', document.querySelector('.element-btn'));
    }

    // 4. View Character Detail & Skills Modal
    async function viewCharacterDetail(id) {
      openModal('detail-modal');
      const body = document.getElementById('detail-body');
      const title = document.getElementById('detail-title');
      body.innerHTML = '<div class="state-message"><div class="spinner"></div><p>Memuat rincian talenta dari API...</p></div>';

      try {
        const res = await fetch(`/api/characters/${id}`);
        const json = await res.json();
        if (json.status !== 'success') {
          body.innerHTML = `<p style="color:var(--danger)">${escapeHtml(json.message)}</p>`;
          return;
        }

        const char = json.data;
        const elColor = char.warna_hex || ELEMENT_COLORS[char.nama_elemen] || '#94a3b8';
        title.innerHTML = `${escapeHtml(char.nama_karakter)} <span style="font-size:0.85rem; color:${elColor}">[${escapeHtml(char.nama_elemen)}]</span>`;

        let skillsHtml = '';
        if (char.skills && char.skills.length > 0) {
          skillsHtml = char.skills.map(skill => `
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:var(--radius-sm); padding:0.85rem; margin-top:0.65rem;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.25rem;">
                <strong style="color:var(--text-main); font-size:0.95rem;">${escapeHtml(skill.nama_talent)}</strong>
                <span class="tag-pill" style="color:var(--primary);">${escapeHtml(skill.tipe_talent)}</span>
              </div>
              <p style="font-size:0.8rem; color:var(--text-dim); line-height:1.45; margin-bottom:0.4rem;">${escapeHtml(skill.deskripsi)}</p>
              <div style="display:flex; gap:1rem; font-size:0.75rem; color:var(--text-muted);">
                ${(skill.cooldown_seconds !== null && skill.cooldown_seconds !== undefined) ? `<span>⏱ Cooldown: <strong>${skill.cooldown_seconds}s</strong></span>` : ''}
                ${(skill.energy_cost !== null && skill.energy_cost !== undefined) ? `<span>⚡ Energy Cost: <strong>${skill.energy_cost}</strong></span>` : ''}
              </div>
            </div>
          `).join('');
        } else {
          skillsHtml = '<p style="color:var(--text-muted); font-size:0.825rem; margin-top:0.5rem;">Tidak ada skill aktif yang terdaftar untuk karakter ini.</p>';
        }

        body.innerHTML = `
          <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; background:rgba(10,14,23,0.5); padding:1rem; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); font-size:0.85rem;">
            <div><span style="color:var(--text-muted);">Tipe Senjata:</span> <strong>${escapeHtml(char.tipe_senjata)}</strong></div>
            <div><span style="color:var(--text-muted);">Role Utama:</span> <strong>${escapeHtml(char.role_utama)}</strong></div>
            <div><span style="color:var(--text-muted);">Base HP:</span> <strong>${(Number(char.base_hp) || 0).toLocaleString()}</strong></div>
            <div><span style="color:var(--text-muted);">Base ATK:</span> <strong>${(Number(char.base_atk) || 0).toLocaleString()}</strong></div>
            <div><span style="color:var(--text-muted);">Base DEF:</span> <strong>${(Number(char.base_def) || 0).toLocaleString()}</strong></div>
            <div><span style="color:var(--text-muted);">Ascension Stat:</span> <strong style="color:var(--primary)">${escapeHtml(char.ascension_stat)}</strong></div>
            <div style="grid-column: 1 / -1;"><span style="color:var(--text-muted);">Efek Reaksi Elemen:</span> <em>${escapeHtml(char.reaksi_efek || '-')}</em></div>
          </div>
          <div style="margin-top:1rem;">
            <h4 style="font-size:0.95rem; font-weight:700; color:var(--text-main); margin-bottom:0.25rem;">Talenta & Skill Terdaftar</h4>
            ${skillsHtml}
          </div>
        `;

      } catch (err) {
        body.innerHTML = `<p style="color:var(--danger)">Gagal mengambil detail karakter: ${escapeHtml(err.message)}</p>`;
      }
    }

    // 5. Add / Edit Character Modal
    function openAddModal() {
      const form = document.getElementById('character-form');
      if (form) form.reset();
      document.getElementById('modal-title').textContent = 'Tambah Karakter Baru';
      document.getElementById('char-id').value = '';
      document.getElementById('char-name').value = '';
      document.getElementById('char-element').value = elementsList[0]?.id || 1;
      document.getElementById('char-rarity').value = '5';
      document.getElementById('char-weapon').value = 'Sword';
      document.getElementById('char-role').value = 'Main DPS';
      document.getElementById('char-hp').value = '15000';
      document.getElementById('char-atk').value = '250';
      document.getElementById('char-def').value = '750';
      document.getElementById('char-ascension').value = 'CRIT DMG';
      document.getElementById('submit-btn').textContent = 'Simpan Karakter (POST)';
      openModal('character-modal');
    }

    function openEditModal(id) {
      const char = charactersCache.get(id);
      if (!char) return;
      document.getElementById('modal-title').textContent = `Edit Karakter: ${char.nama_karakter}`;
      document.getElementById('char-id').value = char.id;
      document.getElementById('char-name').value = char.nama_karakter;
      document.getElementById('char-element').value = char.id_elemen;
      document.getElementById('char-rarity').value = char.rarity;
      document.getElementById('char-weapon').value = char.tipe_senjata;
      document.getElementById('char-role').value = char.role_utama;
      document.getElementById('char-hp').value = char.base_hp;
      document.getElementById('char-atk').value = char.base_atk;
      document.getElementById('char-def').value = char.base_def;
      document.getElementById('char-ascension').value = char.ascension_stat;
      document.getElementById('submit-btn').textContent = 'Perbarui Karakter (PUT)';
      openModal('character-modal');
    }

    async function handleCharacterSubmit(e) {
      e.preventDefault();
      const submitBtn = document.getElementById('submit-btn');
      const charId = document.getElementById('char-id').value;
      const isEdit = Boolean(charId);

      const payload = {
        nama_karakter: document.getElementById('char-name').value.trim(),
        id_elemen: parseInt(document.getElementById('char-element').value, 10),
        rarity: parseInt(document.getElementById('char-rarity').value, 10),
        tipe_senjata: document.getElementById('char-weapon').value,
        role_utama: document.getElementById('char-role').value,
        base_hp: parseInt(document.getElementById('char-hp').value, 10),
        base_atk: parseInt(document.getElementById('char-atk').value, 10),
        base_def: parseInt(document.getElementById('char-def').value, 10),
        ascension_stat: document.getElementById('char-ascension').value.trim()
      };

      submitBtn.disabled = true;
      submitBtn.textContent = 'Memproses...';

      try {
        const url = isEdit ? `/api/characters/${charId}` : '/api/characters';
        const method = isEdit ? 'PUT' : 'POST';

        const res = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const json = await res.json();
        if (res.ok && json.status === 'success') {
          showToast(json.message, 'success');
          closeModal('character-modal');
          fetchCharacters();
        } else {
          const errMsg = json.errors ? json.errors.join(', ') : json.message;
          showToast(`Gagal: ${errMsg}`, 'error');
        }
      } catch (err) {
        showToast(`Koneksi error: ${err.message}`, 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = isEdit ? 'Perbarui Karakter (PUT)' : 'Simpan Karakter (POST)';
      }
    }

    // 6. Delete Character
    async function deleteCharacter(id) {
      const char = charactersCache.get(id);
      const name = char ? char.nama_karakter : `ID #${id}`;
      if (!confirm(`Apakah Anda yakin ingin menghapus karakter '${name}' (ID: ${id})?\\n\\nCatatan: Karakter yang terikat pada inventori pemain akan ditolak oleh Foreign Key constraint (409 Conflict).`)) {
        return;
      }

      try {
        const res = await fetch(`/api/characters/${id}`, {
          method: 'DELETE',
          headers: { 'Accept': 'application/json' }
        });
        const json = await res.json();

        if (res.status === 200) {
          showToast(json.message, 'success');
          fetchCharacters();
        } else if (res.status === 409) {
          // Foreign Key Violation
          alert(`[409 CONFLICT: FOREIGN KEY PROTECTION]\\n\\n${json.message}`);
          showToast('Penghapusan ditolak: Terikat inventori pemain', 'error');
        } else {
          showToast(`Error: ${json.message}`, 'error');
        }
      } catch (err) {
        showToast(`Gagal menghapus: ${err.message}`, 'error');
      }
    }

    // 7. Fetch Party Teams
    async function fetchTeams() {
      const container = document.getElementById('teams-container');
      try {
        const res = await fetch('/api/teams');
        const json = await res.json();
        if (json.status !== 'success') {
          container.innerHTML = `<div class="state-message"><p style="color:var(--danger)">${escapeHtml(json.message)}</p></div>`;
          return;
        }

        const teams = json.data || [];
        document.getElementById('badge-teams').textContent = json.total_teams;
        document.getElementById('stat-total-teams').textContent = json.total_teams;

        if (teams.length === 0) {
          container.innerHTML = '<div class="state-message"><p>Belum ada formasi party tim terdaftar.</p></div>';
          return;
        }

        container.innerHTML = teams.map(team => `
          <div class="team-card">
            <div class="team-header">
              <div>
                <div class="team-title">⚔ ${escapeHtml(team.nama_party)}</div>
                <div class="team-owner">Player: <strong>${escapeHtml(team.username)}</strong> &bull; UID: <code>${escapeHtml(team.in_game_uid)}</code></div>
              </div>
              <span class="tag-pill" style="color:var(--primary); font-weight:700;">${team.members.length} Anggota</span>
            </div>
            <div class="team-members-grid">
              ${team.members.map(m => {
                const elColor = ELEMENT_COLORS[m.nama_elemen] || '#94a3b8';
                return `
                  <div class="member-slot">
                    <span class="slot-num">${m.slot_position}</span>
                    <div class="member-name">
                      <span class="element-dot" style="background-color: ${elColor};"></span>
                      ${escapeHtml(m.nama_karakter)}
                    </div>
                    <div class="member-meta">
                      <div>Level: <strong>Lv. ${m.character_level}</strong> (C${m.constellation_level})</div>
                      <div>Weapon: <em>${escapeHtml(m.nama_senjata || 'None')}</em></div>
                      <div>Role: <span style="color:var(--text-main); font-weight:600;">${escapeHtml(m.role_dalam_party)}</span></div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `).join('');

      } catch (err) {
        container.innerHTML = `<div class="state-message"><p style="color:var(--danger)">Gagal memuat formasi tim: ${escapeHtml(err.message)}</p></div>`;
      }
    }

    // 8. Fetch Weapons Catalog
    async function fetchWeapons() {
      const container = document.getElementById('weapons-container');
      try {
        const res = await fetch('/api/weapons');
        const json = await res.json();
        if (json.status !== 'success') {
          container.innerHTML = `<div class="state-message"><p style="color:var(--danger)">${escapeHtml(json.message)}</p></div>`;
          return;
        }

        const weapons = json.data || [];
        document.getElementById('badge-weapons').textContent = json.total;

        container.innerHTML = weapons.map(w => {
          const stars = '★'.repeat(w.rarity);
          const substatDisplay = w.substat_type === 'Elemental Mastery' ? w.substat_value : `${w.substat_value}%`;
          return `
            <div class="weapon-card rarity-${w.rarity}">
              <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                  <div class="weapon-name">${escapeHtml(w.nama_senjata)}</div>
                  <div class="char-stars">${stars}</div>
                </div>
                <span class="tag-pill">${escapeHtml(w.tipe_senjata)}</span>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:0.8rem; background:rgba(10,14,23,0.5); padding:0.4rem 0.65rem; border-radius:var(--radius-sm);">
                <span>Base ATK: <strong>${w.base_atk}</strong></span>
                <span>${escapeHtml(w.substat_type)}: <strong style="color:var(--primary)">${substatDisplay}</strong></span>
              </div>
              <div class="weapon-desc">${escapeHtml(w.pasif_deskripsi)}</div>
            </div>
          `;
        }).join('');

      } catch (err) {
        container.innerHTML = `<div class="state-message"><p style="color:var(--danger)">Gagal memuat data senjata: ${escapeHtml(err.message)}</p></div>`;
      }
    }

    // Initial Load
    document.addEventListener('DOMContentLoaded', () => {
      checkHealth();
      fetchElements();
      fetchCharacters();
      fetchTeams();
      fetchWeapons();

      // Live monitoring health ping every 30 seconds
      if (healthInterval) clearInterval(healthInterval);
      healthInterval = setInterval(checkHealth, 30000);
    });
  </script>
</body>
</html>
"""
