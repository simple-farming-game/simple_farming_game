package dev.sinoka.utility;

import org.lwjgl.stb.STBImage;
import org.lwjgl.system.MemoryStack;

import java.nio.ByteBuffer;
import java.nio.IntBuffer;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL11.GL_NEAREST;
import static org.lwjgl.opengl.GL12.GL_CLAMP_TO_EDGE;
import static org.lwjgl.opengl.GL30.glGenerateMipmap;

public class TextureManager {
    private static TextureManager instance;

    private TextureManager() {}

    public static TextureManager getInstance() {
        if (instance == null) {
            instance = new TextureManager();
        }
        return instance;
    }

    public TextureData loadTexture(String path) {
        int textureID = glGenTextures();
        int width = 0;
        int height = 0;

        try (MemoryStack stack = MemoryStack.stackPush()) {
            IntBuffer widthBuffer = stack.mallocInt(1);
            IntBuffer heightBuffer = stack.mallocInt(1);
            IntBuffer nrComponents = stack.mallocInt(1);

            // Load image using STBImage
            ByteBuffer data = STBImage.stbi_load(path, widthBuffer, heightBuffer, nrComponents, 0);
            if (data != null) {
                width = widthBuffer.get(0);
                height = heightBuffer.get(0);
                int format;
                if (nrComponents.get(0) == 1) {
                    format = GL_RED;
                } else if (nrComponents.get(0) == 3) {
                    format = GL_RGB;
                } else if (nrComponents.get(0) == 4) {
                    format = GL_RGBA;
                } else {
                    throw new RuntimeException("Unsupported number of components: " + nrComponents.get(0));
                }

                glBindTexture(GL_TEXTURE_2D, textureID);
                glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, GL_UNSIGNED_BYTE, data);
                glGenerateMipmap(GL_TEXTURE_2D);

                // Set texture wrapping and filtering
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

                STBImage.stbi_image_free(data);
            } else {
                System.err.println("Failed to load texture: " + path);
                if (data != null) {
                    STBImage.stbi_image_free(data);
                }
            }
        }

        return new TextureData(textureID, width, height);
    }

    public static class TextureData {
        private final int textureID;
        private final int width;
        private final int height;

        public TextureData(int textureID, int width, int height) {
            this.textureID = textureID;
            this.width = width;
            this.height = height;
        }

        public int getTextureID() {
            return textureID;
        }

        public int getWidth() {
            return width;
        }

        public int getHeight() {
            return height;
        }
    }
}
