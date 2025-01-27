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

    public void render(Model model, Texture texture, Vector3f position, float scale) {
        ShaderManager.getInstance().useDefaultShader(); // 자동으로 쉐이더 사용

        texture.bind();
        ShaderManager.getInstance().getDefaultShader().setInt("material.diffuse", 0);
        Matrix4f mmodel = new Matrix4f();
        mmodel.identity().translate(position).scale(scale);
        ShaderManager.getInstance().getDefaultShader().setMat4("model", mmodel);
        glBindVertexArray(model.getVaoID());
        glDrawElements(GL_TRIANGLES, model.getVertexCount(), GL_UNSIGNED_INT, 0);
        glBindVertexArray(0);
        texture.unbind();
    }
}
