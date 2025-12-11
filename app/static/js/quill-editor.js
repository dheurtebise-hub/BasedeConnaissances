/**
 * Quill WYSIWYG Editor Configuration
 * Supports: clipboard image paste, Word/PDF paste, drag & drop
 */

// Global Quill instance (accessible from other scripts)
window.quillInstance = null;

function initQuillEditor() {
    const editorContainer = document.getElementById('quill-editor');
    const hiddenTextarea = document.getElementById('content');

    if (!editorContainer || !hiddenTextarea) {
        console.error('Quill editor container or textarea not found');
        return;
    }

    try {
        // Configuration Quill avec modules étendus
        window.quillInstance = new Quill('#quill-editor', {
            theme: 'snow',
            placeholder: 'Rédigez votre procédure ici... Vous pouvez coller du texte, des images depuis Word/PDF...',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                    [{ 'font': [] }],
                    [{ 'size': ['small', false, 'large', 'huge'] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'script': 'sub'}, { 'script': 'super' }],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'indent': '-1'}, { 'indent': '+1' }],
                    [{ 'align': [] }],
                    ['blockquote', 'code-block'],
                    ['link', 'image'],
                    ['clean']
                ],
                clipboard: {
                    // Permet de coller du HTML/Word avec mise en forme
                    matchVisual: true
                },
                imageResize: {
                    displayStyles: {
                        backgroundColor: 'black',
                        border: 'none',
                        color: 'white'
                    },
                    modules: ['Resize', 'DisplaySize']
                }
            }
        });

        // Charger le contenu initial depuis le textarea caché
        const initialContent = hiddenTextarea.value;
        if (initialContent) {
            window.quillInstance.clipboard.dangerouslyPasteHTML(initialContent);
        }

        // Synchroniser Quill vers textarea caché (pour soumission du formulaire)
        window.quillInstance.on('text-change', function() {
            const html = window.quillInstance.root.innerHTML;
            hiddenTextarea.value = html;
        });

        // Support du copier-coller d'images depuis le presse-papier
        window.quillInstance.root.addEventListener('paste', function(e) {
            if (e.clipboardData && e.clipboardData.items) {
                const items = e.clipboardData.items;

                for (let i = 0; i < items.length; i++) {
                    const item = items[i];

                    // Si c'est une image
                    if (item.type.indexOf('image') !== -1) {
                        e.preventDefault();

                        const blob = item.getAsFile();
                        const reader = new FileReader();

                        reader.onload = function(event) {
                            const base64 = event.target.result;
                            const range = window.quillInstance.getSelection(true);
                            window.quillInstance.insertEmbed(range.index, 'image', base64);
                        };

                        reader.readAsDataURL(blob);
                    }
                }
            }
        });

        // Support du drag & drop d'images
        window.quillInstance.root.addEventListener('drop', function(e) {
            e.preventDefault();

            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length) {
                const files = e.dataTransfer.files;

                for (let i = 0; i < files.length; i++) {
                    const file = files[i];

                    if (file.type.match(/^image\//)) {
                        const reader = new FileReader();

                        reader.onload = function(event) {
                            const base64 = event.target.result;
                            const range = window.quillInstance.getSelection(true);
                            window.quillInstance.insertEmbed(range.index, 'image', base64);
                        };

                        reader.readAsDataURL(file);
                    }
                }
            }
        });

        // Empêcher le comportement par défaut du drag over
        window.quillInstance.root.addEventListener('dragover', function(e) {
            e.preventDefault();
        });

        console.log('✓ Quill editor initialized successfully');

        // Cacher l'indicateur de chargement s'il existe
        const loadingIndicator = document.getElementById('editor-loading');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }

        // Afficher l'éditeur
        editorContainer.style.display = 'block';

    } catch (error) {
        console.error('Failed to initialize Quill editor:', error);

        // Fallback: afficher le textarea brut
        const fallbackTextarea = document.getElementById('content');
        if (fallbackTextarea) {
            fallbackTextarea.style.display = 'block';
            fallbackTextarea.classList.add('form-textarea');
            fallbackTextarea.rows = 20;
        }

        // Cacher le conteneur Quill
        if (editorContainer) {
            editorContainer.style.display = 'none';
        }

        alert('L\'éditeur avancé n\'a pas pu se charger. Mode texte simple activé.');
    }
}

// Initialiser quand le DOM et Quill sont prêts
document.addEventListener('DOMContentLoaded', function() {
    // Attendre que Quill soit chargé depuis le CDN
    const checkQuillLoaded = setInterval(function() {
        if (typeof Quill !== 'undefined') {
            clearInterval(checkQuillLoaded);
            initQuillEditor();
        }
    }, 100);

    // Timeout de 5 secondes - si Quill ne charge pas, utiliser textarea
    setTimeout(function() {
        if (typeof Quill === 'undefined') {
            clearInterval(checkQuillLoaded);
            console.error('Quill failed to load from CDN');

            // Afficher le textarea en fallback
            const textarea = document.getElementById('content');
            if (textarea) {
                textarea.style.display = 'block';
                textarea.classList.add('form-textarea');
                textarea.rows = 20;
            }

            const editorContainer = document.getElementById('quill-editor');
            if (editorContainer) {
                editorContainer.style.display = 'none';
            }

            const loadingIndicator = document.getElementById('editor-loading');
            if (loadingIndicator) {
                loadingIndicator.innerHTML = '⚠️ Éditeur non disponible - Mode texte simple';
                loadingIndicator.style.color = '#fbbf24';
            }
        }
    }, 5000);
});

// Validation avant soumission du formulaire
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('procedureForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (window.quillInstance) {
                const content = window.quillInstance.root.innerHTML;
                document.getElementById('content').value = content;
            }
        });
    }
});
