// 简单的文件管理功能
class FileManager {
    constructor() {
        this.files = JSON.parse(localStorage.getItem('sharedFiles')) || [];
        this.init();
    }

    init() {
        // 如果是下载页面，加载文件列表
        if (window.location.pathname.includes('download.html')) {
            this.loadFileList();
            this.setupSearch();
        }

        // 如果是上传页面，设置表单提交
        if (window.location.pathname.includes('upload.html')) {
            this.setupUploadForm();
        }
    }

    setupUploadForm() {
        const form = document.getElementById('uploadForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.addFile();
            });
        }
    }

    addFile() {
        const name = document.getElementById('fileName').value;
        const url = document.getElementById('fileUrl').value;
        const description = document.getElementById('fileDescription').value;

        const newFile = {
            id: Date.now(),
            name: name,
            url: url,
            description: description,
            size: '未知',
            uploadDate: new Date().toLocaleDateString()
        };

        this.files.push(newFile);
        this.saveFiles();
        
        alert('文件提交成功！');
        document.getElementById('uploadForm').reset();
    }

    loadFileList() {
        const fileList = document.querySelector('.file-list');
        const noFiles = document.getElementById('noFiles');

        if (this.files.length === 0) {
            fileList.style.display = 'none';
            noFiles.style.display = 'block';
            return;
        }

        fileList.innerHTML = '';
        this.files.forEach(file => {
            const fileElement = this.createFileElement(file);
            fileList.appendChild(fileElement);
        });
    }

    createFileElement(file) {
        const div = document.createElement('div');
        div.className = 'file-item';
        div.innerHTML = `
            <div class="file-info">
                <h4>${this.escapeHtml(file.name)}</h4>
                <p class="file-desc">${this.escapeHtml(file.description || '暂无描述')}</p>
                <span class="file-size">${file.uploadDate} • ${file.size}</span>
            </div>
            <a href="${this.escapeHtml(file.url)}" class="download-btn" target="_blank">下载</a>
        `;
        return div;
    }

    setupSearch() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterFiles(e.target.value);
            });
        }
    }

    filterFiles(searchTerm) {
        const filteredFiles = this.files.filter(file => 
            file.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (file.description && file.description.toLowerCase().includes(searchTerm.toLowerCase()))
        );

        const fileList = document.querySelector('.file-list');
        fileList.innerHTML = '';
        
        filteredFiles.forEach(file => {
            const fileElement = this.createFileElement(file);
            fileList.appendChild(fileElement);
        });
    }

    saveFiles() {
        localStorage.setItem('sharedFiles', JSON.stringify(this.files));
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// 初始化文件管理器
document.addEventListener('DOMContentLoaded', () => {
    new FileManager();
});
