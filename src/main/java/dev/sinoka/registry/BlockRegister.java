package dev.sinoka.registry;

import dev.sinoka.block.Block;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class BlockRegister {
    private final Map<String, Block> blockRegistry = new ConcurrentHashMap<>();

    public void register(Block block) {
        if (blockRegistry.containsKey(block.getBlockID())) {
            System.err.println("⚠️ Block ID '" + block.getBlockID() + "' is already registered!");
            return;
        }
        blockRegistry.put(block.getBlockID(), block);
        System.out.println("✅ Registered block: " + block.getBlockID());
    }

    public Block getBlock(String blockID) {
        Block block = blockRegistry.get(blockID);
        if (block == null) {
            System.err.println("❌ Block ID '" + blockID + "' does not exist!");
        }
        return block;
    }

    public boolean isRegistered(String blockID) {
        return blockRegistry.containsKey(blockID);
    }

    public void unregisterBlock(String blockID) {
        if (blockRegistry.remove(blockID) != null) {
            System.out.println("❎ Unregistered block: " + blockID);
        } else {
            System.err.println("❌ Block ID '" + blockID + "' was not found!");
        }
    }

    public void listAllBlocks() {
        System.out.println("📜 Registered Blocks:");
        if (blockRegistry.isEmpty()) {
            System.out.println("(No blocks registered)");
        } else {
            for (String blockID : blockRegistry.keySet()) {
                System.out.println("- " + blockID);
            }
        }
    }
}
