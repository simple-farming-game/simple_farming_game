package dev.sinoka.block;

import dev.sinoka.utility.JsonFileReader;
import dev.sinoka.utility.ResourceUtil;
import dev.sinoka.utility.Texture;

public class BlockBuilder {
    private String blockID;
    private Texture texture;
    private float strength = 1;
    private boolean isBreakable = true;
    private JsonFileReader modelJFR = new JsonFileReader(ResourceUtil.getAbsolutePath("model/json/block.json"));

    public BlockBuilder setBlockID(String id) {
        this.blockID = id;
        return this;
    }

    public BlockBuilder setTextureID(Texture texture) {
        this.texture = texture;
        return this;
    }

    public BlockBuilder setStrength(float time) {
        this.strength = time;
        return this;
    }

    public BlockBuilder setBreakable(boolean breakable) {
        this.isBreakable = breakable;
        return this;
    }

    public BlockBuilder setModel(JsonFileReader JFR) {
        this.modelJFR = JFR;
        return this;
    }

    public Block build() {
        return new Block(blockID, texture, strength, isBreakable, modelJFR);
    }
}
