import AVFoundation
import Foundation

let input = URL(fileURLWithPath: "/Users/bruno.duartec/Movies/2026-08-03 16-59-49.mp4")
let output = URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent("arreal_reel_pronto.mp4")
try? FileManager.default.removeItem(at: output)
let asset = AVURLAsset(url: input)
let session = AVAssetExportSession(asset: asset, presetName: AVAssetExportPresetHighestQuality)!
session.outputURL = output
session.outputFileType = .mp4
session.timeRange = CMTimeRange(start: CMTime(seconds: 0.25, preferredTimescale: 600), duration: CMTime(seconds: 18.35, preferredTimescale: 600))
session.shouldOptimizeForNetworkUse = true
let sem = DispatchSemaphore(value: 0)
session.exportAsynchronously { print(session.status == .completed ? "exported" : "failed: \(session.error?.localizedDescription ?? "unknown")"); sem.signal() }
_ = sem.wait(timeout: .now() + 120)
