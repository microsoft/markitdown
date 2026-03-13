"""
MarkItDown GUI - 可视化文件转Markdown工具
支持拖拽文件到窗口，自动转换为Markdown格式
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import shutil

# 尝试导入 tkinterdnd2 支持拖拽，如果不可用则使用纯点击方式
try:
    import tkinterdnd2
    DND2_AVAILABLE = True
except ImportError:
    DND2_AVAILABLE = False

# 尝试导入markitdown
try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False


class MarkItDownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown工具")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置颜色
        self.bg_color = '#f5f5f5'
        self.drop_zone_bg = '#e8f4fc'
        self.drop_zone_active = '#c8e6f9'
        self.success_color = '#d4edda'
        self.error_color = '#f8d7da'
        self.root.configure(bg=self.bg_color)
        
        # 变量
        self.output_dir = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        self.is_converting = False
        self.converted_files = []
        
        # 初始化markitdown
        self._init_markitdown()
        
        # 创建界面
        self._create_widgets()
        
        # 绑定拖拽事件（如果tkinterdnd2可用）
        if DND2_AVAILABLE:
            self._bind_drag_events()
    
    def _init_markitdown(self):
        """初始化MarkItDown"""
        if MARKITDOWN_AVAILABLE:
            try:
                self.md = MarkItDown(enable_plugins=False)
            except Exception as e:
                self.md = None
                print(f"MarkItDown初始化错误: {e}")
        else:
            self.md = None
    
    def _create_widgets(self):
        """创建界面组件"""
        # 顶部标题
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="MarkItDown工具",
            font=("Microsoft YaHei", 20, "bold"),
            bg=self.bg_color,
            fg='#333'
        )
        title_label.pack(side='left')
        
        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="支持 PDF, Word, Excel, PPTX, 图片等格式",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            fg='#666'
        )
        subtitle_label.pack(side='left', padx=(10, 0))
        
        # 设置区域
        settings_frame = tk.LabelFrame(
            self.root,
            text="输出设置",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            padx=15,
            pady=10
        )
        settings_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # 输出目录选择
        dir_frame = tk.Frame(settings_frame, bg=self.bg_color)
        dir_frame.pack(fill='x')
        
        tk.Label(
            dir_frame,
            text="输出目录:",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color
        ).pack(side='left')
        
        self.dir_entry = tk.Entry(
            dir_frame,
            textvariable=self.output_dir,
            font=("Microsoft YaHei", 10),
            width=50,
            relief='solid',
            bd=1
        )
        self.dir_entry.pack(side='left', padx=10, fill='x', expand=True)
        
        dir_button = tk.Button(
            dir_frame,
            text="浏览...",
            font=("Microsoft YaHei", 10),
            command=self._browse_output_dir,
            bg='#1890ff',
            fg='white',
            activebackground='#096dd9',
            activeforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0,
            padx=15,
            cursor='hand2'
        )
        dir_button.pack(side='left')
        
        # 拖拽区域
        self.drop_frame = tk.Frame(
            self.root,
            bg=self.drop_zone_bg,
            relief='groove',
            borderwidth=3
        )
        self.drop_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 使用Frame来垂直居中内容
        content_frame = tk.Frame(self.drop_frame, bg=self.drop_zone_bg)
        content_frame.place(relx=0.5, rely=0.5, anchor='center')

        # 拖拽提示
        self.drop_label = tk.Label(
            content_frame,
            text="拖拽文件到这里",
            font=("Microsoft YaHei", 16, "bold"),
            bg=self.drop_zone_bg,
            fg='#555'
        )
        self.drop_label.pack(pady=(0, 20))

        # 选择文件按钮 - 蓝色样式（与浏览按钮一致）
        select_btn = tk.Button(
            content_frame,
            text="选择文件",
            font=("Microsoft YaHei", 12, "bold"),
            command=self._select_files,
            bg='#1890ff',
            fg='white',
            activebackground='#096dd9',
            activeforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0,
            highlightcolor='#1890ff',
            highlightbackground='#1890ff',
            overrelief='flat',
            takefocus=0,
            width=10,
            cursor='hand2'
        )
        select_btn.pack(padx=10, pady=10)
        
        # 转换状态区域
        status_frame = tk.LabelFrame(
            self.root,
            text="转换状态",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            padx=10,
            pady=5
        )
        status_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # 进度条
        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(side='left', padx=(0, 10))
        
        # 状态标签
        self.status_label = tk.Label(
            status_frame,
            text="就绪",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            fg='#333'
        )
        self.status_label.pack(side='left')
        
        # 清空历史按钮
        clear_btn = tk.Button(
            status_frame,
            text="清空历史",
            font=("Microsoft YaHei", 9),
            command=self._clear_history,
            bg='#1890ff',
            fg='white',
            activebackground='#096dd9',
            activeforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0,
            padx=10,
            cursor='hand2'
        )
        clear_btn.pack(side='right')
        
        # 已转换文件列表区域
        result_frame = tk.LabelFrame(
            self.root,
            text="转换结果",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            padx=10,
            pady=5
        )
        result_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # 创建Treeview显示结果
        columns = ('filename', 'status', 'output')
        self.result_tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show='headings',
            height=5
        )
        
        self.result_tree.heading('filename', text='文件名')
        self.result_tree.heading('status', text='状态')
        self.result_tree.heading('output', text='输出路径')
        
        self.result_tree.column('filename', width=200)
        self.result_tree.column('status', width=80)
        self.result_tree.column('output', width=400)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 双击打开文件
        self.result_tree.bind('<Double-1>', self._open_file)
        
        # 底部信息
        footer = tk.Label(
            self.root,
            text="支持格式: PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, HTML, CSV, JSON, XML, TXT, EPUB, ZIP, 图片, 音频",
            font=("Microsoft YaHei", 8),
            bg=self.bg_color,
            fg='#888',
            pady=5
        )
        footer.pack(fill='x')
    
    def _bind_drag_events(self):
        """绑定拖拽事件"""
        if DND2_AVAILABLE:
            # 使用 tkinterdnd2 支持拖拽
            from tkinterdnd2 import DND_FILES, TkinterDnD
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind('<<Drop>>', self._on_drop)
        else:
            # 不支持拖拽，更新提示文字
            self.drop_label.config(text="点击下方按钮选择文件\n\n拖拽功能需安装 tkinterdnd2")
        
        # 鼠标事件
        self.drop_frame.bind('<Enter>', self._on_drag_enter)
        self.drop_frame.bind('<Leave>', self._on_drag_leave)
    
    def _on_drag_enter(self, event):
        """拖拽进入时高亮"""
        pass
    
    def _on_drag_leave(self, event):
        """拖拽离开时恢复"""
        pass
    
    def _on_drop(self, event):
        """处理拖拽文件"""
        # 获取拖拽的文件列表
        files = self.root.tk.splitlist(event.data)
        
        if files:
            self._convert_files(files)
    
    def _select_files(self):
        """选择文件"""
        file_paths = filedialog.askopenfilenames(
            title="选择要转换的文件",
            filetypes=[
                ("所有支持的文件", "*.pdf *.docx *.doc *.xlsx *.xls *.pptx *.ppt *.html *.htm *.csv *.json *.xml *.txt *.epub *.zip *.jpg *.jpeg *.png *.gif *.bmp *.mp3 *.wav"),
                ("PDF文件", "*.pdf"),
                ("Word文档", "*.docx *.doc"),
                ("Excel文件", "*.xlsx *.xls"),
                ("PowerPoint", "*.pptx *.ppt"),
                ("图片文件", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_paths:
            self._convert_files(file_paths)
    
    def _browse_output_dir(self):
        """选择输出目录"""
        dir_path = filedialog.askdirectory(
            title="选择输出目录",
            initialdir=self.output_dir.get()
        )
        
        if dir_path:
            self.output_dir.set(dir_path)
    
    def _convert_files(self, file_paths):
        """转换文件"""
        if self.is_converting:
            messagebox.showwarning("警告", "正在转换中，请稍后...")
            return
        
        if not MARKITDOWN_AVAILABLE or self.md is None:
            messagebox.showerror(
                "错误",
                "MarkItDown未正确安装！\n\n请运行:\npip install 'markitdown[all]'"
            )
            return
        
        # 验证文件
        valid_files = []
        for path in file_paths:
            path = Path(path)
            if path.exists():
                valid_files.append(path)
            else:
                messagebox.showwarning("警告", f"文件不存在: {path}")
        
        if not valid_files:
            return
        
        # 开始转换
        self.is_converting = True
        self.progress.start()
        self.status_label.config(text="正在转换...", fg='#007bff')
        
        # 禁用拖拽区域
        self.drop_label.config(text="转换中...\n请稍候", fg='#007bff')
        
        # 在后台线程中转换
        thread = threading.Thread(target=self._convert_thread, args=(valid_files,))
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self, file_paths):
        """转换线程"""
        for file_path in file_paths:
            self._convert_single_file(file_path)
        
        # 完成
        self.root.after(0, self._conversion_complete)
    
    def _convert_single_file(self, file_path):
        """转换单个文件"""
        try:
            self.root.after(0, lambda: self.status_label.config(
                text=f"正在转换: {file_path.name}",
                fg='#007bff'
            ))
            
            # 执行转换
            result = self.md.convert(str(file_path))
            
            # 生成输出文件名
            output_dir = Path(self.output_dir.get())
            output_file = output_dir / f"{file_path.stem}.md"
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            
            # 记录结果
            self.converted_files.append((file_path.name, str(output_file), True))
            
            self.root.after(0, lambda: self._add_result_item(
                file_path.name,
                "✓ 成功",
                str(output_file),
                success=True
            ))
            
        except Exception as e:
            error_msg = str(e)
            self.converted_files.append((file_path.name, error_msg, False))
            
            self.root.after(0, lambda: self._add_result_item(
                file_path.name,
                f"✗ 失败",
                error_msg,
                success=False
            ))
    
    def _add_result_item(self, filename, status, output, success):
        """添加结果项"""
        item = self.result_tree.insert('', 'end', values=(filename, status, output))
        
        # 设置颜色
        if success:
            self.result_tree.item(item, tags=('success',))
        else:
            self.result_tree.item(item, tags=('error',))
        
        self.result_tree.tag_configure('success', foreground='#28a745')
        self.result_tree.tag_configure('error', foreground='#dc3545')
    
    def _conversion_complete(self):
        """转换完成"""
        self.is_converting = False
        self.progress.stop()
        
        # 恢复拖拽区域
        self.drop_label.config(text="拖拽文件到这里", fg='#555')
        
        # 统计
        success_count = sum(1 for _, _, success in self.converted_files if success)
        total_count = len(self.converted_files)
        
        self.status_label.config(
            text=f"完成! 成功: {success_count}/{total_count}",
            fg='#28a745' if success_count == total_count else '#ffc107'
        )
        
        if success_count > 0:
            messagebox.showinfo(
                "转换完成",
                f"成功转换 {success_count} 个文件！\n\n输出目录: {self.output_dir.get()}"
            )
    
    def _clear_history(self):
        """清空历史"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.converted_files.clear()
        self.status_label.config(text="就绪", fg='#333')
    
    def _open_file(self, event):
        """双击打开文件"""
        selection = self.result_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.result_tree.item(item, 'values')
        
        if len(values) >= 3:
            output_path = values[2]
            
            # 如果是成功状态，打开文件
            if '✓' in values[1]:
                try:
                    # Windows系统用默认程序打开
                    if sys.platform == 'win32':
                        os.startfile(output_path)
                    else:
                        import subprocess
                        subprocess.call(['open', output_path])
                except Exception as e:
                    messagebox.showerror("错误", f"无法打开文件: {e}")


def main():
    """主函数"""
    # 如果安装了tkinterdnd2，使用它来支持拖拽
    if DND2_AVAILABLE:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    # 设置高DPI支持
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = MarkItDownGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
