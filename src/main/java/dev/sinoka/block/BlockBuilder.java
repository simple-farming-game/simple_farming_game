package dev.sinoka.block;

import dev.sinoka.model.Model;
import dev.sinoka.model.ModelFactory;
import dev.sinoka.utility.JsonFileReader;
import dev.sinoka.utility.ResourceUtil;
import dev.sinoka.utility.Texture;

public class BlockBuilder {
    private String blockID;
    private Texture texture;
    private float strength = 1;
    private boolean isBreakable = true;
    private Model model = ModelFactory.loadModelFromJson(ResourceUtil.getAbsolutePath("model/json/block.json"));
    private boolean isSolid = true;

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

    public BlockBuilder setSolid(boolean isSolid) {
        this.isSolid = isSolid;
        return this;
    }

    public Block build() {
        return new Block(blockID, texture, strength, isBreakable, model, isSolid);
    }
}
