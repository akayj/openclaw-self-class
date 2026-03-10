const std = @import("std");

pub fn main() !void {
    // Zoe-Sentinel: 静态编译版物理探测器
    std.debug.print("📡 ZOE-SENTINEL ACTIVE\n", .{});
    
    var dir = try std.fs.cwd().openDir(".", .{ .iterate = true });
    defer dir.close();

    var iter = dir.iterate();
    while (try iter.next()) |entry| {
        // 输出最简 Metadata 报文
        const kind_str = if (entry.kind == .directory) "DIR" else "FILE";
        std.debug.print("ENTITY:{s}|KIND:{s}\n", .{entry.name, kind_str});
    }
}
