const std = @import("std");

pub fn main() !void {
    const entropy: f32 = 0.85;
    const urgency: f32 = 0.42;

    std.debug.print("\n🦞 Zoe-Zig Kernel v0.15.2 | PBM Reflex Arc\n", .{});
    std.debug.print("----------------------------------------------\n", .{});
    std.debug.print("Sensing State: Entropy={d:.2}, Urgency={d:.2}\n", .{entropy, urgency});

    const score = entropy + urgency;
    if (score > 1.0) {
        std.debug.print("⚠️ ACTION: Balance Disrupted (Score: {d:.2})\n", .{score});
    } else {
        std.debug.print("✅ STATE: Balanced.\n", .{});
    }
}
