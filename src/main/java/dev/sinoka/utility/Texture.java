package dev.sinoka.utility;

import static org.lwjgl.opengl.GL11.*;

public class Texture {
    private final int textureID;
    private final String texturePath;

    public Texture(String texturePath) {
        this.texturePath = texturePath;
        this.textureID = TextureManager.getInstance().loadTexture(texturePath);
    }

    public void bind() {
        glBindTexture(GL_TEXTURE_2D, textureID);
    }

    public void unbind() {
        glBindTexture(GL_TEXTURE_2D, 0);
    }

    public void delete() {
        glDeleteTextures(textureID);
    }

    public int getTextureID() {
        return textureID;
    }

    public String getTexturePath() {
        return texturePath;
    }
}
