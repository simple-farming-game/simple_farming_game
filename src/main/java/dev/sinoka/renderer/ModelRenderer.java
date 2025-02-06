package dev.sinoka.renderer;

import dev.sinoka.utility.Texture;
import dev.sinoka.utility.ShaderManager;
import dev.sinoka.model.Model;
import org.joml.Matrix4f;
import org.joml.Vector3f;

import static org.lwjgl.opengl.GL30.*;

public class ModelRenderer {
    private static ModelRenderer instance;

    private ModelRenderer() {}

    public static ModelRenderer getInstance() {
        if (instance == null) {
            instance = new ModelRenderer();
        }
        return instance;
    }

    public void render(Model model, Texture texture, Vector3f position, float scale, boolean wireframe) {
        ShaderManager.getInstance().useDefaultShader(); // 자동으로 쉐이더 사용

        ShaderManager.getInstance().getDefaultShader().setBool("wireframe", wireframe);
        if (wireframe) {
            glLineWidth(10.0f);  // 라인의 두께를 2.0으로 설정
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE); // 와이어프레임 모드로 설정

        } else {
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL); // 기본 모드로 설정
        }

        glActiveTexture(GL_TEXTURE0);
        texture.bind();
        ShaderManager.getInstance().getDefaultShader().setInt("material.diffuse", 0);

        Matrix4f mmodel = new Matrix4f();
        mmodel.identity().translate(position).scale(scale);
        ShaderManager.getInstance().getDefaultShader().setMat4("model", mmodel);

        glBindVertexArray(model.getVaoID());
        glDrawElements(GL_TRIANGLES, model.getVertexCount(), GL_UNSIGNED_INT, 0);
        glBindVertexArray(0);

        texture.unbind();

        if (wireframe) {
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL); // 렌더링 후 기본 모드로 복원
        }
    }
}
