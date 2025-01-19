package dev.sinoka.utility;

import static org.lwjgl.opengl.GL20.*;

public class ShaderManager {
    private static ShaderManager instance;
    private Shader defaultShader;

    private ShaderManager() {
        loadDefaultShader();
    }

    public static ShaderManager getInstance() {
        if (instance == null) {
            instance = new ShaderManager();
        }
        return instance;
    }

    private void loadDefaultShader() {
        defaultShader = new Shader(ResourceUtil.getAbsolutePath("shader/vertex.glsl"), ResourceUtil.getAbsolutePath("shader/fragment.glsl"));
    }

    public void useDefaultShader() {
        if (defaultShader != null) {
            defaultShader.use();
        }
    }

    public Shader getDefaultShader() {
        return defaultShader;
    }

    public void delete() {
        if (defaultShader != null) {
            defaultShader.delete();
        }
    }
}
