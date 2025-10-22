class FileBrowser {
    constructor() {
        this.currentPath = "";
        this.searchTerm = "";
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
        this.updateStats();
    }

    setupEventListeners() {
        // 搜索功能
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', (e) => {
            this.searchTerm = e.target.value.toLowerCase();
            this.render();
        });

        // 模态框关闭
        const modal = document.getElementById('previewModal');
        const closeBtn = document.querySelector('.close');
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    navigateTo(path) {
        this.currentPath = path;
        this.render();
        this.updateBreadcrumb();
        this.updateStats();
    }

    updateBreadcrumb() {
        const breadcrumb = document.querySelector('.breadcrumb');
        const paths = this.currentPath ? this.currentPath.split('/') : [];
        
        let html = '<span class="crumb" data-path="">首页</span>';
        
        let currentPath = '';
        paths.forEach((folder, index) => {
            currentPath += (currentPath ? '/' : '') + folder;
            html += `<span class="crumb" data-path="${currentPath}">${folder}</span>`;
        });
        
        breadcrumb.innerHTML = html;
        
        // 添加面包屑点击事件
        breadcrumb.querySelectorAll('.crumb').forEach(crumb => {
            crumb.addEventListener('click', (e) => {
                const path = e.target.getAttribute('data-path');
                this.navigateTo(path);
            });
        });
    }

    render() {
        const currentData = fileDatabase[this.currentPath] || { folders: [], files: [] };
        
        this.renderFolders(currentData.folders);
        this.renderFiles(currentData.files);
    }

    renderFolders(folders) {
        const container = document.getElementById('foldersContainer');
        
        let filteredFolders = folders;
        if (this.searchTerm) {
            filteredFolders = folders.filter(folder => 
                folder.name.toLowerCase().includes(this.searchTerm) ||
                (folder.description && folder.description.toLowerCase().includes(this.searchTerm))
            );
        }

        if (filteredFolders.length === 0) {
            container.innerHTML = '<div class="no-items">暂无文件夹</div>';
            return;
        }

        container.innerHTML = filteredFolders.map(folder => `
            <div class="folder-item" onclick="fileBrowser.navigateTo('${this.currentPath ? this.currentPath + '/' : ''}${folder.id}')">
                <div class="folder-icon">${folder.icon}</div>
                <div class="folder-name">${folder.name}</div>
                <div class="file-size">${folder.description || '暂无描述'}</div>
            </div>
        `).join('');
    }

    renderFiles(files) {
        const container = document.getElementById('filesContainer');
        
        let filteredFiles = files;
        if (this.searchTerm) {
            filteredFiles = files.filter(file => 
                file.name.toLowerCase().includes(this.searchTerm) ||
                (file.description && file.description.toLowerCase().includes(this.searchTerm))
            );
        }

        if (filteredFiles.length === 0) {
            container.innerHTML = '<div class="no-items">暂无文件</div>';
            return;
        }

        container.innerHTML = filteredFiles.map(file => `
            <div class="file-item">
                <div class="file-icon">${file.icon}</div>
                <div class="file-name">${file.name}</div>
                <div class="file-size">${file.size} • ${file.description || '暂无描述'}</div>
                <div class="file-actions">
                    ${file.preview ? `<button class="btn btn-preview" onclick="fileBrowser.previewFile('${file.url}')">预览</button>` : ''}
                    <a href="${this.getDownloadUrl(file.url)}" class="btn btn-download" download="${file.name}">下载</a>
                </div>
            </div>
        `).join('');
    }

    getDownloadUrl(filePath) {
        // 生成 GitHub Raw 文件链接
        const username = 'YOUR_USERNAME'; // 需要替换为你的 GitHub 用户名
        const repo = 'file-sharing-website';
        const branch = 'main';
        
        return `https://raw.githubusercontent.com/${username}/${repo}/${branch}/${filePath}`;
    }

    previewFile(fileUrl) {
        const modal = document.getElementById('previewModal');
        const modalBody = document.getElementById('modalBody');
        
        const extension = fileUrl.split('.').pop().toLowerCase();
        const fullUrl = this.getDownloadUrl(fileUrl);
        
        let content = '';
        
        if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
            content = `<img src="${fullUrl}" alt="预览图片" onerror="this.style.display='none'; document.getElementById('modalBody').innerHTML='<div class=unsupported>图片加载失败或格式不支持预览</div>'">`;
        } else if (['pdf'].includes(extension)) {
            content = `<embed src="${fullUrl}" type="application/pdf" width="100%" height="600px">`;
        } else {
            content = '<div class="unsupported">该文件格式不支持在线预览，请下载后查看</div>';
        }
        
        modalBody.innerHTML = content;
        modal.style.display = 'block';
    }

    updateStats() {
        const currentData = fileDatabase[this.currentPath] || { folders: [], files: [] };
        
        // 计算当前路径下的所有文件和文件夹数量
        let totalFolders = currentData.folders.length;
        let totalFiles = currentData.files.length;
        
        document.getElementById('folderCount').textContent = totalFolders;
        document.getElementById('fileCount').textContent = totalFiles;
    }
}

// 添加一些额外的 CSS
const additionalStyles = `
.no-items {
    text-align: center;
    padding: 40px;
    color: #7f8c8d;
    font-style: italic;
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// 初始化文件浏览器
const fileBrowser = new FileBrowser();
