import time
import random
import sys
import threading
import tkinter as tk
try:
    import pygetwindow as gw
    import pyautogui
except ImportError:
    print("请先安装依赖库：")
    print("pip install pygetwindow pyautogui")
    sys.exit(1)

# 全局控制变量
is_running = True
popup_windows = []

class ChaosSystem:
    def __init__(self, duration=360):
        self.duration = duration
        self.screen = pyautogui.size()
        self.root = tk.Tk()
        self.root.withdraw()
        self.popup_count = 0
        self.windows = []
        self.original_pos = {}

    # ===== 窗口移动模块 =====
    def _get_valid_windows(self):
        """获取可操作窗口列表"""
        return [win for win in gw.getAllWindows() 
               if win.visible and win.title and win.width > 100]

    def chaos_windows(self):
        """窗口随机移动核心逻辑"""
        self.windows = self._get_valid_windows()
        self.original_pos = {win._hWnd: (win.left, win.top) for win in self.windows}
        
        end_time = time.time() + self.duration
        while time.time() < end_time and is_running:
            for win in self.windows:
                try:
                    new_x = random.randint(0, self.screen.width - win.width)
                    new_y = random.randint(0, self.screen.height - win.height)
                    win.moveTo(new_x, win.top)  # 先移动X轴
                    win.moveTo(win.left, new_y) # 再移动Y轴
                except:
                    pass
            time.sleep(0.08)  # 控制移动频率

    # ===== 鼠标移动模块 =====
    def chaos_mouse(self):
        """鼠标随机移动核心逻辑"""
        end_time = time.time() + self.duration
        while time.time() < end_time and is_running:
            try:
                # 随机移动模式选择
                if random.random() > 0.3:
                    # 瞬移模式
                    x = random.randint(0, self.screen.width)
                    y = random.randint(0, self.screen.height)
                    pyautogui.moveTo(x, y, duration=0.05)
                else:
                    # 抖动模式
                    dx = random.randint(-150, 150)
                    dy = random.randint(-150, 150)
                    pyautogui.moveRel(dx, dy, duration=0.05)
                time.sleep(random.uniform(0.05, 0.15))
            except:
                pass

    # ===== 弹窗模块 =====
    def create_popup(self):
        """创建单个弹窗"""
        if self.popup_count >= 100:
            return
        
        x = random.randint(50, self.screen.width - 300)
        y = random.randint(50, self.screen.height - 150)
        
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.geometry(f"300x150+{x}+{y}")
        popup.configure(bg='#ff0000')
        
        label = tk.Label(popup,
            text="你的电脑被我控制360秒了", 
            font=("微软雅黑", 18, "bold"),
            fg='white',
            bg='#ff0000'
        )
        label.pack(expand=True)
        
        popup.attributes('-topmost', True)
        popup.protocol("WM_DELETE_WINDOW", lambda: None)
        
        popup_windows.append(popup)
        self.popup_count += 1

    def popup_generator(self):
        """弹窗生成控制器"""
        start_time = time.time()
        while time.time() - start_time < self.duration and is_running:
            self.root.after(0, self.create_popup)
            time.sleep(0.2)  # 严格0.2秒间隔

    # ===== 清理模块 =====
    def restore_system(self):
        """恢复系统状态"""
        # 恢复窗口位置
        for win in self.windows:
            try:
                hwnd = win._hWnd
                win.moveTo(*self.original_pos[hwnd])
            except:
                pass
        
        # 清除弹窗
        for popup in popup_windows:
            try:
                popup.destroy()
            except:
                pass
        self.root.destroy()

def main():
    global is_running
    chaos = ChaosSystem(duration=360)
    
    # 启动所有线程
    threads = [
        threading.Thread(target=chaos.chaos_windows),
        threading.Thread(target=chaos.chaos_mouse),
        threading.Thread(target=chaos.popup_generator)
    ]
    
    for t in threads:
        t.daemon = True
        t.start()
    
    # 运行Tkinter主循环
    try:
        chaos.root.mainloop()
    except KeyboardInterrupt:
        print("\n用户中断！")
    finally:
        is_running = False
        chaos.restore_system()
        print("系统已恢复！")

if __name__ == "__main__":
    print("=== 混沌模式启动 ===")
    main()