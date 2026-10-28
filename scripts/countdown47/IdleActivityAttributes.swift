import Foundation
import ActivityKit

// Compiled from the same file in both targets; persisted state remains compatible with 2.3.9.
struct IdleActivityAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        var startTime: Date
        var targetMinutes: Int
        var endTime: Date { startTime.addingTimeInterval(Double(max(1, min(targetMinutes, 1440))) * 60) }
    }
    var title: String
}
