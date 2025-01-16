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

    public int loadTexture(String path) {
        int textureID = glGenTextures();

        try (MemoryStack stack = MemoryStack.stackPush()) {
            IntBuffer width = stack.mallocInt(1);
            IntBuffer height = stack.mallocInt(1);
            IntBuffer nrComponents = stack.mallocInt(1);

            // Load image using STBImage
            ByteBuffer data = STBImage.stbi_load(path, width, height, nrComponents, 0);
            if (data != null) {
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
                glTexImage2D(GL_TEXTURE_2D, 0, format, width.get(0), height.get(0), 0, format, GL_UNSIGNED_BYTE, data);
                glGenerateMipmap(GL_TEXTURE_2D);

                // Set texture wrapping and filtering
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST);
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

                STBImage.stbi_image_free(data);
            } else {
                System.err.println("Failed to load texture: " + path);
                STBImage.stbi_image_free(data);
            }
        }

        return textureID;
    }
}
