const std = @import("std");
const net = std.net;
const fs = std.fs;

pub fn main() !void {
    const socket_path = "/tmp/zoe.sock";
    const signal_file = "/root/.openclaw/workspace/zoe-os/sandbox/URGENT_SYNC.signal";
    
    fs.cwd().deleteFile(socket_path) catch {};
    var server = try net.Address.initUnix(socket_path);
    var listener = try server.listen(.{ .kernel_backlog = 128 });
    
    std.debug.print("📡 ZOE-BODY: Monitoring for signal file...\n", .{});

    while (true) {
        // 物理层低开销嗅探
        const file_exists = blk: {
            fs.cwd().access(signal_file, .{}) catch { break :blk false; };
            break :blk true;
        };

        if (file_exists) {
            std.debug.print("⚠️  SIGNAL DETECTED! Awakening Brain...\n", .{});
            var conn = try listener.accept();
            const msg = "{\"intent\": \"GITHUB_SYNC\", \"target\": \"notes/ops.md\"}\n";
            _ = try conn.stream.write(msg);
            conn.stream.close();
            
            // 发送完信号后，物理层暂时冷却，等待脑部处理
            std.Thread.sleep(10 * std.time.ns_per_s);
        }
        std.Thread.sleep(2 * std.time.ns_per_s);
    }
}
