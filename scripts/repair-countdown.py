from pathlib import Path
import os,re,shutil
root=Path(os.environ.get('PROJECT_DIR','src'))
templates=Path(__file__).parent/'countdown47'
(root/'Shared').mkdir(exist_ok=True)
for name,dest in [('IdleActivityAttributes.swift','Shared'),('IdleLiveActivity.swift','CarIdle'),('IdleWidget.swift','CarIdleWidget')]:
 shutil.copyfile(templates/name,root/dest/name)
p=root/'project.yml';s=p.read_text()
s=re.sub(r'MARKETING_VERSION: "[^"]+"','MARKETING_VERSION: "2.3.12"',s)
s=re.sub(r'CURRENT_PROJECT_VERSION: "[^"]+"','CURRENT_PROJECT_VERSION: "47"',s)
s=s.replace('com.trollbox.caridle.liveactivity','com.trollbox.caridle.widget')
s=s.replace('      - CarIdle\n','      - CarIdle\n      - Shared\n').replace('      - CarIdleWidget\n','      - CarIdleWidget\n      - Shared\n')
p.write_text(s)
p=root/'CarIdle/SettingsView.swift';s=p.read_text();s=s.replace('    @ObservedObject var store: IdleStore','    @ObservedObject var store: IdleStore\n    @ObservedObject private var liveActivity = IdleLiveActivity.shared')
key='                    Toggle("实时显示发动机计时", isOn: $liveActivityEnabled)'
s=s.replace(key,key+'''\n                        .onChange(of: liveActivityEnabled) { _ in
                            liveActivity.sync(start: store.currentRecord?.startTime, targetMinutes: store.countdownMinutes)
                        }
                    Text(liveActivity.status)
                        .font(.caption).foregroundStyle(.secondary)
                        .textSelection(.enabled)
''');p.write_text(s)
p=root/'CarIdle/ContentView.swift';s=p.read_text().replace('    @StateObject private var store = IdleStore()','    @StateObject private var store = IdleStore()\n    @Environment(\\.scenePhase) private var scenePhase')
key='            .onChange(of: store.countdownMinutes) { minutes in'
s=s.replace(key,'''            .onChange(of: scenePhase) { phase in
                if phase == .active {
                    IdleLiveActivity.shared.sync(start: store.currentRecord?.startTime, targetMinutes: store.countdownMinutes)
                }
            }
            .onChange(of: store.currentRecord?.startTime) { _ in
                IdleLiveActivity.shared.sync(start: store.currentRecord?.startTime, targetMinutes: store.countdownMinutes)
            }
'''+key);p.write_text(s)
p=root/'CarIdle/VersionHistoryView.swift';s=p.read_text();key='    private let logs: [VersionLog] = [\n';s=s.replace(key,key+'        VersionLog(version: "v2.3.12 / Build 47", date: "2026年10月28日", changes: ["恢复原实时活动扩展标识，取消启动时无条件结束活动", "锁屏、展开和收起倒计时直接显示并预留数字空间；删除黄色暂停", "活动创建状态和真实错误在设置中可见；前台恢复时同步计时"]),\n',1);p.write_text(s)
(root/'README.md').write_text('''# CarIdle 2.3.12 / Build 47

基于2.3.9 / Build44原始完整源码，集中修复2.3.10/11实时活动显示问题。

- 恢复 com.trollbox.caridle.widget 扩展标识，保留主App标识与数据结构。
- 两个Target共同编译Shared/IdleActivityAttributes.swift，保持旧状态字段兼容。
- 直接显示Text(timerInterval:)，锁屏/展开/收起给定独立数字宽度；无隐藏占位、无无限宽度紧凑布局。
- 删除黄色暂停与空Button；保留灰色关闭图形和点击打开App行为。
- 不再每次启动先结束活动。先请求新活动，成功后再清理旧活动；失败保留旧活动。
- 设置显示真实请求状态或NSError。创建成功不代表已验证系统绘制。
- 不使用后台秒级/10秒循环；由系统更新倒计时。回到前台、启动/结束或改变目标时同步。

工作流会验证iOS16.2最低版本、App/扩展标识、47版本号、共享状态文件和IPA内嵌扩展；产出IPA与完整源码ZIP。
真机显示尚待验证，不能将编译成功等同于修复确认。
''')
p=root/'CHANGELOG.md';p.write_text('# 2.3.12 / Build47\n\n'+(root/'README.md').read_text()+'\n'+p.read_text())
print('2.3.12 / Build47 source prepared from 2.3.9')
