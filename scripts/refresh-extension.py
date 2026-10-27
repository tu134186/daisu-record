from pathlib import Path
import os
root=Path(os.environ.get('PROJECT_DIR','src'))
p=root/'CarIdleWidget/IdleWidget.swift';s=p.read_text()
s=s.replace('// V2.3.10 / Build 45', '// V2.3.11 / Build 46')
s=s.replace('Text("怠速记录")','Text("怠速记录 ·46")')
a=s.index('                compactTimer(',s.index('} compactTrailing:'));b=s.index('            } minimal:',a)
s=s[:a]+'''                // A static digit template gives the flexible system timer a measured width.
                Text(context.state.targetMinutes >= 60 ? "0:00:00" : "00:00")
                    .font(.system(size: 13, weight: .semibold, design: .rounded))
                    .monospacedDigit()
                    .hidden()
                    .overlay(alignment: .trailing) {
                        compactTimer(context.state.startTime, context.state.targetMinutes, size: 13)
                            .multilineTextAlignment(.trailing)
                    }
                    .frame(height: 22)
''' +s[b:]
s=s.replace('            .contentMargins(.all, 0, for: .compactTrailing)','            .widgetURL(URL(string: "caridle://record"))')
p.write_text(s)
p=root/'project.yml';s=p.read_text().replace('com.trollbox.caridle.widget','com.trollbox.caridle.liveactivity').replace('"2.3.10"','"2.3.11"').replace('"45"','"46"');p.write_text(s)
p=root/'CarIdle/IdleLiveActivity.swift';s=p.read_text();a=s.index('    // 常驻');s=s[:a]+'''    // Serialize ActivityKit changes so an end operation cannot remove a newly created activity.
    private var operation: Task<Void, Never>?
    private var revision = 0
    private var replacedExistingActivities = false

    func sync(start: Date?, targetMinutes: Int) {
        revision += 1
        let requestedRevision = revision
        let previous = operation
        operation = Task { [weak self] in
            await previous?.value
            guard let self = self, requestedRevision == self.revision else { return }
            // Once per process: discard existing presentations and create the current extension UI.
            if !self.replacedExistingActivities {
                for activity in Activity<IdleActivityAttributes>.activities {
                    await activity.end(nil, dismissalPolicy: .immediate)
                }
                self.replacedExistingActivities = true
            }
            guard self.enabled, let start = start else {
                for activity in Activity<IdleActivityAttributes>.activities {
                    await activity.end(nil, dismissalPolicy: .immediate)
                }
                return
            }
            guard ActivityAuthorizationInfo().areActivitiesEnabled else { return }
            let state = IdleActivityAttributes.ContentState(startTime: start, targetMinutes: targetMinutes)
            let activities = Activity<IdleActivityAttributes>.activities
            if let existing = activities.first {
                if existing.content.state != state {
                    await existing.update(ActivityContent(state: state, staleDate: nil))
                }
                for duplicate in activities.dropFirst() {
                    await duplicate.end(nil, dismissalPolicy: .immediate)
                }
            } else {
                do {
                    _ = try Activity<IdleActivityAttributes>.request(
                        attributes: IdleActivityAttributes(title: "怠速记录"),
                        content: ActivityContent(state: state, staleDate: nil), pushType: nil
                    )
                } catch {
                    NSLog("[CarIdle] Live Activity start failed: %@", String(describing: error))
                }
            }
        }
    }

    func endAll() {
        sync(start: nil, targetMinutes: 0)
    }
}
''';p.write_text(s)
p=root/'CarIdle/VersionHistoryView.swift';s=p.read_text();key='    private let logs: [VersionLog] = [\n';s=s.replace(key,key+'        VersionLog(version: "v2.3.11 / Build 46", date: "2026年10月27日", changes: ["重新注册实时活动扩展，打开 App 自动重建旧活动", "倒计时采用数字占位约束，删除无效的重复刷新任务", "锁屏与展开标题显示 46，便于核对扩展实际加载版本"]),\n',1);p.write_text(s)
for name in ['README.md','CHANGELOG.md']:
 p=root/name;p.write_text('# CarIdle 2.3.11 / Build 46\n\n重新注册实时活动扩展；启动后自动重建旧活动。去除无效暂停按钮，收起倒计时采用数字占位约束。标题中的46用于核对扩展加载。真机效果待验证。\n\n'+p.read_text())
assert 'pause.fill' not in (root/'CarIdleWidget/IdleWidget.swift').read_text()
print('Prepared 2.3.11 / Build46')
