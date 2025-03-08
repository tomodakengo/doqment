/**
 * セクションテンプレート管理用のJavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // セクションテンプレートのコンテナ
    const templatesContainer = document.getElementById('section-templates-container');
    
    // プロジェクトID
    const projectId = document.getElementById('project-id').value;
    
    // CSRFトークン
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
    // 新しいセクションテンプレートを追加するボタン
    const addTemplateBtn = document.getElementById('add-template-btn');
    if (addTemplateBtn) {
        addTemplateBtn.addEventListener('click', function() {
            addNewTemplate();
        });
    }
    
    // セクションテンプレートをドラッグ可能にする
    if (templatesContainer) {
        initSortable();
    }
    
    /**
     * 新しいセクションテンプレートを追加する
     */
    function addNewTemplate() {
        // モーダルを表示
        const modal = document.getElementById('template-modal');
        modal.classList.remove('hidden');
        
        // モーダルを閉じるボタン
        const closeModalBtn = document.getElementById('close-modal-btn');
        closeModalBtn.addEventListener('click', function() {
            modal.classList.add('hidden');
        });
        
        // フォームの送信
        const templateForm = document.getElementById('template-form');
        templateForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(templateForm);
            formData.append('csrfmiddlewaretoken', csrfToken);
            
            fetch(`/projects/${projectId}/templates/add/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 新しいテンプレートをDOMに追加
                    const newTemplate = createTemplateElement(data.template_id, data.template_title);
                    templatesContainer.appendChild(newTemplate);
                    
                    // モーダルを閉じる
                    modal.classList.add('hidden');
                    
                    // フォームをリセット
                    templateForm.reset();
                    
                    // ソータブルを再初期化
                    initSortable();
                } else {
                    alert('エラーが発生しました: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('エラーが発生しました。');
            });
        });
    }
    
    /**
     * テンプレート要素を作成する
     */
    function createTemplateElement(id, title) {
        const template = document.createElement('div');
        template.className = 'bg-white p-4 rounded-lg shadow-sm mb-4 cursor-move';
        template.dataset.id = id;
        
        template.innerHTML = `
            <div class="flex justify-between items-center">
                <h3 class="font-medium text-gray-900">${title}</h3>
                <div class="flex space-x-2">
                    <a href="/templates/${id}/update/" class="text-gray-700 hover:text-gray-900">編集</a>
                    <a href="/templates/${id}/delete/" class="text-red-600 hover:text-red-800">削除</a>
                </div>
            </div>
        `;
        
        return template;
    }
    
    /**
     * ソータブルを初期化する
     */
    function initSortable() {
        if (typeof Sortable !== 'undefined') {
            const sortable = Sortable.create(templatesContainer, {
                animation: 150,
                ghostClass: 'bg-gray-100',
                onEnd: function() {
                    updateTemplateOrder();
                }
            });
        }
    }
    
    /**
     * テンプレートの順序を更新する
     */
    function updateTemplateOrder() {
        const templateIds = Array.from(templatesContainer.children).map(el => el.dataset.id);
        
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfToken);
        templateIds.forEach(id => {
            formData.append('template_ids[]', id);
        });
        
        fetch('/templates/update-order/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('順序の更新に失敗しました: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('順序の更新中にエラーが発生しました。');
        });
    }
}); 