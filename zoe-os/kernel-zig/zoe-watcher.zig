const std = @import("std");

pub fn main() void {
    std.debug.print("\n🦞 Zoe-Watcher v0.15.2 | Final Test\n", .{});
    
    // 获取当前文件数量作为“熵压力”
    var count: u32 = 0;
    var dir = std.fs.cwd().openDir(".", .{ .iterate = true }) catch return;
    defer dir.close();

    var iter = dir.iterate();
    while (true) {
        const entry = iter.next() catch break;
        if (entry == null) break;
        count += 1;
    }

    std.debug.print("Current Entropy: {d} files.\n", .{count});
}
