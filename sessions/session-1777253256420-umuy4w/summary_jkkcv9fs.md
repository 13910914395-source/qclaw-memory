## 任务背景
UTM VM因Bookmark数据损坏导致路径双重拼接无法启动，尝试克隆VM生成新的Bookmark数据。

## 执行过程
1. 清除com.utmapp.UTM.plist中ExternalDrives的Bookmark数据
2. 搜索config.plist二进制数据寻找隐藏路径信息
3. 用`utmctl clone Windows WindowsClone`克隆VM
4. 检查克隆VM的配置和磁盘（30GB正常）
5. 启动克隆VM测试

## 关键结果
- **克隆VM启动成功！** 路径完全正确：`WindowsClone.utm/Data/C00496F7-5ABA-4A9B-A9DE-97AC88E45B69.qcow2`
- 原因：原始VM的Bookmark数据损坏，克隆后生成新Bookmark
- 克隆VM状态：started
- 原Windows VM可删除或保留配置后重建
- memory/2026-04-28.md已更新

## 结论建议
在UTM GUI中打开WindowsClone查看Windows启动画面。如SPICE连接失败可点击工具栏🔌图标重连。原Windows VM可从UTM中删除——问题已通过克隆解决。