import SwiftUI
import WidgetKit
import ActivityKit

@available(iOS 16.2, *)
private struct CountdownText: View {
    let state: IdleActivityAttributes.ContentState
    let size: CGFloat
    let width: CGFloat
    var body: some View {
        Group {
            if state.endTime > Date() {
                Text(timerInterval: state.startTime...state.endTime,
                     countsDown: true, showsHours: state.targetMinutes >= 60)
            } else {
                Text("00:00")
            }
        }
        .font(.system(size: size, weight: .semibold, design: .rounded))
        .monospacedDigit()
        .foregroundColor(.white)
        .multilineTextAlignment(.trailing)
        .lineLimit(1)
        .frame(width: width, height: size * 1.4, alignment: .trailing)
        .layoutPriority(1)
        .privacySensitive(false)
        .unredacted()
    }
}

@available(iOS 16.2, *)
struct IdleWidget: Widget {
    private func car(_ size: CGFloat) -> some View {
        Image("IdleCarLogo").resizable().scaledToFit()
            .frame(width: size, height: size)
            .accessibilityLabel("怠速记录")
    }
    private var close: some View {
        Image(systemName: "xmark")
            .font(.system(size: 15, weight: .semibold))
            .foregroundColor(.white)
            .frame(width: 30, height: 30)
            .background(Color.white.opacity(0.2)).clipShape(Circle())
    }
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: IdleActivityAttributes.self) { context in
            HStack(spacing: 10) {
                close
                Text("怠速记录")
                    .font(.system(size: 17, weight: .semibold))
                    .foregroundColor(.white).lineLimit(1)
                Spacer(minLength: 0)
                CountdownText(state: context.state, size: 32,
                              width: context.state.targetMinutes >= 60 ? 162 : 116)
            }
            .padding(.horizontal, 18).padding(.vertical, 12)
            .activityBackgroundTint(.black)
            .activitySystemActionForegroundColor(.white)
            .widgetURL(URL(string: "caridle://record"))
        } dynamicIsland: { context in
            DynamicIsland {
                DynamicIslandExpandedRegion(.leading) {
                    HStack(spacing: 6) {
                        car(20)
                        Text("怠速记录").font(.system(size: 15, weight: .semibold)).lineLimit(1)
                    }.foregroundColor(.white)
                }
                DynamicIslandExpandedRegion(.trailing) { close }
                DynamicIslandExpandedRegion(.bottom) {
                    HStack {
                        CountdownText(state: context.state, size: 44,
                                      width: context.state.targetMinutes >= 60 ? 220 : 160)
                        Spacer(minLength: 0)
                    }.padding(.bottom, 4)
                }
            } compactLeading: {
                car(18)
            } compactTrailing: {
                CountdownText(state: context.state, size: 13,
                              width: context.state.targetMinutes >= 60 ? 64 : 48)
            } minimal: {
                car(18)
            }
            .widgetURL(URL(string: "caridle://record"))
        }
    }
}

@main
struct IdleWidgetBundle: WidgetBundle {
    var body: some Widget { IdleWidget() }
}
