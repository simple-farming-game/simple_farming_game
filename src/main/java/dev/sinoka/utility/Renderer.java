package dev.sinoka.utility;

import org.joml.*;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL30.*;

public class Renderer {
    public static void drawTexture(Texture texture, Vector2f texRegion, Vector2f texSize, int VAO, Shader shaderProgram, Vector2f pos, float scale) {
        glEnable(GL_BLEND); // 블렌딩 활성화
        glBlendFunc(GL_ONE, GL_ONE);
        glDisable(GL_DEPTH_TEST);

        glActiveTexture(GL_TEXTURE1);
        texture.bind();

        shaderProgram.use();
        shaderProgram.setInt("texture1", 1);
        shaderProgram.setVec2("uTexRegion", texRegion);
        shaderProgram.setVec2("uTexSize", texSize);

        // 모델 변환 행렬 설정
        Matrix4f model = new Matrix4f();
        model.identity()
                .translate(pos.x, pos.y, 0.0f) // 위치 변환
                .scale(scale);                 // 크기 조정
        shaderProgram.setMat4("model", model);

        // VAO 바인딩 및 드로우 호출
        glBindVertexArray(VAO);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

        // 블렌딩 상태는 끄지 않음 (글로벌 설정 유지)
        glEnable(GL_DEPTH_TEST);
    }

}
