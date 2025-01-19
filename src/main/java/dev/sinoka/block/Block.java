package dev.sinoka.block;

import dev.sinoka.utility.JsonFileReader;
import dev.sinoka.utility.Texture;
import dev.sinoka.utility.ShaderManager;
import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3d;
import org.joml.Vector3f;
import org.json.JSONArray;
import org.json.JSONObject;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.glEnableVertexAttribArray;
import static org.lwjgl.opengl.GL20.glVertexAttribPointer;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL30.*;
import static org.lwjgl.system.MemoryUtil.*;

public class Block {
    private final String blockID;
    private final Texture texture;
    private final float strength;
    private final boolean isBreakable;
    private final JsonFileReader JFR;
    private int cubeVAO;
    private int cubeVBO;
    private int cubeEBO;
    private float blockSize = 0.5f;

    public Block(String blockID, Texture texture, float strength, boolean isBreakable, JsonFileReader JFR) {
        this.blockID = blockID;
        this.texture = texture;
        this.strength = strength;
        this.isBreakable = isBreakable;
        this.JFR = JFR;

        JSONObject blockData = JFR.readJson();
        JSONArray cubeVerticesArray = blockData.getJSONArray("vertices");
        JSONArray cubeIndicesArray = blockData.getJSONArray("indices");

        // Vertex 데이터 로드
        float[] cubeVertices = new float[cubeVerticesArray.length()];
        for (int i = 0; i < cubeVerticesArray.length(); i++) {
            cubeVertices[i] = cubeVerticesArray.getFloat(i);
        }

        // Index 데이터 로드
        int[] cubeIndices = new int[cubeIndicesArray.length()];
        for (int i = 0; i < cubeIndicesArray.length(); i++) {
            cubeIndices[i] = cubeIndicesArray.getInt(i);
        }

        // OpenGL 버퍼 생성
        this.cubeVAO = glGenVertexArrays();
        this.cubeVBO = glGenBuffers();
        this.cubeEBO = glGenBuffers();

        glBindVertexArray(cubeVAO);

        glBindBuffer(GL_ARRAY_BUFFER, cubeVBO);
        glBufferData(GL_ARRAY_BUFFER, cubeVertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cubeEBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, cubeIndices, GL_STATIC_DRAW);

        glVertexAttribPointer(0, 3, GL_FLOAT, false, 8 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, 3, GL_FLOAT, false, 8 * Float.BYTES, 3 * Float.BYTES);
        glEnableVertexAttribArray(1);

        glVertexAttribPointer(2, 2, GL_FLOAT, false, 8 * Float.BYTES, 6 * Float.BYTES);
        glEnableVertexAttribArray(2);

        glBindVertexArray(0); // VAO 바인딩 해제
    }

    public void render(Vector3f pos) {
        ShaderManager.getInstance().useDefaultShader(); // 자동으로 쉐이더 사용
        texture.bind();
        Matrix4f model = new Matrix4f();
        model.identity().translate(pos).scale(blockSize);
        ShaderManager.getInstance().getDefaultShader().setMat4("model", model);
        glBindVertexArray(cubeVAO);
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0);
        glBindVertexArray(0);
        texture.unbind();
    }

    public void delete() {
        glDeleteBuffers(cubeVBO);
        glDeleteBuffers(cubeEBO);
        glDeleteVertexArrays(cubeVAO);
    }

    // Getter 메서드
    public String getBlockID() {
        return blockID;
    }

    public int getTextureID() {
        return texture.getTextureID();
    }

    public float isStrength() {
        return strength;
    }

    public boolean isBreakable() {
        return isBreakable;
    }

    // 블록이 부서질 때 실행될 동작 (추후 오버라이드 가능)
    public void onBreak() {
        System.out.println(blockID + " has been broken.");
    }
}
