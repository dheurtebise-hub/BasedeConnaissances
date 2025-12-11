/**
 * KB Support Basedoc - Main JavaScript
 */

// ========== Categories Tree Sidebar ==========

// Charger l'arborescence des catégories
function loadCategoriesTree() {
    fetch('/api/categories/tree')
        .then(response => response.json())
        .then(categories => {
            const container = document.getElementById('categoriesTree');
            if (container) {
                container.innerHTML = renderCategoriesTree(categories);
                attachCategoryToggleListeners();
            }
        })
        .catch(error => console.error('Error loading categories:', error));
}

// Rendre l'arborescence HTML
function renderCategoriesTree(categories, level = 0) {
    let html = '';

    categories.forEach(category => {
        const hasChildren = category.children && category.children.length > 0;
        const colorStyle = `background-color: ${category.color_code}`;

        html += `<div class="category-item">`;

        if (hasChildren) {
            html += `
                <div class="category-link category-parent" data-category-id="${category.id}">
                    <span class="category-expand">▸</span>
                    <span class="category-color" style="${colorStyle}"></span>
                    <span class="category-name">${category.name}</span>
                </div>
                <div class="subcategories" style="display: none;">
                    ${renderCategoriesTree(category.children, level + 1)}
                </div>
            `;
        } else {
            html += `
                <a href="/procedures/list?category=${category.id}" class="category-link">
                    <span class="category-color" style="${colorStyle}"></span>
                    <span class="category-name">${category.name}</span>
                    <span class="category-short">${category.short_name}</span>
                </a>
            `;
        }

        html += `</div>`;
    });

    return html;
}

// Attacher les événements de toggle
function attachCategoryToggleListeners() {
    document.querySelectorAll('.category-parent').forEach(parent => {
        parent.addEventListener('click', function() {
            const subcategories = this.nextElementSibling;
            const expandIcon = this.querySelector('.category-expand');

            if (subcategories.style.display === 'none') {
                subcategories.style.display = 'block';
                expandIcon.classList.add('expanded');
            } else {
                subcategories.style.display = 'none';
                expandIcon.classList.remove('expanded');
            }
        });
    });
}

// ========== Search Auto-completion ==========

let searchTimeout;
let suggestionsContainer;

function initSearchAutocomplete() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    // Créer le conteneur de suggestions
    suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions';
    suggestionsContainer.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background-color: #374151;
        border: 1px solid #4b5563;
        border-radius: 4px;
        margin-top: 4px;
        max-height: 400px;
        overflow-y: auto;
        display: none;
        z-index: 1000;
    `;

    searchInput.parentElement.style.position = 'relative';
    searchInput.parentElement.appendChild(suggestionsContainer);

    // Événement input
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value;

        clearTimeout(searchTimeout);

        if (query.length < 3) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(() => {
            fetchSearchSuggestions(query);
        }, 300);
    });

    // Fermer les suggestions au clic extérieur
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.style.display = 'none';
        }
    });

    // Soumettre la recherche avec Enter
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = e.target.value;
            if (query.length >= 3) {
                window.location.href = `/search?q=${encodeURIComponent(query)}`;
            }
        }
    });
}

function fetchSearchSuggestions(query) {
    fetch(`/search/suggestions?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(suggestions => {
            displaySearchSuggestions(suggestions);
        })
        .catch(error => console.error('Error fetching suggestions:', error));
}

function displaySearchSuggestions(suggestions) {
    if (suggestions.length === 0) {
        suggestionsContainer.style.display = 'none';
        return;
    }

    let html = '';

    suggestions.forEach(suggestion => {
        html += `
            <a href="/procedures/${suggestion.id}" class="suggestion-item" style="
                display: block;
                padding: 12px 16px;
                color: #f9fafb;
                text-decoration: none;
                border-bottom: 1px solid #4b5563;
                transition: background-color 0.2s;
            " onmouseover="this.style.backgroundColor='#4b5563'" onmouseout="this.style.backgroundColor='transparent'">
                <div style="font-weight: 600; margin-bottom: 4px;">${suggestion.title}</div>
                <div style="font-size: 0.75rem; color: #9ca3af;">
                    <span style="color: #06b6d4;">${suggestion.category}</span>
                    ${suggestion.description ? ' • ' + suggestion.description.substring(0, 80) : ''}
                </div>
            </a>
        `;
    });

    suggestionsContainer.innerHTML = html;
    suggestionsContainer.style.display = 'block';
}

// ========== Flash Messages Auto-dismiss ==========

function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(message => {
        // Auto-dismiss après 5 secondes
        setTimeout(() => {
            message.style.transition = 'opacity 0.3s';
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}

// ========== Confirmation Dialogs ==========

function initConfirmDialogs() {
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// ========== Markdown Preview (pour l'éditeur) ==========

function initMarkdownPreview() {
    const contentTextarea = document.getElementById('content');
    const previewButton = document.getElementById('previewButton');

    if (previewButton && contentTextarea) {
        previewButton.addEventListener('click', function() {
            const content = contentTextarea.value;

            // Simple conversion markdown vers HTML (basique)
            const html = simpleMarkdownToHtml(content);

            // Créer une modal de preview
            showPreviewModal(html);
        });
    }
}

function simpleMarkdownToHtml(markdown) {
    let html = markdown;

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Code blocks
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

    // Inline code
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');

    // Links
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');

    // Lists
    html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Line breaks
    html = html.replace(/\n/g, '<br>');

    return html;
}

function showPreviewModal(html) {
    // Créer une modal simple
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        padding: 20px;
    `;

    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background-color: #374151;
        border-radius: 8px;
        padding: 32px;
        max-width: 900px;
        width: 100%;
        max-height: 80vh;
        overflow-y: auto;
    `;

    modalContent.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
            <h2 style="color: #06b6d4; margin: 0;">Aperçu</h2>
            <button onclick="this.closest('.modal').remove()" style="
                background: transparent;
                border: none;
                font-size: 32px;
                color: #9ca3af;
                cursor: pointer;
            ">×</button>
        </div>
        <div class="markdown-content">${html}</div>
    `;

    modal.className = 'modal';
    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Fermer au clic extérieur
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// ========== Initialization ==========

document.addEventListener('DOMContentLoaded', function() {
    loadCategoriesTree();
    initSearchAutocomplete();
    initFlashMessages();
    initConfirmDialogs();
    initMarkdownPreview();

    console.log('KB Support Basedoc initialized');
});
