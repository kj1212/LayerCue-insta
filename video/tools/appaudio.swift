// 앱 하나의 소리만 녹음한다(ScreenCaptureKit) — 11편: LayerCue 음악이 영상에 들리게.
//   appaudio <pid> <out.wav> <seconds>
// 첫 줄에 "start <epoch>" 를 찍는다: wav 의 0 초가 그 순간(time.time() 과 같은 시계)이다.
import Foundation
import ScreenCaptureKit
import AVFoundation
import CoreMedia

let args = CommandLine.arguments
guard args.count >= 4, let pid = Int32(args[1]), let secs = Double(args[3]) else {
    print("usage: appaudio <pid> <out.wav> <seconds>"); exit(2)
}
let outURL = URL(fileURLWithPath: args[2])
let SR = 48000.0

final class Rec: NSObject, SCStreamOutput, SCStreamDelegate {
    var L = [Float](), R = [Float]()
    var startHost = 0.0
    let lock = NSLock()
    func stream(_ s: SCStream, didOutputSampleBuffer sb: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .audio, sb.isValid, let fd = sb.formatDescription,
              var asbd = fd.audioStreamBasicDescription, let fmt = AVAudioFormat(streamDescription: &asbd) else { return }
        let n = CMSampleBufferGetNumSamples(sb)
        guard let pcm = AVAudioPCMBuffer(pcmFormat: fmt, frameCapacity: AVAudioFrameCount(n)) else { return }
        pcm.frameLength = AVAudioFrameCount(n)
        guard CMSampleBufferCopyPCMDataIntoAudioBufferList(sb, at: 0, frameCount: Int32(n), into: pcm.mutableAudioBufferList) == noErr,
              let ch = pcm.floatChannelData else { return }
        let pts = CMSampleBufferGetPresentationTimeStamp(sb).seconds
        let pos = Int(((pts - startHost) * SR).rounded())
        if pos < 0 { return }
        lock.lock(); defer { lock.unlock() }
        let need = pos + n
        if L.count < need { L += [Float](repeating: 0, count: need - L.count); R += [Float](repeating: 0, count: need - R.count) }
        let c2 = fmt.channelCount > 1 ? 1 : 0
        for i in 0..<n { L[pos + i] = ch[0][i]; R[pos + i] = ch[c2][i] }
    }
    func stream(_ stream: SCStream, didStopWithError error: Error) { FileHandle.standardError.write("stopped: \(error)\n".data(using: .utf8)!) }
}

let rec = Rec()
let sema = DispatchSemaphore(value: 0)
Task {
    do {
        let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: false)
        guard let app = content.applications.first(where: { $0.processID == pid }), let disp = content.displays.first else {
            print("no app \(pid)"); exit(3)
        }
        let filter = SCContentFilter(display: disp, including: [app], exceptingWindows: [])
        let cfg = SCStreamConfiguration()
        cfg.capturesAudio = true; cfg.sampleRate = Int(SR); cfg.channelCount = 2
        cfg.width = 64; cfg.height = 64; cfg.minimumFrameInterval = CMTime(value: 1, timescale: 2); cfg.queueDepth = 3
        let st = SCStream(filter: filter, configuration: cfg, delegate: rec)
        try st.addStreamOutput(rec, type: .audio, sampleHandlerQueue: DispatchQueue(label: "a"))
        try st.addStreamOutput(rec, type: .screen, sampleHandlerQueue: DispatchQueue(label: "v"))
        rec.startHost = CMClockGetTime(CMClockGetHostTimeClock()).seconds
        let epoch = Date().timeIntervalSince1970
        try await st.startCapture()
        print(String(format: "start %.4f", epoch)); fflush(stdout)
        try await Task.sleep(nanoseconds: UInt64(secs * 1e9))
        try await st.stopCapture()
        rec.lock.lock()
        let n = max(rec.L.count, Int(secs * SR))
        let fmt = AVAudioFormat(standardFormatWithSampleRate: SR, channels: 2)!
        let buf = AVAudioPCMBuffer(pcmFormat: fmt, frameCapacity: AVAudioFrameCount(n))!
        buf.frameLength = AVAudioFrameCount(n)
        for i in 0..<n { buf.floatChannelData![0][i] = i < rec.L.count ? rec.L[i] : 0; buf.floatChannelData![1][i] = i < rec.R.count ? rec.R[i] : 0 }
        rec.lock.unlock()
        let f = try AVAudioFile(forWriting: outURL, settings: [AVFormatIDKey: kAudioFormatLinearPCM, AVSampleRateKey: SR, AVNumberOfChannelsKey: 2,
                                                                AVLinearPCMBitDepthKey: 32, AVLinearPCMIsFloatKey: true])
        try f.write(from: buf)
        print(String(format: "wrote %.1f s", Double(n) / SR))
    } catch { print("error \(error)"); exit(1) }
    sema.signal()
}
sema.wait()
