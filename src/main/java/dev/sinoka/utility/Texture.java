package dev.sinoka.utility;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL13.*;

public class Texture {
    private int textureID;
    private final String texturePath;
    private static final Logger logger = LogManager.getLogger(Texture.class);

    public Texture(String texturePath) {
        this.texturePath = texturePath;
        this.textureID = TextureManager.getInstance().loadTexture(texturePath);

        if (textureID == 0) {
            System.err.println("⚠️ Failed to load texture: " + texturePath);
        } else {
            logger.debug("✅ Texture loaded successfully: " + texturePath + " (ID: " + textureID + ")");
        }
    }

    public void bind() {
        if (textureID == 0) {
            System.err.println("⚠️ Attempting to bind an invalid texture: " + texturePath);
            return;
        }
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, textureID);
    }

    public void unbind() {
        glBindTexture(GL_TEXTURE_2D, 0);
    }

    public void delete() {
        if (textureID != 0) {
            glDeleteTextures(textureID);
            logger.debug("❌ Deleted texture: " + texturePath + " (ID: " + textureID + ")");
            textureID = 0;
        }
    }

    public boolean isValid() {
        return textureID != 0;
    }

    public int getTextureID() {
        return textureID;
    }

    public String getTexturePath() {
        return texturePath;
    }
}
