from pathlib import Path
import os,plistlib,zipfile
root=Path(os.environ.get('PROJECT_DIR','src'))
p=root/'CarIdleWidget/IdleWidget.swift';s=p.read_text()
a=s.index('    // 暂停按钮');b=s.index('    // 关闭按钮',a);s=s[:a]+s[b:]
s=s.replace('                pauseButton()\n','')
a=s.index('                        Button { } label: {\n                            Image(systemName: "pause.fill")');b=s.index('                        Button { } label: {\n                            Image(systemName: "xmark")',a);s=s[:a]+s[b:]
s=s.replace('Text("计时器")','Text("怠速记录")')
s=s.replace('Text(timerInterval: remainingInterval(start, targetMinutes), countsDown: true)\n            .font(.system(size: size, weight: .semibold, design: .rounded))', 'Text(timerInterval: remainingInterval(start, targetMinutes), countsDown: true, showsHours: targetMinutes >= 60)\n            .font(.system(size: size, weight: .semibold, design: .rounded))',1)
s=s.replace('compactTimer(context.state.startTime, context.state.targetMinutes, size: 13)\n                    .frame(maxWidth: .infinity, alignment: .trailing)', 'compactTimer(context.state.startTime, context.state.targetMinutes, size: 13)\n                    .multilineTextAlignment(.trailing)\n                    .frame(width: context.state.targetMinutes >= 60 ? 62 : 46, height: 22, alignment: .trailing)')
a=s.index('// V2.3.9');b=s.index('struct IdleActivityAttributes',a);s=s[:a]+'''// V2.3.10 / Build 45: remove the nonfunctional yellow pause controls.
// Preserve lock-screen and expanded island layout; constrain the compact trailing timer.
// Native timerInterval text continues to count down when the app is backgrounded.
'''+s[b:]
assert 'pause.fill' not in s and 'pauseButton' not in s
compact=s[s.index('} compactTrailing:'):s.index('} minimal:')]
assert '.infinity' not in compact and 'width:' in compact
p.write_text(s)
p=root/'CarIdle/IdleLiveActivity.swift';s=p.read_text().replace('IdleActivityAttributes(title: "计时器")','IdleActivityAttributes(title: "怠速记录")');p.write_text(s)
p=root/'project.yml';s=p.read_text();assert s.count('MARKETING_VERSION: "2.3.9"')==2 and s.count('CURRENT_PROJECT_VERSION: "44"')==2;s=s.replace('MARKETING_VERSION: "2.3.9"','MARKETING_VERSION: "2.3.10"').replace('CURRENT_PROJECT_VERSION: "44"','CURRENT_PROJECT_VERSION: "45"');p.write_text(s)
p=root/'CarIdle/VersionHistoryView.swift';s=p.read_text();key='    private let logs: [VersionLog] = [\n';assert key in s;s=s.replace(key,key+'        VersionLog(version: "v2.3.10 / Build 45", date: "2026年10月27日", changes: ["删除锁屏和展开灵动岛里的黄色暂停按钮", "限制收起灵动岛右侧倒计时宽度，修复无限伸展布局", "保留汽车图标、锁屏及长按展开布局、点击跳转和历史数据"]),\n',1);p.write_text(s)
p=root/'CHANGELOG.md';p.write_text('# V2.3.10 / Build 45 — 2026-10-27\n\n- 删除实时活动中的黄色暂停按钮。\n- 收起灵动岛右侧采用固定宽度的系统倒计时文本。\n- 保留汽车图标、锁屏和展开布局，历史/备份数据结构不变。\n- 真机倒计时显示待测试。\n\n'+p.read_text())
(root/'README.md').write_text('# 怠速记录 2.3.10 / Build 45\n\n基于 V2.3.9 / Build 44。删除黄色暂停，修复 compactTrailing 的无限宽度计时布局。\n锁屏和展开计时布局、按钮跳转、汽车图片、历史记录及备份逻辑保留。\n\n安装后结束旧实时活动，再开始一次记录测试新版布局。真机效果尚待确认。\n')
for p in root.rglob('*.plist'):plistlib.loads(p.read_bytes())
assert s.count('private let logs:')==1
print('2.3.10 / Build 45 source prepared; pause controls removed; finite compact timer width verified')
