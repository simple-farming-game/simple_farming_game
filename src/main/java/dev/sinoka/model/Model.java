package dev.sinoka.model;

import org.lwjgl.opengl.GL15;
import org.lwjgl.opengl.GL30;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.glEnableVertexAttribArray;
import static org.lwjgl.opengl.GL20.glVertexAttribPointer;
import static org.lwjgl.opengl.GL30.*;

import java.util.Arrays;

public class Model {
    private int vaoID;
    private int vboID;
    private int eboID;
    private int vertexCount;
    private String name;
    private float offsetX, offsetY, offsetZ;

    public Model(float[] vertices, int[] indices, String name) {
        this.name = name;
        this.vertexCount = indices.length;

        // 오프셋 계산 및 적용 (왼쪽 위 기준)
        computeOffset(vertices);
        applyOffset(vertices);

        vaoID = glGenVertexArrays();
        vboID = glGenBuffers();
        eboID = glGenBuffers();

        System.out.println("🛠️ Generating Model: " + name);
        System.out.println("🟢 VAO ID: " + vaoID + ", VBO ID: " + vboID + ", EBO ID: " + eboID);

        if (vaoID == 0 || vboID == 0 || eboID == 0) {
            throw new RuntimeException("❌ Model creation failed! OpenGL didn't assign valid buffer IDs.");
        }

        glBindVertexArray(vaoID);

        System.out.println(Arrays.toString(vertices));
        System.out.println(Arrays.toString(indices));

        glBindBuffer(GL_ARRAY_BUFFER, vboID);
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eboID);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW);

        glVertexAttribPointer(0, 3, GL_FLOAT, false, 8 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, 3, GL_FLOAT, false, 8 * Float.BYTES, 3 * Float.BYTES);
        glEnableVertexAttribArray(1);

        glVertexAttribPointer(2, 2, GL_FLOAT, false, 8 * Float.BYTES, 6 * Float.BYTES);
        glEnableVertexAttribArray(2);

        glBindVertexArray(0);
    }

    /**
     * 🛠️ **왼쪽 위를 중심으로 모델 정렬**
     * - `minX` → 가장 왼쪽 정점
     * - `maxY` → 가장 위쪽 정점
     * - `minZ` → 가장 앞쪽 정점
     */
    private void computeOffset(float[] vertices) {
        float minX = Float.MAX_VALUE;
        float minY = Float.MAX_VALUE;
        float minZ = Float.MAX_VALUE;

        for (int i = 0; i < vertices.length; i += 8) { // 8개씩 건너뛰며 처리 (XYZ 포함)
            float x = vertices[i];
            float y = vertices[i + 1];
            float z = vertices[i + 2];

            if (x < minX) minX = x; // 가장 왼쪽 X 찾기
            if (y < minY) minY = y; // 가장 아래쪽 Y 찾기 (수정)
            if (z < minZ) minZ = z; // 가장 뒤쪽 Z 찾기
        }

        this.offsetX = -minX; // 왼쪽 기준
        this.offsetY = -minY; // 아래쪽 기준 (수정)
        this.offsetZ = -minZ; // 뒤쪽 기준
    }


    /**
     * 🏗️ **정점 데이터에 오프셋 적용**
     * - X축: `minX`만큼 이동 → 가장 왼쪽이 원점
     * - Y축: `maxY`만큼 이동 → 가장 위쪽이 원점
     * - Z축: `minZ`만큼 이동 → 가장 앞쪽이 원점
     */
    private void applyOffset(float[] vertices) {
        for (int i = 0; i < vertices.length; i += 8) {
            vertices[i] += offsetX;     // X 좌표 조정 (왼쪽 기준)
            vertices[i + 1] += offsetY; // Y 좌표 조정 (위쪽 기준)
            vertices[i + 2] += offsetZ; // Z 좌표 조정 (앞쪽 기준)
        }
    }

    public int getVaoID() {
        return vaoID;
    }

    public int getVertexCount() {
        return vertexCount;
    }

    public float getOffsetX() {
        return offsetX;
    }

    public float getOffsetY() {
        return offsetY;
    }

    public float getOffsetZ() {
        return offsetZ;
    }

    public String getName() {
        return name;
    }

    public void cleanup() {
        if (vboID != 0) {
            glDeleteBuffers(vboID);
            vboID = 0;
        }
        if (eboID != 0) {
            glDeleteBuffers(eboID);
            eboID = 0;
        }
        if (vaoID != 0) {
            glDeleteVertexArrays(vaoID);
            vaoID = 0;
        }
    }
}
