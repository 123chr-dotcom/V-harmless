from cx_Freeze import setup, Executable

# 依赖项
build_options = {
    "packages": ["tkinter", "pygetwindow", "pyautogui"],
    "excludes": [],
    "include_files": []
}

# 可执行文件配置
executables = [
    Executable(
        "chaos_demo.py",
        base="Win32GUI",  # 隐藏控制台窗口
        target_name="ChaosDemo.exe",
        icon=None
    )
]

setup(
    name="ChaosDemo",
    version="1.0",
    description="桌面混沌效果演示程序",
    options={"build_exe": build_options},
    executables=executables
)
