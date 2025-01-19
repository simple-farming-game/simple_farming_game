package dev.sinoka.registry;

import dev.sinoka.block.Block;

import java.util.HashMap;
import java.util.Map;

public class BlockRegister {
    private final Map<String, Block> blockRegistry = new HashMap<>();

    public void regist(Block block, String blockID) {
        if (blockRegistry.containsKey(blockID)) {
            System.err.println("Block ID '" + blockID + "' is already registered!");
            return;
        }
        blockRegistry.put(blockID, block);
        System.out.println("Registered block: " + blockID);
    }

    public Block getBlock(String blockID) {
        return blockRegistry.get(blockID);
    }

    public boolean isRegistered(String blockID) {
        return blockRegistry.containsKey(blockID);
    }

    public void listAllBlocks() {
        System.out.println("Registered Blocks:");
        for (String blockID : blockRegistry.keySet()) {
            System.out.println("- " + blockID);
        }
    }
}
