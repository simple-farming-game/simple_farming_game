package dev.sinoka.block;

import dev.sinoka.utility.JsonFileReader;
import dev.sinoka.utility.Texture;
import dev.sinoka.renderer.ModelRenderer;
import dev.sinoka.model.Model;
import org.joml.*;
import org.json.JSONArray;
import org.json.JSONObject;

public class Block {
    private final String blockID;
    private final Texture texture;
    private final float strength;
    private final boolean isBreakable;
    private final Model model;
    private final float blockSize = 1f;

    public Block(String blockID, Texture texture, float strength, boolean isBreakable, Model model) {
        this.blockID = blockID;
        this.texture = texture;
        this.strength = strength;
        this.isBreakable = isBreakable;
        this.model = model;
    }

    public void render(Vector3f position) {
        ModelRenderer.getInstance().render(model, texture, position, blockSize);
    }

    // Getter 메서드
    public String getBlockID() {
        return blockID;
    }

    public int getTextureID() {
        return texture.getTextureID();
    }

    public float getStrength() {
        return strength;
    }

    public boolean isBreakable() {
        return isBreakable;
    }

    public float getBlockSize() {
        return blockSize;
    }

    public Model getModel() {
        return model;
    }

    public void onBreak() {
        System.out.println(blockID + " has been broken.");
    }

    public void delete() {
        model.cleanup(); // 🚀 모델 내 VAO, VBO, EBO 제거
        texture.delete(); // 🚀 텍스처 제거
    }
}
