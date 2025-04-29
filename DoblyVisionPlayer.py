import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD, Tk
import subprocess

# 创建 GUI 应用程序
class MPVPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MPV 播放器 - 播放列表")

        # 初始化播放列表
        self.playlist = []

        # 添加拖放支持
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_files)

        # 选择文件按钮
        self.select_button = tk.Button(root, text="选择视频文件", command=self.select_files)
        self.select_button.pack(pady=10)

        # 播放按钮
        self.play_button = tk.Button(root, text="播放列表", command=self.play_playlist, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        # 播放列表框
        self.playlist_label = tk.Label(root, text="播放列表：")
        self.playlist_label.pack(pady=5)
        self.playlist_box = tk.Listbox(root, width=50, height=10)
        self.playlist_box.pack(pady=10)

        # 删除文件按钮
        self.remove_button = tk.Button(root, text="移除选中的文件", command=self.remove_selected, state=tk.DISABLED)
        self.remove_button.pack(pady=10)

    def select_files(self):
        # 打开文件对话框选择视频文件
        files = filedialog.askopenfilenames(
            filetypes=[("视频文件", "*.mp4 *.mkv *.mov *.ts *.avi *.flv *.wmv")]
        )
        if files:
            self.playlist.extend(files)
            self.update_playlist()
            self.play_button.config(state=tk.NORMAL)
            self.remove_button.config(state=tk.NORMAL)

    def update_playlist(self):
        # 更新播放列表显示
        self.playlist_box.delete(0, tk.END)
        for idx, file in enumerate(self.playlist, start=1):
            self.playlist_box.insert(tk.END, f"{idx}. {file}")

    def remove_selected(self):
        # 移除选中的文件
        selected_indices = self.playlist_box.curselection()
        if selected_indices:
            for index in reversed(selected_indices):  # 从后往前移除，避免索引问题
                self.playlist.pop(index)
            self.update_playlist()
            if not self.playlist:  # 如果播放列表为空，禁用按钮
                self.play_button.config(state=tk.DISABLED)
                self.remove_button.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("警告", "未选择任何文件！")

    def play_playlist(self):
        # 将播放列表传递给 mpv，并启用全屏模式
        if self.playlist:
            command = ["mpv", "--vo=gpu-next", "--fs"] + self.playlist
            subprocess.run(command)
        else:
            messagebox.showerror("错误", "播放列表为空！")

    def drop_files(self, event):
        # 响应文件拖拽并添加到播放列表
        files = self.root.tk.splitlist(event.data)  # 处理拖拽的文件列表
        for file in files:
            if file not in self.playlist:  # 避免重复添加
                self.playlist.append(file)
        self.update_playlist()
        self.play_button.config(state=tk.NORMAL)
        self.remove_button.config(state=tk.NORMAL)

# 创建主窗口
if __name__ == "__main__":
    # 初始化支持拖拽的 Tk 窗口
    root = TkinterDnD.Tk()
    app = MPVPlayerApp(root)
    root.mainloop()
