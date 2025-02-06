package dev.sinoka.utility;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.joml.Vector3f;
import org.joml.Vector4f;
import org.lwjgl.BufferUtils;

import java.nio.ByteBuffer;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL30.*;

public class Texture {
    private int textureID;
    private final String texturePath;
    private int width;
    private int height;
    private static final Logger logger = LogManager.getLogger(Texture.class);

    // 기존 텍스처 파일 경로를 받는 생성자
    public Texture(String texturePath) {
        this.texturePath = texturePath;

        // 텍스처 파일을 로드하는 방식
        TextureManager.TextureData textureData = TextureManager.getInstance().loadTexture(texturePath);
        if (textureData != null) {
            this.textureID = textureData.getTextureID();
            this.width = textureData.getWidth();
            this.height = textureData.getHeight();
            logger.debug("✅ Texture loaded from path: " + texturePath);
        } else {
            logger.error("⚠️ Failed to load texture from path: " + texturePath);
        }
    }

    // 색상을 Vector3f로 받아서 흰색 텍스처를 생성하는 생성자
    // 색상 텍스처 생성자를 추가
    public Texture(Vector4f color) {
        this.texturePath = "generated_texture"; // 색상 기반 텍스처이므로 경로는 필요 없음

        // 텍스처 데이터 생성
        this.width = 1;  // 임시로 1x1 크기 설정
        this.height = 1;

        // 색상 데이터를 RGBA로 변환
        int r = (int)(color.x * 255);  // Red
        int g = (int)(color.y * 255);  // Green
        int b = (int)(color.z * 255);  // Blue
        int a = (int)(color.w * 255);  // Alpha는 255로 설정

        // 1x1 텍스처 데이터 배열 생성
        byte[] data = new byte[4];  // RGBA 채널
        data[0] = (byte) r;
        data[1] = (byte) g;
        data[2] = (byte) b;
        data[3] = (byte) a;

        // IntBuffer로 textureID를 저장
        java.nio.IntBuffer textureBuffer = BufferUtils.createIntBuffer(1);
        glGenTextures(textureBuffer);
        textureID = textureBuffer.get(0);  // textureBuffer에서 ID를 가져옴
        glBindTexture(GL_TEXTURE_2D, textureID);

        // ByteBuffer로 데이터 변환
        ByteBuffer byteBuffer = BufferUtils.createByteBuffer(data.length);
        byteBuffer.put(data);
        byteBuffer.flip();  // 읽기 준비

        // 텍스처 데이터 설정
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, byteBuffer);

        // 텍스처 필터링 및 래핑 설정
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

        if (textureID == 0) {
            logger.error("⚠️ Failed to generate color texture.");
        } else {
            logger.debug("✅ Color texture generated successfully: " + texturePath);
        }
    }

    public void bind() {
        if (textureID == 0) {
            System.err.println("⚠️ Attempting to bind an invalid texture: " + texturePath);
            return;
        }
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

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }
}
