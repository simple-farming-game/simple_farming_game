package dev.sinoka.renderer;

import dev.sinoka.utility.Shader;
import dev.sinoka.utility.Texture;
import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;
import org.joml.Vector3fc;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL13.GL_TEXTURE1;
import static org.lwjgl.opengl.GL13.glActiveTexture;
import static org.lwjgl.opengl.GL30.glBindVertexArray;

public class TextureRenderer {
    public static void drawTexture(Texture texture, Vector2f texRegion, Vector2f texSize, int VAO, Shader shaderProgram, Vector2f pos, Vector2f scale) {
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
                .scale(new Vector3f(scale, 1));                 // 크기 조정
        shaderProgram.setMat4("model", model);

        // VAO 바인딩 및 드로우 호출
        glBindVertexArray(VAO);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

        glEnable(GL_DEPTH_TEST);
        glDisable(GL_BLEND); // 블렌딩 활성화
    }

}
