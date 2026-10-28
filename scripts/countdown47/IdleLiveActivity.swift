import Foundation
import ActivityKit
import Combine

@MainActor
final class IdleLiveActivity: ObservableObject {
    static let shared = IdleLiveActivity()
    @Published private(set) var status = "尚未启动实时活动"
    private var operation: Task<Void, Never>?
    private var revision = 0
    private var enabled: Bool { UserDefaults.standard.object(forKey: "liveActivityEnabled") as? Bool ?? true }
    private init() {}

    func sync(start: Date?, targetMinutes: Int) {
        revision += 1
        let requestedRevision = revision
        let previous = operation
        operation = Task { [weak self] in
            await previous?.value
            guard let self = self, self.revision == requestedRevision else { return }
            let activities = Activity<IdleActivityAttributes>.activities
            guard self.enabled, let start = start else {
                for activity in activities { await activity.end(nil, dismissalPolicy: .immediate) }
                self.status = self.enabled ? "未计时，实时活动未启动" : "实时活动已关闭"
                return
            }
            guard ActivityAuthorizationInfo().areActivitiesEnabled else {
                self.status = "系统未允许实时活动，请在系统设置中开启"
                return
            }
            let state = IdleActivityAttributes.ContentState(startTime: start, targetMinutes: max(1, min(targetMinutes, 1440)))
            let reusable = activities.first {
                ($0.activityState == .active || $0.activityState == .stale) && $0.attributes.title == "怠速记录 ·47"
            }
            if let existing = reusable {
                if existing.content.state != state {
                    await existing.update(ActivityContent(state: state, staleDate: nil))
                }
                for duplicate in activities where duplicate.id != existing.id {
                    await duplicate.end(nil, dismissalPolicy: .immediate)
                }
                self.status = "实时活动已创建 · 请求版本 47 · " + existing.id
                return
            }
            // Request first. A registration/permission failure must not destroy an existing presentation.
            do {
                let activity = try Activity<IdleActivityAttributes>.request(
                    attributes: IdleActivityAttributes(title: "怠速记录 ·47"),
                    content: ActivityContent(state: state, staleDate: nil), pushType: nil)
                self.status = "实时活动已创建 · 请求版本 47 · " + activity.id
                for old in activities { await old.end(nil, dismissalPolicy: .immediate) }
            } catch {
                let error = error as NSError
                self.status = "创建失败：\(error.domain) / \(error.code)\n\(error.localizedDescription)"
                NSLog("[CarIdle] %@", self.status)
            }
        }
    }
    func endAll() { sync(start: nil, targetMinutes: 0) }
}
