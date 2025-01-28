package dev.sinoka.registry;

import dev.sinoka.block.Block;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class BlockRegister {
    private final Map<String, Block> blockRegistry = new ConcurrentHashMap<>();
    private static final Logger logger = LogManager.getLogger(BlockRegister.class);

    public void register(Block block) {
        if (blockRegistry.containsKey(block.getBlockID())) {
            System.err.println("⚠️ Block ID '" + block.getBlockID() + "' is already registered!");
            return;
        }
        blockRegistry.put(block.getBlockID(), block);
        logger.debug("✅ Registered block: " + block.getBlockID());
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
            logger.debug("❎ Unregistered block: " + blockID);
        } else {
            System.err.println("❌ Block ID '" + blockID + "' was not found!");
        }
    }

    public void listAllBlocks() {
        logger.debug("📜 Registered Blocks:");
        if (blockRegistry.isEmpty()) {
            logger.debug("(No blocks registered)");
        } else {
            for (String blockID : blockRegistry.keySet()) {
                logger.debug("- " + blockID);
            }
        }
    }
}
