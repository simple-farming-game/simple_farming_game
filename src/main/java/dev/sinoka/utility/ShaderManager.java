package dev.sinoka.utility;

import java.util.HashMap;
import java.util.Map;
import static org.lwjgl.opengl.GL20.*;

public class ShaderManager {
    private static ShaderManager instance;
    private Shader defaultShader;
    private final Map<String, Shader> shaderMap = new HashMap<>();

    private ShaderManager() {
        // 생성자에서 `loadDefaultShader()` 호출 제거 → 명시적으로 호출 필요
    }

    public static ShaderManager getInstance() {
        if (instance == null) {
            instance = new ShaderManager();
        }
        return instance;
    }

    public void loadDefaultShader() {
        if (defaultShader == null) {
            System.out.println("🚀 Loading Default Shader...");
            defaultShader = new Shader(
                    ResourceUtil.getAbsolutePath("shader/vertex.glsl"),
                    ResourceUtil.getAbsolutePath("shader/fragment.glsl")
            );
            shaderMap.put("default", defaultShader);
            System.out.println("✅ Default Shader Loaded Successfully!");
        }
    }

    public Shader getDefaultShader() {
        if (defaultShader == null) {
            loadDefaultShader(); // 🚀 기본 쉐이더가 없으면 자동 로드
        }
        return defaultShader;
    }

    public void useDefaultShader() {
        useShader("default");
    }

    public void loadShader(String name, String vertexPath, String fragmentPath) {
        if (!shaderMap.containsKey(name)) {
            Shader shader = new Shader(ResourceUtil.getAbsolutePath(vertexPath), ResourceUtil.getAbsolutePath(fragmentPath));
            shaderMap.put(name, shader);
            System.out.println("✅ Loaded Shader: " + name);
        } else {
            System.err.println("⚠️ Shader '" + name + "' is already loaded!");
        }
    }

    public Shader getShader(String name) {
        if (shaderMap.containsKey(name)) {
            return shaderMap.get(name);
        } else {
            System.err.println("❌ Shader '" + name + "' not found! Using default shader.");
            return getDefaultShader();
        }
    }

    public void useShader(String name) {
        Shader shader = getShader(name);
        if (shader != null) {
            shader.use();
        }
    }

    public void cleanup() {
        for (Shader shader : shaderMap.values()) {
            shader.delete();
        }
        shaderMap.clear();
        System.out.println("✅ All shaders deleted.");
    }
}
