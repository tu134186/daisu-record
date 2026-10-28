from pathlib import Path
import os,subprocess,plistlib
root=Path(os.environ.get('PROJECT_DIR','src'))
subprocess.run(['python3',str(Path(__file__).parent/'repair-countdown.py')],check=True)
p=root/'project.yml';s=p.read_text().replace('"2.3.12"','"2.3.13"').replace('"47"','"48"').replace('CODE_SIGN_ENTITLEMENTS: CarIdle/CarIdle.entitlements','CODE_SIGN_ENTITLEMENTS: Signing/CarIdle.entitlements').replace('      APPLICATION_EXTENSION_API_ONLY: YES','      APPLICATION_EXTENSION_API_ONLY: YES\n      CODE_SIGN_ENTITLEMENTS: Signing/CarIdleWidget.entitlements');p.write_text(s)
(root/'Signing').mkdir(exist_ok=True)
for filename,bundle in [('CarIdle','com.trollbox.caridle'),('CarIdleWidget','com.trollbox.caridle.widget')]:
 ent={'application-identifier':'TROLLTROLL.'+bundle,'com.apple.developer.team-identifier':'TROLLTROLL'}
 (root/'Signing'/(filename+'.entitlements')).write_bytes(plistlib.dumps(ent))
for name in ['CarIdle/IdleLiveActivity.swift']:
 p=root/name;p.write_text(p.read_text().replace('请求版本 47','请求版本 48').replace('怠速记录 ·47','怠速记录 ·48'))
p=root/'CarIdle/VersionHistoryView.swift';s=p.read_text();key='    private let logs: [VersionLog] = [\n';s=s.replace(key,key+'        VersionLog(version: "v2.3.13 / Build 48", date: "2026年10月28日", changes: ["补齐主 App 与实时活动扩展的签名身份及共同团队标识", "打包后重新读取签名权限并核对扩展身份；保留 Build47 倒计时布局", "显示效果仍需真机验证"]),\n',1);p.write_text(s)
(root/'README.md').write_text('''# CarIdle 2.3.13 / Build48

本轮仅修复打包签名身份，保留Build47计时和布局实现。
主App与Widget扩展各自带明确的application-identifier，并使用共同TROLLTROLL团队前缀。
TROLLTROLL是TrollStore官方源码中的后备前缀，不是Apple付费开发团队或分发证书。
IPA在打包后重新读取签名权限、核对App/扩展身份和共同团队，并验证签名结构。
这修复了已确认的打包漏项；尚未证实为设备端不显示的唯一原因。
\n研究依据见docs/live-activity-signing-evidence.md。\n''')
print('2.3.13 / Build48 signing identities prepared')
