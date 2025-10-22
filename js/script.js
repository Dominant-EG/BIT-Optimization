// 增强的文件管理功能
class FileManager {
    constructor() {
        this.files = JSON.parse(localStorage.getItem('sharedFiles')) || [];
        // 添加一些示例文件
        if (this.files.length === 0) {
            this.files = [
                {
                    id: 1,
                    name: 'example.jpg',
                    path: 'files/example.jpg',
                    description: '示例图片文件',
                    size: '1.2 MB',
                    uploadDate: '2024-01-01'
                }
            ];
            this.saveFiles();
        }
        this.init();
    }

    init() {
        if (window.location.pathname.includes('download.html')) {
            this.loadFileList();
            this.setupSearch();
        }

        if (window.location.pathname.includes('upload.html')) {
            this.setupFileRecordForm();
            // 更新 GitHub 链接为用户的实际用户名
            this.updateGitHubLinks();
        }
    }

    // 更新 GitHub 链接
    updateGitHubLinks() {
        // 这里需要用户手动替换用户名，或者通过其他方式获取
        const githubLinks = document.querySelectorAll('a[href*="你的用户名"]');
        githubLinks.forEach(link => {
            // 提示用户需要手动修改链接
            console.log('请手动将 upload.html 中的"你的用户名"替换为你的实际 GitHub 用户名');
        });
    }

    setupFileRecordForm() {
        const form = document.getElementById('fileRecordForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.recordFile();
            });
        }
    }

    recordFile() {
        const name = document.getElementById('fileName').value;
        const path = document.getElementById('filePath').value;
        const description = document.getElementById('fileDescription').value;

        // 生成 GitHub 原始文件链接
        const githubRawUrl = this.generateGitHubRawUrl(path);

        const newFile = {
            id: Date.now(),
            name: name,
            path: path,
            url: githubRawUrl,
            description: description,
            size: '未知',
            uploadDate: new Date().toLocaleDateString('zh-CN')
        };

        this.files.push(newFile);
        this.saveFiles();
        
        alert('文件记录成功！现在可以在下载页面看到了。');
        document.getElementById('fileRecordForm').reset();
    }

    // 生成 GitHub 原始文件链接
    generateGitHubRawUrl(filePath) {
        // 用户需要手动修改这里的用户名和仓库名
        const username = '你的用户名'; // 需要用户手动修改
        const repo = 'file-sharing-website';
        const branch = 'main';
        
        return `https://raw.githubusercontent.com/${username}/${repo}/${branch}/${filePath}`;
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
        
        // 根据文件类型显示不同的图标
        const icon = this.getFileIcon(file.name);
        
        div.innerHTML = `
            <div class="file-info">
                <h4>${icon} ${this.escapeHtml(file.name)}</h4>
                <p class="file-desc">${this.escapeHtml(file.description || '暂无描述')}</p>
                <span class="file-size">${file.uploadDate} • ${file.size}</span>
            </div>
            <a href="${this.escapeHtml(file.url)}" class="download-btn" target="_blank" download="${this.escapeHtml(file.name)}">下载</a>
        `;
        return div;
    }

    getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const icons = {
            'pdf': '📄',
            'doc': '📝',
            'docx': '📝',
            'txt': '📃',
            'jpg': '🖼️',
            'jpeg': '🖼️',
            'png': '🖼️',
            'gif': '🖼️',
            'zip': '📦',
            'rar': '📦',
            'mp4': '🎬',
            'mp3': '🎵'
        };
        return icons[ext] || '📁';
    }

    // 其他方法保持不变...
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
