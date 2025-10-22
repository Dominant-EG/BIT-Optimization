// 文件数据库 - 你只需要修改这个文件来添加/删除文件
const fileDatabase = {
    // 根目录文件
    "": {
        folders: [
            {
                id: "tech",
                name: "技术文档",
                icon: "📚",
                description: "技术相关文档和指南"
            },
            {
                id: "images",
                name: "图片资源", 
                icon: "🖼️",
                description: "图片和设计资源"
            },
            {
                id: "software",
                name: "软件工具",
                icon: "⚙️",
                description: "实用软件和工具"
            },
            {
                id: "templates",
                name: "模板资源",
                icon: "📋",
                description: "各种模板文件"
            }
        ],
        files: [
            {
                id: "readme",
                name: "使用说明.pdf",
                icon: "📄",
                size: "2.3 MB",
                url: "files/使用说明.pdf",
                description: "网站使用说明文档",
                preview: false
            }
        ]
    },

    // 技术文档文件夹
    "tech": {
        folders: [
            {
                id: "api",
                name: "API文档",
                icon: "🔌",
                description: "接口文档和规范"
            },
            {
                id: "guides", 
                name: "使用指南",
                icon: "📖",
                description: "详细的使用教程"
            }
        ],
        files: [
            {
                id: "tech1",
                name: "系统架构设计.docx",
                icon: "📝",
                size: "1.8 MB", 
                url: "files/tech/系统架构设计.docx",
                description: "系统整体架构设计文档",
                preview: false
            },
            {
                id: "tech2",
                name: "开发规范.pdf",
                icon: "📋",
                size: "3.2 MB",
                url: "files/tech/开发规范.pdf", 
                description: "项目开发编码规范",
                preview: true
            }
        ]
    },

    // 图片资源文件夹
    "images": {
        folders: [],
        files: [
            {
                id: "img1",
                name: "产品展示图.jpg",
                icon: "🖼️",
                size: "4.5 MB",
                url: "files/images/产品展示图.jpg",
                description: "产品展示图片",
                preview: true
            },
            {
                id: "img2", 
                name: "公司logo.png",
                icon: "🏢",
                size: "1.2 MB",
                url: "files/images/公司logo.png",
                description: "公司标志图片",
                preview: true
            },
            {
                id: "img3",
                name: "背景图片.jpg", 
                icon: "🎨",
                size: "6.7 MB",
                url: "files/images/背景图片.jpg",
                description: "网站背景图片资源",
                preview: true
            }
        ]
    },

    // 软件工具文件夹  
    "software": {
        folders: [
            {
                id: "windows",
                name: "Windows软件",
                icon: "🪟",
                description: "Windows平台软件"
            },
            {
                id: "macos",
                name: "MacOS软件", 
                icon: "🍎",
                description: "MacOS平台软件"
            }
        ],
        files: [
            {
                id: "soft1",
                name: "工具集合.zip",
                icon: "📦",
                size: "15.2 MB",
                url: "files/software/工具集合.zip",
                description: "常用工具软件集合",
                preview: false
            }
        ]
    },

    // 模板资源文件夹
    "templates": {
        folders: [],
        files: [
            {
                id: "temp1",
                name: "简历模板.docx",
                icon: "📄",
                size: "2.1 MB",
                url: "files/templates/简历模板.docx",
                description: "专业简历模板",
                preview: false
            },
            {
                id: "temp2",
                name: "演示文稿模板.pptx",
                icon: "📊", 
                size: "8.7 MB",
                url: "files/templates/演示文稿模板.pptx",
                description: "商务演示文稿模板",
                preview: false
            }
        ]
    },

    // 子文件夹内容
    "tech/api": {
        folders: [],
        files: [
            {
                id: "api1",
                name: "REST API文档.pdf",
                icon: "🔗",
                size: "5.6 MB",
                url: "files/tech/api/REST API文档.pdf",
                description: "RESTful API接口文档",
                preview: true
            }
        ]
    },

    "tech/guides": {
        folders: [],
        files: [
            {
                id: "guide1",
                name: "安装指南.pdf",
                icon: "📥",
                size: "3.4 MB",
                url: "files/tech/guides/安装指南.pdf",
                description: "软件安装详细指南",
                preview: true
            }
        ]
    },

    "software/windows": {
        folders: [],
        files: [
            {
                id: "win1",
                name: "编辑器安装包.exe",
                icon: "⚙️",
                size: "45.2 MB",
                url: "files/software/windows/编辑器安装包.exe",
                description: "代码编辑器安装程序",
                preview: false
            }
        ]
    },

    "software/macos": {
        folders: [],
        files: [
            {
                id: "mac1",
                name: "设计工具.dmg",
                icon: "🎨",
                size: "78.3 MB", 
                url: "files/software/macos/设计工具.dmg",
                description: "Mac设计工具安装包",
                preview: false
            }
        ]
    }
};
